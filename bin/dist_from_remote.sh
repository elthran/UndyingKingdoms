HOST="undyingkingdoms@ssh.pythonanywhere.com"
UDK="undyingkingdoms"

rm -r $UDK/static/dist
rm -r $UDK/templates/dist

scp -rC $HOST:~/UndyingKingdoms/$UDK/static/dist $UDK/static
scp -rC $HOST:~/UndyingKingdoms/$UDK/templates/dist $UDK/templates
