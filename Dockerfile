ARG SRC_IMAGE
FROM $SRC_IMAGE
LABEL maintainer="Davide De Tommaso <dtmdvd@gmail.com>"
ARG LOCAL_USER_ID

USER root
RUN usermod -u ${LOCAL_USER_ID} docky

ENV DEBIAN_FRONTEND noninteractive

# 1: tobii glasses

RUN apt-get update
RUN apt-get install -y python3-pip git libsm6 libxext6 libjpeg8-dev \
                       libpng-dev libavcodec-dev libxrender1 \
                       libswscale-dev libv4l-dev libgtk2.0-dev \
                       libatlas-base-dev gfortran libavformat-dev \
                       snapd cmake wget;

USER docky
ENV PATH=${PATH}:/home/docky/.local/bin
ENV QT_X11_NO_MITSHM=1


# RUN git clone https://github.com/ddetommaso/TobiiGlassesPySuite && \
#     cd TobiiGlassesPySuite && \
#     pip3 install --user . && \
#     cd .. && \
#     rm -rf TobiiGlassesPySuite;

# 2: prepare multimedia packages for qt5

USER root

RUN apt-get update
RUN apt-get install -y \
    libqt5multimedia5 libqt5multimedia5-plugins libqt5multimediawidgets5 \
    python3-pyqt5.qtmultimedia gstreamer1.0-libav ubuntu-restricted-extras \
    python3-yaml gstreamer1.0-plugins-good alsa-utils \
    fonts-crosextra-carlito fonts-open-sans

COPY workdir/pulse-client.conf /etc/pulse/client.conf

USER docky

# placeholder # RUN pip3 install pykron
RUN cd $HOME &&\
    git clone https://github.com/s4hri/pykron &&\
    cd pykron &&\
    git checkout 0.6 &&\
    pip3 install --user .

RUN cd $HOME &&\
    git clone --recursive https://github.com/ddetommaso/TobiiGlassesPyController &&\
    cd TobiiGlassesPyController &&\
    git checkout 2.2.8 &&\
    pip3 install --user .


RUN cd $HOME &&\
    git clone --recursive https://github.com/ddetommaso/TobiiGlassesPySuite &&\
    cd TobiiGlassesPySuite &&\
    git checkout 1.1 &&\
    pip3 install --user .

RUN pip3 install --user python-statemachine

ENTRYPOINT ["/home/docky/init.sh"]
