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
from mesa.time import SimultaneousActivation
from mesa.datacollection import DataCollector

# AGENT CLASS

class RoadAgent(Agent):
    def __init__(self, unique_id, model, x, y, right_position, left_position, front_position, velocity):
        super().__init__(unique_id, model)
        self.actual_position = (x, y)
        # self.front_position = front_position
        # self.right_position = right_position
        # self.left_position = left_position
        self.velocity = velocity

    def step(self):
         self.check_roads()
        

         # self.actual_position = self.actual_position[0] + self.velocity

    def check_roads(self):
        # Front
        next_cell_position = (self.actual_position[1], self.actual_position[0] + 1) 
        next_cell_ = self.model.grid.get_cell_list_contents(
                [next_cell_position_east])
        if (self.actual_position[0] + 2 == )


def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        grid[x][y] = content.live
    return grid


class GameLifeModel(Model):
    def __init__(self, width, height):
        self.num_agents = width * height
        self.grid = SingleGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

        for (content, x, y) in self.grid.coord_iter():
            a = GameLifeAgent((x, y), self)
            self.grid.place_agent(a, (x, y))
            self.schedule.add(a)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

GRID_SIZE = 100
MAX_GENERATIONS = 100

start_time = time.time()
model = GameLifeModel(GRID_SIZE, GRID_SIZE)
for i in range (MAX_GENERATIONS):
    model.step()
print("Tiempo de ejecucion: ", str(datetime.timedelta(seconds= (time.time() - start_time))))

all_grid = model.datacollector.get_model_vars_dataframe()

fig, axs = plt.subplots(figsize=(7, 7))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(all_grid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames=MAX_GENERATIONS)
plt.show()