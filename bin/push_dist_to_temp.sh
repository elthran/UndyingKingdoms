#!/bin/bash

echo "Do you wish to update the server TEMP dist files with your local files?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

source bin/config.sh

rsync -avzr -e "$SSH_CONFIG" --progress \
  $UDK/static/dist $HOST:~/tmp/static
rsync -avzr -e "$SSH_CONFIG" --progress \
  $UDK/templates/dist $HOST:~/tmp/templates
