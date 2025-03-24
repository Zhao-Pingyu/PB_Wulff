import glob
import os
import numpy as np
import re
from natsort import natsorted
import matplotlib.pyplot as plt

def get_energy():
    """
    Function for calculating the phase boundary energies of the different boundary plane inclinations
    """    
    
    E_Al = -3.81685565877244 # average per-atom energy of Al in perfect Al3Ni ortho (eV), two types -3.84109*1,-3.80474*2
    E_Ni = -4.03275843383911 # per-atom energy of Ni in perfect Al3Ni (eV)
    A = 80**2 # sphere phase boundary area (angstrom^2)
    ecoh_Al = -3.35999998818379 # cohesive energy of Al in perfect Al lattice (eV)
    PBE_min = []
    for i in range(181):
        file = f'log-Al-NiAl3-{i}.lammps'
        TE = []
        N_Al = []
        N_Al_NiAl3 = []
        N_Ni_NiAl3 = []
        with open(file, 'r') as infile:
            data = infile.readlines()
            for line in data:
                match1 = re.match(r'Total energy (\S+)', line)
                match2 = re.match(r'Number of atoms in Al (\S+)', line)
                match3 = re.match(r'Number of Al in NiAl3 (\S+)', line)
                if match1:
                    b = re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0]
                    TE.append(b)
                if match2:
                    s = re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0]
                    N_Al.append(s)
                if match3:
                    n1 = re.findall(r"[-+]?(?:\d*\.*\d+)", line)[1]
                    n2 = re.findall(r"[-+]?(?:\d*\.*\d+)", line)[3]
                    N_Al_NiAl3.append(n1)
                    N_Ni_NiAl3.append(n2)

        TE = np.array(TE).astype('float')
        N_Al = np.array(N_Al).astype('int')
        N_Al_NiAl3 = np.array(N_Al_NiAl3).astype('int')
        N_Ni_NiAl3 = np.array(N_Ni_NiAl3).astype('int')
        #print(N_Al,N_Al_NiAl3,N_Ni_NiAl3)
        PBE = (TE-ecoh_Al*N_Al-E_Al*N_Al_NiAl3-E_Ni*N_Ni_NiAl3)/A*16021.7733 # phase boundary energy (mJ/m^2)
        PBE_min.append(np.min(PBE))
    return PBE_min

def get_full_range(PBE_min):
    """
    Function for obtaining the full range of boundary plane inclinations (0-360 degrees) through crystal symmetry
    """
    deg = np.arange(0,361)
    En = np.zeros_like(deg)
    for i in range(0,361):
        if i<=180:
            En[i] = PBE_min[i]
        else:
            En[i] = PBE_min[i-180]
    return En
        
def plot_wulff(En):
    """
    Function for Wulff shape construction
    """
    
    fi = np.arange(0,361)
    r = En*20
    x = r*np.cos(fi*np.pi/180)
    y = r*np.sin(fi*np.pi/180)
    incs = np.arange(0,361)
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    # Wulff construction
    for i, p in zip(fi, fi*np.pi/180):
        t = np.linspace(-1, 1, 100)
        x1 = -1.5*np.sin(p)*t + x[i]
        y1 = 1.5*np.cos(p)*t + y[i]
        ax.plot(x1, y1, "r--", linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')

    ax.plot(x,y)
    plt.tick_params(left = False, right = False , labelleft = False,labelbottom = False, bottom = False)
    plt.show()

    # Generate mask
    incs = np.append(incs, np.argsort(r))
    mask = np.zeros(shape=(1000, 1000))
    xx, yy = np.meshgrid(np.arange(-500, 500), np.arange(-500, 500))
    r0 = 250
    ratio = 1.2
    for i, p in zip(chosen, fi*np.pi/180):
        xx1 = (xx*np.cos(p) - yy*np.sin(p))
        mask[xx1 >= (r[i]*r0/np.min(r)/ratio)] = 1

    plt.axis('off')
    plt.imshow(mask, cmap='gray')
    plt.show()
    
if __name__=="__main__":
    PBE_min = get_energy()
    En = get_full_range(PBE_min)
    plot_wulff(En)
