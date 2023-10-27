import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''
source ../../scripts/gmx_venv_activate.sh
python ../../scripts/python/angles.py -f angles_mapped/distr_ang_*.xvg
'''

def moving_average(x,w):
	return np.convolve(x, np.ones(w), 'valid')/ w

parser = argparse.ArgumentParser(description='Plot angle distributions from gromacs xvg')
parser.add_argument('-f', help='Filename (.xvg)', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-l', help='Filename labels for the plot.', nargs='+')
parser.add_argument('-s', help='Cumulative (c) / Individual (i) / Both (b)')
args = parser.parse_args()

colors = "bgrcmykwbgrcmykw"
flabels = args.l

if args.s == 'c':
	_sum = True
	_both = False
elif args.s == 'b':
	_sum = True
	_both = True
else:
	_sum = False
	_both = False

ax = plt.subplot(1,1,1)
p = []

_sum_angle = np.linspace(0, 181, 182)
_sum_quant = [0]*182

for _i, f in enumerate(args.f):
	lines = f.readlines()[:-1]

	angle = [0]*len(lines)
	quant = [0]*len(lines)

	for i, _l in enumerate(lines):
		_sl = _l.split()
		angle[i] = float(_sl[0])
		quant[i] = float(_sl[1])

	if _sum and not _both:
		for _j, q in enumerate(quant):
			adj = int(angle[_j])
			_sum_quant[adj]+= quant[_j]

	elif _sum and _both:
		for _j, q in enumerate(quant):
			adj = int(angle[_j])
			_sum_quant[adj]+= quant[_j]

		if flabels is not None:
			ax.plot(angle,quant, colors[_i], label=flabels[_i])
		else:
			ax.plot(angle,quant, colors[_i])

	else:
		if flabels is not None:
			ax.plot(angle,quant, colors[_i], label=flabels[_i])
		else:
			ax.plot(angle,quant, colors[_i])

if _sum:
	if flabels is not None:
		ax.plot(_sum_angle,_sum_quant, 'k', label=flabels[_i])
	else:
		ax.plot(_sum_angle,_sum_quant, 'k')

handles, labels = ax.get_legend_handles_labels()

plt.xlabel('Angle [Degree]')
plt.ylabel('Probability')
plt.xticks([-180, -120, -60, 0, 60, 120, 180])
plt.xlim([0, 180])
# ax.set_aspect('equal', adjustable='box')
if flabels is not None:
	ax.legend(handles, labels)
plt.show()
