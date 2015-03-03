FROM bingli/kazoo-base
MAINTAINER Bing Li <enst.bupt@gmail.com>

RUN yum update -y && yum install -y git

WORKDIR /tmp/
RUN git clone https://github.com/2600hz/community-scripts.git
RUN cp -r /tmp/community-scripts/simple-installer /opt/kazoo_install
RUN rm -rf /tmp/commumity-scripts

#iptables causes exit
RUN sed -i '/iptables/s/^/#/' /opt/kazoo_install/setup_packages

WORKDIR /opt/kazoo_install

RUN chmod +x setup* install*

CMD ./install_kazoo

