# Equipo 1:
# Andrés Magaña - A01067963
# Ricardo Cáceres - A01706972
# Said Ortigoza - A01707430

# Importamos las clases que se requieren para manejar los agentes (Agent) y su entorno (Model).
# Cada modelo puede contener múltiples agentes.
from mesa import Agent, Model

# Debido a que sólo puede existir un agente por celda, elegimos SingleGrid.
from mesa.space import SingleGrid

# Con BaseScheduler, hacemos que los agentes se activen en el orden que aparecen.
from mesa.time import BaseScheduler

# Utilizamos DataCollector para obtener información de cada paso de la simulación.
from mesa.datacollection import DataCollector

# Utilizamos matplotlib para crear una animación de cada uno de los pasos del modelo.
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

# Utilizamos los siguientes paquetes para el manejo de valores numéricos.
import pandas as pd
import numpy as np

# Utilizamos time y datetime para medir el tiempo de ejecución de nuestro algoritmo.
import time
import datetime

# Definimos la clase del agente.
class Car(Agent):
    def __init__(self, unique_id, model, x, y):
        super().__init__(unique_id, model)
        self.pos = (y, x)
        self.velocity = 3
        self.in_road = 1
        self.stopped = False
        self.signal = None

    # Este método especifica lo que debe hacer el agente en cada step.
    def step(self):
        self_y, self_x = self.pos
        if not (self.model.grid.out_of_bounds((self_y, self_x + self.velocity))) and self.model.grid.is_cell_empty((self_y, self_x + self.velocity)):
            self.model.grid.move_agent(self, (self_y, self_x + self.velocity))
        else:
            self.in_road = 0

# Esta función nos permite obtener el estado de los diferentes agentes.
def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        if model.grid.is_cell_empty((x, y)):
            grid[x][y] = 0
        else:
            grid[x][y] = 1
    return grid

# Definimos la clase del modelo.
class Road(Model):
    def __init__(self, width, height, num_cars):
        super().__init__()
        self.width = width
        self.height = height
        self.num_cars = num_cars
        self.current_id = 0
        self.signal = False
        self.grid = SingleGrid(height, width, False)
        self.schedule = BaseScheduler(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    # Este método define lo que debe hacer el modelo en cada step.
    def step(self):
        y = np.random.choice([0, 1, 2])
        agent = Car(self.next_id(), self, 0, y)
        if self.num_cars > 0 and self.grid.is_cell_empty((y, 0)):
            self.schedule.add(agent)
            self.grid.place_agent(agent, agent.pos)
            self.num_cars -= 1
        self.datacollector.collect(self)
        self.schedule.step()
        for car in self.schedule.agent_buffer():
            if car.in_road == 0:
                agent.model.grid.remove_agent(car)
                self.schedule.remove(car)

# Definimos las dimensiones del grid.
HEIGHT = 3
WIDTH = 250

# Definimos el número de agentes.
NUM_CARS = 850

# Definimos el número máximo de ejecuciones.
MAX_GENERATIONS = 1900

# Registramos el tiempo de inicio y ejecutamos la simulación.
start_time = time.time()
model = Road(WIDTH, HEIGHT, NUM_CARS)
for i in range (MAX_GENERATIONS):
    model.step()

# Imprimimos el tiempo que le tomó correr al modelo.
print('Tiempo de ejecución:', str(datetime.timedelta(seconds=(time.time() - start_time))))

# Simulacion gráfica.
all_grid = model.datacollector.get_model_vars_dataframe()

fig, axs = plt.subplots(figsize=(15, 5))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(all_grid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames = MAX_GENERATIONS)

plt.show()
