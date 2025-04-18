import random

from constants import *
import matplotlib as plt
import numpy as np 



class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        # Q-table: maps states to action values
        self.q_table = {}
        
        # Learning parameters
        self.alpha = 0.2  # Learning rate (increased)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Start with full exploration
        self.epsilon_min = 0.05  # Higher minimum exploration
        self.epsilon_decay = 0.99  # Slower decay for more exploration
        
        # For tracking performance
        self.rewards_history = []
        self.steps_history = []
        self.completion_history = []  # Track if goal was reached
        
    def get_action(self, state):
        # Epsilon-greedy action selection
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_size)
        
        # If state is not in Q-table, add it
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)
            
        return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state, done):
        # If state/next_state is not in Q-table, add it
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.action_size)
        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(self.action_size)
        
        # Q-learning formula
        if not done:
            target = reward + self.gamma * np.max(self.q_table[next_state])
        else:
            target = reward
        
        # Update Q-value
        self.q_table[state][action] += self.alpha * (target - self.q_table[state][action])
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def epsilon_reset(self, episode, num_episodes):
        # Gradually reduce starting epsilon over time
        # This creates a cycle of exploration followed by exploitation
        if episode % 50 == 0 and episode > 0:
            # After every 50 episodes, increase epsilon again but less than before
            self.epsilon = max(0.5, 1.0 - (episode / num_episodes) * 0.5)
            print(f"Epsilon reset to {self.epsilon:.4f}")
    
    def remember(self, episode_reward, episode_steps, goal_reached):
        self.rewards_history.append(episode_reward)
        self.steps_history.append(episode_steps)
        self.completion_history.append(1 if goal_reached else 0)
        
    def save_q_table(self, filename="q_table.npy"):
        np.save(filename, self.q_table)
        print(f"Q-table sauvegardée dans {filename}")
        
    def plot_performance(self):
        plt.figure(figsize=(15, 5))
        
        # Plot rewards
        plt.subplot(1, 3, 1)
        plt.plot(self.rewards_history)
        plt.title('Rewards per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        
        # Plot steps
        plt.subplot(1, 3, 2)
        plt.plot(self.steps_history)
        plt.title('Steps per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Steps')
        
        # Plot completion rate (moving average)
        plt.subplot(1, 3, 3)
        window_size = min(10, len(self.completion_history))
        if window_size > 0:
            completion_rate = np.convolve(self.completion_history, 
                                         np.ones(window_size)/window_size, 
                                         mode='valid')
            plt.plot(range(window_size-1, len(self.completion_history)), completion_rate)
            plt.title('Goal Completion Rate (Moving Avg)')
            plt.xlabel('Episode')
            plt.ylabel('Completion Rate')
            plt.ylim([0, 1.1])
        
        plt.tight_layout()
        plt.savefig('performance.png')
        plt.close()