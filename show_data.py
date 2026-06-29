
from matplotlib.widgets import Slider
from postprocessing.processing import load_radar_data, extractSig
from scipy.ndimage import convolve1d

import matplotlib.pyplot as plt
import numpy as np
import argparse

def pulse_compress(file_prefix, plot=True, do_window=True):
	t, sr, x = load_radar_data(file_prefix)
	x_ref = extractSig("data/chirp.bin")
	x_ref = x_ref[:]
	x_ref = x_ref[::-1].conj()
	window = np.ones_like(x_ref)
	# # This is for trapezoidal windows, 20% on each side
	# if do_window:
	#	cutoff = int(0.2 * window.shape[0])
	#	window[ : cutoff] = np.linspace(0, 1, cutoff)
	#	window[window.shape[0]-cutoff : ] = np.linspace(1, 0, cutoff)
	# # This os for hanning window
	if do_window:
		window = 0.5 - 0.5 * np.cos(
		2 * np.pi * np.linspace(0, 1, window.shape[0]))
	x_ref *= window
	print("Data and Chirp loaded!")
	x_cmp = np.apply_along_axis(
		lambda m: np.convolve(m, x_ref, mode="same"),
		axis=0, arr=x)
	xavg_cmp = np.abs(np.sum(x_cmp, axis=1))
	print("Compression complete!")
	if not plot: return x_cmp, x_ref

	n_rx, n_samps = x.shape
	noisefloor = np.median(np.abs(xavg_cmp))
	noisefloor_dB = -100 if np.isclose(noisefloor, 0, atol=1e-10) else 10*np.log10(noisefloor)

	fig, axs = plt.subplots(nrows=4)
	plt.subplots_adjust(bottom=0.25)
	pltraw, = axs[0].plot(x[:, 0].real)
	pltref, = axs[1].plot(x_ref.real)
	pltcmp, = axs[2].plot(x_cmp[:, 0].real)
	pltavg, = axs[3].plot(np.clip(10*np.log10(xavg_cmp), noisefloor_dB, np.inf))

	def update_plots(val):
		pltraw.set_ydata(x[:,int(val)].real)
		pltcmp.set_ydata(x_cmp[:, int(val)].real)
		fig.canvas.draw_idle()
	
	slider_pos = plt.axes([0.25, 0.1, 0.65, 0.03])
	slider = Slider(ax=slider_pos, label="Sample#", valmin=0, valmax=n_samps-1, valstep=1)
	slider.on_changed(update_plots)

	plt.show()
	
	return x_cmp, x_ref

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("prefix", type=str, help="File prefix to be shown.")
	parser.add_argument("--window", action="store_true")

	args = parser.parse_args()

	xcmp, xref = pulse_compress(args.prefix, plot=True, do_window=args.window)
