FROM python:3.10.12-slim as base

ENV USER=my_user \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install --no-install-recommends -y \
    dumb-init \
    curl \
    && apt-get clean \
    && addgroup --system $USER && adduser --system --group $USER

ENV BUILDER_DIR=/usr/src/$USER

FROM base as builder

WORKDIR $BUILDER_DIR

COPY req.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir "$BUILDER_DIR"/wheels \
    -r req.txt

FROM base

ENV HOME_DIR=/home/$USER
ENV APP_DIR=$HOME_DIR/src

WORKDIR $APP_DIR

COPY --from=builder $BUILDER_DIR/wheels /wheels
COPY --from=builder $BUILDER_DIR/req.txt $HOME_DIR
RUN pip install --no-cache-dir /wheels/*

COPY . $APP_DIR

ENV PYTHONPATH=$APP_DIR

RUN chown -R "$USER":"$USER" $APP_DIR
RUN chown -R "$USER":"$USER" /opt
USER $USER

CMD ["bash", "-c", "chmod +x alembic.ini && dumb-init alembic -c alembic.ini upgrade head && uvicorn src.main:app --reload --host 0.0.0.0 --port 8001"]
