# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.6
FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

# ✅ Use gunicorn to run the app in production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
