FROM python:3.11-slim

WORKDIR /app

COPY api/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .
COPY models/ ../models/

EXPOSE 5000

CMD ["python", "app.py"]
