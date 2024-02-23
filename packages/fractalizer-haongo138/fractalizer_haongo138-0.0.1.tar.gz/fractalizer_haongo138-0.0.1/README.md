# Fractal Generator

This is a Python package that allows you to generate and display various fractals, including the Mandelbrot set and Julia set.

## Features
- Generate different fractals by specifying the formula and parameters.
- Visualize the fractals using matplotlib with customizable colormaps.
- Save generated images as PNG files (optional).

## Installation
Install the package using pip:
```bash
pip install fractalizer
```


## Usage
```python
import fractalizer

fractal_type = "mandelbrot"  # Or "julia"
c = complex(-0.5, 0.0)  # For Julia set, specify the complex number 'c'
max_iter = 256

# Additional parameters (optional):
x_min, x_max = -2.5, 1.5
y_min, y_max = -2.0, 2.0
width, height = 1200, 1200
colormap = "hot"

data = fractalizer.generate(fractal_type, c, max_iter, x_min, x_max, y_min, y_max, width, height, colormap)

# Display the fractal
fractalizer.display(data)

# Save the fractal as an image (optional)
fractalizer.save_image(data, "fractal.png")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)