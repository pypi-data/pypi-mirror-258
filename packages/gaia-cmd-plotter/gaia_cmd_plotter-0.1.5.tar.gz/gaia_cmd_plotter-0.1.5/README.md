# gaia-cmd-plotter

`gaia_cmd_plotter` is a Python package for creating customized Matplotlib axes that display a Gaia Color-Magnitude
Diagram (CMD) background. This package is useful for visualising astronomical data within the context of a Gaia CMD.

## Installation

You can install gaia_cmd_plotter using `pip`:

```bash
pip install gaia-cmd-plotter
```

## Usage

To use the package, first import the `GaiaCMDAxis` class from the `gaia_cmd_plotter.gaia_cmd_plotter` module.
```python
from gaia_cmd_plotter.gaia_cmd_axis import GaiaCMDAxis
```

Next, create a new `GaiaCMDAxis` object and add it to a Matplotlib figure.
```python
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8, 8))
ax = GaiaCMDAxis(fig)
```

You can then use the `GaiaCMDAxis` object like any other Matplotlib axis. For example, you can plot data on top of 
the Gaia CMD background, 
```python
bp_rp = 3.5
g_abs = 5.0
ax.plot(bp_rp, g_abs, "ko", ms=10, mec="k")
```

## Acknowledgements
This package has made use of data from the European Space Agency (ESA) [Gaia mission](https://www.cosmos.esa.int/gaia), 
processed by the [Gaia Data Processing and Analysis Consortium](https://www.cosmos.esa.int/web/gaia/dpac/consortium). 
The CMD background data was obtained from the Gaia data release 3 (DR3; Gaia Collaboration et al. 2016, 2023). The bulk 
of points in the CMD background are retrieved from the Gaia DR3 catalog, using the query in Gaia Collaboration 2018.


## References
1. [Gaia Collaboration, 2016, A&A, 595, A1](https://ui.adsabs.harvard.edu/abs/2016A%26A...595A...1G/abstract)
2. [Gaia Collaboration, 2018, A&A, 616, A10](https://ui.adsabs.harvard.edu/abs/2018A%26A...616A...1G/abstract)
3. [Gaia Collaboration, 2023, A&A, 674, A38](https://ui.adsabs.harvard.edu/abs/2023A%26A...674A...1G/abstract)
