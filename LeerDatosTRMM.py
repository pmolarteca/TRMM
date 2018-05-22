
from netCDF4 import Dataset
import numpy as np
import datetime
import pandas as pd


Waves=Dataset('http://apdrc.soest.hawaii.edu/datadoc/trmm_pr_3a12.php','r')
#print Waves.variables
#print Waves.variables.keys()
print Waves.variables['swh']
#print Waves.variables['mwd']
#print Waves.variables['mwp']
print Waves.variables['time']
tempe=Dataset('sst.mnmean.nc','r')
#tempe2=Dataset('sst.wkmean.1990-present.nc', 'r')
print tempe.variables


altura= np.array(Waves.variables['swh'][:])
direccion= np.array(Waves.variables['mwd'][:])
periodo= np.array(Waves.variables['mwp'][:])
lat= np.array(Waves.variables['latitude'][:])
lon= np.array(Waves.variables['longitude'][:])
time= np.array(Waves.variables['time'][:]).astype(np.float)

altura[altura==-32767]=np.nan
direccion[direccion==-32767]=np.nan
periodo[periodo==-32767]=np.nan
sst[sst==32767]=np.nan


fecha = np.array([datetime.datetime(1900,01,01)+\
datetime.timedelta(hours = time[i]) for i in range(len(time))])

#se recorta lat y lon para el punto 1

lat1=np.where(lat==12.625)[0][0]
lon1=np.where(lon==278.375)[0][0]
#se recort la info (time, lat , lon)

alt1=altura[:,lat1,lon1]
dir1=direccion[:,lat1,lon1]
per1=periodo[:,lat1,lon1]


#ciclo anual punto 1 SAI
altura1= alt1[np.isfinite(alt1)]

CicloAnual_altura1= np.zeros([12]) * np.NaN

Meses = np.array([fecha[i].month for i in range(len(fecha))])
for k in range(1,13):
    tmpp = np.where(Meses == k)[0]
   
    altura1_tmp= altura1[tmpp]
    CicloAnual_altura1[k-1]= np.mean(altura1_tmp)

Fig= plt.figure()
plt.rcParams.update({'font.size':14})
plt.plot(CicloAnual_altura1,'-', color='skyblue',lw=3,label='Hs')
x_label = ['Año']
plt.title('Ciclo Anual Altura de Ola Significante', fontsize=24)
plt.xlabel('Mes',fontsize=18)
plt.ylabel('Hs(metros)',fontsize=18)
plt.legend(loc=0)

axes = plt.gca()
axes.set_xlim([0,11])
axes.set_ylim([0.9,2.0])
axes.set_xticks([0,1,2, 3, 4, 5, 6, 7,8, 9, 10 ,11]) #choose which x locations to have ticks
axes.set_xticklabels(['Ene','Feb','Mar','Abr','May','Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic' ]) 
plt.savefig('CicloAnualAltura1.png')

#ciclo anual con pandas

Waves=pd.Series(index=fecha, data=altura1)

WavesM=Waves.resample('M').mean()
WavesD=Waves.resample('D').mean()

WM=np.array(WavesM)
WM=WM[:-6]
WM=np.reshape(WM,(-1,12))
WMM=np.mean(WM,axis=0)
WMS=np.std(WM, axis=0)

plt.plot(WMM)
