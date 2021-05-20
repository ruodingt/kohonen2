FROM python:3.7.10-buster

RUN pip3 install --upgrade pip

COPY . kohonen2/

WORKDIR kohonen2/
RUN pip3 install -e .

EXPOSE 8888

CMD ['jupyter', 'notebook', '--ip', '"0.0.0.0"']
