FROM nginx:1.20.0

LABEL maintainer = "wangcheng" version = "v1.0" description = "MSB"

RUN sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list

RUN apt clean && apt-get update -y \
