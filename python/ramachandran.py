import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

parser = argparse.ArgumentParser(description='Ramachandran plotting from gromacs xvg')
parser.add_argument('-f', '-filename', help='Filename (.xvg)', type=argparse.FileType('r'))
args = parser.parse_args()

lines = args.f.readlines()[34:-1]

phi = [0]*len(lines)
psi = [0]*len(lines)
stype = [0]*len(lines)

for i, _l in enumerate(lines):
	_sl = _l.split()
	phi[i] = float(_sl[0])
	psi[i] = float(_sl[1])
	stype[i] = _sl[2]

# res = sns.kdeplot(x=np.array(phi), y=np.array(psi), color='blue',shade=True)
fig = plt.figure()
ax = fig.add_subplot()

plt.scatter(phi,psi, marker='.', color='k', alpha = 0.025)

plt.xlim([-180, 180])
plt.xlabel('$\phi$ [Degrees]')
plt.ylim([-180,180])
plt.ylabel('$\psi$ [Degrees]')

ax.set_aspect('equal', adjustable='box')
plt.show()