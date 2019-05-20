A fun game.

#### Development Setup Instructions

I am going to be adding to this through the next few days.

1. `git clone https://github.com/elthran/UndyingKingdoms.git udk`

3. `cd udk`

2. `chmod +x bin/install.sh`

3. `bin/install.sh`

4. `source bin/activate` or `. bin/activate`

5. `python manage.py reset_db` which incidentally creates the database if it doesn't exist.

6. `python manage.py serve`

This install script uses information from:
From https://github.com/PyMySQL/mysqlclient-python

#### Front-end Development instructions.

1. `sudo apt install npm`

From https://www.linuxuprising.com/2018/04/how-to-install-and-configure-nodejs-and.html

From https://www.npmjs.com/package/n

If Node.js version is incompatible with npm version

3. `npm install -g n`

3. If it npm say it only works with version 9, the do `n 9` and it will install the latest Node.js of 9.x.x.

5. `npm install vue`

4. `npm install -g @vue/cli`

From https://stackoverflow.com/q/41159264

3. `cd frontend` (if inside udk folder)

4. `npm install`

This uses information from https://stackoverflow.com/q/41159264
