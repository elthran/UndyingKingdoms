#!/bin/bash

echo "Do you wish to update the server TEMP dist files with your local files?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

HOST="undyingkingdoms@ssh.pythonanywhere.com"
ssh $HOST '
rm -r ~/tmp/static/dist
rm -r ~/tmp/templates/dist
exit
'

UDK="undyingkingdoms"
scp -rC $UDK/static/dist $HOST:~/tmp/static
scp -rC $UDK/templates/dist $HOST:~/tmp/templates

