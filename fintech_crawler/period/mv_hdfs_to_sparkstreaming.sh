#!/bin/bash
minute=`date -d "5 minutes ago" +%Y-%m-%d_%H-%M`
path=`date -d "5 minutes ago" +%Y-%m-%d_%H`
echo $minute, $path
sleep 30
echo "/abc_crawler_data/${path}h/${minute}.json downloading"
hadoop fs -get "/abc_crawler_data/${path}h/${minute}.json" "/niub/szliu/hdfs_data"
hadoop fs -mv "/abc_crawler_data/${path}h/${minute}.json" "/abc_crawler_data/page_index"
rm -rf "/abc_crawler_data/${path}h/${minute}.json"
echo "/abc_crawler_data/${path}h/${minute}.json uploaded"