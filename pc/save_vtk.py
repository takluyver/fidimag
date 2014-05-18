import os
import pyvtk
import numpy as np


class SaveVTK():
    def __init__(self,mesh,m,name='unnamed',vtkname='m'):
        self.mesh=mesh
        self.m=m
        self.nx=mesh.nx
        self.ny=mesh.ny
        self.nz=mesh.nz
        self.dx=mesh.dx
        self.dy=mesh.dy
        self.dz=mesh.dz
        self.name = '%s_vtks'%name
        self.vtkname = vtkname
        xyz=np.array(mesh.pos)
        self.x=np.array(xyz[:,0],dtype='float32')
        self.y=np.array(xyz[:,1],dtype='float32')
        self.z=np.array(xyz[:,2],dtype='float32')
        
        if not os.path.exists(self.name):
            os.makedirs(self.name)
        
        #build a new index since we have used difference order 
        ids = [self.mesh.index(i,j,k) for k in range(self.nz) for j in range(self.ny) for i in range(self.nx)]
        self.ids = np.array(ids)
        
        self.pos = []
        for i in range(len(ids)):
            self.pos.append(self.mesh.pos[self.ids[i]])
                    
    def save_vtk(self,m, step):
        
        pos=pyvtk.StructuredGrid([self.nx,self.ny,self.nz],self.pos)
        
        m.shape=(3,-1)
        data=pyvtk.PointData(pyvtk.Vectors(np.transpose(m)[self.ids],'m'))
        m.shape=(-1,)
        
        vtk = pyvtk.VtkData(pos,data,'spins')
                      
        vtk.tofile("%s/%s.%06d"%(self.name,self.vtkname,step),'binary')
        