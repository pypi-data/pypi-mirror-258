import numpy as np
from pypqd import parameters

# Get default values for general parameters
ts = parameters.signal_duration
fs = parameters.sampling_freq
ns = parameters.signals_quant

# Get default values for normal signal
A = parameters.amplitude
f = parameters.fundamental_freq
phi = parameters.phase_angle

# Get default values for sag
alpha = parameters.sag_magnitude
t1 = parameters.sag_start
t2 = parameters.sag_stop

# Sag dataset
def sag(amplitude=A, fundamental_freq=f, phase_angle=phi,
        signal_duration=ts, sampling_freq=fs, signals_quant=ns,
        sag_magnitude = alpha, sag_start=t1, sag_stop=t2):
    """Generates one or more sag synthetic signals.
    

    Parameters
    ----------
    amplitude : tuple, optional
        Normal signal amplitude, in volts (V). The default is (0.95, 1.05)
    fundamental_freq : int, optional
        Nominal system frequency, in hertz (Hz). The default is 50
    phase_angle : tuple, optional
        Phase angle of the signal, in radians (rad). The default is (0, 0)
    signal_duration : float, optional
        Signal duration, in seconds (s). The default is 0.2
    sampling_freq : int, optional
        Signal sampling frequency, in hertz (Hz). The default is 3200
    signals_quant : int, optional
        Number of signals that are generated. The default is 100
    sag_magnitude : tuple, optional
        Disturbance magnitude in per unit (pu). The default is (0.1, 0.9)
    sag_start : float, optional
        Disturbance start time, in seconds (s). The default is 0.04
    sag_stop : float, optional
        Disturbance stop time, in seconds (s). The default is 0.16

    Returns
    -------
    discrete_time_vector : array
        Vector with the time values in which the signal is sampled.
    sag_dataset : array
        Matrix with synthetic signals, one for each row.

    Examples
    -------
    >>> from pypqd import synthetic
    >>> time, voltage = synthetic.sag(signals_quant=5)

    """
    # Calculate the number of nodes
    nodes_quant = int(np.ceil(signal_duration*sampling_freq))
    # Random values array for amplitude in defined range
    amplitude_vector = np.random.rand(signals_quant, 1)*(amplitude[1]-amplitude[0])+amplitude[0]
    amplitude_matrix = np.full((signals_quant, nodes_quant), amplitude_vector)
    # Discrete time matrix
    discrete_time_vector = np.linspace(0, signal_duration, nodes_quant)
    discrete_time_matrix = np.full((signals_quant, nodes_quant), discrete_time_vector)
    # Random values array for phase angle in defined range
    phase_angle_vector = np.random.rand(signals_quant, 1)*(phase_angle[1]-phase_angle[0])+phase_angle[0]
    phase_angle_matrix = np.full((signals_quant, nodes_quant), phase_angle_vector)
    # Sine function argument matrix
    sine_argument_matrix = 2*np.pi*fundamental_freq*discrete_time_matrix+phase_angle_matrix
    # Normal signal dataset
    normal_matrix = amplitude_matrix*np.sin(sine_argument_matrix)
    # Array of all ones
    ones_matrix = np.ones((signals_quant, nodes_quant))
    # Unit step function
    step_vector_ini = np.piecewise(discrete_time_vector,
                                    [discrete_time_vector<sag_start, discrete_time_vector>=sag_start], [0, 1])
    step_vector_fin = np.piecewise(discrete_time_vector,
                                    [discrete_time_vector<sag_stop, discrete_time_vector>=sag_stop], [0, 1])
    step_vector = step_vector_ini-step_vector_fin
    step_matrix = np.full((signals_quant, nodes_quant), step_vector)
    # Random values array for sag magnitude in defined range
    sag_magnitude_vector = np.random.rand(signals_quant, 1)*(sag_magnitude[1]-sag_magnitude[0])+sag_magnitude[0]
    sag_magnitude_matrix = np.full((signals_quant, nodes_quant), sag_magnitude_vector)
    # Disturbance factor matrix
    disturbance_matrix = ones_matrix-sag_magnitude_matrix*step_matrix
    # Sag dataset
    sag_dataset = normal_matrix*disturbance_matrix
    
    return discrete_time_vector, sag_dataset
    















