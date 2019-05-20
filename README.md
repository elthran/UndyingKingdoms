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

Configure npm to install packages globally without root

Using npm installed from either the Ubuntu repositories or the Node.js repository requires running under root by default to install packages. This should be avoided, as per many articles around the web.

To get npm to install packages globally in your home folder (and add the folder to your PATH), you can use a simple script available here. This script does not work if you use NVM!

You can download the script and run it using these commands:

```
cd && wget https://raw.githubusercontent.com/glenpike/npm-g_nosudo/master/npm-g-nosudo.sh
chmod +x npm-g-nosudo.sh
./npm-g-nosudo.sh
```

After **following the instructions**, source your .bashrc file:

`source ~/.bashrc`

Now you will be able to install npm packages globally without root / sudo, like this:

`npm install -g <some package>`

From https://www.npmjs.com/package/n

To avoid requiring sudo for n and npm global installs, it is recommended you either install to your home directory using N_PREFIX, or take ownership of the system directories:

```
# make cache folder (if missing) and take ownership 
sudo mkdir -p /usr/local/n
sudo chown -R $(whoami) /usr/local/n
# take ownership of node install destination folders 
sudo chown -R $(whoami) /usr/local/bin /usr/local/lib /usr/local/include /usr/local/share
```

If Node.js version is incompatible with npm version

3. `npm install -g n`

3. If it npm say it only works with version 9, the do `n 9` and it will install the latest Node.js of 9.x.x.

5. `npm install vue`

4. `npm install -g @vue/cli`

3. `cd frontend` (if inside udk folder)

4. `npm install`

5. `npm run serve` should serve your app. `npm run build` builds it.

This uses information from https://stackoverflow.com/q/41159264
