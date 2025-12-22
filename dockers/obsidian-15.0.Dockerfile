FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install git make cmake wget curl gcc g++ clang llvm lld

RUN git init Obsidian && \
    cd Obsidian && \
    git remote add origin https://github.com/gab8192/Obsidian.git && \
    git fetch --depth 1 origin 328b493cce625aa97ae7dd55eb77e35af97f341e && \
    git checkout FETCH_HEAD && \
    make -j EXE=Obsidian build=avx2

FROM ubuntu:24.04

COPY --from=builder /Obsidian/Obsidian /usr/local/bin/Obsidian

CMD [ "/usr/local/bin/Obsidian" ]
