import numpy as np
import random

# Environment setup
class BinPackingEnv:
    def __init__(self, packages, containers):
        self.packages = packages
        self.containers = containers
        self.reset()

    def reset(self):
        self.remaining_packages = self.packages.copy()
        self.container_states = {key: {"remaining_weight": c["weight_limit"], "used_space": np.zeros((c["length"], c["width"], c["height"]))}
                                 for key, c in self.containers.items()}
        return self.remaining_packages, self.container_states

    def is_valid(self, package, container):
        """Check if the package can fit in the container."""
        p_dims = np.array([package['length'], package['width'], package['height']])
        c_dims = np.array([container['length'], container['width'], container['height']])
        if not np.all(p_dims <= c_dims):
            return False
        if package['weight'] > container["remaining_weight"]:
            return False
        return True

    def step(self, package_id, container_id):
        package = self.remaining_packages[package_id]
        container = self.container_states[container_id]

        if self.is_valid(package, container):
            # Update container state
            container["remaining_weight"] -= package["weight"]
            # Simulate placement
            container["used_space"] += 1  # Simulate (simplified)
            reward = 1 if package["type"] == "Priority" else -package["cost_delay"]
            del self.remaining_packages[package_id]
            done = len(self.remaining_packages) == 0
            return (self.remaining_packages, self.container_states), reward, done, {}
        else:
            return (self.remaining_packages, self.container_states), -10, False, {}  # Penalty for invalid action


# RL Agent
class RLAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.env = env
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay

    def get_state_key(self, state):
        """Convert the state to a hashable key."""
        packages, containers = state
        return (tuple(sorted(packages.keys())), tuple(containers.keys()))

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.random() < self.exploration_rate:
            return random.choice(list(self.env.remaining_packages.keys())), random.choice(list(self.env.containers.keys()))
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        return max(self.q_table[state_key], key=self.q_table[state_key].get, default=random.choice(list(self.env.remaining_packages.keys())))

    def update_q_value(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        if action not in self.q_table[state_key]:
            self.q_table[state_key][action] = 0
        next_max = max(self.q_table.get(next_state_key, {}).values(), default=0)
        self.q_table[state_key][action] += self.learning_rate * (reward + self.discount_factor * next_max - self.q_table[state_key][action])

    def train(self, episodes):
        for _ in range(episodes):
            state = self.env.reset()
            done = False
            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(*action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state
            self.exploration_rate *= self.exploration_decay


# Main
packages = {
    "P-1": {"length": 99, "width": 53, "height": 55, "weight": 61, "type": "Economy", "cost_delay": 176},
    "P-2": {"length": 56, "width": 99, "height": 81, "weight": 53, "type": "Priority", "cost_delay": 0},
    "P-3": {"length": 42, "width": 101, "height": 51, "weight": 17, "type": "Priority", "cost_delay": 0},
    "P-4": {"length": 108, "width": 75, "height": 56, "weight": 73, "type": "Economy", "cost_delay": 138},
    "P-5": {"length": 88, "width": 58, "height": 64, "weight": 93, "type": "Economy", "cost_delay": 139},
    "P-6": {"length": 91, "width": 56, "height": 84, "weight": 47, "type": "Priority", "cost_delay": 0},
    "P-7": {"length": 88, "width": 78, "height": 93, "weight": 117, "type": "Economy", "cost_delay": 102},
    "P-8": {"length": 108, "width": 105, "height": 76, "weight": 142, "type": "Economy", "cost_delay": 108}
}

containers = {
    "U1": {"length": 224, "width": 318, "height": 162, "weight_limit": 2500},
    "U2": {"length": 224, "width": 318, "height": 162, "weight_limit": 2500},
    "U3": {"length": 244, "width": 318, "height": 244, "weight_limit": 2800}
}

env = BinPackingEnv(packages, containers)
agent = RLAgent(env)
agent.train(episodes=1000)

# Final policy evaluation
state = env.reset()
done = False
while not done:
    package, container = agent.choose_action(state)
    state, reward, done, _ = env.step(package, container)
