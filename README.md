# tdhwebscraper

## Prerequisites

- have Docker installed and running:
    - [macOS](https://docs.docker.com/docker-for-mac/install/)
    - [Windows 10](https://docs.docker.com/docker-for-windows/install/)
    - [CentOS](https://docs.docker.com/install/linux/docker-ce/centos/)
    - [Debian](https://docs.docker.com/install/linux/docker-ce/debian/)
    - [Fedorda](https://docs.docker.com/install/linux/docker-ce/fedora/)
    - [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- build the app:

```sh
# change change directories to this folder
cd ~/<REPO PATH>/tdhwebscraper/

# create a docker image with a helpful tag name
docker build --tag=tdhwebscraper .

```

## Running the app locally

```sh
docker run -p <LOCAL PORT>:80 tdhwebscraper
```

using `docker-compose`

```sh
# change change directories to this folder
cd ~/<REPO PATH>/tdhwebscraper/

docker-compose up
```
