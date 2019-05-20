# vrt_blending
Python package for applying a blending function to a GDAL VRT.
Includes collateral for GBDX task deployment.


This package includes one CLI tool:
*vrtamix.py:*

This tool apply a blending PixelFunction to an existing tiled VRT, produced by the gdalbuildvrt CLI. The options for blending include 'min', 'mean', and 'max'. The tool outputs a new VRT, which can then be used via gdal_translate to produce a mosaic with blending at the overlaps between images, as follows:
`env GDAL_VRT_ENABLE_PYTHON=YES gdal_translate blended.vrt blended.tif`.

Warning: It is meant to be used on single band data and will likely fail on multiband inputs.

For more information about VRT PixelFunctions, see: https://www.gdal.org/gdal_vrttut.html#gdal_vrttut_derived_python.

------------
## Installation

### Development
#### Requirements:
- General requirements listed above
- Anaconda or Miniconda

#### To set up your local development environment:
This will install the s1_preprocessor package from the local repo in editable mode.
Any changes to Python files within the local repo should immediately take effect in this environment.

1. Clone the repo
`git clone https://github.com/GeoBigData/vrt_blending.git`

2. Move into the local repo
`cd vrt_blending`

3. Create conda virtual environment
`conda env create -f environment.yml`

4. Activate the environment
`source activate vrt_blending`

5. Install Python package
`pip install -r requirements_dev.txt`

### Common Issues:
- TBD
