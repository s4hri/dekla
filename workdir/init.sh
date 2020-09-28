#!/bin/bash

#        Based on: xpy-chicken-docker
#                  by Davide De Tommaso, Marwen Belkaid
#        
#        Social cognition in human-robot interaction (S4HRI)
#        Istituto Italiano di Tecnologia (IIT)

env_robot()
{
export PATH=${PATH}:/home/docky/apps
export PYTHONPATH=${PYTHONPATH}:/home/docky/modules

ssh-keygen -t rsa
ssh-copy-id icub@pc104

yarpserver --write &
sleep 2
ssh -f icub@pc104 'yarprun --server /pc104 --log &'
yarprun --server /icubsrv --log &

yarpmanager --application /home/docky/apps/applications/icub-attcap.xml --from /home/docky/apps/cluster-config.xml

ssh icub@pc104 "kill -9 \$(ps -aux | grep yarprun | awk '{print \$2}')"
}

env_sim()
{
export PATH=${PATH}:/home/docky/apps
export PYTHONPATH=${PYTHONPATH}:/home/docky/modules
yarpserver --write &
sleep 2
yarprun --server /icubsrv --log &

yarpmanager --application /home/docky/apps/applications/icub-sim-attcap.xml --from /home/docky/apps/cluster-config.xml
}

clear
PS3='Please enter your choice: '
options=("Run robot environment" "Run simulation environment" "Shell" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Run robot environment")
            env_robot
            exit
            ;;
        "Run simulation environment")
            env_sim
            exit
            ;;
        "Shell")
            /bin/bash
            exit
            ;;

        "Quit")
            exit
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
