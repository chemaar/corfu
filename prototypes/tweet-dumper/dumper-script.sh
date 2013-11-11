#!/bin/bash
echo "Reading words file " $1
while read line
do
    echo "Creating dir for $line"
    mkdir "$line"
    nohup ruby mydumper2.rb "$line" &
done < $1
