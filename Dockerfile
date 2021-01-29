FROM python:3.9

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry

ARG UID=1216

RUN useradd -m -u ${UID} sudoisytdl && \
        mkdir /ytdl && \
        chown sudoisytdl:sudoisytdl /ytdl
USER sudoisytdl
WORKDIR ytdl

ADD pyproject.toml /ytdl
ADD poetry.lock /ytdl
RUN poetry install

ADD sudoisytdl/ /ytdl/sudoisytdl

ENTRYPOINT ["poetry"]
CMD ["run", "ytdl", "tg"]
