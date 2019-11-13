From python:2
MAINTAINER yubarajpoudel708@gmail.com
ENV KOBOCAT_TMP_DIR=/srv/kobocat_tmp \
    # Store editable packages (pulled from VCS repos) in their own directory.
    PIP_EDITABLE_PACKAGES_DIR=/srv/pip_editable_packages \
    UWSGI_USER=wsgi \
    UWSGI_GROUP=wsgi

RUN apt-get -qq update && \
    apt-get -qq -y install \
        binutils \
        default-jre-headless \
        gdal-bin \
        libpcre3-dev \
        libpq-dev \
        libproj-dev \
        libxml2 \
        libxml2-dev \
        libxslt1-dev \
        libjpeg-dev \
        libffi-dev \
        npm \
        postgresql-client \
        python2.7-dev \
        wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    curl -s https://bootstrap.pypa.io/get-pip.py | python && \
    # FIXME: Temporarily install `pip` < v8.1.2 until `pip-tools` is compatible.
    pip install --upgrade pip==8.1.1 && \
    pip install uwsgi && \
    useradd -s /bin/false -m wsgi


###########################
# Install `apt` packages. #
###########################

COPY ./apt_requirements.txt ${KOBOCAT_TMP_DIR}/base_apt_requirements.txt
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y $(cat ${KOBOCAT_TMP_DIR}/base_apt_requirements.txt) && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

###########################
# Install `pip` packages. #
###########################

COPY ./requirements/ ${KOBOCAT_TMP_DIR}/base_requirements/
RUN mkdir -p ${PIP_EDITABLE_PACKAGES_DIR} && \
    pip install --upgrade 'pip>=10,<11' && \
    pip install --src ${PIP_EDITABLE_PACKAGES_DIR}/ -r ${KOBOCAT_TMP_DIR}/base_requirements/base.pip && \
    pip install --src ${PIP_EDITABLE_PACKAGES_DIR}/ -r ${KOBOCAT_TMP_DIR}/base_requirements/s3.pip && \
        pip install --src ${PIP_EDITABLE_PACKAGES_DIR}/ -r ${KOBOCAT_TMP_DIR}/base_requirements/fieldsight.pip && \
    rm -rf ~/.cache/pip