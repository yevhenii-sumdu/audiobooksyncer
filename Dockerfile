FROM python:3.10

RUN apt update && apt install gcc libespeak-dev ffmpeg -y

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN python -c "import bertalign; bertalign.load_model()"

RUN python -c "import whisper; whisper.load_model('base')"

COPY pyproject.toml audiobooksyncer/

COPY audiobooksyncer audiobooksyncer/audiobooksyncer

RUN pip install ./audiobooksyncer

WORKDIR /work

ENTRYPOINT ["audiobooksyncer"]
