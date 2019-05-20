from xml.dom import minidom
from xml.sax.saxutils import unescape
import os
import click


@click.command()
@click.argument('source')
@click.argument('destination')
@click.option('--blend_func', '-b', required=False, type=str, default='mean',
              help="Mathematical function to be used for blending overlapping pixels in VRT. "
                   "Valid options are: min, mean, max. Default: mean")
def main(source, destination, blend_func='mean'):

    # check the input blend_func
    if blend_func not in ('min', 'max', 'mean'):
        raise ValueError

    # make sure the output file doesn't already exist
    if os.path.exists(destination) is True:
        raise FileExistsError("Destination file already exists, cannot overwrite.")

    # make sure the input exists
    if os.path.exists(source) is False:
        raise FileExistsError("Source file does not exist.")

    # open the vrt
    xmldoc = minidom.parse(source)

    # get the VRTRasterBand Element
    vrt_raster_band = xmldoc.getElementsByTagName('VRTRasterBand')[0]
    # add the subclass attribute tag
    vrt_raster_band.setAttribute('subClass', "VRTDerivedRasterBand")

    # get the no_data value
    no_data_value = xmldoc.getElementsByTagName('NoDataValue')[0].childNodes[0].nodeValue

    # add the pixelfunction tags
    new_elements = {'PixelFunctionType': 'blend',
                    'PixelFunctionLanguage': 'Python',
                    'PixelFunctionCode': '''<![CDATA[
import numpy as np
def blend(in_ar, out_ar, xoff, yoff, xsize, ysize, raster_xsize,
                   raster_ysize, buf_radius, gt, **kwargs):
    no_data = np.array({no_data_value}, out_ar.dtype).tolist()
    in_ar_masked = np.ma.masked_array([out_ar] * len(in_ar), mask=False)
    for i, a in enumerate(in_ar):
        in_ar_masked[i, :, :] = a
        in_ar_masked.mask[i, :, :] = (a == no_data)
    out_ar[:] = in_ar_masked.{blend_func}(axis = 0).filled(no_data)
]]>'''.format(no_data_value=no_data_value,
                  blend_func=blend_func)}
    for k, v in new_elements.items():
        new_child_element = xmldoc.createElement(k)
        new_child_text = xmldoc.createTextNode(v)
        new_child_element.appendChild(new_child_text)
        vrt_raster_band.appendChild(new_child_element)

    with open(destination, 'w') as o:
        o.write(unescape(xmldoc.toprettyxml()[22:]))


if __name__ == '__main__':
    main()

