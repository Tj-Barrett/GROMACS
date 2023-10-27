import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''
source ../../scripts/gmx_venv_activate.sh
python ../../scripts/python/bonds.py -f bonds_mapped/distr_bond_*.xvg
'''

def moving_average(x,w):
	return np.convolve(x, np.ones(w), 'valid')/ w

parser = argparse.ArgumentParser(description='Plot angle distributions from gromacs xvg')
parser.add_argument('-f', help='Filename (.xvg)', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-l', help='Filename labels for the plot.', nargs='+')
args = parser.parse_args()

colors = "bgrcmykwbgrcmykw"
flabels = args.l

ax = plt.subplot(1,1,1)
p = []

for _i, f in enumerate(args.f):
	lines = f.readlines()[:-1]

	bond = [0]*len(lines)
	quant = [0]*len(lines)

	for i, _l in enumerate(lines):
		_sl = _l.split()
		bond[i] = float(_sl[0])
		quant[i] = float(_sl[1])

	if flabels is not None:
		ax.plot(bond,quant, colors[_i], label=flabels[_i])
	else:
		ax.plot(bond,quant, colors[_i])

handles, labels = ax.get_legend_handles_labels()

plt.xlabel('Distance [nm]')
plt.ylabel('Count')
# plt.ylim([1.5, 1.7])
# ax.set_aspect('equal', adjustable='box')
if flabels is not None:
	ax.legend(handles, labels)
plt.show()
