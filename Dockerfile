FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
# Run as non-root
RUN adduser -D workeruser
USER workeruser
CMD ["python", "-u", "main.py"]
