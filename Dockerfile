FROM python:alpine AS stage

WORKDIR /server

FROM stage AS install

COPY requirements.txt .
RUN pip install --no-cache-dir --user --requirement=requirements.txt

FROM stage AS prod

COPY --from=install /root/.local /root/.local
COPY src .

FROM --platform=$BUILDPLATFORM alpine AS database

WORKDIR /server
COPY data data
RUN apk add --no-cache sqlite
RUN sqlite3 database.sqlite " \
    CREATE TABLE element ( \
        id INTEGER PRIMARY KEY AUTOINCREMENT, \
        text TEXT UNIQUE NOT NULL, \
        emoji TEXT NOT NULL \
    ); \
    CREATE TABLE pair ( \
        first_id INTEGER NOT NULL, \
        second_id INTEGER NOT NULL, \
        result_id INTEGER NOT NULL, \
        PRIMARY KEY (first_id, second_id), \
        FOREIGN KEY (first_id) REFERENCES element (id), \
        FOREIGN KEY (second_id) REFERENCES element (id), \
        FOREIGN KEY (result_id) REFERENCES element (id) \
    ); \
    "
RUN head -1 data/element/0.csv > data/element.csv && \
    tail -n +2 -q data/element/*.csv >> data/element.csv && \
    sqlite3 database.sqlite ".mode csv" ".import data/element.csv element"
RUN head -1 data/pair/0.csv > data/pair.csv && \
    tail -n +2 -q data/pair/*.csv >> data/pair.csv && \
    sqlite3 database.sqlite ".mode csv" ".import data/pair.csv pair"
RUN sqlite3 database.sqlite " \
    DELETE \
    FROM pair \
    WHERE result_id = (SELECT id FROM element WHERE text = 'Nothing'); \
    VACUUM; \
    "

FROM prod

COPY --from=database /server/database.sqlite .

EXPOSE 8000
ENTRYPOINT ["/root/.local/bin/uvicorn", "main:app"]
CMD ["--host=0.0.0.0"]
