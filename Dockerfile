FROM python:3.9

RUN apt-get update && \
    apt-get clean && \
    apt-get install -y wget && \
    apt-get install -y gnupg && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get -y install google-chrome-stable --fix-missing

# ENV SENDGRID_API_KEY=SG.DrDnr-ZeTi-18A80GoCnDA.
# REST OF KEY l7JQ7dRUO_QYsKu_0jXeRSDf3n1nQkiYGC194fa8nuU
RUN apt-get update && \
    apt-get install -y wget && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb --fix-missing

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "functions_framework", "--source", "function_send_to_ben.py", "--target", "send_email", "--port", "8080"]
