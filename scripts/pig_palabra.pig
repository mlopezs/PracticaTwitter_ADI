/****************************************************/
-- ~$ pig -f pig_palabra.pig -p PIG_HOME=$PIG_HOME -p WORD=<palabra>
/****************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'text' MATCHES '.* $WORD .*';

out = FOREACH filtered GENERATE json#'user'#'name' AS name, json#'user'#'screen_name' AS user, json#'text' AS tweet, json#'retweet_count' as rts, json#'favorite_count' as mgs;

STORE out INTO '/user/storage/sol_palabra.json' USING JsonStorage();
