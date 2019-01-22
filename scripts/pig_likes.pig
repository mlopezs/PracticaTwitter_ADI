/*****************************************************************/
-- ~$ pig -f pig_likes.pig -p PIG_HOME=$PIG_HOME -p LIKES=<numero_likes_minimo>
/*****************************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'favorite_count' < $LIKES;

out = FOREACH filtered GENERATE json#'user'#'name' AS name, json#'user'#'screen_name' AS user, json#'tweet' as tweet, json#'retweet_count' as rts, json#'favorite_count' as mgs;

STORE out INTO '/user/storage/sol_mgs.json' USING JsonStorage();

fs -rm /user/storage/sol_mgs.json/.pig_schema
fs -getmerge /user/storage/sol_mgs.json/ data/results/sol_mgs.txt

fs -rm -r /user/storage/sol_mgs.json