FROM python:3.10

RUN pip3 install --no-cache-dir --upgrade pip &&\
    apt install -y adduser &&\
    adduser -m worker &&\
    apt -y remove adduser &&\
    rm -rf /var/lib/apt/lists/*

USER worker
WORKDIR /home/worker

COPY --chown=worker:worker . .

RUN pip3 install --no-cache-dir --user -r requirements.txt && \
    pip3 install --no-cache-dir --user gunicorn

ENV PATH="/home/worker/.local/bin:${PATH}"

EXPOSE 5001

ENTRYPOINT [ "gunicorn", "proxy:app" ]
