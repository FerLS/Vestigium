def _smoothstep(t: float) -> float:
    """
    Smoothstep function for easing.

    :param t: The interpolation factor (0.0 to 1.0).
    :return: The eased interpolation factor.
    """
    return t * t * (3 - 2 * t)


def smooth_lerp(start: float , end: float, t: float) -> float:
    """
    Smoothly interpolates between start and end by t using smoothstep.

    :param start: The starting value.
    :param end: The ending value.
    :param t: The interpolation factor (0.0 to 1.0).
    :return: The interpolated value.
    """
    t = _smoothstep(t)
    return start + t * (end - start)
