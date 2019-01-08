#!/bin/bash

hdfs dfs -mkdir -p /user/tweets-collect
flume-ng agent -n TwitterAgent -f config/flume.conf
