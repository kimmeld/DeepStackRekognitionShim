FROM python:3.13

RUN pip3 install --no-cache-dir --upgrade pip &&\
    adduser worker

USER worker
WORKDIR /home/worker

COPY . .

RUN pip3 install --no-cache-dir --user -r requirements.txt && \
    pip3 install --no-cache-dir --user gunicorn

ENV PATH="/home/worker/.local/bin:${PATH}"

EXPOSE 5001

ENTRYPOINT [ "gunicorn", "DSShim:app" ]
