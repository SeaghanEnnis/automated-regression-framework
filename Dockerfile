FROM organization.jfrog.io/docker-dev/alpine:3.20

LABEL source_url="$SOURCE_URL"

ARG JFROG_USER
ARG JFROG_PASSWORD
ARG SOURCE_URL

# CONFIGURE PACKAGE REPOS
# INSTALL PACKAGES

RUN  echo $(cat /etc/apk/repositories) \
    && echo "https://$JFROG_USER:$JFROG_PASSWORD@organization.jfrog.io/artifactory/apk-dev/v3.20/main" >> /etc/apk/repositories \
    && echo "https://$JFROG_USER:$JFROG_PASSWORD@organization.jfrog.io/artifactory/apk-dev/v3.20/community" >> /etc/apk/repositories \
    && apk update \
    && apk upgrade \
    && apk add curl bash file python3 py3-pip 


COPY ./requirements.txt ./requirements.txt
RUN cat requirements.txt

RUN mkdir ~/.pip

RUN --mount=type=secret,id=aws \
    echo -e "[global]\nindex-url = https://$JFROG_USER:$JFROG_PASSWORD@organization.jfrog.io/artifactory/api/pypi/dev-pypi/simple" > ~/.pip/pip.conf

RUN python -m pip install -r ./requirements.txt --break-system-packages

RUN mkdir tests
COPY ./tests/* ./tests

COPY ./environment.json .
COPY ./environment-dev.json .
COPY ./environment-int.json .
COPY ./environment-test.json .
COPY ./environment-prod.json .

COPY ./run_regression.sh .
COPY ./upload_to_s3.py .

RUN chmod a+x run_regression.sh
RUN dos2unix run_regression.sh
RUN python -v

CMD ["/bin/bash","/run_regression.sh"]
