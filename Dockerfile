FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

RUN addgroup -g 1001 -S backend && \
    adduser -u 1001 -G backend -S -D -H backend_user

FROM base AS builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /home/project

COPY uv.lock pyproject.toml /home/project/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY ./app /home/project/app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM base AS final

WORKDIR /home/project

COPY --from=builder --chown=backend_user:backend /home/project/.venv /home/project/.venv
COPY --from=builder --chown=backend_user:backend /home/project/app /home/project/app

RUN mkdir -p /home/project/logs && \
    chown backend_user:backend /home/project/logs

ENV PATH="/home/project/.venv/bin:$PATH"

USER backend_user

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
