# Equipo 1:
# Andrés Magaña - A01067963
# Ricardo Cáceres - A01706972
# Said Ortigoza - A01707430

from mesa import Agent, Model
from mesa.space import SingleGrid
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
from http.server import BaseHTTPRequestHandler, HTTPServer

import json
import logging
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128
import pandas as pd
import numpy as np

import time
import datetime

# Definimos la clase del agente
class Car(Agent):
    def __init__(self, unique_id, model, x, y, signal):
        super().__init__(unique_id, model)
        self.pos = (y, x)
        self.velocity = 4
        self.in_road = 1
        self.signal = signal
        self.reduce_velocity = 6

    def stop(self):
        if self.reduce_velocity % 2 == 0 and self.reduce_velocity >= 0:
            self.velocity -= 1
        if self.reduce_velocity != -1:
            self.reduce_velocity -= 1

    def change_lane(self):
        self_y, self_x = self.pos

        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False, radius = 5)
        for neighbor in neighbors:
            y, x = neighbor.pos

            # Checar carril superior
            if (y == self_y - 1) and not (self_x - 5 > x < self_x + 2):
                self.model.grid.move_agent(self, (self_y - 1, self_x + 2))
            # Checar carril inferior
            elif (y == self_y + 1) and not (self_x - 5 > x < self_x + 2):
                self.model.grid.move_agent(self, (self_y + 1, self_x + 2))
            else:
                rd_lane = np.random.choice([0, 2])
                self.model.grid.move_agent(self, (rd_lane, self_x + 2))

    def step(self):
        # Posición del agente
        self_y, self_x = self.pos

        # If siguiente posición sigue dentro del grid
        if not (self.model.grid.out_of_bounds((self_y, self_x + self.velocity))):
            # If la siguiente posición está vacía
            if self.model.grid.is_cell_empty((self_y, self_x + self.velocity)):
                # El coche avanza
                self.model.grid.move_agent(self, (self_y, self_x + self.velocity))
                if self_x >= (self.model.grid.height * 0.4) and self.signal == True:
                    self.stop()
            else:
                # Cambio de carril
                if self.signal == False and self_y == 1:
                    self.change_lane()
        else:
            self.in_road = 0

def get_grid(model):
    grid = np.zeros((model.grid.width, model.grid.height))
    for (content, x, y) in model.grid.coord_iter():
        if model.grid.is_cell_empty((x, y)):
            grid[x][y] = 0
        else:
            grid[x][y] = 1
    return grid

# Definimos la clase del modelo
class Road(Model):
    def __init__(self, width, height, num_cars):
        super().__init__()
        self.width = width
        self.height = height
        self.total_cars = num_cars
        self.num_cars = num_cars
        self.current_id = 0
        self.lock = True
        self.grid = SingleGrid(width, height, False)
        self.schedule = BaseScheduler(self)
        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})

    def step(self):
        if self.num_cars > 0:
            # Crear flujo irregular de coches
            flow_choice = np.random.choice([0, 1, 2, 3, 4])
            
            if self.num_cars == self.total_cars:
                flow_choice = 0
            
            # Colocar coches
            if flow_choice == 0 or flow_choice == 2 or flow_choice == 4:
                y = np.random.choice([0, 1, 2])
                chosen = False
                if self.num_cars <= self.total_cars * 0.60 and y == 1 and self.lock:
                    chosen = True
                    self.lock = False
                car = Car(self.next_id(), self, 0, y, chosen)
                self.schedule.add(car)
                self.grid.place_agent(car, car.pos)
                self.num_cars -= 1

        self.datacollector.collect(self)
        self.schedule.step()

        # Eliminar coches que terminaron su recorrido
        for car in self.schedule.agent_buffer():
            if car.in_road == 0:
                car.model.grid.remove_agent(car)
                self.schedule.remove(car)

# Definimos las dimensiones de la carretera
WIDTH = 3
HEIGHT = 250

# Definimos el número de agentes
NUM_CARS = 50

# Definimos el número máximo de ejecuciones
MAX_GENERATIONS = 1900

# Registramos el tiempo de inicio y ejecutamos la simulación
# start_time = time.time()
model = Road(WIDTH, HEIGHT, NUM_CARS)
# for i in range (MAX_GENERATIONS):
#     model.step()

# Imprimimos el tiempo que le tomó correr al modelo
# print('Tiempo de ejecución:', str(datetime.timedelta(seconds=(time.time() - start_time))))

# Simulacion gráfica
# all_grid = model.datacollector.get_model_vars_dataframe()

# fig, axs = plt.subplots(figsize=(15, 5))
# axs.set_xticks([])
# axs.set_yticks([])
# patch = plt.imshow(all_grid.iloc[0][0], cmap=plt.cm.binary)

# def animate(i):
#     patch.set_data(all_grid.iloc[i][0])

# anim = animation.FuncAnimation(fig, animate, frames = MAX_GENERATIONS)

# plt.show()

def ModelAgent_Data(model):

    # varsthingy = {}
    agent_data = []
    for agent in model.schedule.agent_buffer(False):
        if agent.pos != None:
            lane = agent.pos[0]
        else:
            lane = -1
        aux = {
            "id" : agent.unique_id,
            "speed" : agent.velocity,
            "lane" : int(lane)
        }
        agent_data.append(aux)
    
    vars = {
        "agents_data" : agent_data
    }

    jsonOut = json.dumps(vars, sort_keys=True)

    model.step()

    return jsonOut

class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        jsonOut = ModelAgent_Data(model)
        
        self._set_response()
        
        self.wfile.write(str(jsonOut).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()