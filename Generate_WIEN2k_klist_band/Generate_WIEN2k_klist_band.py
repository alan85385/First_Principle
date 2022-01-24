import sys
import numpy as np

def main():
    library = init()
    kpoints_matrix, lattice_type, kpoints = get_parameter(library)
    kpath_denominators, number = transform_kpoints_matrix_into_kpath(kpoints_matrix)
    write_file(kpath_denominators, lattice_type, kpoints, number)

def init():

    '''
    Initialize the lattice types and the k points library through Lattice_Information.txt
    '''

    library = {} #collect the information of the lattice types and the k points
    file_name = 'Lattice_Information.txt' #Lattice_Information.txt records some lattice types and their k points

    try: #check if the Lattice_Information.txt exists
        library = read_lattice_infomation(library, file_name)
    except:
        library = {}
        sys.stderr.write('Not find the file %s\n' %file_name)

    return library

def read_lattice_infomation(library, file_name):

    '''
    A function which reads the lattice information and return library
    '''

    with open(file_name, 'r') as fh:
        lines = fh.readlines()

    try: #check if all k vectors are numeric
        library = tranform_data_into_library(library, file_name, lines)
        print('Successfully initialize with the file %s' %file_name)

    except:
        sys.stderr.write('There exists some non-numeric type data of k vectors in the file %s\n' %file_name)
    
    return library

def tranform_data_into_library(library, file_name, lines):

    '''
    A function which transforms data into the standard form of library and return library
    '''

    for line in lines:

        line = line.split()

        if len(line) == 1: #the length of the line = 1 means the line contains the information of the lattice type
            lattice_type = str(line[0])
            library[lattice_type] = {}
        elif len(line) == 4: #the length of the line = 4 means the line contains the information of the k point
            high_symmetry_kpoint = str(line[0])
            library[lattice_type][high_symmetry_kpoint] = np.array(line[1:4], dtype = 'float')
        else:
            print('There exists some wrong form of lattice types or k vectors in the file %s' %file_name)

    return library

def get_parameter(library):

    file_name = 'kpoints.txt'

    if len(library) == 0:

        kpoints_matrix, kpoints = matrix_mode(file_name)
        
    else:

        while True:

            lattice_type = input(f'Enter the lattice type in the lattice type library {tuple(library.keys())} \nor enter \'m\' to change to the matrix mode\n')
        
            if lattice_type == 'm':
                kpoints_matrix, kpoints = matrix_mode(file_name)

                break
            elif lattice_type in library.keys():
                kpoints_matrix, kpoints = ask_kpoints_string(library[lattice_type])
                break
            else:
                print(f'There is no \'{lattice_type}\' lattice type in the lattice type library {tuple(library.keys())}')

    return np.array(kpoints_matrix), lattice_type, kpoints

def matrix_mode(file_name):

    try:
        kpoints_matrix, kpoints = read_kpoints(file_name)
        print('Successfully read the file %s' %file_name)

    except:
        print('Not find the file %s' %file_name)
        kpoints_matrix, kpoints = ask_kpoints_vector()
    
    return kpoints_matrix, kpoints

def read_kpoints(file_name):

    kpoints_matrix = []
    kpoints = []

    with open(file_name, 'r') as fh:
        lines = fh.readlines()

    for line in lines:

        line = line.split()

        if len(line) == 3:

            try:
                kpoints_matrix.append(np.array(line, dtype = 'float'))
                kpoints.append(line)
            except:
                sys.stderr.write('There exists some non-numeric type data of k vectors in the file %s\n' %file_name)
            
        else:
            print('There exists some problems in the file %s' %file_name)
    
    return kpoints_matrix, kpoints

def ask_kpoints_vector():

    kpoints_matrix = []
    kpoints = []

    while True:

        kpoint = input('Enter a kpoint in vector form or enter \'d\' if you\'ve entered all kpoint\n')
        kpoint = kpoint.split()
                
        if kpoint[0] == 'd' and len(kpoint) == 1:
            break
        elif len(kpoint) == 3:
            try:
                kpoints_matrix.append(np.array(kpoint, dtype = 'float'))
                kpoints.append(kpoint) 
            except:
                sys.stderr.write('Wrong form!\n')
        else:
            print('Invalid arguments!')

    return kpoints_matrix, kpoints

def ask_kpoints_string(kpoints_library):

    while True:

        kpoints_matrix = []
        kpoints = input(f'Enter the kpath with the string form \n{tuple(kpoints_library.keys())}\n')
        all_correct = True

        for kpoint in kpoints:

            if kpoint in kpoints_library:
                kpoints_matrix.append(kpoints_library[kpoint])
            else:
                all_correct = False
                print(f'{kpoint} doesn\'t exist in {tuple(kpoints_library.keys())}')
        
        if all_correct == True:
            break

    return kpoints_matrix, kpoints

def transform_kpoints_matrix_into_kpath(kpoints_matrix):

    try:
        total_kpoints = int(input('Enter total kpoints\n'))
    except:
        sys.stderr.write('Invalid argumets!\n')

    kpath_denominators, number = calculate_kpath(kpoints_matrix, total_kpoints)

    return kpath_denominators, number

def calculate_kpath(kpoints_matrix, total_kpoints):

    n = len(kpoints_matrix)
    kpoints_delta = kpoints_matrix[1:n] - kpoints_matrix[0:n-1]
    length = np.linalg.norm(kpoints_delta, axis = 1)
    total_length = length.sum()
    kpoints_number_of_each_kpath = np.round(total_kpoints*length/total_length)

    for i, N in enumerate(kpoints_number_of_each_kpath):
        
        N = int(N)
        
        start = np.array(kpoints_matrix[i])
        end = np.array(kpoints_matrix[i+1])
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

def write_file(kpath_denominators, lattice_type, kpoints, number):

    filename = input('Enter the filename to save file\n')

    write_klist_band(filename, kpath_denominators)

    write_k_label(filename, lattice_type, kpoints, number)

def write_klist_band(filename, kpath_denominators):

    with open(filename + '.klist_band', 'w') as fh:

        for i, k in enumerate(kpath_denominators):
            
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

def write_k_label(filename, lattice_type, kpoints, number):

    with open(filename + '_k_label.txt', 'w') as fh:

        fh.write(lattice_type+'\n')

        number = list(number)
        number.insert(0, 0)
        num = 0

        for k, n in zip(kpoints, number):

            num += int(n)
            
            if len(k) == 1:
                line = k + ' '
            else:
                line = k[0] + ' '
                line += k[1] + ' '
                line += k[2] + ' '
            
            line += str(num) + ' '*(8 - len(str(num)))
            fh.write(line+'\n')

    print(f'Successfully create the {filename}_k_label.txt file!')

if __name__ == '__main__':
    main()