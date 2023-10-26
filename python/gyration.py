import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def moving_average(x,w):
	return np.convolve(x, np.ones(w), 'valid')/ w

parser = argparse.ArgumentParser(description='Radius of gyration plotting from gromacs xvg')
parser.add_argument('-f', help='Filename (.xvg)', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-l', help='Filename labels for the plot.', nargs='+')
args = parser.parse_args()

colors = "bgrcmykw"
flabels = args.l

ax = plt.subplot(1,1,1)
p = []

for _i, f in enumerate(args.f):
	lines = f.readlines()[28:-1]

	time = [0]*len(lines)
	Rg = [0]*len(lines)
	Rgx = [0]*len(lines)
	Rgy = [0]*len(lines)
	Rgz = [0]*len(lines)

	for i, _l in enumerate(lines):
		_sl = _l.split()
		time[i] = float(_sl[0])/1000.
		Rg[i] = float(_sl[1])
		Rgx[i] = float(_sl[2])
		Rgy[i] = float(_sl[3])
		Rgz[i] = float(_sl[4])

	_Rg = moving_average(Rg,50)
	_time = moving_average(time,50)

	ax.plot(time, Rg, colors[_i], alpha=0.2)
	p.append( ax.plot(_time,_Rg, colors[_i], label=flabels[_i]) )

handles, labels = ax.get_legend_handles_labels()

plt.xlabel('Time (ns)')
plt.ylabel('$R_g$ (nm)')
# plt.ylim([1.5, 1.7])
# ax.set_aspect('equal', adjustable='box')
ax.legend(handles, labels)
plt.show()
