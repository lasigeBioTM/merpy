#### To build:
## docker build github.com/lasigeBioTM/merpy -t fjmc/merpy-image
#### To test it:
## docker run -it --rm --name mer-container fjmc/merpy-image example1.py

#### To build with lexicons:
## curl -O -L https://github.com/lasigeBioTM/merpy/archive/master.zip
## unzip master.zip
## cd merpy-master 
## cat Dockerfile-LexiconsSimilarity >> Dockerfile
## docker build . -t fjmc/merpy-image:lexicons202103
#### To test it:
## docker run -it --rm --name mer-container fjmc/merpy-image:lexicons202103 example2.py

FROM python:3.7
LABEL maintainer="fcouto@di.fc.ul.pt"

# Labels
LABEL org.label-schema.description="MER (Minimal Named-Entity Recognizer) Python Interface (merpy + ssmpy)"
LABEL org.label-schema.url="http://labs.rd.ciencias.ulisboa.pt/mer/"
LABEL org.label-schema.vcs-url="https://github.com/lasigeBioTM/merpy"
LABEL org.label-schema.docker.cmd="docker run -it --rm --name mer-container fjmc/mer-image ./test.sh"

RUN apt-get update 
RUN apt-get install -y gawk 

RUN pip install --no-cache-dir merpy ssmpy

WORKDIR /usr/src/app

COPY example1.py ./

RUN apt-get autoremove
RUN apt-get clean

ENTRYPOINT ["python3"]


