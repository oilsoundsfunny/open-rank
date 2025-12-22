FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install git make cmake wget curl gcc g++ clang llvm lld

RUN git init Obsidian && \
    cd Obsidian && \
    git remote add origin https://github.com/gab8192/Obsidian.git && \
    git fetch --depth 1 origin 2838ce52c1a3f997cb1175b360cd8c6b2ae6791c && \
    git checkout FETCH_HEAD && \
    make -j EXE=Obsidian build=avx2

FROM ubuntu:24.04

COPY --from=builder /Obsidian/Obsidian /usr/local/bin/Obsidian

CMD [ "/usr/local/bin/Obsidian" ]
