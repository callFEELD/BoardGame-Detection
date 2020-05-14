FROM jjanzic/docker-python3-opencv

COPY ./src /src
WORKDIR /

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD uvicorn src.api.main:app --host 0.0.0.0 --port 80 --timeout-keep-alive 500 --workers 2