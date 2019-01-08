/****************************************************/
-- ~$ pig -f pig_palabra.pig -p WORD=<palabra>
/****************************************************/

tweets = LOAD '/user/tweets-collect/' USING com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') AS (json:map[]);

filtered = FILTER tweets BY json#'text' MATCHES '.*$WORD.*';

out = FOREACH filtered GENERATE json AS tweet;

DUMP out;

-- STORE out INTO '/user/storage/sol_palabra' USING PigStorage(',');
