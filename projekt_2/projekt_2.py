import argparse
import numpy as np
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt 
plt.rcParams.update({'font.size': 22})

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

class Ising():

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
                energy += -np.float(args.J)*nb*S - np.float(args.B)*S
        return energy/2.

    
    def simulate(self):   
        N, beta = int(np.sqrt(int(args.grid_size))), np.float(args.beta)
        config = np.random.choice([-1, 1], p=[1-np.float(args.density), np.float(args.density)], size=(N,N))
        f = plt.figure(figsize=(15, 15), dpi=80)    
        self.configPlot(config, 0, N)
        energy = dict()
        for i in tqdm(range(int(args.steps))):
            self.mcmove(config, N, beta)
            if i % int(args.n_image)== 0: self.configPlot(config, i, N)
            energy[i] = self.calcEnergy(config, N)
        w = csv.writer(open("energy.csv", "w"))
        for time, e in energy.items():
            w.writerow([time, e])
                     
    def configPlot(self, config, i, N):
        X, Y = np.meshgrid(range(N), range(N))    
        plt.pcolormesh(X, Y, config, cmap=plt.cm.seismic)
        plt.title('Time=%d'%i)
        plt.axis('tight')
        plt.savefig("{}_{}.png".format(args.img_file, i))
        
rm = Ising()
rm.simulate()
