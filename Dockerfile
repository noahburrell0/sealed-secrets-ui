FROM python:3.10-slim
WORKDIR /app

# Install process tools for startup probes, and apply latest minor patchsets from base tag
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install --no-install-recommends -y procps curl && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
# RUN dpkg -r --force-all apt apt-get && dpkg -r --force-all debconf dpkg

# Copy required files
COPY requirements.txt ./
COPY *.py ./
COPY static/ ./static/
COPY modules/ ./modules/
COPY templates/ ./templates/

# Create bin directory
RUN mkdir ./bin

# Add in Kubeseal binary
ADD https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.19.5/kubeseal-0.19.5-linux-amd64.tar.gz /tmp/kubeseal.tar.gz
RUN tar -xvzf /tmp/kubeseal.tar.gz -C /app/bin kubeseal

# Add in GKE authentication binary
ADD https://dl.google.com/dl/cloudsdk/release/downloads/for_packagers/linux/google-cloud-cli-gke-gcloud-auth-plugin_421.0.0.orig_amd64.tar.gz /tmp/gke-gcloud-auth-plugin.tar.gz
RUN tar -xvzf /tmp/gke-gcloud-auth-plugin.tar.gz -C /tmp && mv /tmp/google-cloud-sdk/bin/gke-gcloud-auth-plugin ./bin/

# Cleanup tar files
RUN rm -rf /tmp/*

# Set User
RUN useradd -c 'Sealed Secrets UI user' -m -d /app -s /bin/bash sealedsecrets
RUN chown -R sealedsecrets.sealedsecrets /app
USER sealedsecrets
ENV HOME=/app

# Setup Path
RUN mkdir -p .local/bin
ENV PATH="$PATH:/app/.local/bin"
ENV PATH="$PATH:/app/bin"

# Update pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Gunicorn Port
EXPOSE 5000/tcp

# Application Startup
ENTRYPOINT ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
