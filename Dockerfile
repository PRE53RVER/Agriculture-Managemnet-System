FROM python:3.10
WORKDIR /ams
COPY requirments.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirments.txt
COPY src .
EXPOSE 5000
CMD python3 app.py