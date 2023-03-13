FROM python

RUN mkdir /service
COPY proto/ /service/proto/
COPY client/ /service/client/
WORKDIR /service/client
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../proto --python_out=. \
    --grpc_python_out=. ../proto/temporal_parsing.proto

EXPOSE 5000
ENV FLASK_APP=client.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]