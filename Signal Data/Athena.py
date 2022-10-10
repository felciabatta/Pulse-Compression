import numpy

class Athena:
    def ReadAScan(self, filename):
        fid=open(filename,mode="r")

        line=fid.readline().strip()
        if line!="#Milena A-Scan result file               Version 2.1":
            print("ReadAScan: unsupported file format")
            fid.close()
            return None, None

        nit, dt, t0,_=fid.readline().split()
        nit, dt, t0= int(nit), float(dt), float(t0)/1e9
        data=numpy.array([float(l) for l in fid.readlines()])
        t= numpy.arange(t0,t0+len(data)*dt,dt)
        fid.close()

        return t, data

    def ReadBScan(self, filename):
        fid=open(filename,mode="r")

        line=fid.readline().strip()
        if line!="#BSCAN format 2D":
            print("ReadBScan: unsupported file format")
            fid.close()
            return None, None, None

        nix, nit, _=fid.readline().split()
        nix, nit= int(nix), int(nit)
        dx, dt, _=fid.readline().split()
        dx, dt= float(dx), float(dt)
        data=numpy.array([float(l) for l in fid.readlines()]).reshape((nit,nix))
        t= numpy.arange(0,nit,1)*dt
        x= numpy.arange(0,nix,1)*dx

        fid.close()

        return t,x,data

