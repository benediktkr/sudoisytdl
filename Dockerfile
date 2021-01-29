FROM python:3.9

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry

ARG UID=1216

RUN useradd -m -u ${UID} sudois && \
        mkdir /sudois && \
        chown sudois:sudois /sudois
USER sudois
WORKDIR /sudois

ADD pyproject.toml /sudois
ADD poetry.lock /sudois
RUN poetry install

ADD sudoisytdl/ /sudois/sudoisytdl

ENTRYPOINT ["poetry"]
CMD ["run", "ytdl", "tg"]
