DIRSRC := src/
DIRUTL := utils/
DIRCFG := config/
DIRDAT := data/
DIRPIG := scripts/

all: start-hadoop run-api

start-hadoop:
	./$(DIRUTL)start_hadoop_cluster.sh

stop-hadoop:
	./$(DIRUTL)stop_hadoop_cluster.sh

start-flume:
	./$(DIRUTL)start_flume_collect.sh

stop-flume:
	./$(DIRUTL)stop_flume_collect.sh

rm-logs:
	find . -name "*.log" -type f -delete

run-api:
	python $(DIRSRC)server/Server.py

run-client:
	python $(DIRSRC)client/Client.py

tests:
	nosetests --with-coverage --cover-html --cover-html-dir=src/server/test/html src/server