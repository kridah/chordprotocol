trap "kill 0" EXIT

python3 dummynode.py --port 5001 127.0.0.1:5002 127.0.0.1:5003 --die-after-seconds 120 &
python3 dummynode.py --port 5002 127.0.0.1:5001 127.0.0.1:5003 --die-after-seconds 120 &
python3 dummynode.py --port 5003 127.0.0.1:5001 127.0.0.1:5002 --die-after-seconds 120 &

#python3 client.py 127.0.0.1:5002 127.0.0.1:5003 127.0.0.1:5004 127.0.0.1:5005

wait