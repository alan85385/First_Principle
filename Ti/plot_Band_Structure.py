import numpy as np
import matplotlib.pyplot as plt
import sys

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
    
    xticks, xlabels, start, end = read_klabel()
    show = np.full((E_of_k.shape[0]), True)
    
    for i,(s, e) in enumerate(zip(start,end)):
        
        if s == 0:
            d = 0
        else:
            d += s-end[i-1]
            
        ax.plot(np.arange(s-d,e+1-d),E_of_k[s:e+1],color='b')
        plt.axvline(s-d,color='black',linewidth = 1.8)
        
    ax.set_title(input('Enter the title of the band plot\n'))
    ax.set_xlabel('Wave Vector')
    ax.set_ylabel('E - $E_F$ (eV)')
    
    ax.set_xlim(0,E_of_k.shape[0]-d-1)
    
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
        xticks.append(line.split()[-1])
    
    xlabels = np.array(xlabels,dtype='U25')
    
    xlabels[xlabels=='G'] = '$\Gamma$'
    
    xlabels_new = []
    xticks_new  = []
    
    start = [0]
    end   = []
    
    d = 0
    for i,(k,t) in enumerate(zip(xlabels,xticks)):
        
        if i == 0 or i == len(xlabels)-1:
            xlabels_new.append(k)
            xticks_new.append(int(t)-d)
        else:
            if k == 'd':
                xlabels_new.append( xlabels[i-1] + '|' + xlabels[i+1] )
                d += int(xticks[i+1]) - int(xticks[i-1])
                xticks_new.append(int(xticks[i-1]))
                start.append(int(xticks[i+1]))
                end.append(int(xticks[i-1]))
            elif k != 'd' and xlabels[i-1] != 'd' and xlabels[i+1] != 'd':
                xlabels_new.append(k)
                xticks_new.append(int(t)-d)
            else:
                pass
            
    end.append(int(xticks[-1]))
            
    xticks, xlabels = xticks_new.copy(), xlabels_new.copy()
    
    return xticks, xlabels, start, end

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
