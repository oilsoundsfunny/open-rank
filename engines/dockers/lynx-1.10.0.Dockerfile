FROM ubuntu:24.04 AS builder

ARG DEBIAN_FRONTEND=noninteractive
ARG LYNX_VERSION=1.10.0

RUN apt update && apt-get -y install wget unzip

RUN wget https://github.com/lynx-chess/Lynx/releases/download/v${LYNX_VERSION}/lynx-${LYNX_VERSION}-linux-x64.zip \
    && unzip lynx-${LYNX_VERSION}-linux-x64.zip -d lynx \
    && chmod +x lynx/Lynx.Cli

FROM ubuntu:24.04

COPY --from=builder /lynx /usr/local/bin/lynx/

ENV DOTNET_gcServer=0

CMD [ "/usr/local/bin/lynx/Lynx.Cli" ]