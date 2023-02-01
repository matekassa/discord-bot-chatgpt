#!/bin/bash

start() {
    if [[ $(isrunning) == "false" ]]
    then
        echo "Bot starting"
        python3 "$(pwd)"/bot.py &
    else
        echo "Bot is already running"
    fi
}

stop() {
    process_id_bot=$(ps -ef | grep 'bot.py' | grep -v grep | awk '{print $2}')
    if [[ $(isrunning) == "true" ]]
    then
        sudo kill -15 "$process_id_bot"
    elif [[ $(isrunning) == "false" ]]
    then
        echo "Bot is not running"
    fi
}

isrunning() {
    process=$(ps -ef | grep 'bot.py' | grep -v grep | awk '{print $2}')
    running=""
    if [[ -z "$process" ]];
    then
        running="false"
    else
        running="true"
    fi
    echo "$running"
}

main() {
    if [[ -z "$1" ]]
    then
        echo "Please give an argument (start or stop)"
    elif [[ -z "$2" ]]
    then
        if [[ "$1" == "start" ]]
        then
            start
        elif [[ "$1" == "stop" ]]
        then
            stop
        elif [[ "$1" == "status" ]]
        then
            if [[ $(isrunning) == "true" ]]
            then
		process_id=$(ps -ef | grep 'bot.py' | grep -v grep | awk '{print $2}')
		echo "Bot is running (PID: $process_id)"
            elif [[ $(isrunning) == "false" ]]
            then
                echo "Bot is not running"
            fi
        else
            echo "Not valid argument (valid arguments are only: start or stop)"
        fi
    else
        echo "Too many arguments given"
    fi
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]
then
    main "$@"
fi
