import sys
import numpy as np

def main():

    '''
    The main program flow
    '''

    library = init() #Initialize with Lattice_Information.txt
    kpath_matrix, total_kpoints, lattice_type, kpath = ask(library) #Get parameters from user
    fraction, number = generate_kpath(kpath_matrix, total_kpoints) #Generate kpoints between kpath's high symmetry points
    write_file(fraction, lattice_type, kpath, number) #Write 3 files: klist_band, KPOINTS and klabel

def init():

    '''
    Initialize the lattice types and the k points library through Lattice_Information.txt
    '''

    file_name = 'Lattice_Information.txt' #Lattice_Information.txt records some lattice types and their k points

    lines = read_file(file_name)
    library = tranform_lines_into_library(file_name, lines)

    return library

def read_file(file_name):

    '''
    A function which reads the Lattice_Information.txt file and return lines
    '''
    
    try:
        with open(file_name, 'r') as fh:
            lines = fh.readlines()

    except:
        sys.stderr.write(f'{file_name} is Not Found')
    
    return lines

def tranform_lines_into_library(file_name, lines):

    '''
    A function which transforms lines into the standard form of library and return library
    '''

    library = {} #collect the information of the lattice types and the k points
    
    for line in lines:

        line = line.split()

        if len(line) == 1: #the length of the line = 1 means the line contains the information of the lattice type
            lattice_type = line[0]
            library[lattice_type] = {}
        elif len(line) == 4: #the length of the line = 4 means the line contains the information of the k point
            high_symmetry_kpoint = line[0]
            library[lattice_type][high_symmetry_kpoint] = np.array(line[1:4], dtype = 'float')
        else:
            print(f'There are some problems in the {file_name} file')

    return library

def ask(library):
    
    lattice_type = ask_lattice_type(library)
    
    kpath_matrix, kpath = ask_kpath(library, lattice_type)
    
    total_kpoints = ask_total_kpoints()
    
    return kpath_matrix, total_kpoints, lattice_type, kpath

def ask_lattice_type(library):

    '''
    To ask kpath from user
    '''

    while True:
        
        lattice_type = input(f'Enter the lattice type in the lattice type library {tuple(library.keys())} \n')
        
        if lattice_type in library.keys():
            break
        else:
            print(f'There is no \'{lattice_type}\' lattice type in the lattice type library {tuple(library.keys())}')

    return lattice_type

def ask_kpath(library, lattice_type):

    '''
    The function can collect kpath from user
    '''

    while True:
        
        kpath = input(f'Enter the kpath with the string form \n{tuple(library[lattice_type])}\n')
        kpath_matrix = np.zeros(shape=(len(kpath),3))
        all_correct = True

        for i, k in enumerate(kpath):

            if k in library[lattice_type]:
                kpath_matrix[i] = library[lattice_type][k]
            else:
                all_correct = False
                print(f'{k} doesn\'t exist in {tuple(library[lattice_type].keys())}')
        
        if all_correct == True:
            break

    return kpath_matrix, kpath

def ask_total_kpoints():
    
    try:
        total_kpoints = int(input('Enter total kpoints\n'))
    except:
        sys.stderr.write('Invalid argumets!\n')
        
    return total_kpoints

def generate_kpath(kpath_matrix, total_kpoints):

    kpath_delta = kpath_matrix[1:] - kpath_matrix[0:-1]
    length = np.linalg.norm(kpath_delta, axis = 1)
    total_length = length.sum()
    kpoints_number_of_each_kpath = np.round(total_kpoints*length/total_length)

    for i, N in enumerate(kpoints_number_of_each_kpath):
        
        N = int(N)
        
        start = np.array(kpath_matrix[i])
        end = np.array(kpath_matrix[i+1])
        denominator = 10000

        start *= denominator
        end *= denominator

        start_end_denominator = np.append(np.append(start,end),denominator)
        gcd = np.gcd.reduce(np.array(start_end_denominator, dtype='int32'))

        start = np.rint(start/gcd)
        end = np.rint(end/gcd)
        denominator //= gcd

        delta_N = np.append(np.rint(end - start), N)
        gcd = np.gcd.reduce(np.array(delta_N, dtype='int32'))

        start = np.rint(start*N//gcd)
        end = np.rint(end*N//gcd)
        denominator *= N//gcd
        
        if i == 0:

            if len(kpoints_number_of_each_kpath) == 1:
                kpath = np.linspace(start, end, N+1)
            else:
                kpath = np.linspace(start, end, N, endpoint=False)
            
            denominators = np.full((kpath.shape[0], 1), denominator)
            kpath_denominators = np.append(kpath, denominators,1)

        elif i == len(kpoints_number_of_each_kpath) - 1:
            kpath = np.linspace(start, end, N+1)
            denominators = np.full((kpath.shape[0], 1), denominator)
            kpath_denominators_new = np.append(kpath, denominators,1)
            kpath_denominators = np.append(kpath_denominators, kpath_denominators_new, 0)

        else:
            kpath = np.linspace(start, end, N, endpoint=False)
            denominators = np.full((kpath.shape[0], 1), denominator)
            kpath_denominators_new = np.append(kpath, denominators,1)
            kpath_denominators = np.append(kpath_denominators, kpath_denominators_new, 0)

    return np.array(kpath_denominators, dtype='int32'), kpoints_number_of_each_kpath

def write_file(fraction, lattice_type, kpath, number):

    filename = input('Enter the filename to save file\n')

    write_klist_band(filename, fraction)
    
    write_KPOINTS(filename, fraction)

    write_klabel(filename, lattice_type, kpath, number)

def write_klist_band(filename, fraction):

    with open(filename + '.klist_band', 'w') as fh:

        for i, k in enumerate(fraction):
            
            line = ' '*(15 - len(str(k[0]))) + str(k[0])
            line += ' '*(5 - len(str(k[1]))) + str(k[1])
            line += ' '*(5 - len(str(k[2]))) + str(k[2])
            line += ' '*(5 - len(str(k[3]))) + str(k[3])
            line += ' '*(5 - len('2.0')) + '2.0'

            if i == 0:
                line += ' '*(5 - len('-1.0')) + '-1.0'
                line += ' '*(4 - len('1.5')) + '-1.5'
            
            fh.write(line+'\n')

        fh.write('END')

    print(f'Successfully create the {filename}.klist_band file!')

def write_KPOINTS(filename, fraction):
    
    with open(f'KPOINTS_{filename}', 'w') as fh:
        
        line = f'{filename}'
        fh.write(line+'\n')
        line = '2'
        fh.write(line+'\n')
        line = 'Line-mode'
        fh.write(line+'\n')
        line = 'Cartesian'
        fh.write(line+'\n')
        
        for i, k in enumerate(fraction):
            
            kx   = k[0]/k[3]
            line = f'{kx:7f}' + ' '*(10 - len(f'{kx:7f}'))
            ky   = k[1]/k[3]
            line += f'{ky:7f}' + ' '*(10 - len(f'{ky:7f}'))
            kz   = k[2]/k[3]
            line += f'{kz:7f}'
            
            fh.write(line+'\n')
            
    print(f'Successfully create the KPOINTS_{filename} file!')

def write_klabel(filename, lattice_type, kpath, number):

    with open('klabel', 'w') as fh:

        fh.write(lattice_type+'\n')

        number = list(number)
        number.insert(0, 0)
        num = 0

        for k, n in zip(kpath, number):

            num += int(n)
            
            if len(k) == 1:
                line = k + ' '
            else:
                line = k[0] + ' '
                line += k[1] + ' '
                line += k[2] + ' '
            
            line += str(num) + ' '*(8 - len(str(num)))
            fh.write(line+'\n')

    print(f'Successfully create the klabel file!')

if __name__ == '__main__':
    main()