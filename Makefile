DIRUTIL := utils/

all: start-hadoop-cluster

start-hadoop-cluster:
	./$(DIRUTIL)start_hadoop_cluster.sh

stop-hadoop-cluster:
	./$(DIRUTIL)stop_hadoop_cluster.sh

start-flume-collect:
	./$(DIRUTIL)start_flume_collect.sh
