FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install git make cmake wget curl gcc g++ clang llvm lld

RUN git init PlentyChess && \
    cd PlentyChess && \
    git remote add origin https://github.com/Yoshie2000/PlentyChess.git && \
    git fetch --depth 1 origin c8f51e7f982af0b1f885dfc6cf889e1354ddf1bc && \
    git checkout FETCH_HEAD && \
    make -j EXE=PlentyChess ARCH=avx2

FROM ubuntu:24.04

COPY --from=builder /PlentyChess/PlentyChess /usr/local/bin/PlentyChess

CMD [ "/usr/local/bin/PlentyChess" ]
