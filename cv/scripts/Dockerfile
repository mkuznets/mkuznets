FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    LANG='en_US.UTF-8' \
    LANGUAGE='en_US:en' \
    APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1 \
    TERM=xterm-color

RUN apt-get update -q && \
    apt-get install -y -q --no-upgrade --no-install-recommends \
        python-is-python3 \
        python3-venv \
        pandoc \
        texlive \
        lmodern \
        texlive-latex-extra \
        texlive-plain-generic \
        texlive-lang-cyrillic \
        cm-super \
        latexmk \
        make \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD requirements.txt /tmp/requirements.txt
RUN python -m venv /py && \
    /py/bin/pip install -U pip==21.0.1 setuptools==53.0.0 && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

ENV PATH=/py/bin:$PATH
WORKDIR /cv
