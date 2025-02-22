FROM python:3.9-slim

WORKDIR /opt/${app_name}

COPY volumes/app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${port}

CMD ["python", "${main}"]