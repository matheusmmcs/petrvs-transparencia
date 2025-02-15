FROM python:3.9
WORKDIR /app
COPY requirements.txt ./
ENV PIP_NO_PROGRESS_BAR=off
RUN pip install --no-cache-dir --upgrade "pip<25" setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8880"]