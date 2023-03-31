import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import *

def read_energy():
    
    mainfilename = input('Enter main file name of your energy file\n')
    with open(mainfilename + '.energy','r') as fh:
        lines = fh.readlines()
    status = 'transform'
    return lines, status

def transform_bands_to_E_of_k(lines):
    
    numbers_of_bands = []
    bands = []
    kpoints = []
    E_of_k = []

    for line in lines[4:]:
    
        line_split = line.split()
    
        if len(line_split) == 2:
            bands[-1].append(float(line_split[1]))
        else:
            bands.append([])
            kpoints.append([float(line_split[0]), float(line_split[1]), float(line_split[2]), int(line_split[3])])
            numbers_of_bands.append(int(line_split[4]))

    for bands_of_kpoint in bands:
        E_of_k.append(bands_of_kpoint[:min(numbers_of_bands)])

    E_of_k = (np.array(E_of_k) - float(input('Enter fermi energy\n')))* 13.6056980659

    status = 'plot'
    return E_of_k, status

def plot_E_of_k(E_of_k):
    
    fig, ax = plt.subplots() 
    ax.plot(E_of_k)
    ax.set_title(input('Enter the title of the band plot\n'))
    ax.set_xlabel('Wave Vector')
    ax.set_ylabel('E - $E_F$ (eV)')
    ax.set_xlim(0, 999)
    ax.set_ylim(float(input('Enter lower limit of energy window\n')),float(input('Enter upper limit of energy window\n')))
    
    form = input('Choose string form or matrix form for constructing x label. (\'s\' or \'m\')\n')
    if form == 's':
        xticks = [0]
        xlabels = []
        lattice_type = input('Enter lattice type\n')
        kpath = input('Enter kpath\n')
        kpath_vec, kpath = kpath_translate(lattice_type, kpath)
        nk_new = uniform_sampling(kpath_vec, len(E_of_k) )
        for i, nk in enumerate(nk_new):
            xticks.append( xticks[i] + nk )
    elif form == 'm':
        xticks = [0]
        lattice_type = input('Enter lattice type\n')
        kpath = input('Enter kpath\n')
        nk_new = uniform_sampling( kpath_translate( input('Enter lattice type\n'), input('Enter kpath\n') ), len(E_of_k) )
        for i, nk in enumerate(nk_new):
            xticks.append( xticks[i] + nk )
    for i, k in enumerate(kpath):
        if k == 'G':
            k = '$\Gamma$'
        if i == 0 or i == len(kpath)-1:
            xlabels.append(k)
        else:
            if k == 'd':
                xlabels.append( kpath[i-1] + '|' + kpath[i+1] )
            elif k != 'd' and kpath[i-1] != 'd' and kpath[i+1] != 'd':
                xlabels.append(k)
    plt.xticks( xticks, xlabels )
    plt.savefig(input('Enter the name of the .png file\n') + '.png', format='png')

if __name__ == '__main__':

    status = 'read'
    
    while True:
        if status == 'read':
            
            try:
                lines, status = read_energy()
            except:
                sys.stderr.write('Invalid main file name\n')
            
        elif status == 'transform':
            
            try:
                E_of_k, status = transform_bands_to_E_of_k(lines)
            except:
                sys.stderr.write('Invalid number\n')
        
        elif status == 'plot':
            
            plot_E_of_k(E_of_k)
            status = 'rerun_or_exit'
        
        elif status == 'rerun_or_exit':

            status = input('Enter rerun or exit\n')
            
            if status == 'rerun':
                status = 'read'
            elif status == 'exit':
                break
            else:
                status = 'rerun_or_exit'
                print('Please enter rerun or exit\n')
