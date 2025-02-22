FROM python:3.9-slim

WORKDIR /opt/pyreleases

COPY generate.py .
COPY src/ ./src/
COPY templates/ ./templates/

RUN chmod u+x ./templates/systemd/postinst ./templates/systemd/prerm

RUN  apt-get update && \
apt-get install -y --no-install-recommends ruby-full binutils
RUN gem install fpm
RUN pip install --no-cache-dir pyinstaller

ENTRYPOINT ["python", "generate.py"]