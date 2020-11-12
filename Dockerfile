
FROM lijiajiajia/ubuntu-blog:v1
MAINTAINER lijiajiajia

WORKDIR /home/blog

COPY requirements.txt ./
RUN pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --no-cache-dir -r requirements.txt

EXPOSE 39005
EXPOSE 39006
