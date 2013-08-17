import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

from pc import Anisotropy
from pc import FDMesh
from pc import Sim
from pc import Nickel
from pc import Zeeman
import numpy as np

def init_m(pos):
    x,y,z=pos
    if (x,y,z)==(1,2,3):
        return (1,2,3)
    elif z<1:
        return (0,0,-1)
    else:
        return (0,0,1)
    
def init_T(pos):
    return np.sum(pos)


def test_sim_init_m():
    mesh=FDMesh(nx=3,ny=4,nz=5)
    sim=Sim(mesh)
    sim.set_m((0,1,0))
    sim.spin.shape=(3,-1)
    spin_y=sim.spin[1]
    assert(spin_y.any()==1)


def test_sim_init_m_fun():
    mesh=FDMesh(nx=3,ny=4,nz=5)
    sim=Sim(mesh)
    sim.set_m(init_m,normalise=False)
    assert(sim.spin_at(1,2,3)==(1,2,3))


def test_sim_T_fun():
    mesh=FDMesh(nx=3,ny=4,nz=5)
    sim=Sim(mesh)
    sim.set_T(init_T)
    assert(sim.T[0]==0)
    assert(sim.T[-1]==9)
    
def test_sim_single_spin_vode(do_plot=False):
    ni=Nickel()
    mesh=FDMesh(nx=1,ny=1,nz=1)
    
    ni.alpha=0.1
    sim=Sim(mesh,T=0,mat=ni)
    sim.set_m((1, 0, 0))
    
    H0 = 1
    sim.add(Zeeman(H0,(0, 0, 1)))
    
    dt = 1e-12; 
    ts = np.linspace(0, 200 * dt, 101)
    
    
    precession = ni.gamma/(1+ni.alpha**2)
    
    mz_ref = []
    
    mz = []
    real_ts=[]
    for t in ts:
        sim.run_until(t)
        real_ts.append(sim.t)
        print sim.t
        mz_ref.append(np.tanh(precession * ni.alpha * H0 * sim.t))
        mz.append(sim.spin[-1])
    
    mz=np.array(mz)
    
    if do_plot:
        ts_ns = np.array(real_ts) * 1e9
        plt.plot(ts_ns, mz, "b.", label="computed") 
        plt.plot(ts_ns, mz_ref, "r-", label="analytical") 
        plt.xlabel("time (ns)")
        plt.ylabel("mz")
        plt.title("integrating a macrospin")
        plt.legend()
        plt.savefig("test_llb.png")
        
    print("Deviation = {}, total value={}".format(
            np.max(np.abs(mz - mz_ref)),
            mz_ref))
   
    assert np.max(np.abs(mz - mz_ref)) < 5e-7


def test_sim_single_spin(do_plot=False):
    ni=Nickel()
    mesh=FDMesh(nx=1,ny=1,nz=1)
    
    ni.alpha=0.1
    sim = Sim(mesh,T=1e-100,mat=ni)
    sim.set_m((1, 0, 0))
    
    H0 = 1
    sim.add(Zeeman(H0,(0, 0, 1)))
    
    dt = 1e-12; 
    ts = np.linspace(0, 100 * dt, 101)
    
    
    precession = ni.gamma/(1+ni.alpha**2)
    
    mz_ref = []
    
    mz = []
    real_ts=[]
    for t in ts:
        sim.run_until(t)
        real_ts.append(sim.t)
        print sim.t
        mz_ref.append(np.tanh(precession * ni.alpha * H0 * sim.t))
        mz.append(sim.spin[-1])
    
    mz=np.array(mz)
    
    if do_plot:
        ts_ns = np.array(real_ts) * 1e9
        plt.plot(ts_ns, mz, "b.", label="computed") 
        plt.plot(ts_ns, mz_ref, "r-", label="analytical") 
        plt.xlabel("time (ns)")
        plt.ylabel("mz")
        plt.title("integrating a macrospin")
        plt.legend()
        plt.savefig("test_llb.png")
        
    print("Deviation = {}, total value={}".format(
            np.max(np.abs(mz - mz_ref)),
            mz_ref))
   
    assert np.max(np.abs(mz - mz_ref)) < 5e-7

  

if __name__=='__main__':
    #test_sim_init_m()
    #test_sim_init_m_fun()
    #test_sim_T_fun()
    test_sim_single_spin(do_plot=True)