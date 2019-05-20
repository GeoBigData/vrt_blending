FROM continuumio/miniconda:latest

# create the conda environment
RUN mkdir /helper
COPY ./environment.yml /helper
RUN conda env create -f /helper/environment.yml

# move the scripts over
ADD . /vrt_blending
SHELL ["/bin/bash", "-c"]
RUN echo "source activate vrt_blending" > ~/.bashrc
ENV PATH /opt/conda/envs/vrt_blending/bin:$PATH
RUN cd /vrt_blending && python setup.py install

ENV PYTHONPATH /vrt_blending









