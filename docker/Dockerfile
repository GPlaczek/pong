FROM debian:bullseye

RUN apt-get update \
    && apt-get -y install cmake \
    clang \
    git \
    gcc-arm-none-eabi
RUN git clone https://github.com/raspberrypi/pico-sdk.git
WORKDIR /pico-sdk
RUN git submodule update --init --recursive
ENV PICO_SDK_PATH=/pico-sdk
RUN apt-get clean
WORKDIR /
