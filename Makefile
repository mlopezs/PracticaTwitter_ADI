DIRSRC := src/
DIRUTL := utils/
DIRCFG := config/
DIRDAT := data/
DIRPIG := scripts/

all: start-hadoop run-api run-client

start-hadoop:
	./$(DIRUTL)start_hadoop_cluster.sh

stop-hadoop:
	./$(DIRUTL)stop_hadoop_cluster.sh

pig-test:
	pig -f $(DIRPIG)pig_likes.pig -p LIKES=100
	pig -f $(DIRPIG)pig_rts.pig -p RTS=20
	pig -f $(DIRPIG)pig_palabra.pig -p WORD="internet"

rm-logs:
	find . -name "*.log" -type f -delete

run-api:
	python $(DIRSRC)server/Server.py

run-client:
	python $(DIRSRC)client/Client.py

tests:
	nosetests --with-coverage --cover-html --cover-html-dir=src/server/test/results src/server