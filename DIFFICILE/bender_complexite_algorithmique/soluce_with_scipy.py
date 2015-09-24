import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

import math

eps = 0.00000001 # max error allowed
def w0(x): # Lambert W function using Newton's method
    w = x
    while True:
        ew = math.exp(w)
        wNew = w - (w * ew - x) / (w * ew + ew)
        if abs(w - wNew) <= eps: break
        w = wNew
    return w

def compute_r2(x, y):
	A = np.vstack((x, np.ones(x.size))).T
	model, resid = np.linalg.lstsq(A, y)[:2]

	r2 = 1 - resid / (y.size * y.var())
	return r2

def func_log(x, a, b, c):
	return a * np.log(b * x) + c

def func_nlogn(x, a, b, c):
	return x * a * np.log(b * x) + c

def func_n3(x, a, b, c):
	return a * np.power(b * x, 3) + c

def func_n(x, a, b, c):
	return a * b * x + c

def func_n2(x, a, b, c):
	return a * np.power(b * x, 2) + c

def func_2powN(x, a, b, c):
	# 2**N
	return a * np.power(2, b * x) + c


def func_inv_log(y):
	return np.exp(y)	

def compute_inv_nlogn(y):
	return np.apply_along_axis(lambda x: 1.0/w0(x), 0, y)

def func_inv_n3(y):
	return np.power(y, 1.0/3.0)

def func_inv_n2(y):
	return np.power(y, 1.0/320)

def func_inv_2powN(y):
	return np.log(y)/math.log(2.0)

def generate_input():	
	x = np.linspace(1,10,50)
	y = func(x, 1.0, 1.0, 0.0)
	yn = y + 0.0*np.random.normal(size=len(x))

	return x, yn

def get_input():
	x = []
	y = []
	N = int(raw_input())
	for i in xrange(N):
	    num, t = [int(j) for j in raw_input().split()]
	    #
	    x.append(num)
	    y.append(t)

	x = np.asarray(x)
	y = yn = np.asarray(y)

	return x,y

def normalize_space(x):
	max_x, min_x = max(x), min(x)	

	delta_min_max_x = float(max_x - min_x)
	
	#norm_x = map(lambda x: (float(x) - min_x)/delta_min_max_x, x)
	#norm_y = map(lambda x: (float(x) - min_y)/delta_min_max_y, y)
	norm_x =  (x - min_x) / delta_min_max_x

	return norm_x

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')

#func = func_n
#func = func_log
#func = func_nlogn
#func = func_n2
func = func_n3
#func = func_2powN

#func = func_log
x, yn = generate_input()
#x, yn = get_input()

yn_filter = savitzky_golay(savitzky_golay(yn, 21, 1), 21, 1)

#x = normalize_space(x)
#yn = normalize_space(yn)

#yn = normalize_space(yn)

#x_log = np.log(x)
#yn  = np.interp(x_log, x, yn)

dydx = np.gradient(yn_filter, np.gradient(x))
#dydx = savitzky_golay(savitzky_golay(dydx, 21, 1), 21, 1)
#dydx = np.power(dydx, -1)
#dydx = savitzky_golay(savitzky_golay(dydx, 21, 1), 21, 1)

func_to_fit = func_log
popt, pcov = curve_fit(func_to_fit, x, yn)

fit_curve = func_to_fit(x, *popt)

print len(x), len(yn), len(fit_curve)

plt.figure()
plt.plot(x, yn, 'ko', label="Original Noised Data")
#plt.plot(x, yn_filter, 'r-', label="Filter Noised Data")
#
#plt.plot(x, fit_curve, 'r-', label="Fitted Curve")
#
plt.plot(x, dydx, 'bo', label="Gradient Noised Data")

#inv_func = func_inv_log
#plt.plot(x, inv_func(yn), 'g-', label="Inverse Original Noised Data")
#inv_func = func_inv_n2
#plt.plot(x, inv_func(yn), 'y+', label="Inverse Original Noised Data")
#inv_func = func_inv_n3
#plt.plot(x, inv_func(yn), 'yo', label="Inverse Original Noised Data")

#plt.plot(x, np.exp(func(x, *popt)), 'b+', label="Inverse Fit Curve")

plt.legend()
plt.show()

#print compute_r2(x, func_inv_log(yn))
#print compute_r2(x, func_inv_nlogn(yn))
#print compute_r2(x, func_inv_n2(yn))
#print compute_r2(x, func_inv_n3(yn))
#print compute_r2(x, func_inv_2powN(yn))

coefficients = np.polyfit(x, yn , 3)
polynomial = np.poly1d(coefficients)
ys = polynomial(x)
print polynomial

#plt.plot(x, yn, 'r,')	#show scatter plot of original data
#plt.plot(x, ys, 'b-')	#show fitted line
#plt.show()
