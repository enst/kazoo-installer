FROM centos:6
MAINTAINER Bing Li <enst.bupt@gmail.com>

RUN useradd -r -g daemon bigcouch
RUN useradd -r -g daemon freeswitch
RUN useradd -r -g daemon kazoo
RUN useradd -r -g daemon kamailio

RUN curl -o /etc/yum.repos.d/2600hz.repo http://repo.2600hz.com/2600hz.repo

RUN yum update -y && yum install -y git

WORKDIR /tmp/
RUN git clone https://github.com/2600hz/community-scripts.git
RUN cp -r /tmp/community-scripts/simple-installer /opt/kazoo_install
RUN rm -rf /tmp/commumity-scripts

WORKDIR /opt/kazoo_install

RUN chmod +x setup* install*

RUN mkdir -p /srv
RUN mkdir -p /opt/kazoo/log
RUN chown bigcouch:daemon /srv -R
RUN chmod a+rw /var/log
RUN chmod a+rw /opt/kazoo/log

VOLUME ["/srv", /var/log", "/opt/kazoo/log"]

CMD ./install_kazoo

