FROM python:3.10-slim
WORKDIR /app

# Copy required files
COPY requirements.txt ./
COPY *.py ./
COPY static/ ./static/
COPY modules/ ./modules/
COPY bin/ ./bin/
COPY templates/ ./templates/

# Set User
RUN useradd -c 'Sealed Secrets UI user' -m -d /app -s /bin/bash sealedsecrets
RUN chown -R sealedsecrets.sealedsecrets /app
USER sealedsecrets
ENV HOME /app

# Setup Path
RUN mkdir -p .local/bin
ENV PATH="$PATH:/app/.local/bin"

# Update pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Gunicorn Port
EXPOSE 5000/tcp

# Application Startup
ENTRYPOINT ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
