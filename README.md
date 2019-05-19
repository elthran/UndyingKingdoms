A fun game.

#### Development Setup Instructions 

**NOTE: THESE WILL NOT WORK YET, as I'm having some trouble installing all the correct python packages in my container and my internet is to slow to upload the images :P**

I am going to be adding to this through the next few days.

1. Install docker with `sudo apt install docker.io`

From https://linuxconfig.org/how-to-install-docker-on-ubuntu-18-04-bionic-beaver

2. The following linux commands will start Docker and ensure that starts after the reboot:
    > $ sudo systemctl start docker
    
    > $ sudo systemctl enable docker

    All done.

    > $ docker --version
    
    > Docker version 17.03.2-ce, build f5ec1e2

From https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04

3. If you want to avoid typing sudo whenever you run the docker command, add your username to the docker group:

    > sudo usermod -aG docker ${USER}
    
    Then restart your computer.

From https://docker-curriculum.com/

4. `docker run -d -p 8888:5000 --name undykingkingdoms klondikemarlen/undykingkindoms`

Useful docker commands:

Docker cleanup: $`docker container prune`

Run interactive terminal: $`docker run -it <container-name> sh`
