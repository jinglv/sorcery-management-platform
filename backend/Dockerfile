FROM python:3.9.0
MAINTAINER lvjing
EXPOSE 8000
RUN pip install requirements.txt.bak -i https://pypi.douban.com/simple/
RUN pip install uwsgi -i https://pypi.douban.com/simple/
VOLUME ["/root"]
WORKDIR /root/sorcery-management-platform/backend
CMD ["uwsgi", "--ini", "uwsgi.ini"]