import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import *

def read_energy():
    
    try:
        with open('EIGENVAL','r') as fh:
            lines = fh.readlines()
    except:
        
        sys.stderr.write('EIGENVAL file Not Found\n')
        
        mainfilename = input('Enter main file name of your energy file\n')
        
        with open(mainfilename,'r') as fh:
            lines = fh.readlines()
    
    status = 'transform'
    
    return lines, status

def transform_bands_to_E_of_k(lines):
    
    numbers_of_bands = []
    bands = []
    kpoints = []
    E_of_k = []
    
    Ef = float(input('Enter fermi energy\n'))
    
    if len(lines[0].split()) == 4:
        
        NBANDS = int(lines[5].split()[2])
        
        for line in lines[7:]:
            
            l = line.split()
            
            if len(l) == 3:
                E_of_k.append(float(l[1]))
        
        E_of_k = np.array(E_of_k).reshape((-1,NBANDS)) - Ef
        
    else:
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

        E_of_k = (np.array(E_of_k) - Ef)* 13.6056980659

    status = 'plot'
    return E_of_k, status

def plot_E_of_k(E_of_k):
    
    fig, ax = plt.subplots() 
    ax.plot(E_of_k,color='b')
    ax.set_title(input('Enter the title of the band plot\n'))
    ax.set_xlabel('Wave Vector')
    ax.set_ylabel('E - $E_F$ (eV)')
    ax.set_xlim(0, E_of_k.shape[0]-1)
    ax.set_ylim(float(input('Enter lower limit of energy window\n')),float(input('Enter upper limit of energy window\n')))
    
    try:
        xticks, xlabels = read_klabel()
    except:
        sys.stderr.write('File Not Found!\n')
        xticks, xlabels = write_klabel(E_of_k)
    
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    ax.grid()
    plt.savefig(input('Enter the name of the .png file\n') + '.png', format='png')

def read_klabel():
    
    try:
        
        with open('klabel', 'r') as fh:
        
            lines = fh.readlines()
        
    except:
        
        sys.stderr.write('klabel file Not Found\n')
        
        kpath_file = input('Enter your kpath file name\n')
    
        with open(kpath_file, 'r') as fh:
        
            lines = fh.readlines()
    
    xlabels = []
    xticks  = []
    
    for line in lines[1:]:
        
        xlabels.append(line.split()[0])
        xticks.append(int(line.split()[1]))
    
    return xticks, xlabels

def write_klabel(E_of_k):
    
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
    
    return xticks, xlabels

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
