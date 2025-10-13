# Jenkins

Jenkins is an open-source automation platform that allows you to build, test, and deploy software using pipelines. </br>
It's not just limited to creating pipeline for code, but can be used to automate any task. 

There're 2 main categories of Jenkins agents:
- **Permanent Agent:** think of this agent as a dedicated, reliable, and always-on worker bee for a specific type of task within your Jenkins ecosystem.
- **Cloud Agent:** this agent is ephemeral, on-demand workers that execute a CI/CD job and then disappear. 

There're 2 main build types:
- **Freestyle Build:** A Freestyle project is the simplest and most traditional type of Jenkins job. You configure everything by clicking around in the Jenkins web UI.
- **Pipelines:** A Pipeline is a modern and more robust way to define a CI/CD workflow as code. You write a script, called a Jenkinsfile, which is typically stored in your project's code repository. This file defines all the stages and steps of your entire delivery process, from building to deploying.

## Instalation

### Build the Jenkins BlueOcean Docker Image
```bash
docker build -t myjenkins-blueocean:2.528 .
```

### Create the network named "jenkins"
```bash
docker network create jenkins
```

You can check networks by
```bash
docker network ls
```

### Run the container
```bash
docker run \
    --name jenkins-blueocean \
    --restart=on-failure \
    --detach \
    --network jenkins \
    --env DOCKER_HOST=tcp://docker:2376 \
    --env DOCKER_CERT_PATH=/certs/client \
    --env DOCKER_TLS_VERIFY=1 \
    --publish 8080:8080 \
    --publish 50000:50000 \
    --volume jenkins-data:/var/jenkins_home \
    --volume jenkins-docker-certs:/certs/client:ro \
    myjenkins-blueocean:2.528
```
1. Specifies the Docker container name for this instance of the Docker image.
2. Always restart the container if it stops. If it is manually stopped, it is restarted only when Docker daemon restarts or the container itself is manually restarted.
3. Runs the current container in the background, known as "detached" mode, and outputs the container ID. If you do not specify this option, then the running Docker log for this container is displayed in the terminal window.
4. Connects this container to the jenkins network previously defined.
5. Specifies the environment variables used by docker, docker-compose, and other Docker tools.
6. This maps port 8080 on your host machine to port 8080 inside the container. This means you can access the Jenkins web UI by opening your web browser and going to http://localhost:8080.
7. This maps port 50000 on your host to port 50000 in the container. This is a special port used by Jenkins for communication with its worker nodes (agents). 
8. This creates a named volume called `jenkins-data` and mounts it to the `/var/jenkins_home` directory inside the container.
9. This mounts another named volume, `jenkins-docker-certs`, into the container's `/certs/client directory`. The `:ro` flag makes this volume read-only, meaning the container can't modify the certificates, which is a security best practice.
10. The name of the Docker image.

### Connect to the Jenkins
```
https://localhost:8080/
```

Get the password to unlock Jenkin
```bash
sudo docker exec jenkins-blueocean cat /var/jenkins_home/secrets/initialAdminPassword
```

### Connect to the Jenkins terminal
```bash
docker exec -it jenkins-blueocean bash
```

## Connect Jenkins container to the host socket

Since you're running the Jenkins as a container, the container can't reach docker host unix post.</br>
In order to resolve this, we have to run another container that can mediate between docker host and jenkins container. It will public docker host's unix port as its tcp port. 
```bash
docker run \
    -d --restart=always \
    -p 127.0.0.1:2376:2375 \
    --network jenkins \
    -v /var/run/docker.sock:/var/run/docker.sock \
    alpine/socat \
    tcp-listen:2375,fork,reuseaddr unix-connect:/var/run/docker.sock
```
To get the IP Address of the container:
```bash
docker inspect <NAMES> | grep IPAddress
```