from __future__ import absolute_import
import os
import json
import glob
from vrt_blending import vrtamix


def convert_type(var, f, expected_type):

    # try to convert the inputs to correct types
    if var is None:
        return None

    try:
        var = f(var)
    except ValueError as e:
        err = "Inputs {var} cannot be converted to type {expected_type}".format(var=var,
                                                                                expected_type=expected_type)
        raise ValueError(err)

    return var


def main():

    # get the inputs
    string_ports = '/mnt/work/input/ports.json'
    input_data = '/mnt/work/input/data'

    # create output directory
    out_path = '/mnt/work/output/data'
    if os.path.exists(out_path) is False:
        os.makedirs(out_path)
    out_vrt = os.path.join(out_path, 'blended.vrt')

    # read the inputs
    with open(string_ports) as ports:
        inputs = json.load(ports)
    blend_func = inputs.get('blend_func', 'mean')

    # convert the inputs to the correct dtypes
    blend_func = convert_type(blend_func, str, 'String').lower()

    # get the VRT file in the input folder
    vrts = glob.glob1(input_data, '*.vrt')
    if len(vrts) == 0:
        raise ValueError("No VRTs found in input data port")
    if len(vrts) > 1:
        raise ValueError("Multiple VRTs found in input data port")
    in_vrt = os.path.join(input_data, vrts[0])

    # run the processing
    print("Adding blending PixelFunction to {}".format(in_vrt))
    vrtamix.main([in_vrt,
                  out_vrt,
                  '--blend_func', blend_func
                  ])
    print("Processing completed successfully.")


if __name__ == '__main__':
    main()
