HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh $HOST '
rm -r ~/UndyingKingdoms/undyingkingdoms/static/dist
rm -r ~/UndyingKingdoms/undyingkingdoms/templates/dist
exit
'

UDK="undyingkingdoms"
scp -rC $UDK/static/dist $HOST:~/UndyingKingdoms/$UDK/static
scp -rC $UDK/templates/dist $HOST:~/UndyingKingdoms/$UDK/templates

