#!/usr/bin/python

import sys
import numpy as np
import getopt

atomlist=[]
inc = 0.0
nval = 0

def readgeom(f):
   fgeom = open(f, "r") 
   geom=[]
   for line in fgeom.readlines():
     geom.append(line.strip())
   fgeom.close()
   return geom

def usage():
   print 'Usage: '+sys.argv[0]+' [-h -v -i inc -n nval -l "atom list to define av. plane" -g <file>]'

def main():
   global atomlist
   geomfile="opt.xyz"
   inc=0.5 #angstrom
   nval=4
   verbose=0
   try:
      opts, args = getopt.getopt(sys.argv[1:], "hvi:n:l:g:", ["help", "verbose", "inc=","nval=","list=","geom="])
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
      elif o in ("-v", "--verb"):
         verbose=1
      elif o in ("-i", "--inc"):
         inc = float(a)
      elif o in ("-n", "--nval"):
         nval = float(a)
      elif o in ("-l", "--list"):
         atomlist = [int(i) for i in a.split()]
      elif o in ("-g", "--geom"):
         geomfile = a
      else:
         assert False, "unhandled option"
   if (verbose==1):
      print "list",atomlist
   geom = readgeom(geomfile)
   #
   coords=[]
   for at in atomlist:
      pos = np.asarray(geom[at+1].split()[1:4], dtype=np.float64)
      coords.append(pos)
      #print at, pos
   pos = np.asarray(geom[atomlist[0]+1].split()[1:4], dtype=np.float64)
   coords.append(pos)
   
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
   if (verbose==1):
      print "plane: ", a, b, c
   origin=[np.mean(x),np.mean(y),np.mean(z)]
   if (verbose==1):
      print "Average plane origin {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format(origin)
      print "Average plane pt1 {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format([1,0,a+c])
      print "Average plane pt2 {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format([0,1,b+c])
   v=[a,b,-1]
   v=v/np.linalg.norm(v)
   if (verbose==1):
      print   "point at  0    {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format( origin      )
   else:
      print   "{0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f}".format( origin      )
   for i in range(1, nval+1):
     pointP = origin+i*inc*v
     pointM = origin-i*inc*v
     if (verbose==1):
       print "point at +{1}v {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format( pointP, i*inc )
       print "point at -{1}v {{ {0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f} }}".format( pointM, i*inc )
     else:
       print "{0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f}".format( pointP, i*inc )
       print "{0[0]:16.10f} {0[1]:16.10f} {0[2]:16.10f}".format( pointM, i*inc )

if __name__ == "__main__":
   main()
