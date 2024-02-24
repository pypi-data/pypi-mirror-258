# pointextract

Topological transforms by point sampling. Includes:

- Unwrapping circular and annular regions of images into linear or 2D arrays

Designed to unwrap 2D cross section images of 3D X-ray computed tomography scans.
The transformation enables the surface of a circular object to be aligned for downsteam analysis and a topological transform.

<img src="./figs/unwrap_example.png" width="400">

## Installation

You can install the package with:
```bash
pip install pointextract
```

Before using this package, ensure you have Python installed on your system. This package requires the following dependencies:
- numpy
- skimage

## Example

Simple example:
```python
import pointextract
from skimage.io import imread

img_arr = imread('example.png')

ellipse = ellipse_detect(img_arr, sigma=2)

img_unwrap = unwrap_image(img_arr, ellipse, radial_distance=50, num_points=400)
```

## Questions
This package is still in early development. Please feel free to contact us directly with any questions or bugs. We are currently working to provide an open-source repository where issues and feature requests can be submitted.

## Acknowledgements
This material is based upon research in the Materials Data Science for Stockpile Stewardship Center of Excellence (MDS3-COE).

[Case Western Reserve University, SDLElab] [1]
 
[1]: http://sdle.case.edu