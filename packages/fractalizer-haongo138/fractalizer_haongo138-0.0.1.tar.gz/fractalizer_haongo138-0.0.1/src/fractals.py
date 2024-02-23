import numpy as np

def mandelbrot(c, max_iter):
  """
  Calculates the number of iterations required to determine if a complex number 'c' belongs to the Mandelbrot set.

  Args:
      c: A complex number represented as a tuple (real, imaginary).
      max_iter: The maximum number of iterations allowed to classify 'c' within the Mandelbrot set.

  Returns:
      The number of iterations needed to classify 'c' within the Mandelbrot set, 
      or 'max_iter' if the limit is not reached.
  """
  z = c
  for n in range(max_iter):
    if abs(z) > 2.0:
      return n
    z = z * z + c
  return max_iter