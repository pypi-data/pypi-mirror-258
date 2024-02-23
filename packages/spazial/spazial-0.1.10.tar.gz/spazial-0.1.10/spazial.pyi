"""
A module for calculating stochastic functions of data sets.
"""
import numpy as np
import numpy.typing as npt
from typing import Any

def initialize() -> None:
    """Displays the version string."""
    pass

def khat_test(points, width, height, max_d, use_weights) -> npt.NDArray:
	"""
	Calculate the K-Function for the points in the area for a range of distances.
	The resulting distances are logarithmically spaced from 0 to max_d.

	Arguments:
		points: The points to calculate the K-Function for. [n,2] ndarray.
		area: The area to calculate the K-Function for.
		max_d: The maximum distance to calculate the K-Function for.
        use_weights: Whether to use weights in the calculation.

	Returns:
		ndarray: Array with (n,2) dimensions. (,0) is the x values, (,1) is the y values.
	"""

def lhatc_test(points, width, height, max_d, use_weights) -> npt.NDArray:
	"""
	Calculate the CENTERED L-Function for the points in the area for a range of distances.
	The resulting distances are logarithmically spaced from 0 to max_d.

	Arguments:
		points: The points to calculate the L-Function for. [n,2] ndarray.
		area: The area to calculate the L-Function for.
		max_d: The maximum distance to calculate the L-Function for.
        use_weights: Whether to use weights in the calculation.

	Returns:
		ndarray: Array with (n,2) dimensions. (,0) is the x values, (,1) is the y values.
	"""
def lhat_test(points, width, height, max_d, use_weights) -> npt.NDArray:
	"""
	Calculate the L-Function for the points in the area for a range of distances.
	The resulting distances are logarithmically spaced from 0 to max_d.

	Arguments:
		points: The points to calculate the L-Function for. [n,2] ndarray.
		area: The area to calculate the L-Function for.
		max_d: The maximum distance to calculate the L-Function for.
        use_weights: Whether to use weights in the calculation.

	Returns:
		ndarray: Array with (n,2) dimensions. (,0) is the x values, (,1) is the y values.
	"""

def csstraussproc(rect_area: tuple[float, float], delta: float, n: int, c: float, max_iter: int) -> list[tuple[float, float]]:
    """
    Simulates a Strauss process.

    Args:
        rect_area (Tuple[float, float]): The area in which to generate points.
        delta (float): The minimum distance between points.
        n (int): The number of points to generate.
        c (float): The probability of accepting a new point.
        max_iter (int): The maximum number of iterations to perform.

    Returns:
        List[Tuple[float, float]]: A list of generated points, each represented as a tuple of two floats.
    """
    pass


def csstraussproc2(width: float, height: float, delta: float, n: int, c: float, i_max: int) -> list[tuple[float, float]]:
    """
    Simulates a Strauss process.

    Args:
        width (float): The width of the area in which to generate points.
        height (float): The height of the area in which to generate points.
        delta (float): The minimum distance between points.
        n (int): The number of points to generate.
        c (float): The probability of accepting a new point even if it is closer to another point than delta.
        max_iter (int): The maximum number of iterations to perform.

    Returns:
        List[Tuple[float, float]]: A list of generated points, each represented as a tuple of two floats.
    """
    pass



def csstraussproc_rhciter(
    width: float,
    height: float,
    r_delta: np.ndarray,
    impact_point: np.ndarray,
    n: int,
    c: float,
    i_max: int
) -> list[tuple[float, float]]:
    """
    Simulates a Strauss process with a variable hard core radius, that is linearly interpolated using
    the distance of a candidate point to the impact_point.

    Args:
        width (float): The width of the area in which to generate points in mm.
        height (float): The height of the area in which to generate points in mm.
        r_delta (float): Rhc array, with r_delta[0,:] = r and r_delta[1,:] = rhc.
        impact_point (tuple[float,float]): Impact point in mm.
        n (int): The number of points to generate.
        c (float): The probability of accepting a new point even if it is closer to another point than delta.
        max_iter (int): The maximum number of iterations to perform.

    Returns:
        List[Tuple[float, float]]: A list of generated points, each represented as a tuple of two floats.
    """
    pass

def bohmann_process(
    width: float,
    height: float,
    r_range: np.ndarray,
    r_lambda: np.ndarray,
    r_delta: np.ndarray,
    impact_pos: tuple[float,float],
    c: float,
    i_max: int,
    no_warn: bool) -> np.ndarray:
    """
    Simulates a Bohmann process with a variable hard core radius, that is linearly interpolated using
    the distance of a candidate point to the impact_point.

    Arguments:
        width (float): The width of the area in which to generate points in mm.
        height (float): The height of the area in which to generate points in mm.
        r_range (ndarray): The range of r values to simulate.
        r_lambda (ndarray): Intensity array, with r_lambda[0,:] = r and r_lambda[1,:] = lambda.
        r_delta (ndarray): Rhc array, with xy_delta[0,:] = r and xy_delta[1,:] = rhc.
        impact_pos (tuple[float,float]): Impact point in mm.
        c (float): The probability of accepting a new point even if it is closer to another point than delta.
        i_max (int): The maximum number of iterations to perform.

    Returns:
        ndarray: A list of generated points, each represented as a tuple of two floats.
    """
    pass


def poisson(width: float, height: float, n: int) -> np.ndarray:
    """
    Simulates a Poisson process.

    Arguments:
        width (float): The width of the area in which to generate points in mm.
        height (float): The height of the area in which to generate points in mm.
        n (int): The number of points to generate.

    Returns:
        ndarray: A list of generated points, each represented as a tuple of two floats.
    """
    pass