#!/bin/bash

dir=`dirname $0`
dbname=us_congress
cd $dir

if [[ "$1" == "full" ]]; then
    dropdb $dbname
    createdb --locale=en_US.utf8 --encoding=UTF8 --template=template0 $dbname
    mkdir -p raw
    ./scripts/download.sh raw 2013 2014
    mkdir -p data
    ./scripts/parse-legislators.py
    ./scripts/parse-bills.py
    ./scripts/parse-votes.py
    ./scripts/key-votes.py
    psql -af sql/create.sql $dbname
    psql -af sql/load.sql $dbname
    #psql -af sql/common_votes.sql $dbname
    #psql -af sql/majority_vote.sql $dbname
elif [[ "$1" == "dump" ]]; then
    pg_dump --no-owner --encoding=UTF8 $dbname | gzip - > "dumped_contents.sql.gz"
else 
    dropdb $dbname
    createdb --locale=en_US.utf8 --encoding=UTF8 --template=template0 $dbname
    gunzip --stdout "dumped_contents.sql.gz" | psql -f - $dbname
    exit 
fi
