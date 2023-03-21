#!/bin/bash
# reference from
# https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html

# Install system packages required by PyTorch:
echo "Install system packages required by PyTorch"
sudo apt update
sudo apt-get -y install autoconf bc \
          build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping \
          libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev \
          libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev \
          locales moreutils openssl python-openssl rsync scons \
          python3-pip \
          libopenblas-dev

      # libopenmpi-dev \
      #     libopenmpi2 \
      #       openmpi-bin \
      #       openmpi-common \
		  # gfortran \
# pip3 install setuptools Cython wheel
# pip3 install numpy


# python3 -m pip --no-cache-dir install torch-1.12.0a0+2c916ef.nv22.3-cp38-cp38-linux_aarch64.whl \
#     -f https://developer.download.nvidia.com/compute/redist/jp/v50/pytorch

# PYTORCH_URL=https://nvidia.box.com/shared/static/ssf2v7pf5i245fk4i0q926hy4imzs2ph.whl	
# PYTORCH_WHL=torch-1.11.0-cp38-cp38-linux_aarch64.whl

# wget --quiet --show-progress --progress=bar:force:noscroll --no-check-certificate $PYTORCH_URL -O $PYTORCH_WHL && \
# pip3 install $PYTORCH_WHL --verbose
# rm $PYTORCH_WHL
# export TORCH_INSTALL=https://nvidia.box.com/shared/static/ssf2v7pf5i245fk4i0q926hy4imzs2ph.whl
export TORCH_INSTALL=./torch-1.11.0-cp38-cp38-linux_aarch64.whl

# Install python dependencies:
echo "Install python dependencies"
python3 -m pip install --upgrade pip
python3 -m pip install expecttest xmlrunner hypothesis aiohttp numpy==1.17.4 pyyaml scipy ninja cython typing_extensions protobuf
export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"
python3 -m pip install --upgrade protobuf
# Install PyTorch
echo "Install PyTorch 1.11.0"
python3 -m pip install --no-cache $TORCH_INSTALL
echo "Install torchvision and others"
python3 -m pip install torchvision==0.12.0 
python3 -m pip install pycuda pillow==7.0.0

# add ros into env
echo "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
