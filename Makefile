DIRSRC := src/
DIRUTL := utils/
DIRCFG := config/
DIRDAT := data/
DIRDOC := docs/
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

pig-test:
	pig -f $(DIRPIG)pig_likes.pig -p LIKES=100
	pig -f $(DIRPIG)pig_rts.pig -p RTS=20
	pig -f $(DIRPIG)pig_palabra.pig -p WORD="internet"

rm-logs:
	find . -name "*.log" -type f -delete

run-api:
	python $(DIRSRC)run.py