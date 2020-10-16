ARG SRC_IMAGE

FROM ${SRC_IMAGE}
LABEL maintainer="Davide De Tommaso <davide.detommaso@iit.it>"

ARG LOCAL_USER_ID
ENV DEBIAN_FRONTEND noninteractive
USER root

RUN usermod -u ${LOCAL_USER_ID} docky


RUN apt-get install -y python3-pip git libsm6 libxext6 libjpeg8-dev \
                       libpng-dev libavcodec-dev libxrender1 \
                       libswscale-dev libv4l-dev libgtk2.0-dev \
                       libatlas-base-dev gfortran libavformat-dev \
                       snapd cmake wget;

RUN apt-get install -y libqt5multimedia5 libqt5multimedia5-plugins libqt5multimediawidgets5 \
                       python3-pyqt5.qtmultimedia gstreamer1.0-libav ubuntu-restricted-extras \
                       python3-yaml gstreamer1.0-plugins-good alsa-utils \
                       fonts-crosextra-carlito fonts-open-sans

USER docky
ENV PATH=${PATH}:/home/docky/.local/bin
ENV QT_X11_NO_MITSHM=1

RUN cd $HOME &&\
    python3.8 -m pip install --user git+https://github.com/s4hri/pykron

RUN cd $HOME &&\
    python3.8 -m pip install --user git+https://github.com/s4hri/quantica

RUN cd $HOME &&\
    git clone -b autumn_refactor https://github.com/s4hri/dekla

ENV PYTHONPATH ${PYTHONPATH}:/home/docky/
