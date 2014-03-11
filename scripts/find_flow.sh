#!/bin/bash

if [ $# -lt 1 ]; then
	echo 'the flow name is need';
	exit 1;
fi

path=`dirname $0`
flow=$1

entry=`grep $flow $path/../flow_data/flow_index.txt`
if [ "$entry" == "" ]; then
	echo 'could not find the flow';
	exit 1;
fi

begin=`echo $entry | awk '{print $2}'`
end=`echo $entry | awk '{print $3}'`

sed -n "${begin},${end}p;d" $path/../flow_data/clean_flows.txt
