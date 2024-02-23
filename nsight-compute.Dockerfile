FROM nvidia/cuda:12.2-base

# Install basic dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Nsight Compute
RUN wget -O /tmp/nsight_compute.deb https://developer.download.nvidia.com/devtools/repos/ubuntu2004/amd64/nsight-compute-2021.1.2_2021.1.2.19-1_amd64.deb \
    && dpkg -i /tmp/nsight_compute.deb \
    && rm /tmp/nsight_compute.deb
