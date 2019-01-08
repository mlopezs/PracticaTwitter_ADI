/*****************************************************************/
-- ~$ pig -f pig_likes.pig -p LIKES=<numero_likes_minimo>
/*****************************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'favorite_count' < $LIKES;

out = FOREACH filtered GENERATE json as tweet;

DUMP out;

--STORE out INTO '/user/storage/sol_likes' USING PigStorage(',');

