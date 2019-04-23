#!/bin/bash

echo "Do you wish to update your local dist files with files from the server?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done


HOST="undyingkingdoms@ssh.pythonanywhere.com"
UDK="undyingkingdoms"

rm -r $UDK/static/dist
rm -r $UDK/templates/dist

scp -rC $HOST:~/UndyingKingdoms/$UDK/static/dist $UDK/static
scp -rC $HOST:~/UndyingKingdoms/$UDK/templates/dist $UDK/templates
