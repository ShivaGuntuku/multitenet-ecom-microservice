FROM python:3.10-slim-bullseye

WORKDIR /user_service

COPY . /user_service

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
