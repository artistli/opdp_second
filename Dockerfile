FROM python:3.7.7-slim
  
COPY opdp_second ./opdp_second
RUN pip install --no-cache-dir -r opdp_second/requirements.txt


COPY opdp_second /opt/opdp_second/

EXPOSE 9906
WORKDIR /opt/opdp_second

CMD ["python", "main.py", "9906"]
