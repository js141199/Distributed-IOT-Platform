FROM python:3.10
WORKDIR /deployer
COPY . /deployer
RUN pip install -r /deployer/requirements.txt
ENTRYPOINT ["python3", "/deployer/main.py"]
