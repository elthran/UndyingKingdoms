#!/usr/bin/env bash
# install all necessary things to develop this app.

# This script uses sudo only where absolutely necessary.
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path/.."  # make sure you are in the udk directory
randpw() { < /dev/urandom tr -dc "[:alnum:]" | head -c${1:-${1-32}};echo; }

# install modules
echo "Installing requisite apt modules ..."
sudo apt-get update
sudo apt install python3 python3-venv python3-dev libmysqlclient-dev mysql-server build-essential
sudo -k

# assert python3 version >=3.6
echo "Checking python3 version ..."
version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
parsedVersion=$(expr ${version//./} \* 10)
if (( $parsedVersion < 3600 )); then
    echo "Requires python>=3.6"; exit 1
else
  echo "Python3 version is new enough."
fi

# setup virtual environment
rm -rf ~/virtual_envs/udk_env
python3 -m venv ~/virtual_envs/udk_env
rm -f bin/activate
ln -s ~/virtual_envs/udk_env/bin/activate bin/activate
# allow activate script to auto start mysql
echo "
# Inject mysql startup into environment activation
sudo /etc/init.d/mysql start
sudo -k
" >> bin/activate
. bin/activate
pip install -U pip
echo "Pip activated\n: $( pip --version )"

# install app
pip install .
deactivate
exit 1
# Install mysql stuff
# Add new user with access to UDK tables.
echo "Enter your mysql root password"
read -s -p "(or a new password if you are just setting up mysql): " mysql_passwd

mysql_cnf=~/.udk_mysql_config.cnf
rm -rf $mysql_cnf
echo "
[client]
user = root
password = $mysql_passwd
# Before use set file to read-only with \$ chmod 400 $mysql_cnf
" > $mysql_cnf
chmod 400 $mysql_cnf
echo "Enter your sudo password to gain access up mysql."
sudo mysql --defaults-file=$mysql_cnf -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$mysql_passwd';"
sudo -k

udk_user="elthran"
udk_db="undyingkingdoms"
udk_mysql_passwd=$(randpw 16)
mysql --defaults-file=$mysql_cnf -e "CREATE USER '$udk_user'@'localhost'IDENTIFIED BY '$udk_mysql_passwd';" \
    || mysql --defaults-file=$mysql_cnf -e "ALTER USER '$udk_user'@'localhost'IDENTIFIED BY '$udk_mysql_passwd';"
mysql --defaults-file=$mysql_cnf -e "GRANT ALL ON $udk_db.* TO '$udk_user'@'localhost' WITH GRANT OPTION;"
mysql --defaults-file=$mysql_cnf -e "GRANT ALL ON ${udk_db}_test.* TO '$udk_user'@'localhost' WITH GRANT OPTION;"
chmod 600 $mysql_cnf
sed -i 's/root/'${udk_user}'/g' $mysql_cnf
sed -i '/password/ c\password = '${udk_mysql_passwd} $mysql_cnf
chmod 400 $mysql_cnf

config=private_config.py
config_bak=private_config.py.bak
template_config=template_private_config.py
if [[ -e $config && ! -e $config_bak ]]; then
  mv $config $config_bak
fi
yes | cp -rf $template_config $config
sed -i 's/db_passwd/'$udk_mysql_passwd'/g' $config
sed -i 's/complex_pass/'$(randpw 64)'/g' $config
sed -i 's/complex_pass2/'$(randpw 64)'/g' $config
sed -i 's/complex_pass3/'$(randpw 64)'/g' $config
