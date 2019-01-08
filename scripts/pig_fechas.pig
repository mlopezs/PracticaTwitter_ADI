/*************************************************/
-- Ejecutar con ~$ pig -f pig_fechas.pig
/*************************************************/

tweets = LOAD '/user/tweets-collect/tweets.txt' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

DUMP tweets;

-- STORE tweets INTO '/user/results' USING com.twitter.elephantbird.pig.load.LzoJsonStorage();
