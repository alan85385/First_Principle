import numpy as np
from Generate_KPATH import read_lattice_infomation, tranform_data_into_library

def uniform_sampling(kpath_vecs, nk):

    nk = int(nk)
    distance = []
    nk_new = []

    for i, kpath_vec in enumerate(kpath_vecs):
        if kpath_vec != 'd' and kpath_vecs[i-1] != 'd' and i != 0:
            distance.append( np.linalg.norm( np.array(kpath_vec) - np.array(kpath_vecs[i-1]) ) )
            
    D = sum(distance)
    
    for d in distance:
        nk_new.append( round( nk*d/D ) )
   
    return nk_new

def kpath_translate(lattice_type, kpath):

    file_name = 'Lattice_Information.txt'
    kpath_vec = []
    library   = {}
    
    try: #check if the Lattice_Information.txt exists
        library = read_lattice_infomation(library, file_name)
    except:
        library = {}
        sys.stderr.write('Not find the file %s\n' %file_name)
    
    if lattice_type in library.keys():
        
        for k in kpath:
            
            if k in library[lattice_type].keys():
                kpath_vec.append( library[lattice_type][k] )
            elif k == 'd':
                kpath_vec.append( k )
            else:
                print('There is no %s kpoint.\n' %k)
    else:
        print(f'There is no \'{lattice_type}\' lattice type in the lattice type library {tuple(library.keys())}')

    return kpath_vec, kpath
