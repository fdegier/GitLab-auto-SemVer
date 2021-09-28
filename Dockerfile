FROM python:3.9.4

RUN apt-get -yqq update \
	&& apt-get -yqq install --no-install-recommends git-lfs \
	&& apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

WORKDIR /setup

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app/ .
RUN chmod +x main.py && ln -s /app/main.py /app/auto-semver
ENV PATH="$PATH:/app"

CMD ["auto-semver"]
