BEGIN{AU2ANG=0.5291772108;i=0}
/atomic coordinates/,/center of nuclear mass/{
  if (NF==6) {
     i++
     coords[i,0] = $1*AU2ANG
     coords[i,1] = $2*AU2ANG
     coords[i,2] = $3*AU2ANG
     lbl[i]      = $4
  }
  nat=i
}
/ISOTROPIC/{
  idx=$3
  val[idx] = $5
}
END{
  print nat
  print
  for (i=1; i<=nat; i++) {
    printf("%3s   %10.6f   %10.6f   %10.6f   %10.6f\n",lbl[i], coords[i,0], coords[i,1], coords[i,2], val[i])
  } 
}
