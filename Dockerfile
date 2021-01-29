FROM python:3.9 as base

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin
ENV TERM=xterm-256color

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry

ARG UID=1216
RUN useradd -m -u ${UID} sudois \
        && mkdir /sudois \
        && chown sudois:sudois /sudois \
        && poetry config virtualenvs.create false

WORKDIR /sudois

FROM base as builder

COPY --chown=sudois:sudois pyproject.toml /sudois
COPY --chown=sudois:sudois poetry.lock /sudois

RUN poetry install --no-interaction --no-root --ansi

COPY --chown=sudois:sudois sudoisytdl/ /sudois/sudoisytdl

RUN poetry install --no-interaction --ansi

USER sudois
CMD ["ytdl", "tg"]
