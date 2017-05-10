#!/bin/bash
SHELL=/bin/sh


export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

cd /
cd /newsbyte

source env/bin/activate

scrapy crawl news_sam -o "/var/www/vhosts/localhost.localdomain/m.newsbyte.org/storage/json/sam_2.json" -t json