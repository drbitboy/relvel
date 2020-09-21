"""
Model instrument offset from S/C Center Of Mass (COM) in linear flyby

Usage:  python relvel.py orx.bsp defs.pinpoint
"""
import os
import sys
import spiceypy as sp
try: import simplejson as sj
except: import json as sj

if "__main__" == __name__ and sys.argv[1:]:

  ### FURNSH kernels
  list(map(sp.furnsh,sys.argv[1:]))

  ### Initialize lists
  ets,dvs = list(),list()
  porxs,vorxs = list(),list()
  porxinstrs,vorxinstrs = list(),list()

  ### Loop over ETs 0+/-40s
  for iet in range(-400,401):

    ### ET (TDB)
    et = float(iet) / 10
    ets.append(et)

    ### Position of Bennu (2101955) wrt instrument
    storxinstr,ltorxinstr = sp.spkezr('2101955',et,'J2000','none','-64999')
    storx,ltorx = sp.spkezr('2101955',et,'J2000','none','-64')

    ### Position of Bennu (2101955) wrt S/C COM
    porxinstr,vorxinstr = storxinstr[:3],storxinstr[3:]
    porx,vorx = storx[:3],storx[3:]

    ### Delta dRange/dt
    dvs.append( sp.vdot(vorxinstr,sp.vhat(porx))
              - sp.vdot(vorx,sp.vhat(porx))
              )

    porxinstrs.append(list(porxinstr))
    vorxinstrs.append(list(vorxinstr))
    porxs.append(list(porx))
    vorxs.append(list(vorx))

  with open('relvel.json','w') as fjson:
    sj.dump(dict(porxinstrs=porxinstrs
                ,vorxinstrs=vorxinstrs
                ,porxs=porxs
                ,vorxs=vorxs
                ,dvs=dvs
                ,ets=ets
                )
           ,fjson
           ,indent=2
           )

  import matplotlib.pyplot as plt
  plt.axhline(0,color='k',linewidth=0.5)
  plt.axvline(0,color='k',linewidth=0.5)
  plt.plot(ets,dvs)
  plt.xlabel('Time, s past TCA')
  plt.ylabel('Differential dRange/dt, km/s')
  plt.title('dRange/dt difference\n[Target wrt Instr] - [Target wrt S/C]')
  plt.show()
  
  plt.axhline(8,color='k',linewidth=0.5)
  plt.axhline(10,color='k',linewidth=0.5)
  plt.axvline(0,color='k',linewidth=0.5)
  plt.plot(ets,[sp.vnorm(porx) for porx in porxs],'r',label='Bennu wrt S/C')
  plt.plot(ets,[sp.vnorm(porxinstr) for porxinstr in porxinstrs],'g',label='Bennu wrt Instr',linewidth=0.65)
  plt.xlabel('Time, s past TCA')
  plt.ylabel('Range, km')
  plt.title('Time vs. Range to target:  wrt Instr; wrt S/C')
  plt.legend(loc='best')
  plt.show()
  
  plt.axhline(8,color='k',linewidth=0.5)
  plt.axhline(10,color='k',linewidth=0.5)
  plt.axvline(6,color='k',linewidth=0.5)
  plt.axvline(0,color='k',linewidth=0.5)
  plt.plot([porx[0] for porx in porxs]
          ,[sp.vnorm(porx) for porx in porxs]
          ,'r',label='Bennu wrt S/C')
  plt.plot([porxinstr[0] for porxinstr in porxinstrs]
          ,[sp.vnorm(porxinstr) for porxinstr in porxinstrs]
          ,'g',label='Bennu wrt Instr',linewidth=0.65)
  plt.xlabel('Along-track Bennu Position, km downtrack')
  plt.ylabel('Range, km')
  plt.title('Range to target vs. along-track Bennu position:  wrt Instr; wrt S/C')
  plt.legend(loc='upper center')
  plt.show()
