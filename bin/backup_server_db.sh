#!/bin/bash

echo "Do you wish to backup the server and overwrite your local database?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

source bin/config.sh

ssh -t $HOST '
mysqldump --defaults-extra-file=~/.mysql/mysql.cnf > ~/dump.sql
exit
'
scp -rC $HOST:~/dump.sql .
sed -i 's/`undyingkingdoms$undyingkingdoms`/`undyingkingdoms`/g' dump.sql
mysql --defaults-extra-file=~/.mysql/mysql.cnf < dump.sql

