import gymnasium as gym
from gymnasium import Env
from gymnasium.spaces import Discrete, Box
import numpy as np
import random

class SnakeEnv(Env):
    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.grid_size = 10
        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=1, shape=(self.grid_size, self.grid_size), dtype=np.float32)
        self.reset()

    def reset(self):
        self.snake = [(5, 5)]
        self.food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
        while self.food in self.snake:
            self.food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
        self.done = False
        self.direction = 0
        return self._get_observation(), {}

    def step(self, action):
        if action in [0, 1, 2, 3]:
            self.direction = action

        head = self.snake[0]
        if self.direction == 0:
            new_head = (head[0] - 1, head[1])
        elif self.direction == 1:
            new_head = (head[0] + 1, head[1])
        elif self.direction == 2:
            new_head = (head[0], head[1] - 1)
        elif self.direction == 3:
            new_head = (head[0], head[1] + 1)

        if (new_head[0] < 0 or new_head[0] >= self.grid_size or
            new_head[1] < 0 or new_head[1] >= self.grid_size or
            new_head in self.snake):
            self.done = True
            reward = -10
        else:
            self.snake.insert(0, new_head)
            if new_head == self.food:
                reward = 10
                self.food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
                while self.food in self.snake:
                    self.food = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            else:
                self.snake.pop()
                reward = -0.1

        return self._get_observation(), reward, self.done, {}

    def render(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype=str)
        grid[:] = '.'
        for (x, y) in self.snake:
            grid[x, y] = 'S'
        grid[self.food[0], self.food[1]] = 'F'
        print("\n".join(["".join(row) for row in grid]))
        print()

    def _get_observation(self):
        obs = np.zeros((self.grid_size, self.grid_size), dtype=np.float32)
        for (x, y) in self.snake:
            obs[x, y] = 1.0
        obs[self.food[0], self.food[1]] = 0.5
        return obs

def manual_control(env):
    action_map = {'w': 0, 's': 1, 'a': 2, 'd': 3}
    obs, info = env.reset()
    env.render()

    while True:
        key = input("Digite w (cima), s (baixo), a (esquerda), d (direita): ")
        if key not in action_map:
            print("Comando inválido! Use apenas 'w', 's', 'a', 'd'.")
            continue
        action = action_map[key]
        obs, reward, done, _ = env.step(action)
        env.render()
        print(f"Reward: {reward}")
        if done:
            print("Game Over!")
            break

def ai_control(env):
    def get_action(snake, food):
        head = snake[0]
        if head[0] < food[0]:
            return 1
        elif head[0] > food[0]:
            return 0
        elif head[1] < food[1]:
            return 3
        elif head[1] > food[1]:
            return 2
        return random.choice([0, 1, 2, 3])

    obs, info = env.reset()
    env.render()

    while True:
        action = get_action(env.snake, env.food)
        obs, reward, done, _ = env.step(action)
        env.render()
        print(f"Reward: {reward}")
        if done:
            print("Game Over!")
            break

if __name__ == "__main__":
    print("Escolha o modo de controle:")
    print("1 - Manual (WASD)")
    print("2 - Automático (IA)")

    choice = input("Digite sua escolha (1 ou 2): ")
    env = SnakeEnv()

    if choice == '1':
        manual_control(env)
    elif choice == '2':
        ai_control(env)
    else:
        print("Opção inválida!")
