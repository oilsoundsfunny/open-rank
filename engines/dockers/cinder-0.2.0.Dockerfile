FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt-get -y install wget

RUN wget https://github.com/brunocodutra/cinder/releases/download/v0.2.0/cinder-v0.2.0-linux-x86-64-v3 && chmod +x cinder-v0.2.0-linux-x86-64-v3

FROM ubuntu:24.04

COPY --from=builder /cinder-v0.2.0-linux-x86-64-v3 /usr/local/bin/cinder-v0.2.0-linux-x86-64-v3

CMD [ "/usr/local/bin/cinder-v0.2.0-linux-x86-64-v3" ]
