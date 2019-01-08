/*************************************************/
-- Ejecutar con ~$ pig -f pig_palabra.pig -p LIKES=<numero_likes_minimo>
/*************************************************/

tweets = LOAD '/user/tweets-collect/tweets.txt' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'favorite_count' < $LIKES;

out = FOREACH filtered GENERATE json as tweet;

DUMP out;

STORE out INTO '/user/filtrados' USING PigStorage(',');

