DIRUTL := utils/
DIRCFG := config/
DIRDAT := data/
DIRDOC := docs/
DIRPIG := scripts/


all: hadoop flume pig-test

hadoop:
	./$(DIRUTL)start_hadoop_cluster.sh
	./$(DIRUTL)stop_hadoop_cluster.sh

flume: hadoop
	./$(DIRUTL)start_flume_collect.sh

pig-test:
	pig -f $(DIRPIG)pig_setup.pig -p PIG_HOME=$(PIG_HOME)
	pig -f $(DIRPIG)pig_likes.pig -p LIKES=100
	pig -f $(DIRPIG)pig_palabra.pig -p WORD="internet"
