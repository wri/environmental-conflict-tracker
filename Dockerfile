FROM tensorflow/tensorflow:1.13.1-gpu-py3

# Adds metadata to the image as a key value pair example LABEL version="1.0"
LABEL maintainer="John Brandt <john.brandt@wri.org>"

##Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update -y && apt-get install --no-install-recommends -y -q \
    ca-certificates gcc libffi-dev wget unzip git openssh-client gnupg curl \
    python3-dev python3-setuptools

# Trick to let tensorflow-gpu work on CPU
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 && \
    echo "/usr/local/cuda/lib64/stubs" >> /etc/ld.so.conf.d/cuda-9-0.conf && \
    ldconfig

RUN pip install --upgrade pip

RUN mkdir src
RUN mkdir notebooks

COPY notebooks/ src/notebooks/

WORKDIR src/
COPY . .

RUN pip install -r requirements.txt
RUN pip install jupyter

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

# docker build -t johnbrandtwri/environmental_conflict_tracker .
# docker run -p 8888:8888 johnbrandtwri/environmental_conflict_tracker
# docker push johnbrandtwri/environmental_conflict_tracker