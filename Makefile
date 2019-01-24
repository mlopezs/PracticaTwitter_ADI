DIRSRC := src/
DIRUTL := utils/
DIRCFG := config/
DIRDAT := data/
DIRDOC := docs/
DIRPIG := scripts/

IMAGNAME 	= twitter_scavenger
CONTNAME 	= practicaADI

DOCK   := docker
BUILD  := build
RUN    := App
STOP   := stop
DEL	   := rm

BFLAGS := . -t $(IMAGNAME)
RFLAGS := --name $(CONTNAME) -i -p 8080:8080 -t $(IMAGNAME)

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
	python $(DIRSRC)server/Server.py

virtualize: run-image stop-image delete-image

run-image:
	$(DOCK) $(RUN) $(RFLAGS)

build-image:
	$(DOCK) $(BUILD) $(BFLAGS)

stop-image:
	$(DOCK) $(STOP) $(CONTNAME)

delete-image: 
	$(DOCK) $(DEL) $(CONTNAME)

tests:
	nosetests --with-coverage --cover-html --cover-html-dir=src/server/test/html src/server