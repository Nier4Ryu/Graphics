

def GenerateTiles_old(self):
        # y value is fixed. and then x/z vaule varies.
        # H is z and W is x
        h,w = self.map.shape
        for hp in range(4*h):
            for wp in range(4*w):
                if hp%2 != wp%2:
                    color = 'black'
                else:
                    color = 'white'

def GenerateWalls_old(self, test: int=0):
        size = self.tile_size/4
        color = 'white'
        threshold = 0
        edge_location=1.875*self.tile_size
        
        for i in range(16):
            for j in range(9):
                if i%2 == j%2:
                    color = 'black'
                else:
                    color = 'white'
                    # checker shape
                # ** Notice: -edge_location+size*i or +edge_location+size*i will give opposite side of edges
                # ** Notice: Changing x and z coordinate will give wall at other axis
                if test == 0:
                    self.GenerateSingleBlock(edge_location, j*size + threshold, -edge_location + size * i, size, color)
                elif test == 1:
                    self.GenerateSingleBlock(-edge_location + size * i, j*size + threshold, -edge_location, size, color)
                elif test == 2:
                    self.GenerateSingleBlock(-edge_location, j*size + threshold, -edge_location + size * i, size, color)
                elif test == 3:
                    self.GenerateSingleBlock(-edge_location + size * i, j*size + threshold, edge_location, size, color)
