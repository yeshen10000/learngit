#!bin/bash
sudo ps -ef | grep pyspider| grep -v grep| awk '{print "sudo kill -9 "$2}' | sh