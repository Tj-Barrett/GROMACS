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
parser.add_argument('-n', help='Normalize.')
parser.add_argument('-xlim', help='X axis limits.', nargs=2)
parser.add_argument('-ylim', help='Y axis limits.', nargs=2)
args = parser.parse_args()

colors = "bgrcmykwbgrcmykw"
flabels = args.l

ax = plt.subplot(1,1,1)
p = []

for _i, f in enumerate(args.f):
	lines = f.readlines()[:-1]

	bond = [0]*len(lines)
	quant = [0]*len(lines)
	if args.n is not None:
		qsum = 0.

	for i, _l in enumerate(lines):
		_sl = _l.split()
		bond[i] = float(_sl[0])
		quant[i] = float(_sl[1])
		if args.n is not None:
			qsum+= float(_sl[1])

	if args.n is not None:
		_quant = quant
		del quant
		quant = [0]*len(lines)
		for i, _q in enumerate(_quant):
			quant[i] = _q/qsum

	if flabels is not None:
		ax.plot(bond,quant, colors[_i], label=flabels[_i])
	else:
		ax.plot(bond,quant, colors[_i])

handles, labels = ax.get_legend_handles_labels()

plt.xlabel('Distance [nm]')

if args.n is not None:
	plt.ylabel('Probability Density')
else:
	plt.ylabel('Count')


if args.xlim is not None:
	_xlim = [float(args.xlim[0]),float(args.xlim[1])]
	plt.xlim(_xlim)

if args.ylim is not None:
	_ylim = [float(args.ylim[0]),float(args.ylim[1])]
	plt.ylim(_ylim)
# ax.set_aspect('equal', adjustable='box')
if flabels is not None:
	ax.legend(handles, labels)
plt.show()
