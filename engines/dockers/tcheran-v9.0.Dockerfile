FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install git make cmake wget curl gcc g++ clang llvm lld

RUN wget https://github.com/tcheran-chess/tcheran/releases/download/v9.0/tcheran-v9.0-linux-x86_64-v3 && \
    chmod +x tcheran-v9.0-linux-x86_64-v3

FROM ubuntu:24.04

COPY --from=builder /tcheran-v9.0-linux-x86_64-v3 /usr/local/bin/tcheran

CMD [ "/usr/local/bin/tcheran" ]
