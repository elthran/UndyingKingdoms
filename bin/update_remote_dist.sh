#!/bin/bash

echo "Do you wish to update the server dist files with your local files?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh $HOST '
rm -r ~/UndyingKingdoms/undyingkingdoms/static/dist
rm -r ~/UndyingKingdoms/undyingkingdoms/templates/dist
exit
'

UDK="undyingkingdoms"
scp -rC $UDK/static/dist $HOST:~/UndyingKingdoms/$UDK/static
scp -rC $UDK/templates/dist $HOST:~/UndyingKingdoms/$UDK/templates

