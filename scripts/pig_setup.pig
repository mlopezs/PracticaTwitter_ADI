/*************************************************/
-- Ejecutar con ~$ pig -f pig_setup.pig -param PIG_HOME=$PIG_HOME
/*************************************************/

REGISTER $PIG_HOME/lib/elephant-bird-hadoop-compat-4.15.jar
REGISTER $PIG_HOME/lib/elephant-bird-pig-4.15.jar
REGISTER $PIG_HOME/lib/json-simple-1.1.jar