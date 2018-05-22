#!/usr/bin/python

import sys
import numpy as np
import getopt

atomlist=[]
alpha = 0.0
dref = 0.0

def readgeom(f):
   fgeom = open(f, "r") 
   geom=[]
   for line in fgeom.readlines():
     geom.append(line.strip())
   fgeom.close()
   return geom

def homa(coords):
   global atomlist, alpha, dref
   distances=[]
   for i in range(0,len(coords)-1):
      dist=np.linalg.norm(coords[i]-coords[i+1])
      distances.append(dist)
   return 1-alpha/len(atomlist)*sum([ (d-dref)**2 for d in distances ])

def gengrid(coords):
   xmax = max([ p[0] for p in coords])
   ymax = max([ p[1] for p in coords])
   zmax = max([ p[2] for p in coords])
   xmin = min([ p[0] for p in coords])
   ymin = min([ p[1] for p in coords])
   zmin = min([ p[2] for p in coords])

   xmax=1.1*xmax; xmin=1.1*xmin
   ymax=1.1*ymax; ymin=1.1*ymin
   zmax=1.1*zmax; zmin=1.1*zmin

   print xmin, xmax, ymin, ymax, zmin, zmax

   x=xmin; y=ymin; z=zmin
   print "MIN: {0} {1} {2}".format(xmin,ymin,zmin)
   grid=[]
   grid.append([x, y, z])
   delta=0.3
   nx=0
   while (x<=xmax) :
     ny=0
     while (y<=ymax) :
       nz=0
       while (z<=zmax) :
         grid.append([x, y, z])
         z=z+delta
         nz=nz+1
       z=zmin
       y=y+delta
       ny=ny+1
     y=ymin
     x=x+delta
     nx=nx+1
   print "nx={0} ny={1} nz={2}".format(nx,ny,nz)

   for pos in grid:
      print "{{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format(pos)
   return grid
     
def usage():
   print 'Usage: '+sys.argv[0]+' [-h -a alpha -d dref -l "i1 .. i6" -g <file>]'

def main():
#default values
# J . Chem. Inf: Comput. Sci. 1993, 33, 70--78
   global atomlist, alpha, dref
   geomfile="opt.xyz"
   dref = 1.388
   alpha=257.7
   print "alpha=",alpha
   try:
      opts, args = getopt.getopt(sys.argv[1:], "ha:d:l:g:", ["help", "alpha=","dref=","list=","geom="])
   except getopt.GetoptError as err:
         # print help information and exit:
         print str(err)  # will print something like "option -a not recognized"
         usage()
         sys.exit(2)
   output = None
   verbose = False
   for o, a in opts:
      if o in ("-h", "--help"):
         usage()
         sys.exit()
      elif o in ("-a", "--alpha"):
         alpha = float(a)
      elif o in ("-d", "--dref"):
         dref = float(a)
      elif o in ("-l", "--list"):
         atomlist = [int(i) for i in a.split()]
      elif o in ("-g", "--geom"):
         geomfile = a
      else:
         assert False, "unhandled option"
   #for arg in sys.argv[1:]:
   #   atomlist.append(int(arg))
   print "list",atomlist
   geom = readgeom(geomfile)
   #print geom[0]
   #print geom[1]
   #print geom[2]
   #
   coords=[]
   for at in atomlist:
      pos = np.asarray(geom[at+1].split()[1:4], dtype=np.float64)
      coords.append(pos)
      #print at, pos
   pos = np.asarray(geom[atomlist[0]+1].split()[1:4], dtype=np.float64)
   coords.append(pos)
   
   #print coords
   
   print "HOMA", homa(coords)
   #print coords
   x=[]
   y=[]
   z=[]
   for pos in coords[:len(coords)-1]:
     x.append(pos[0])
     y.append(pos[1])
     z.append(pos[2])
   covxy=np.cov(x,y,bias=True)[0][1]
   covxz=np.cov(x,z,bias=True)[0][1]
   covyz=np.cov(y,z,bias=True)[0][1]
   covxx=np.cov(x,x,bias=True)[0][1]
   covyy=np.cov(y,y,bias=True)[0][1]
   a=(covxy*covyz-covyy*covxz)/(covxy*covxy-covxx*covyy)
   b=(covxy*covxz-covxx*covyz)/(covxy*covxy-covxx*covyy)
   c=np.mean(z)-a*np.mean(x)-b*np.mean(y)
   #print "plane: ", a, b, c
   origin=[np.mean(x),np.mean(y),np.mean(z)]
   print "origin {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format(origin)
   print "pt1 {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format([1,0,a+c])
   print "pt2 {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format([0,1,b+c])
   v=[a,b,-1]
   #print "normal vector:", v
   v=v/np.linalg.norm(v)
   #print "normalized normal vector:",v
   pointP = origin+v
   pointM = origin-v
   print "point at +v {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format( pointP )
   print "point at -v {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format( pointM )
   gengrid(coords)

if __name__ == "__main__":
   main()
