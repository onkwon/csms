FROM python:3.12-slim-bookworm

WORKDIR /csms
COPY . .
RUN pip install -e .

CMD [ "python", "app/csms.py"]
