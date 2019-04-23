HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh -t $HOST '
mysqldump --defaults-extra-file=~/.mysql/mysql.cnf > ~/dump.sql
exit
'
scp -rC $HOST:~/dump.sql .
sed -i 's/`undyingkingdoms$undyingkingdoms`/`undyingkingdoms`/g' dump.sql
mysql --defaults-extra-file=~/.mysql/mysql.cnf < dump.sql

