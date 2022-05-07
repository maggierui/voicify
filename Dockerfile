FROM python:3.10-windowsservercore

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir
ADD . /code/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
RUN apt-get install -y --no-install-recommends dialog \
RUN apt-get update \
RUN apt-get install -y --no-install-recommends openssh-server \
RUN echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/
COPY Microsoft.CognitiveServices.Speech.extension.audio.sys.dll /usr/local/lib/python3.10/site-packages/azure/cognitiveservices/speech/
COPY Microsoft.CognitiveServices.Speech.core.dll /usr/local/lib/python3.10/site-packages/azure/cognitiveservices/speech/
COPY Microsoft.CognitiveServices.Speech.extension.codec.dll /usr/local/lib/python3.10/site-packages/azure/cognitiveservices/speech/
COPY Microsoft.CognitiveServices.Speech.extension.kws.dll /usr/local/lib/python3.10/site-packages/azure/cognitiveservices/speech/
COPY Microsoft.CognitiveServices.Speech.extension.lu.dll /usr/local/lib/python3.10/site-packages/azure/cognitiveservices/speech/

	
RUN chmod u+x /usr/local/bin/init.sh
EXPOSE 8000 2222
#CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["init.sh"]