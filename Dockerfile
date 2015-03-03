FROM centos:6
MAINTAINER Bing Li <enst.bupt@gmail.com>

RUN useradd -r -g daemon bigcouch
RUN useradd -r -g daemon freeswitch
RUN useradd -r -g daemon kazoo
RUN group -r kamailio && useradd -r -g kamailio kamailio

RUN curl -o /etc/yum.repos.d/2600hz.repo http://repo.2600hz.com/2600hz.repo

RUN yum update -y && yum install -y git

WORKDIR /tmp/
RUN git clone https://github.com/2600hz/community-scripts.git
RUN cp -r /tmp/community-scripts/simple-installer /opt/kazoo_install
RUN rm -rf /tmp/commumity-scripts

WORKDIR /opt/kazoo_install

RUN chmod +x setup* install*

RUN mkdir -p /srv
RUN mkdir -p /var/log/bigcouch
RUN mkdir -p /var/log/freeswitch
RUN mkdir -p /opt/kazoo/log
RUN mkdir -p /var/log/kamailio

RUN chown bigcouch:daemon /srv -R
RUN chown bigcouch:daemon /var/log/bigcouch -R
RUN chown freeswitch:daemon /var/log/freeswitch -R
RUN chown kazoo:daemon /opt/kazoo/log -R
RUN chown kamailio:kamailio /var/log/kamailio -R

VOLUME ["/srv", "/etc/kazoo", "/var/log", "/opt/kazoo/log"]

CMD ./install_kazoo

