A fun game.

#### Development Setup Instructions

I am going to be adding to this through the next few days.

1. `git clone https://github.com/elthran/UndyingKingdoms.git udk`

3. `cd udk`

2. `chmod +x bin/install.sh`

3. `bin/install.sh`

4. `source bin/activate` or `. bin/activate`

5. Edit the template_private_config.py and rename it private_config.py

6. `python manage.py reset_db` which incidentally creates the database if it doesn't exist.

7. `python manage.py serve`

This install script uses information from:
From https://github.com/PyMySQL/mysqlclient-python

