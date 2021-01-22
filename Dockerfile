FROM python:3.9

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install poetry

RUN mkdir /ytdl
WORKDIR ytdl

ADD pyproject.toml /ytdl
ADD poetry.lock /ytdl
RUN poetry install

ADD sudoisytdl/ /ytdl/sudoisytdl

ENTRYPOINT ["poetry"]
CMD ["run", "ytdl", "tg"]
