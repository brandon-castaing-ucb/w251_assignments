FROM w251/cuda:dev-tx2-4.2.1_b97

ARG URL=http://169.44.201.108:7002/jetpacks/4.2.1

RUN apt-get update && apt install -y git pkg-config wget build-essential cmake unzip python-pip

# Install OpenCV + Paho-MQTT
RUN curl $URL/libopencv_3.3.1-2-g31ccdfe11_arm64.deb  -so libopencv_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-dev_3.3.1-2-g31ccdfe11_arm64.deb
RUN curl $URL/libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb -so libopencv-python_3.3.1-2-g31ccdfe11_arm64.deb
RUN apt install -y  libtbb-dev libavcodec-dev libavformat-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgtk2.0-dev
RUN apt install -y libswscale-dev libv4l-dev
RUN dpkg -i *.deb
RUN pip install paho-mqtt numpy

COPY detect_face.py /

RUN pip install ibm-cos-sdk
RUN echo "oSHZPcGNsFqUExzmbZft:wzl0xagvkaAEuga0gUXB3Rs9JglmoviCODdYK0NC" > $HOME/.cos_creds
RUN chmod 600 $HOME/.cos_creds

ENTRYPOINT python detect_face.py
