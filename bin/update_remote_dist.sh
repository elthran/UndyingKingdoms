#!/bin/bash

echo "Do you wish to update the server dist files with your local files?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

UDK="undyingkingdoms"
HOST="$UDK@ssh.pythonanywhere.com"
SSH_CONFIG="ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

rsync -avzr -e "$SSH_CONFIG" --progress \
  $UDK/static/dist $HOST:~/UndyingKingdoms/$UDK/static
rsync -avzr -e "$SSH_CONFIG" --progress \
  $UDK/templates/dist $HOST:~/UndyingKingdoms/$UDK/templates

ssh $HOST '
cd ~/UndyingKingdoms/undyingkingdoms
find static/dist/* -type f > static/dist/dist_files.txt
find templates/dist/* -type f >> static/dist/dist_files.txt
exit
'
