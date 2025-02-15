FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
ENV PIP_NO_PROGRESS_BAR=off
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir setuptools
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8880"]