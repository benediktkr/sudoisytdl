FROM python:3.9

ENV DEBIAN_FRONTEND noninteractive
ENV TZ Europe/Berlin

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry

ARG UID=1216

RUN useradd -m -u ${UID} sudois && \
        mkdir /sudois && \
        chown sudois:sudois /sudois
USER sudois
WORKDIR /sudois

COPY --chown=sudois:sudois pyproject.toml /sudois
COPY --chown=sudois:sudois poetry.lock /sudois
RUN poetry install

COPY --chown=sudois:sudois sudoisytdl/ /sudois/sudoisytdl

ENTRYPOINT ["poetry"]
CMD ["run", "ytdl", "tg"]
