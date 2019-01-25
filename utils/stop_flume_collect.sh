#!/bin/bash

name=$(jps | grep Application)

for i in $name; do
    if [[ $i != "Application" ]]; then
        echo "Process ${i} killed"
        kill $i 
    fi
done

