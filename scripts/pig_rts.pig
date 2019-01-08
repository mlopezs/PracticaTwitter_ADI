/*************************************************/
-- ~$ pig -f pig_rts.pig -p RTS=<numero_retweets_max>
/*************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'retweet_count' > $RTS;

out = FOREACH filtered GENERATE json as tweet;

DUMP out;

-- STORE out INTO '/user/storage/sol_rts' USING PigStorage(',');

