
def generate_step(timespan, sampling_t, delta_t, step_size, min, max, **kwargs) -> Series:
    """
    Generates a time-series step signal as a pandas Series.

    Parameters:
    ----------
    timespan : float
        Total duration of the signal in seconds.

    sampling_t : float
        Sampling interval in seconds (i.e., time between each sample).

    delta_t : float
        Duration of each step in seconds.

    step_size : float
        Magnitude of change between steps.

    min : float
        Minimum value of the signal.

    max : float
        Maximum value of the signal.

    kwargs : dict
        Additional optional parameters for customization (e.g., noise level, seed, etc.).

    Returns:
    -------
    Series
        A pandas Series representing the generated step signal over the specified timespan.
    """

    return # Series(...)


def generate_toggle(timespan, sampling_t, **kwargs) -> Series:
    """
    Generates a binary toggle signal (e.g., alternating between 0 and 1) as a pandas Series.

    Parameters:
    ----------
    timespan : float
        Total duration of the signal in seconds.

    sampling_t : float
        Sampling interval in seconds (i.e., time between each sample).

    kwargs : dict
        Additional optional parameters for customization (e.g., toggle frequency, initial state, randomness, etc.).

    Returns:
    -------
    Series
        A pandas Series representing the generated toggle signal over the specified timespan.
    """
    return  # Series(...)


def generate_sinusoid(timespan, sampling_t, freq=1.0, amp=1.0, offset=0.0, **kwargs) -> Series:
    """
    Generates a sinusoidal signal as a pandas Series.

    Parameters:
    ----------
    timespan : float
        Total duration of the signal in seconds.

    sampling_t : float
        Sampling interval in seconds (i.e., time between each sample).

    freq : float, optional (default=1.0)
        Frequency of the sinusoid in Hz.

    amp : float, optional (default=1.0)
        Amplitude of the sinusoid (peak value).

    offset : float, optional (default=0.0)
        Vertical offset added to the sinusoidal signal.

    kwargs : dict
        Additional optional parameters for customization, such as:
        - phase (float): Phase shift in radians.
        - noise_level (float): Standard deviation of optional Gaussian noise.

    Returns:
    -------
    Series
        A pandas Series representing the generated sinusoidal signal over the specified timespan.
    """
    return  # Series(...)