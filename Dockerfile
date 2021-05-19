FROM python:3.9.4

WORKDIR /setup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY main.py .
RUN chmod +x main.py && ln -s /app/main.py /app/auto-semver
ENV PATH="$PATH:/app"

CMD ["python", "auto-semver.py"]
