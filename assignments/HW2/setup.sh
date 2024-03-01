
# This line uninstall thrid-party docker distribution
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# This section will setup APT distros that are required for docker environment
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# This section will install the more official version of Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# This Line is to test if Docker is setup correctly
sudo docker run hello-world

# Pull Original Ubuntu 20.04 Image From Docker Hub
sudo docker pull amd64/ubuntu:20.04

cd functions
faas-cli build -f ./andy-boto-9.yml
faas-cli push -f ./andy-boto-9.yml
faas-cli deploy -f ./andy-boto-9.yml
<<com
sudo docker container prune --force
# Run the base image with a given container name
sudo docker run --name csen241-hw1-container -it -d --rm amd64/ubuntu:20.04
# Update and setup Docker Environment for testing
sudo docker exec -it csen241-hw1-container sh -c "apt update && apt upgrade -y"
sudo docker exec -it csen241-hw1-container sh -c "apt install git sysbench -y"

# Save update to a Docker Image
sudo docker ps
sudo docker commit csen241-hw1-container csen241-hw1-practice

# Check and run Docker Image we just created
sudo docker images
sudo docker container rm csen241-hw1-container --force
sudo docker run -it csen241-hw1-practice
com
