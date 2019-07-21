#!/bin/bash

echo "Do you wish to reset the the age (wipe all most tables)?"
echo "Type a number then press enter."
select yn in "Yes" "No"; do
	case $yn in
	    Yes ) break;;
	    No ) exit;;
	esac
done

python3.6 - <<-'EOF'
print("Running ...")
from app import app
from app.models.exports import World
app.app_context().push()
world = World.query.first()
world.advance_age()
EOF
