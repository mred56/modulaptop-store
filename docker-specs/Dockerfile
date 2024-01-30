FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3-dev \
    libpq-dev \
    musl-dev \
    gcc \
    procps \
    && apt-get -y autoremove

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -U -r /tmp/requirements.txt

# Install Poetry
ENV POETRY_VERSION="1.5.1"
ENV POETRY_HOME="/etc/poetry"
ENV PATH="${POETRY_HOME}/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python \
    && poetry config virtualenvs.create false

COPY ./docker-specs/scripts/start.sh ./
COPY ./docker-specs/scripts/start-reload.sh ./

ENV WORKDIR /opt
WORKDIR ${WORKDIR}


# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* alembic.ini ./

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./docker-specs/scripts/entrypoint.sh ./
COPY ./migrations ./migrations
COPY ./app ./app

ENTRYPOINT ["/opt/entrypoint.sh"]

# If CMD is defined from the base image, setting ENTRYPOINT will reset CMD to an empty value. In this scenario, CMD must be defined in the current image to have a value.
# Thus, we need to set CMD
CMD [ \
  "sh", \
  "-c", \
  "/start.sh" \
]
