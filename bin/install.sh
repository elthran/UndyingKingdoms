#!/usr/bin/env bash
# Install all necessary things to develop this app.
# This script uses sudo only where absolutely necessary.
set -e

# Set the current directly so that all paths are consistent.
move_to_base() {
	parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P )
	cd "$parent_path/.."  # make sure you are in the udk directory
}

# generate a random password, default is 32 chars
# alterante usage is `randpw 16` (or whatever)
randpw() {
	< /dev/urandom tr -dc "[:alnum:]" | head -c${1:-${1-32}}; echo;
}

# Give all install scripts execute permissions.
# run this in bin/install.sh
# NOT CURRENTLY IN USE
install_docker() {
	curl -fsSL get.docker.com -o /tmp/get-docker.sh && sh /tmp/get-docker.sh
	sudo docker run hello-world
	sudo -k
	cat <<- EOF
	If you want to run docker without root use:
	sudo usermod -aG docker $USER
	Use: 'id -Gn' to check if you are part of the docker group.
	Then re-login or reboot your machine.
	EOF
}

install_apt_modules() {
	echo "Installing requisite apt modules ..."
	sudo apt update
	sudo apt install python3 python3-venv python3-dev libmysqlclient-dev mysql-server build-essential bc -y
	sudo -k
}

check_python3_version() {
	echo "Checking python3 version ..."
	version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
	parsedVersion=$(echo "0.${version//./}")
if (( $(echo "$parsedVersion < 0.36" | bc -l) )); then
	   echo "Requires python>=3.6"; exit 1
	else
	 echo "Python3 version is new enough."
	fi
}


setup_virtual_environment() {
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
}

install_app_into_virtual_environment() {
	# Old: install from setup.py
	# pip install .
	pip install -r requirements.txt
}

build_mysql_config() {
	mysql_cnf=~/.udk_mysql_config.cnf
	rm -rf $mysql_cnf
	echo "
	[client]
	user = ${2-root}
	password = ${1}
	# Before use set file to read-only with \$ chmod 400 $mysql_cnf
	" > $mysql_cnf
	chmod 400 $mysql_cnf
}

# NOTE: you can only have 1 tab, after that uses spaces.
get_set_mysql_root_password() {
	echo "Enter your MYSQL root password"
	read -s -p "(or a new root password if you are just setting up MYSQL): " mysql_passwd
	echo
	build_mysql_config $mysql_passwd
	while ! sudo mysql --defaults-file=$mysql_cnf -e ";" ; do
	    read -s -p "Can't connect, please retry: " mysql_passwd
	    echo
	    build_mysql_config $mysql_passwd
	done
	sudo mysql --defaults-file=$mysql_cnf -e \
	    "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$mysql_passwd';"
	sudo -k
	echo "MYSQL credentials estabished, continuing ..."
}

set_udk_user_grants() {
	udk_user="elthran"
	udk_db="undyingkingdoms"
	udk_mysql_passwd=$(randpw 16)
	mysql --defaults-file=$mysql_cnf -e "DROP USER IF EXISTS '$udk_user'@'localhost';"
	mysql --defaults-file=$mysql_cnf -e "CREATE USER '$udk_user'@'localhost' IDENTIFIED BY '$udk_mysql_passwd';"
	# This will create the user if they don't exist.
	mysql --defaults-file=$mysql_cnf -e "GRANT ALL ON $udk_db.* TO '$udk_user'@'localhost' WITH GRANT OPTION;"
	mysql --defaults-file=$mysql_cnf -e "GRANT ALL ON ${udk_db}_test.* TO '$udk_user'@'localhost' WITH GRANT OPTION;"
	build_mysql_config "$udk_mysql_passwd" "$udk_user"
	chmod 400 $mysql_cnf
	echo "Added new user with access to UDK tables."
}

generate_private_config() {
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
	echo "Private app config generated."
}

# NOTE: to server app from inside vagrant I need to use
# python manage.py serve -h 0.0.0.0
# NOTE: I need to update the dist files!
# chmod +x bin/dist_from_remote.sh
# bin/dist_from_remote.sh
# But this is bad! as it requires access to the pythonanywhere server :P

install() {
	move_to_base
	# install_docker
	install_apt_modules
	check_python3_version
	setup_virtual_environment
	install_app_into_virtual_environment
	get_set_mysql_root_password
	set_udk_user_grants
	generate_private_config
	echo "Undyking Kingdoms back-end development environment installed."
}

# run the actual install script
install
