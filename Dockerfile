FROM centos:6
MAINTAINER Bing Li <enst.bupt@gmail.com>

RUN curl -o /etc/yum.repos.d/2600hz.repo http://repo.2600hz.com/2600hz.repo

RUN yum update -y && yum install -y git

COPY ./community-scripts/simple-installer/ /opt/kazoo_install/

WORKDIR /tmp/
RUN git clone https://github.com/2600hz/community-scripts.git
RUN cp -r /tmp/community-scripts/simple-installer /opt/kazoo_install
RUN rm -rf /tmp/commumity-scripts

WORKDIR /opt/kazoo_install

RUN chmod +x setup* install*

VOLUME ["/var/log", "/opt/kazoo/log"]

CMD ./install_kazoo

