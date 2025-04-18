
import random
import pygame
from constants import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Environment:
    def __init__(self, difficulty_level):
        # Generate obstacles only once
        self.difficulty = difficulty_level  # 👈 Sauvegarde la difficulté
        self.obstacles = []
        self.generate_obstacles()
        self.reset()
        
    def generate_obstacles(self):
        # Initial agent and goal positions
        self.initial_agent_pos = [0, 0]
        self.goal_pos = [GRID_WIDTH - 1, GRID_HEIGHT - 1]
        
        # Generate obstacles once
        num_obstacles = self.difficulty  # 👈 Utilise la difficulté passée
        for _ in range(num_obstacles):
            pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
            # Make sure obstacles don't overlap with agent or goal
            while pos == self.initial_agent_pos or pos == self.goal_pos or pos in self.obstacles:
                pos = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
            self.obstacles.append(pos)
        
    def reset(self):
        # Reset agent to starting position without changing obstacles
        self.agent_pos = self.initial_agent_pos.copy()
        self.visited_cells = set([tuple(self.agent_pos)])  # Track visited cells
        self.done = False
        self.steps = 0
        return self.get_state()
    
    def get_state(self):
        # State is represented as the agent's position
        return tuple(self.agent_pos)
    
    def step(self, action):
        # Actions: 0=up, 1=right, 2=down, 3=left
        self.steps += 1
        
        # Previous position
        old_pos = self.agent_pos.copy()
        
        # Move agent based on action
        if action == 0 and self.agent_pos[1] > 0:  # Up
            self.agent_pos[1] -= 1
        elif action == 1 and self.agent_pos[0] < GRID_WIDTH - 1:  # Right
            self.agent_pos[0] += 1
        elif action == 2 and self.agent_pos[1] < GRID_HEIGHT - 1:  # Down
            self.agent_pos[1] += 1
        elif action == 3 and self.agent_pos[0] > 0:  # Left
            self.agent_pos[0] -= 1
        
        current_pos_tuple = tuple(self.agent_pos)
            
        # Check if agent hit an obstacle
        if self.agent_pos in self.obstacles:
            self.agent_pos = old_pos  # Move back
            reward = -5  # Penalty for hitting obstacle
        elif self.agent_pos == self.goal_pos:
            reward = 100  # Reward for reaching goal
            self.done = True
        else:
            # Base penalty for step
            reward = -1
            
            # Small reward for visiting a new cell (exploration bonus)
            if current_pos_tuple not in self.visited_cells:
                reward += 0.5
                self.visited_cells.add(current_pos_tuple)
            
            # Small reward for getting closer to the goal (Manhattan distance)
            goal_distance = abs(self.agent_pos[0] - self.goal_pos[0]) + abs(self.agent_pos[1] - self.goal_pos[1])
            max_possible_distance = GRID_WIDTH + GRID_HEIGHT
            proximity_reward = 0.2 * (1 - goal_distance / max_possible_distance)
            reward += proximity_reward
            
        # Timeout after too many steps
        if self.steps >= 200:
            self.done = True
            
        return self.get_state(), reward, self.done
    
    def render(self):
        screen.fill((20, 20, 30))  # Darker background
        
        # Draw grid with a soft tint
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                rect = pygame.Rect(i * GRID_SIZE, j * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (40, 40, 60), rect)
                pygame.draw.rect(screen, (60, 60, 90), rect, 1)  # subtle border

        # Draw visited cells with soft highlight
        for cell in self.visited_cells:
            if list(cell) != self.agent_pos and list(cell) != self.goal_pos:
                cell_rect = pygame.Rect(cell[0] * GRID_SIZE + 4, cell[1] * GRID_SIZE + 4,
                                        GRID_SIZE - 8, GRID_SIZE - 8)
                pygame.draw.rect(screen, (80, 80, 120), cell_rect, border_radius=6)

        # Draw obstacles with 3D box effect
        for obs in self.obstacles:
            rect = pygame.Rect(obs[0] * GRID_SIZE + 2, obs[1] * GRID_SIZE + 2,
                            GRID_SIZE - 4, GRID_SIZE - 4)
            pygame.draw.rect(screen, (160, 60, 60), rect, border_radius=6)
            pygame.draw.rect(screen, (200, 100, 100), rect, 2)  # border

        # Draw goal with glowing green effect
        goal_rect = pygame.Rect(self.goal_pos[0] * GRID_SIZE + 4,
                                self.goal_pos[1] * GRID_SIZE + 4,
                                GRID_SIZE - 8, GRID_SIZE - 8)
        pygame.draw.rect(screen, (50, 220, 100), goal_rect, border_radius=8)
        pygame.draw.rect(screen, (180, 255, 180), goal_rect, 2)

        # Draw flag icon on goal
        pygame.draw.polygon(screen, YELLOW,
                            [(self.goal_pos[0]*GRID_SIZE + 20, self.goal_pos[1]*GRID_SIZE + 12),
                            (self.goal_pos[0]*GRID_SIZE + 32, self.goal_pos[1]*GRID_SIZE + 16),
                            (self.goal_pos[0]*GRID_SIZE + 20, self.goal_pos[1]*GRID_SIZE + 20)])

        # Draw agent as glowing ball
        agent_x = self.agent_pos[0] * GRID_SIZE + GRID_SIZE // 2
        agent_y = self.agent_pos[1] * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(screen, (0, 180, 255), (agent_x, agent_y), GRID_SIZE // 2 - 5)
        pygame.draw.circle(screen, (150, 230, 255), (agent_x, agent_y), GRID_SIZE // 2 - 10, 2)

        # Add episode info
        font = pygame.font.SysFont('Consolas', 24, bold=True)
        info_surface = font.render(f"Steps: {self.steps}", True, (255, 255, 255))
        screen.blit(info_surface, (10, 10))

        # Optional: draw frame border
        pygame.draw.rect(screen, (255, 255, 255), 
                        pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)

        pygame.display.flip()

