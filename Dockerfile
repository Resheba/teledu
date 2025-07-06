FROM python:3.11.9-slim

# ENV TELEGRAM_TOKEN
# ENV ADMIN_IDS
# ENV CONTACT_URL

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /code

COPY . .

RUN chmod 777 docker/app.sh

CMD ["bash", "docker/app.sh"]
