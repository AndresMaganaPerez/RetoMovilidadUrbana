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
                