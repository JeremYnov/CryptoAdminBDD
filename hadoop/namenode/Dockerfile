FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

RUN apt -y update
RUN apt -y install vim cron

RUN echo "* * * * * bash /push_to_hdfs.sh >> /var/log/push_to_hdfs.log 2>&1" >> /etc/crontab
RUN update-rc.d cron defaults

HEALTHCHECK CMD curl -f http://localhost:9870/ || exit 1

ENV HDFS_CONF_dfs_namenode_name_dir=file:///hadoop/dfs/name
RUN mkdir -p /hadoop/dfs/name
VOLUME /hadoop/dfs/name

ADD run.sh /run.sh
RUN chmod a+x /run.sh

ADD push_to_hdfs.sh /push_to_hdfs.sh
RUN chmod a+x /push_to_hdfs.sh

EXPOSE 9870

CMD ["/run.sh"]
