
from matplotlib.widgets import Slider
from postprocessing.processing import load_radar_data, extractSig
from scipy.ndimage import convolve1d

import matplotlib.pyplot as plt
import numpy as np

def show_data(file_prefix):
	t, sr, x = load_radar_data(file_prefix)
	x_ref = extractSig("data/chirp.bin")
	print("Data and Chirp loaded!")
	x_cmp = np.apply_along_axis(lambda m: np.convolve(m, x_ref[::-1]), axis=0, arr=x)
	xavg_cmp = np.sum(x_cmp, axis=1)
	print("Compression complete!")

	n_rx, n_samps = x.shape

	fig, axs = plt.subplots(nrows=3)
	plt.subplots_adjust(bottom=0.25)
	pltraw, = axs[0].plot(x[:, 0])
	pltcmp, = axs[1].plot(x_cmp[:, 0])
	pltavg, = axs[2].plot(xavg_cmp)

	def update_plots(val):
		pltraw.set_ydata(x[:,int(val)])
		pltcmp.set_ydata(x_cmp[:, int(val)])
		fig.canvas.draw_idle()
	
	slider_pos = plt.axes([0.25, 0.1, 0.65, 0.03])
	slider = Slider(ax=slider_pos, label="Sample#", valmin=0, valmax=n_samps-1, valstep=1)
	slider.on_changed(update_plots)

	plt.show()
