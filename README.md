# Dekla

## How to run a Docker container with Dekla ?

1. The first step is to build/run the Docker image using docker-compose

```
cd docker
./run.sh
```

2. Then from another terminal you need to execute a bash

```
docker-compose exec dekla /bin/bash
```
