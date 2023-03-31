import numpy as np

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

    kpath_vec = []
    
    if lattice_type == 'S':

        if kpath == 'D':
            kpath = 'GXMGRXdMR'

        for k in kpath:

            if k == 'G':
                kpath_vec.append( [0,0,0] )
            elif k == 'R':
                kpath_vec.append( [0.5,0.5,0.5] )
            elif k == 'X':
                kpath_vec.append( [0,0.5,0] )
            elif k == 'M':
                kpath_vec.append( [0.5,0.5,0] )
            elif k == 'd':
                kpath_vec.append( k )
            else:
                print('There is no %s kpoint.\n' %k)

    elif lattice_type == 'B':

        if kpath == 'D':
            kpath = 'GHNGPHdPN'

        for k in kpath:

            if k == 'G':
                kpath_vec.append( [0,0,0] )
            elif k== 'H':
                kpath_vec.append( [0,0,1] )
            elif k== 'P':
                kpath_vec.append( [0.5,0.5,0.5] )
            elif k== 'N':
                kpath_vec.append( [0,0.5,0.5] )
            elif k == 'd':
                kpath_vec.append( k )
            else:
                print('There is no %s kpoint.\n' %k)

    elif lattice_type == 'F':

        if kpath == 'D':
            kpath = 'GXWKGLUWLKdUX'

        for k in kpath:

            if k == 'G':
                kpath_vec.append( [0,0,0] )
            elif k == 'X':
                kpath_vec.append( [0,1,0] )
            elif k == 'L':
                kpath_vec.append( [0.5,0.5,0.5] )
            elif k == 'W':
                kpath_vec.append( [0.5,1,0] )
            elif k == 'U':
                kpath_vec.append( [0.25,1,0.25] )
            elif k == 'K':
                kpath_vec.append( [0.75,0.75,0] )
            elif k == 'd':
                kpath_vec.append( k )
            else:
                print('There is no %s kpoint.\n' %k)

    else:

        print('There is no %s lattice type. Please use matrix form.\n' %lattice_type)

    return kpath_vec, kpath
