FROM continuumio/miniconda3

LABEL maintainer="areed145@gmail.com"

WORKDIR /metpy-tasks

COPY . /metpy-tasks

RUN conda env create -f environment.yml
RUN echo "source activate $(head -1 environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 environment.yml | cut -d' ' -f2)/bin:$PATH

ENV MONGODB_CLIENT 'mongodb+srv://kk6gpv:kk6gpv@cluster0-kglzh.azure.mongodb.net/test?retryWrites=true&w=majority'

CMD ["python", "metpy-tasks.py"]
