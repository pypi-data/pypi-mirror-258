# Default values for general parameters
signal_duration = 0.2
sampling_freq = 3200
signals_quant = 100

# Default values for normal signal
amplitude_min = 0.95
amplitude_max = 1.05
amplitude = (amplitude_min, amplitude_max)
fundamental_freq = 50
phase_angle_min = 0
phase_angle_max = 0
phase_angle = (phase_angle_min, phase_angle_max)

# Default values for sag
sag_magnitude_min = 0.1
sag_magnitude_max = 0.9
sag_magnitude = (sag_magnitude_min, sag_magnitude_max)
sag_start = 0.02
sag_stop = 0.18