FROM python:3.9.16

RUN apt upgrade --without-new-pkgs && apt full-upgrade
RUN apt install -y git curl make

ENV LINE_NOTIFY_TOKEN=C7***************************************G9 \
    LINE_NOTIFY_BASEURL=https://notify-api.line.me/api \
    ARCH=amd64 \
    GO_VERSION=1.18

RUN set -x \
    && cd /tmp \
    && wget https://dl.google.com/go/go$GO_VERSION.linux-$ARCH.tar.gz \
    && tar -C /usr/local -xzf go$GO_VERSION.linux-$ARCH.tar.gz \
    && rm /tmp/go$GO_VERSION.linux-$ARCH.tar.gz

ENV PATH=$PATH:/usr/local/go/bin \
    GOPATH=$HOME/work \
    PROJECT_ROOTDIR=/app/

WORKDIR $PROJECT_ROOTDIR
RUN mkdir ./python ./go
COPY python/ ./python/
COPY go/ ./go/
RUN cd ./go && go mod download
COPY stock_analytics.sh $PROJECT_ROOTDIR

RUN chmod 744 $PROJECT_ROOTDIR/stock_analytics.sh
