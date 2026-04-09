
FROM apache/spark:latest

USER root

ARG py_ver=3.11

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    build-essential \
    git \
    curl \
    wget && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python${py_ver} \
    python${py_ver}-distutils \
    python${py_ver}-venv \
    python${py_ver}-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python${py_ver} get-pip.py && \
    rm get-pip.py && \
    python${py_ver} -m pip install --upgrade pip setuptools wheel && \
    python${py_ver} -m pip install pyspark pandas jupyter jupyterlab ipython ipykernel

RUN update-alternatives --install /usr/bin/python python /usr/bin/python${py_ver} 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${py_ver} 1

# Create jovyan user
RUN useradd -m -s /bin/bash jovyan && \
    chown -R jovyan:jovyan /home/jovyan

# Install development tools
RUN python -m pip install --no-cache-dir \
    pylint \
    black \
    isort \
    pytest \
    pytest-cov

ENV PYTHONUNBUFFERED=1
WORKDIR /home/jovyan/code
USER jovyan
