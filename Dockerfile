FROM python:3.10

WORKDIR /LPR-App

RUN apt-get update && apt-get install --no-install-recommends -y \
    ffmpeg libsm6 libxext6 \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0", "--port", "8000" ] 