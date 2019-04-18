ssh -t undyingkingdoms@ssh.pythonanywhere.com '
mysqldump --defaults-extra-file=~/.mysql/mysql.cnf > ~/dump.sql
exit
'
scp -rC $HOST:~/dump.sql .
sed -i 's/undyingkingdoms/undyingkingdoms$undyingkingdoms/3' dump.sql
mysql --defaults-extra-file=~/.mysql/mysql.cnf < dump.sql

