FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install wget

RUN wget https://github.com/brunocodutra/cinder/releases/download/v0.3.1/cinder-v0.3.1-linux-avx2 && chmod +x cinder-v0.3.1-linux-avx2

FROM ubuntu:24.04

COPY --from=builder /cinder-v0.3.1-linux-avx2 /usr/local/bin/cinder-v0.3.1-linux-avx2

CMD [ "/usr/local/bin/cinder-v0.3.1-linux-avx2" ]
