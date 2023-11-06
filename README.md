# Robotic Intelligence Formula 1 Simulation

Subject: Cyber-pysical & Robotic Intelligent Systems 
Authors: Arturo Gascó Compte y Miguel Pardo Navarro 

## Installation and running instructions

Download the Docker image:

```shell
docker pull jderobot/robotics-academy:3.4.21
```

Launch container:

```shell
docker run --rm -it -p 7681:7681 -p 2303:2303 -p 1905:1905 -p 8765:8765 \
  -p 6080:6080 -p 1108:1108 -p 7163:7163 -p 7164:7164 \
  jderobot/robotics-academy:3.4.21
```
