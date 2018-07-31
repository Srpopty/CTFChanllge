FROM python:2

COPY ./app/ /opt/
COPY ./root /root/

# install dependencies
RUN python -m pip install flask flask_session && \
#
# access control
# all files owner: root:root, files: 644, dirs: 755, /opt/log/* 622
#
cp /root/*.txt /opt/ && \
find /opt -type d -exec chmod 755 {} \; && \
find /opt -type f -exec chmod 644 {} \; && \
chmod 622 /opt/log/* && \
#
# add user ctf
#
useradd -s /bin/bash -m ctf && chown ctf:ctf /opt/database/ && chown ctf:ctf /opt/session/

CMD ["python", "/opt/app.py"]

