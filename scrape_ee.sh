#!/bin/bash
SHELL=/bin/sh


export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

cd /
cd /newsbyte/current

source env/bin/activate

scrapy crawl news_ee -o "/var/www/vhosts/localhost.localdomain/m.newsbyte.org/current/storage/json/ee_2.json" -t json
