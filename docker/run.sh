source configure.sh

docker-compose -f ${COMPOSE_FILE} build dekla

docker-compose -f ${COMPOSE_FILE} up --remove-orphans
