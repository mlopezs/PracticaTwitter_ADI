/*************************************************/
-- ~$ pig -f pig_rts.pig -p PIG_HOME=$PIG_HOME -p RTS=<numero_retweets_max>
/*************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'retweeted_status'#'retweet_count' > $RTS;

out = FOREACH filtered GENERATE json#'retweeted_status'#'user'#'name' AS name, json#'retweeted_status'#'user'#'screen_name' AS user, json#'retweeted_status'#'text' as tweet, json#'retweeted_status'#'retweet_count' as rts, json#'retweeted_status'#'favorite_count' as mgs;

STORE out INTO '/user/storage/sol_rts.json' USING JsonStorage();

fs -rm /user/storage/sol_rts.json/.pig_schema
fs -getmerge /user/storage/sol_rts.json/ data/results/sol_rts.txt

fs -rm -r /user/storage/sol_rts.json

