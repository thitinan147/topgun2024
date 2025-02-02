FROM python:3
WORKDIR /app
COPY app.py .
COPY requirement.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
