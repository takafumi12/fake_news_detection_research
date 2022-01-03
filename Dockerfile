FROM tensorflow/tensorflow:latest-gpu-py3-jupyter
WORKDIR /usr/local/
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
&& pip install -r requirements.txt
EXPOSE 80
