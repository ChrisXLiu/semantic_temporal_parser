FROM python:3.10.10-slim-bullseye

RUN apt update && apt -y install maven gcc build-essential
RUN mvn -version
RUN mkdir /service
COPY proto/ /service/proto/
COPY server/ /service/server/
WORKDIR /service/server
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python -c 'from importlib import util; import pathlib; print(pathlib.Path(util.find_spec("sutime").origin).parent / "pom.xml")')
RUN python -m grpc_tools.protoc -I ../proto --python_out=. \
    --grpc_python_out=. ../proto/temporal_parsing.proto

EXPOSE 50051
ENTRYPOINT [ "python", "temporal_parsing.py" ]