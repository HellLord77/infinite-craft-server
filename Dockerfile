FROM python:alpine AS stage

WORKDIR /server

FROM stage AS install

COPY requirements.txt .
RUN pip install --no-cache-dir --user --requirement=requirements.txt

FROM stage AS prod

COPY --from=install /root/.local /root/.local
COPY src .

FROM prod AS database

COPY data data
RUN python init.py

FROM prod

COPY --from=database /server/database.sqlite .

EXPOSE 8000
ENTRYPOINT ["/root/.local/bin/uvicorn", "main:app"]
CMD ["--host=0.0.0.0"]
