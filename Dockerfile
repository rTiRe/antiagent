FROM python:3.13.7-alpine

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

RUN pip install --upgrade pip
RUN pip3 install --upgrade poetry==2.1.2

COPY ./poetry.lock /usr/src/bot/poetry.lock
COPY ./pyproject.toml /usr/src/bot/pyproject.toml

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all

COPY . /usr/src/bot

CMD ["python3", "-m", "src"]