class Cars(Agent):
    def _init_(self, uniqueId, model, theChosenOne):
        super()._init_(uniqueId, model)
        self.speed = 4
        self.wantChange = False
        self.preference = np.random.choice([0,2])
        self.locked = theChosenOne
        self.stepStop = 6
        # OTHER ATTRIBBUTES #

    def checkSpeedFront(self, neighbor):
        if neighbor.speed != self.speed and neighbor.speed >= 0 and not self.locked:
            self.speed = neighbor.speed
            if self.pos[0] == 1 and self.speed <= 3:
                self.wantChange = True

    def checkSpeedSide(self, neighbor):
        if neighbor.speed < self.speed and neighbor.speed >= 0:
            if neighbor.pos[0] == 1:
                self.speed = 3

    def stopCar(self):
        if self.stepStop % 2 == 0 and self.stepStop >= 0:
            self.speed -= 1
        if self.stepStop != -1:
            self.stepStop -= 1

    def step(self):
        left = 0
        right = 0
        front = 0
        minfront = 5
        if self.pos != None:
            if self.locked == True:
                if self.pos[1] > self.model.grid.height/3:
                    self.stopCar()
                if not (self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + self.speed))):
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + self.speed))
            else:
                for neighbor in self.model.grid.iter_neighbors(self.pos, moore = True, include_center = False, radius = 5):
                    x, y = neighbor.pos
                    if ((x == self.pos[0]) and (y <= (self.pos[1] + minfront) and y > self.pos[1])):
                        minfront = y - self.pos[1]
                        self.checkSpeedFront(neighbor)
                        front += 1
                    if ((self.pos[0] == 0 or self.pos[0] == 2) and x == 1 and y >= (self.pos[1] + 1)):
                        self.checkSpeedSide(neighbor)
                    if self.pos[0] == 1 and (x == 0 or x == 2) and (y <= self.pos[1] + 1):
                        if x == 0:
                            left += 1
                        else:
                            right += 1

                if not (self.model.grid.out_of_bounds((self.pos[0], self.pos[1] + self.speed))):
                    if self.wantChange and (left == 0 or right == 0) and (self.pos[0] == 1):
                        if self.preference == 0:
                            if left == 0:
                                self.model.grid.move_agent(self, (0, self.pos[1] + 1))
                            else:
                                self.model.grid.move_agent(self, (2, self.pos[1] + 1))
                        else:
                            if right == 0:
                                self.model.grid.move_agent(self, (2, self.pos[1] + 1))
                            else:
                                self.model.grid.move_agent(self, (0, self.pos[1] + 1))
                        self.speed = 2
                    else:
                        if front == 0:
                            self.speed = 4

                        self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + self.speed))
                else:
                    self.model.grid.remove_agent(self)

                

def getGrid(model):
    grid = np.zeros( (model.grid.width, model.grid.height) )
    for (content, x, y) in model.grid.coord_iter():
        if model.grid.is_cell_empty((x, y)):
            grid[x][y] = 0
        else:
            grid[x][y] = 1
    return grid

class Highway(Model):
    def _init_(self, numAgents):
        super()._init_()
        self.numAgents = numAgents
        self.startAgents = numAgents
        self.chosenchosen = False
        self.schedule = BaseScheduler(self)
        self.grid = SingleGrid(3, 300, False)
        self.datacollector = DataCollector(model_reporters={"Grid" : getGrid})

    def step(self):
        if self.numAgents > 0:
            doI = np.random.choice([0,1,2,3,4])
            if self.numAgents == self.startAgents:
                doI = 2
            if doI == 2 or doI == 3:
                lane = np.random.choice([0,1,2])
                theChosen = False
                if self.numAgents < self.startAgents/2 and lane == 1 and not self.chosenchosen:
                    theChosen = True
                    self.chosenchosen = True
                a = Cars(self.numAgents, self, theChosen)
                self.schedule.add(a)
                self.grid.place_agent(a, (lane, 0))
                self.numAgents -= 1
        
        self.datacollector.collect(self)
        self.schedule.step()

numAgents = 1000
model = Highway(numAgents)
MAX_ITER = 300
for i in range(MAX_ITER):
    model.step()

allGrid = model.datacollector.get_model_vars_dataframe()
fig, axs = plt.subplots(figsize = (18, 4))
axs.set_xticks([])
axs.set_yticks([])
patch = plt.imshow(allGrid.iloc[0][0], cmap=plt.cm.binary)

def animate(i):
    patch.set_data(allGrid.iloc[i][0])

anim = animation.FuncAnimation(fig, animate, frames=MAX_ITER)
plt.show()