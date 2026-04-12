FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
https://claude.ai/share/3a814462-7a08-477f-a302-c0373b5ec60b

EXPOSE 7860
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]