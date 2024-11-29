FROM odoo:17.0

USER root

RUN apt-get update && \
    apt-get install -y \
    python3-pip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libcairo2-dev \
    libjpeg-dev \
    libgif-dev \
    && pip3 install cairosvg \
    && apt-get clean

USER odoo
