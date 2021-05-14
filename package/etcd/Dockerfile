FROM centos:7
COPY etcd /
COPY start.sh /
VOLUME /etcd-data
EXPOSE 2379 2380
ENTRYPOINT ["sh", "/start.sh"]
