import seissolxdmfwriter as sxw
import seissolxdmf as sx
import numpy as np
fn = '/home/ulrich/trash/fl33cpu-fault.xdmf'
# Read data from input file using seissolxdmf
sx = sx.seissolxdmf(fn)
geom = sx.ReadGeometry()
connect = sx.ReadConnect()
dt = sx.ReadTimeStep()
SRs = sx.ReadData('SRs')
SRd = sx.ReadData('SRd')
SR = np.sqrt(SRs**2 + SRd**2)

# Write the 0,4 and 8th times steps of array SRs and SR in SRtest-fault.xdmf/SRtest-fault.h5
#sxw.write_seissol_output('test-fault', geom, connect, ['SRs', 'SR'], [SRs, SR], dt, [0, 4, 5], True, False)


dictTime = {dt * i: i for i in [1, 2,3,2,8]}
#dictTime = {}
sxw.write('test-fault', geom, connect, {'SRs': SRs, 'SR':SR}, dictTime, True, 'hdf5', 4)
sxw.write('test-fault-raw', geom, connect, {'SRs': SRs, 'SR':SR}, dictTime, True, 'raw', 4)

