FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip install --no-cache-dir "uvicorn[standard]"

COPY . /app/

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health 

CMD ["python", "-m", "streamlit", "run", "marketplace.py", "--server.port=8000", "--server.address=0.0.0.0"]
