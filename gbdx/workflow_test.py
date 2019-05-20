import os
import gbdxtools
import boto3
gbdx = gbdxtools.Interface()


src_vrt = 's3://gbd-customer-data/{prefix}/mgleason/vrt_sample/hand_default.vrt'.format(**gbdx.s3.info)

vrtamix_task = gbdx.Task('vrtamix:0.0.2',
                         data=src_vrt,
                         blend_func='min')

tasks = [vrtamix_task]

workflow = gbdx.Workflow(tasks)
workflow.savedata(vrtamix_task.outputs.data, location='mgleason/vrt_sample/wf_output')
workflow.execute()

print(workflow.id)

