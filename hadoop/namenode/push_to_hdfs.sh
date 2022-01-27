export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"

if [ -n "$(ls -A /csv 2>/dev/null)" ]
then
  /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /csv
  /opt/hadoop-3.2.1/bin/hdfs dfs -put /csv/* /csv

  rm -rf /csv/*
fi
