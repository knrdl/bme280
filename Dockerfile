FROM alpine

ENV PYTHONIOENCODING=utf-8

RUN apk add --no-cache python3 py3-smbus

COPY src /app

WORKDIR /app

EXPOSE 8080/tcp

CMD ["python3", "main.py"]

HEALTHCHECK --interval=30s --timeout=15s --start-period=5s --retries=3 CMD [ "curl", "--fail", "--silent", "127.0.0.1:8080" ]
