FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY ./app /app
COPY requirements.txt /app
RUN mkdir db
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir --progress-bar off -r /app/requirements.txt
CMD [ "python", "-u", "main.py"]
