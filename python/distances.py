import argparse
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''
source ../../scripts/gmx_venv_activate.sh
python ../../scripts/python/_times.py -f _times_mapped/distr__time_*.xvg
'''

def moving_average(x,w):
	return np.convolve(x, np.ones(w), 'valid')/ w

parser = argparse.ArgumentParser(description='Plot angle distributions from gromacs xvg')
parser.add_argument('-f', help='Filename (.xvg)', type=argparse.FileType('r'), nargs='+')
parser.add_argument('-l', help='Filename labels for the plot.', nargs='+')
parser.add_argument('-ma', help='Moving Average window.', nargs=1)
parser.add_argument('-cut', help='Cutoff distance [nm].', nargs=1)
parser.add_argument('-xlim', help='X axis limits.', nargs=2)
parser.add_argument('-ylim', help='Y axis limits.', nargs=2)
args = parser.parse_args()

colors = "bgrcmykwbgrcmykw"
flabels = args.l

ax = plt.subplot(1,1,1)
p = []

if args.cut is not None:
	_cut = float(args.cut[0])
else:
	_cut = 1.2

if args.ma is not None:
	ma = int(args.ma[0])

for _i, f in enumerate(args.f):
	lines = f.readlines()[24:-1]

	time = [0]*len(lines)
	dist = [0]*len(lines)

	for i, _l in enumerate(lines):
		_sl = _l.split()
		time[i] = float(_sl[0])/1000.
		dist[i] = float(_sl[1])

	_dist = moving_average(dist,ma)
	_time = moving_average(time,ma)

	below = [False]*len(_dist)
	for i, _d in enumerate(_dist):
		if _dist[i] < _cut:
			below[i] = True

	if flabels is not None:
		ax.plot(time,dist, colors[_i], alpha=0.2)
		p.append( ax.plot(_time,_dist, colors[_i], label=flabels[_i]) )
	else:
		ax.plot(time,dist, colors[_i], alpha=0.2)
		p.append( ax.plot(_time,_dist, colors[_i]) )

	a = []
	b = []
	for i, _b in enumerate(below):
		if i < len(below)-1:
			if _b == True and below[i+1] == False:
				b.append(i)
			elif not _b and below[i+1] == True:
				a.append(i)
			elif i == 0 and _b == True:
				a.append(i)
		elif i == len(below)-1 and _b == True:
			b.append(i)
	
	for _a, _b in zip(a,b): 
		plt.axvspan(_time[_a],_time[_b], color='red', alpha=0.2)

handles, labels = ax.get_legend_handles_labels()

plt.xlabel('Time [ns]')
plt.ylabel('Minimum Distance [nm]')	

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
