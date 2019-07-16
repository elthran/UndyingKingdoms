#!/bin/bash

echo "Build a zip of the dist folders (located in /tmp)?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

UDK="app"
zip -r /tmp/dist.zip $UDK/static/dist $UDK/templates/dist
