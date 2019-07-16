#!/bin/bash

echo "Do you wish to update your local dist files with files from the server?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

source ./config.sh

rsync -avzr -e "$SSH_CONFIG" --progress \
  $HOST:~/UndyingKingdoms/$UDK/static/dist $UDK/static
rsync -avzr -e "$SSH_CONFIG" --progress \
  $HOST:~/UndyingKingdoms/$UDK/templates/dist $UDK/templates
