#!/usr/bin/python

from ase import Atoms, Atom, units
import ase.io
from ase.io import Trajectory

import datetime
import time
import os

#=============================================================================
#   trajectory.py
#   Description: 
#=============================================================================
start = time.time()
#=============================================================================
# Welcome message
#=============================================================================
print('This program will generate trajectory files for AtNN aplication')

now = datetime.datetime.now()

print('Today is: ', str(now))
print('The program is running')
#=============================================================================
# initializing some variables
#=============================================================================
traj_name = 'dataset_time.traj'

print('A file named ',traj_name,' will contain the trajectory information')

cfg_r0 = 50 #cantidad de configuraciones a elegir 

cfg_t0 = 8   # el paso de cada configuracion a elegir en la primera etapa  
cfg_t1 = 4   # el paso de cada configuracion a elegir en la segunda etapa 
#=============================================================================
# Open object type trajectory that will contain objects type atom 
#=============================================================================
traj = Trajectory(traj_name, mode='a')
#=============================================================================
# Building list of files names present in directory
#=============================================================================
fnames = os.listdir('.')
#=============================================================================
# Open loop to read file by file in directory
#=============================================================================
ifiles   = 0 # init counter before read the files
iatomtot = 0 # init counter before read the cfg
iatomz1  = 0 # init counter before read the z1 cfg
iatomz2  = 0 # init counter before read the z2 cfg

for fname in fnames:

        if fname.endswith('.xml'):

                ifiles = ifiles + 1
#=============================================================================
# open object atom that will contain information to use in trajectory object
#=============================================================================        
                atoms=ase.io.read(fname,index=':')    
#=============================================================================
# reading the files that contains all the information for trajectories
#=============================================================================
                iatomcfg = 0 # init counter before read each files

                for a in atoms:
#=============================================================================
# increase counter
#============================================================================= 
                        iatomtot = iatomtot + 1
#=============================================================================
# condition zone 1
#============================================================================= 
                        if(iatomcfg <= cfg_r0) and (iatomcfg%cfg_t0 == 0):
#=============================================================================
# writing information in object trajectory each cfg_t0
#=============================================================================
                                traj.write(a)
                                iatomz1 = iatomz1 + 1
#=============================================================================
# condition zone 2
#============================================================================= 
                        elif (iatomcfg%cfg_t1 == 0):
#=============================================================================
# writing information in object trajectory each cfg_t1
#=============================================================================
                                traj.write(a) 
                                iatomz2 = iatomz2 + 1
#=============================================================================
# increase counter
#=============================================================================                
                        iatomcfg = iatomcfg + 1
#=============================================================================
# total configuration in image
#=============================================================================
imagtot = iatomz1 + iatomz2                         
#=============================================================================
# messages
#=============================================================================                 
print(ifiles,   'files has been readed in directory')
print(iatomtot, 'configurations has been readed in files')
print(iatomz1,  'configurations has been readed in zone 1')
print(iatomz2,  'configurations has been readed in zone 2')
print('The training image contains', imagtot, 'configurations')
#=============================================================================
# close traj file
#=============================================================================
traj.close   
#=============================================================================
# end code
#=============================================================================  
end = time.time()
tottime = end - start
     
print('The time of execution was: ', end - start,' seconds')

now = datetime.datetime.now()
print('The execution has been finished at: ', str(now))
