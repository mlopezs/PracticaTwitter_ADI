/*************************************************/
-- Ejecutar con ~$ pig -f pig_palabra.pig -p PIG_HOME=$PIG_HOME -pWORD=<palabra>
/*************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'text' MATCHES '.*$WORD.*';

-- DUMP filtered;

out = FOREACH filtered GENERATE json#'text' AS texto;

DUMP out;

STORE out INTO '/user/filtrados' USING PigStorage(',');
