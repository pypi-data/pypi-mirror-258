import matplotlib.pyplot as plt
import numpy as np

from src.fractals import mandelbrot

width, height = 1200, 1200
x_min, x_max = -2.5, 1.5
y_min, y_max = -2.0, 2.0
max_iter = 256

data = np.zeros((height, width))
for x in range(width):
  for y in range(height):
    real = x_min + (x / (width - 1)) * (x_max - x_min)
    imag = y_min + (y / (height - 1)) * (y_max - y_min)
    c = complex(real, imag)
    data[y, x] = mandelbrot(c, max_iter)

plt.imshow(data, extent=(x_min, x_max, y_min, y_max), cmap='hot')
plt.colorbar()
plt.title("Mandelbrot Set")
plt.show()