# run on cluster

## WORK IN PROGRESS ##
## ssh c2-1 python3 -u $PWD/dummynode.py
# ssh computenode python script --port n neighborIP:port
ssh -f c7-14 python3 $PWD/dummynode.py --port 5001
ssh -f c3-26 python3 $PWD/dummynode.py --port 5002
#c1-0
#c7-11
#c7-18
#c2-15
#c6-1
#c7-29
#c5-5
#c2-51
#c2-6
#c3-10
#c2-52
#c2-5
#c2-42
#c3-35
#c2-13

# Run the client:
# python3 client.py ip-of-a-node:port
# python3 client.py 172.21.21.187:5001