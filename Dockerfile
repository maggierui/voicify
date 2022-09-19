FROM python:3.10.4-windowsservercore-1809
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
#ADD https://aka.ms/vs/17/release/vc_redist.x64.exe /vc_redist.x64.exe
#RUN vc_redist.x64.exe /install /quiet /norestart /log vc_redist.log

ADD https://aka.ms/vs/17/release/vc_redist.x64.exe /vc_redist.x64.exe
RUN C:\vc_redist.x64.exe /install /quiet 

# set environment variables
ENV PYTHONIOENCODING UTF-8
ENV PYTHON_VERSION 3.10.4
ENV PYTHONUNBUFFERED=11

RUN mkdir /code
# set work directory
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt --no-cache-dir

ADD . /code/
EXPOSE 8000
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
