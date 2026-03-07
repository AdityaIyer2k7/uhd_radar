## Config Settings
This is where config settings can be set and where default configs are stored. The recommended default settings for the USRP B205mini-i is `default.yaml`. 
Important Settings:
* `freq` is the center frequency of the output. Default is 450e6 or 450 MHz.
* `num_pulses` is how many pulses are sent before ending the main loop. Default is 10,000. Can set to -1 to keep going indefinitely until manually stopped.
* `save_loc` is where the SDR data will be temporarily saved. Default is `data/rx_samps.bin` in the data folder.
* `max_chirps_per_file` is how much data will be put in each file before breaking into a new file. Can set to -1 to stop chirps from being split between files, default is -1.
