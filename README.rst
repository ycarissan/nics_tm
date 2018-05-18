1. Generation des points où calculer les NICS

Pour chaque groupe d'atomes on lance

# python nics_prep.py -l "at1 at2 at3 at4 ..." -g fichier.xyz -i 0.5 -n 4

Les valeurs par défaut sont -g opt.xyz -i 0.5 -n 4
donc si le fichier xyz se nomme opt.xyz, la commande devient :

# python nics_prep.py -l "at1 at2 at3 at4 ..."

Voir script.sh pour un exemple.

On récupère tous ces points dans un fichier que l'on ajoute à la fin du fichier xyz :

En utilisant script.sh :

# script.sh > points_nics.xyz
# cat points_nics.xyz >> opt.xyz

Puis on prepare turbomole :

# x2t opt.xyz > coord
# define

2. Pour calculer les NICS:

ajouter dans le fichier control les lignes suivantes AVANT $end :

------------------------------------------------------------------
$ricc2
  maxred 200
  maxiter 200
------------------------------------------------------------------

Puis on lance le calcul :

# ridft > ridft.log
# mpshift > mpshift.log

3. Pour récupérer les NICS:

# awk -f get_nics.awk mpshift.log
