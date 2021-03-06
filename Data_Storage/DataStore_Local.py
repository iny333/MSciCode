import numpy as np
from astropy.io import fits
import matplotlib
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os
from ProjectF import MLADataTest,classification, Object,storing
import random

## Loading in data
PlateDir = os.path.normpath("D:\Data\Plate_Name1.txt")
with open(PlateDir) as f:
    Spectra_Files = f.read().splitlines()
print('Yes')  
PLATEIDs = []
BinInfos = []
Flux = []
MJDs = []
log_wavst=[]
ORMASK=[]
ANDMASK=[]
INVAR=[]

TrainingDir = os.path.normpath("D:\Data")
slash =  os.path.normpath("\\")
TrainingFolder =  os.path.normpath("\Training")
slash =  os.path.normpath("\\")
for spectrum in Spectra_Files:
    plate_ = fits.open( TrainingDir +TrainingFolder+slash+ spectrum ,memmap=True)
    Bin_info_ = plate_[5].data
    Flux_ = plate_[0].data
    primhdu_ = plate_[0]
    PLATEIDs.append(primhdu_.header['PLATEID'])
    ORMASK.append( plate_[3].data)
    ANDMASK.append( plate_[2].data)
    INVAR.append( plate_[1].data)
    log_wavst.append(primhdu_.header['COEFF0'])
    MJDs.append(primhdu_.header['MJD'])
    BinInfos.append(Bin_info_)
    Flux.append(Flux_)
    
list = fits.open(TrainingDir+slash+'Superset_DR12Q.fits',memmap=True)#opening file
print(len(log_wavst))
supers=list[1].data # storing  BINTABLE extension data
Full_Data = storing(PLATEIDs,supers)
X,Y,Train_z, Train_mag,wavst = MLAData(Full_Data,BinInfos,Flux, log_wavst,ANDMASK,INVAR)

i=0
d = open(TrainingDir+slash+"Full.txt", 'w')
while i <len(PLATEIDs):
    C_Plate = PLATEIDs[i]
    a1 = X[i] 
    print(len(a1))
    a2 = np.array(Y[i])
    print(len(a2))
    if len(a1)==0 & len(a2)==0:
        i=i+1
    else:
        
        a3=ORMASK[i]
        a4=INVAR[i]
        a5 = Train_z[i]
        a7 = wavst[i]
        col1 = fits.Column(name='Bin_Flux', format='PD()', array=np.array(a1,dtype=np.object))
        col2 = fits.Column(name='Class', format='I', array=np.array(a2))
        col3 = fits.Column(name='ORMASK', format='PD()', array=np.array(a3,dtype=np.object))
        col4 = fits.Column(name='INVAR', format='PD()', array=np.array(a4,dtype=np.object))
        col5 = fits.Column(name='Redshift', format='D', array=np.array(a5))
        cols = fits.ColDefs([col1, col2,col3, col4,col5])
        tbhdu = fits.BinTableHDU.from_columns(cols)
        prihdr = fits.Header()
        prihdr['Plate'] = C_Plate
        prihdr['LogWav'] = a7
        prihdu = fits.PrimaryHDU(header=prihdr)
        file_name = TrainingDir+slash+np.str(C_Plate)+'.fits'
        thdulist = fits.HDUList([prihdu, tbhdu])
        thdulist.writeto(file_name)
        print(file_name)
        d.writelines(file_name+"\n")
        i=i+1
d.close

