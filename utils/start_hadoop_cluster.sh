#!/bin/bash
#!/bin/bash

hdfs namenode -format
~/Programas/hadoop/sbin/start-yarn.sh && ~/Programas/hadoop/sbin/start-dfs.sh
~/Programas/hadoop/sbin/mr-jobhistory-daemon.sh start historyserver
jps
