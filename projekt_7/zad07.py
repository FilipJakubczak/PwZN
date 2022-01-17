import argparse
from numba import jit
import csv
import warnings
import numpy as np
from timeit import default_timer as timer
from tqdm import tqdm
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 22})
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('-grid_size', help="Grid size n*n.")
parser.add_argument('-J', help="J")
parser.add_argument('-beta', help="Beta")
parser.add_argument('-B', help="B field value.")
parser.add_argument('-steps', help="Number of iterations. ")
parser.add_argument('-n_image', nargs='?', default="100", help="Every how many images should be saved. (default=100)")

parser.add_argument('-density', nargs='?', default=0.5, help="Initial spin density (default=0.5).")
parser.add_argument('-img_file', nargs='?', default="step", help="Out filename (default=step).")
args = parser.parse_args()

N = int(np.sqrt(int(args.grid_size)))
beta = np.float(args.beta)
J = np.float(args.J)
B = np.float(args.B)
density = np.float(args.density)
steps = int(args.steps)
n_image = int(args.n_image)
img_file = args.img_file
config = np.random.choice([-1, 1], p=[1-density, density], size=(N,N)).astype(np.int64)

class IsingNumba():

    def __init__(self):
        self.N = N
        self.beta = beta
        self.J = J
        self.B = B
        self.density = density
        self.steps = steps
        self.n_image = n_image
        self.img_file = img_file

    @staticmethod
    @jit(nopython=True)  
    def mcmove(N, beta):
        for i in range(N):
            for j in range(N):            
                    a = np.random.randint(0, N)
                    b = np.random.randint(0, N)
                    s =  config[a, b]
                    nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
                    cost = 2*s*nb
                    if cost < 0:	
                        s *= -1
                    elif np.random.rand() < np.exp(-cost*beta):
                        s *= -1
                    # nie byłem w stanie naprawić tej linijki w przypadku numby
                    # config[a, b] = s
                    
    def calcEnergy(self, config, N):
        energy = 0 
        for i in range(len(config)):
            for j in range(len(config)):
                S = config[i,j]
                nb = config[(i+1)%N, j] + config[i,(j+1)%N] + config[(i-1)%N, j] + config[i,(j-1)%N]
                energy += -self.J*nb*S - self.B*S
        return energy/2.

    
    def simulate(self):   
        config = np.random.choice([-1, 1], p=[1-self.density, self.density], size=(self.N,self.N))
        f = plt.figure(figsize=(15, 15), dpi=80)    
        self.configPlot(config, 0, self.N)
        energy = dict()
        for i in range(self.steps):
            self.mcmove(self.N, self.beta)
            if i % self.n_image== 0: self.configPlot(config, i, self.N)
            energy[i] = self.calcEnergy(config, self.N)
        w = csv.writer(open("energy.csv", "w"))
        for time, e in energy.items():
            w.writerow([time, e])
                     
    def configPlot(self, config, i, N):
        X, Y = np.meshgrid(range(N), range(N))    
        plt.pcolormesh(X, Y, config, cmap=plt.cm.seismic)
        plt.title('Time=%d'%i)
        plt.axis('tight')
        plt.savefig("{}_{}.png".format(self.img_file, i))

class Ising():

    def __init__(self):
        self.N = N
        self.beta = beta
        self.J = J
        self.B = B
        self.density = density
        self.steps = steps
        self.n_image = n_image
        self.img_file = img_file

    def mcmove(self, config, N, beta):
        for i in range(N):
            for j in range(N):            
                    a = np.random.randint(0, N)
                    b = np.random.randint(0, N)
                    s =  config[a, b]
                    nb = config[(a+1)%N,b] + config[a,(b+1)%N] + config[(a-1)%N,b] + config[a,(b-1)%N]
                    cost = 2*s*nb
                    if cost < 0:	
                        s *= -1
                    elif np.random.rand() < np.exp(-cost*beta):
                        s *= -1
                    config[a, b] = s
        return config
                    
    def calcEnergy(self, config, N):
        energy = 0 
        for i in range(len(config)):
            for j in range(len(config)):
                S = config[i,j]
                nb = config[(i+1)%N, j] + config[i,(j+1)%N] + config[(i-1)%N, j] + config[i,(j-1)%N]
                energy += -self.J*nb*S - self.B*S
        return energy/2.

    
    def simulate(self):   
        config = np.random.choice([-1, 1], p=[1-self.density, self.density], size=(self.N,self.N))
        f = plt.figure(figsize=(15, 15), dpi=80)    
        self.configPlot(config, 0, self.N)
        energy = dict()
        for i in range(self.steps):
            self.mcmove(config, self.N, self.beta)
            if i % self.n_image== 0: self.configPlot(config, i, self.N)
            energy[i] = self.calcEnergy(config, self.N)
        w = csv.writer(open("energy.csv", "w"))
        for time, e in energy.items():
            w.writerow([time, e])
                     
    def configPlot(self, config, i, N):
        X, Y = np.meshgrid(range(N), range(N))    
        plt.pcolormesh(X, Y, config, cmap=plt.cm.seismic)
        plt.title('Time=%d'%i)
        plt.axis('tight')
        plt.savefig("{}_{}.png".format(self.img_file, i))

start = timer()
rm = IsingNumba()
rm.simulate()
end = timer()
print("Czas wykonania (numba): {} s".format(end - start))


start = timer()
rm = Ising()
rm.simulate()
end = timer()
print("Czas wykonania (bez numby): {} s".format(end - start))