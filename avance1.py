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
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector

# AGENT CLASS
class Car(Agent):
    def __init__(self, unique_id, model, x, y, signal):
        super().__init__(unique_id, model)
        self.actual_position = (x, y)
        self.velocity = 3
        self.stopped = False
        self.signal = signal

    def step(self):
        self.model.grid.move_agent(self, (self.actual_position[0] + self.velocity, self.actual_position[1]))
        
        # Carro que se detendrá en el carril central

        # Checar carriles solo para el carril central
        if (self.actual_position[1] == 1):
            self.check_roads()

    def check_roads(self):
        for neighbor in self.model.grid.iter_neighbors(self.actual_position, moore = True, include_center = False, radius = 5):
            x, y = neighbor.actual_position
            # Central Lane in Front of Actual Agent
            if ((y == self.actual_position[1]) and (x <= self.actual_position[0] + 4) and (neighbor.stopped == True)):
                # Checar carril superior para cambiar posición
                if not ((y == self.actual_position[1] - 1) and (self.actual_position[0] + 1 < x >= self.actual_position[0] - 4) and (neighbor.stopped != True)):
                    # Cambia a carril superior
                    self.model.grid.move_agent(self, (self.actual_position[0] + 1, 0))
                # Checar carril inferior para cambiar posición
                elif not ((y == self.actual_position[1] + 1) and (self.actual_position[0] + 1 < x >= self.actual_position[0] - 4) and (neighbor.stopped != True)):
                    # Cambia a carril inferior
                    self.model.grid.move_agent(self, (self.actual_position[0] + 1, 2))

def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        grid[x][y] = content.live
    return grid

# MODEL CLASS
class Road(Model):
    def __init__(self, cars):
        super().__init__()
        self.cars = cars
        self.placeAgents = cars
        self.signal = False
        self.grid = SingleGrid(500, 3, False)
        self.schedule = BaseScheduler(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        y = np.random.choice([0, 1, 2])
        agent = Car(self.placeAgents, self, 0, y, self.signal)

        for i in range(0, 10, 1):
            if i == np.random.choice([5,6]):
                lane = np.random.choice([0,1,2])
                self.schedule.add(agent)
                self.grid.place_agent(agent, (lane, 0))
                self.placeAgents -=1

            if self.placeAgents == 50:
                self.signal = True
            else:
                self.signal = False

        self.datacollector.collect(self)
        self.schedule.step()

agents = 100
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