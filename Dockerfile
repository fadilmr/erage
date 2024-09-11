FROM python:3.10-slim

WORKDIR /app



COPY . .

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "server.port=8501"]