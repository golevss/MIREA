FROM ubuntu:20.10

RUN sed -i 's/archive.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
RUN apt update && \
    apt install -y python3 figlet

EXPOSE 8802
CMD ["python3", "-m", "http.server", "8802"]
