
from matplotlib.widgets import Slider
from postprocessing.processing import load_radar_data, extractSig
from scipy.ndimage import convolve1d

import matplotlib.pyplot as plt
import numpy as np
import argparse

def show_data(file_prefix):
	t, sr, x = load_radar_data(file_prefix)
	x_ref = extractSig("data/chirp.bin")
	x_ref = x_ref[int(x_ref.shape[0]*0.2) : int(x_ref.shape[0]*0.8)]
	x_ref = x_ref[::-1].conj()
	print("Data and Chirp loaded!")
	x_cmp = np.apply_along_axis(lambda m: np.convolve(m, x_ref), axis=0, arr=x)
	xavg_cmp = np.sum(np.abs(x_cmp), axis=1)
	print("Compression complete!")

	n_rx, n_samps = x.shape

	fig, axs = plt.subplots(nrows=4)
	plt.subplots_adjust(bottom=0.25)
	pltraw, = axs[0].plot(x[:, 0].real)
	pltref, = axs[1].plot(x_ref.real)
	pltcmp, = axs[2].plot(x_cmp[:, 0].real)
	pltavg, = axs[3].plot(xavg_cmp)

	def update_plots(val):
		pltraw.set_ydata(x[:,int(val)].real)
		pltcmp.set_ydata(x_cmp[:, int(val)].real)
		fig.canvas.draw_idle()
	
	slider_pos = plt.axes([0.25, 0.1, 0.65, 0.03])
	slider = Slider(ax=slider_pos, label="Sample#", valmin=0, valmax=n_samps-1, valstep=1)
	slider.on_changed(update_plots)

	plt.show()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("prefix", type=str, help="File prefix to be shown.")
	args = parser.parse_args()

	show_data(args.prefix)
