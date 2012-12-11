import numpy as np

class FDMesh():
    def __init__(self,dx=1.0,dy=1.0,dz=1.0,nx=10,ny=1,nz=1,unit_length=1.0):
        self.dx=dx
        self.dy=dy
        self.dz=dz
        self.nx=nx
        self.ny=ny
        self.nz=nz
        self.nyz=ny*nz
        self.nxyz=nx*ny*nz
        self.unit_length=unit_length
        self.compute_pos()
        
    def set_material(self,mat):
        self.unit_length=mat.unit_length
        self.dx=mat.a/self.unit_length
        self.dy=mat.b/self.unit_length
        self.dz=mat.c/self.unit_length
        self.compute_pos()
        
    def compute_pos(self):
        self.pos=np.zeros((self.nxyz,3))
        for i in range(self.nx):
            for j in range(self.ny):
                for k in range(self.nz):
                    tp=((i-self.nx/2)*self.dx,
                         (j-self.ny/2)*self.dy,
                         (k-self.nz/2)*self.dz)
                    index=i*self.nyz+j*self.nz+k
                    self.pos[index]=tp

