################################# AVANCE RETO 1 ################################################
#
# Equipo:
# Andrés Magaña Pérez - A01067963
# Ricardo Andrés Cáceres Villibord - A01706972
# Said Guadalupe Ortigoza Trujillo - A01707430
#
################################################################################################

import time
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

import pandas as pd
import numpy as np

from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

# AGENT CLASS
class Car(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.pos = (y, x)
        self.velocity = 3
        self.stopped = False
        self.signal = None

    def step(self):
        print(str(self.unique_id) + ": " + str(self.pos))
        if not (self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + self.velocity))):
            if self.model.grid.is_cell_empty((self.pos[0], self.pos[1] + self.velocity)):
                self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + self.velocity))

        # elif not (self.model.grid.out_of_bounds((self.pos[0] + self.velocity - 2, self.pos[1]))):
        #     self.model.grid.move_agent(self, (self.pos[0] + self.velocity - 2, self.pos[1]))
        else:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)

def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        if model.grid.is_cell_empty((x, y)):
            grid[x][y] = 0
        else:
            grid[x][y] = 1
    return grid

# TODO: Stop Function

# MODEL CLASS
class Road(Model):
    def __init__(self, cars):
        super().__init__()
        self.cars = cars
        self.current_id = 0
        self.signal = False
        self.grid = SingleGrid(3, 500, False)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        y = np.random.choice([0, 1, 2])

        lane = np.random.choice([0,1,2])

        agent = Car(self.next_id(), self, 0, y)
        if self.cars > 0:
            if self.grid.is_cell_empty((y, 0)):
                self.schedule.add(agent)
                self.grid.place_agent(agent, agent.pos)
                self.cars -= 1

        self.datacollector.collect(self)
        self.schedule.step()

agents = 3
model = Road(agents)
MAX_GENERATIONS = 200

# TODO: Add time measurement
for i in range (MAX_GENERATIONS):
    model.step()

# Simulacion grafica
all_grid = model.datacollector.get_model_vars_dataframe()
fig, axs = plt.subplots(figsize=(15, 5))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(all_grid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames = MAX_GENERATIONS)
plt.show()