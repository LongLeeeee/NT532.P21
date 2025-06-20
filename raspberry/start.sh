#!/bin/bash
GPIO_CHIP="gpiochip0"
GPIO_LINE=6
started=0
while true; do
    state=$(gpioget $GPIO_CHIP $GPIO_LINE)

    if [ "$state" = "0" ]; then
        if [ $started -eq 0 ]; then
            echo "Start"
            bash /home/pi5/stream/stream.sh >> /home/pi5/stream/stream.log 2>&1 &
            STREAM_PID=$!
            sleep 0.5
            if ! ps -p $STREAM_PID > /dev/null; then
                echo "Failed to start stream.sh"
                continue
            fi
            python -u /home/pi5/client/client.py >> /home/pi5/client/client.log 2>&1 &
            CLIENT_PID=$!
            sleep 0.5
            if ! ps -p $CLIENT_PID > /dev/null; then
                echo "Failed to start client.py"
                continue
            fi
            echo $STREAM_PID > /tmp/stream.pid
            echo $CLIENT_PID > /tmp/client.pid
            started=1
            echo "Started!"
            sleep 1  
        else
            echo "Stop"
            kill $(cat /tmp/stream.pid)
            kill $(cat /tmp/client.pid)
            started=0
            echo "Stopped!"
            sleep 1 
        fi
    fi
    sleep 0.05
done
