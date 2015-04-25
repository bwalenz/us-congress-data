#!/bin/bash

mkdir -p $1
cd $1
wget -N http://www.govtrack.us/data/congress-legislators/legislators-current.yaml
wget -N http://www.govtrack.us/data/congress-legislators/legislators-historical.yaml

START_YEAR=${2-2013}
END_YEAR=${3-2014}

START_CONGRESS=0
END_CONGRESS=0

for year in `seq $START_YEAR $END_YEAR`
do
	echo '**** Fetching data for' $year '...'

	y=$year
	if [[ $(($y%2)) -eq 1 ]]; then
		(( y += 1 ))
	fi
	let session=`expr $y / 2 - 894`

	if [ $year -eq $START_YEAR ]; then
		START_CONGRESS=$session
	fi
	if [[ $year -eq $END_YEAR ]]; then
		END_CONGRESS=$session
	fi

	rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
    govtrack.us::govtrackdata/congress/$session/votes/$year/ votes-$year/
done

if [[ $START_CONGRESS -ne 0 && $END_CONGRESS -ne 0 ]]; then
	for session in `seq $START_CONGRESS $END_CONGRESS`
		do
			echo '**** Fetching data for' $session '-th congress...'
			rsync -avz --delete --delete-excluded --exclude **/text-versions/ \
    		govtrack.us::govtrackdata/congress/$session/bills/ bills-$session/
		done
fi
