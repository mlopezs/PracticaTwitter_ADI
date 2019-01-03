/*************************************************/
-- Ejecutar con ~$ pig -f pig_fechas.pig -param PIG_HOME=$PIG_HOME
/*************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

DUMP tweets;

-- STORE tweets INTO '/user/results' USING com.twitter.elephantbird.pig.load.LzoJsonStorage();
