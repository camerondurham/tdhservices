# tdaservices

## Prerequisites

- Have Docker installed and running:
    - [macOS](https://docs.docker.com/docker-for-mac/install/)
    - [Windows 10](https://docs.docker.com/docker-for-windows/install/)
    - [CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)
    - [Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
    - [Fedorda](https://docs.docker.com/install/linux/docker-ce/fedora/)
    - [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

## tdhwebscraper

### Build and Run

```sh
# change change directories to this folder
cd ~/<REPO PATH>/tdhwebscraper/

# create a docker image with a helpful tag name
docker build --tag=tdhwebscraper .

# expose the container's port 4000 to some <LOCAL PORT>
docker run -p <LOCAL PORT>:4000 tdhwebscraper
```

_example_:

```sh
cd ~/projects/tdhbackend/tdhwebscraper
docker build --tag=tdhwebscraper .
docker run -p 4000:4000
```

### Build and Run with `docker-compose`

**Warning: still debugging**, may not work yet!

```sh
# change change directories to this folder
cd ~/<REPO PATH>/tdhwebscraper/

docker-compose up
```

_example_:

```sh
cd ~/projects/tdhbackend/tdhwebscraper
docker build --tag=tdhwebscraper .
docker run -p 4000:4000
```
