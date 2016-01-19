#!/bin/bash

dir=`dirname $0`
dbname=us_congress
cd $dir

# download raw data and parse into loadfiles
loadandparse(){
    mkdir -p raw
    ./scripts/download.sh raw 2013 2014
    mkdir -p data
    ./scripts/parse-legislators.py
    ./scripts/parse-bills.py
    ./scripts/parse-votes.py
    ./scripts/key-votes.py
}

if [[ "$1" == "full" ]]; then
    dropdb $dbname
    createdb --locale=en_US.utf8 --encoding=UTF8 --template=template0 $dbname
    loadandparse
    psql -af sql/create.sql $dbname
    psql -af sql/load.sql $dbname
    #psql -af sql/common_votes.sql $dbname
    #psql -af sql/majority_vote.sql $dbname
elif [[ "$1" == "diff" ]]; then
    mkdir -p old
    cp -r data/ old/
    loadandparse
    files='states persons
            person_roles
            votes
            bills
            votes_re_bills
            votes_re_amendments
            votes_re_nominations
            person_votes
            leadership
            bills_subjects'
    touch update.sql
    for f in ${files}
    do
        echo '**** Diff-ing' $f '...'
        diff data/${f}.dat old/data/${f}.dat > diff.txt
        if [[ ! -s diff.txt ]]; then
            echo "\COPY $f FROM 'data/${f}.dat' WITH DELIMITER '|' NULL '' ENCODING 'UTF8'" >> update.sql
        fi
    done
    psql -af update.sql $dbname
    rm diff.txt
    rm update.sql
elif [[ "$1" == "dump" ]]; then
    pg_dump --no-owner --encoding=UTF8 $dbname | gzip - > "dumped_contents.sql.gz"
else 
    dropdb $dbname
    createdb --locale=en_US.utf8 --encoding=UTF8 --template=template0 $dbname
    gunzip --stdout "dumped_contents.sql.gz" | psql -f - $dbname
    exit 
fi
