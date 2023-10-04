# Let's start by adding the necessary methods and functionalities for the Chord protocol

# Importing necessary libraries
import hashlib
import socket
# Adding to the existing code from dummynode.py

# Constants for Chord
M = 160  # Number of bits in the node ID space (using SHA-1)


class ChordNode:
    def __init__(self, address):
        ip, port = address.split(":")
        self.address = socket.gethostbyname(ip) + ":" + port
        self.id = self.hash_function(address)
        self.finger_table = [{"start": None, "node": ChordNode} for _ in range(M)]
        self.predecessor = None

    def hash_function(self, key):
        """Generate a unique ID for a given key using SHA-1 and return the integer value."""
        sha1 = hashlib.sha1()
        sha1.update(key.encode("utf-8"))
        return int(sha1.hexdigest(), 16) % (2 ** M)

    def initialize_finger_table(self, node):
        """Initialize the finger table of the current node."""
        self.finger_table[0]['node'] = node
        for i in range(0, M - 1):
            start = (self.id + 2 ** i) % (2 ** M)
            self.finger_table[i]['start'] = start

            # If start is between [self.id, self.finger_table[i]['node'].id)
            if self.is_id_in_range(start, self.id, self.finger_table[i]['node'].id, inclusive_end=False):
                self.finger_table[i + 1]['node'] = self.finger_table[i]['node']
            else:
                self.finger_table[i + 1]['node'] = node  # This will be the successor lookup
                self.update_finger_table(node, i)
        print(f"Finger table {self.finger_table[i]}")

    def update_others(self):
        for i in range(M):
            # Find the last node whose i-th finger might be the current node
            predecessor = self.find_predecessor(self.id - 2 ** i)
            predecessor.update_finger_table(self, i)

    def update_finger_table(self, node, i):
        if self.is_id_in_range(node.id, self.id, self.finger_table[i]['node'].id, inclusive_end=False):
            self.finger_table[i]['node'] = node
            p = self.predecessor
            p.update_finger_table(node, i)
            print("Updated finger table of node " + str(self.id) + " at index " + str(i) + " to " + str(node.id))

    def is_id_in_range(self, node_id, start, end, inclusive_end=False):
        if start <= end:
            return True
        if inclusive_end:
            if start < end:
                return start < node_id <= end
            else:
                return start < node_id or node_id <= end
        else:
            if start < end:
                return start < node_id < end
            else:
                return start < node_id or node_id < end

    def find_successor(self, identifier) -> 'ChordNode':
        if self.is_id_in_range(identifier, self.id, self.finger_table[0]['node'].id, inclusive_end=False):
            return self.finger_table[0]['node']
        else:
            node = self.closest_preceding_node(identifier)
            return node.find_successor(identifier)

    def find_predecessor(self, id):
        predecessor = self.find_predecessor(id)
        return predecessor.finger_table[0]['node']
    
    def closest_preceding_node(self, id):
        try:
            for i in range(M - 1, -1, -1):
                finger_node_id = self.finger_table[i]['node'].id
                if self.is_id_in_range(finger_node_id, self.id, id, inclusive_end=True):
                    return self.finger_table[i]['node']

        # Return the current node if no preceding node is found in the finger table
        except:
            print("No preceding node found in the finger table")

    #
    # def join(self, node):
    #     self.initialize_finger_table(node)
    #     self.update_others()

    def join(self, node_ip, node_port):
        '''
        Function responsible to join any new nodes to the chord ring it finds out the successor and the predecessor of the
        new incoming node in the ring and then it sends a send_keys request to its successor to recieve all the keys
        smaller than its id from its successor.
        '''
        data = 'join_request|' + str(self.id)
        succ = self.request_handler.send_message(node_ip, node_port, data)
        ip, port = self.get_ip_port(succ)
        self.successor = ChordNode(ip + port)
        self.finger_table.table[0][1] = self.successor
        self.predecessor = None

        if self.successor.id != self.id:
            data = self.request_handler.send_message(self.successor.ip, self.successor.port,
                                                     "send_keys|" + str(self.id))
            # print("data recieved" , data)
            for key_value in data.split(':'):
                if len(key_value) > 1:
                    # print(key_value.split('|'))
                    self.data_store.data[key_value.split('|')[0]] = key_value.split('|')[1]

    def stabilize(self):
        """Stabilization process to ensure the network remains consistent."""
        # Check the immediate successor's predecessor
        x = self.finger_table[0]['node'].predecessor
        if x and self.is_id_in_range(x.id, self.id, self.finger_table[0]['node'].id, inclusive_end=False):
            self.finger_table[0]['node'] = x
        # Notify the successor about the current node
        self.finger_table[0]['node'].notify(self)

    def notify(self, node):
        """Used during stabilization. If the current node doesn't have a predecessor,
        or the notifying node is closer to the current node than its current predecessor, 
        then update the predecessor."""
        if not self.predecessor or self.is_id_in_range(node.id, self.predecessor.id, self.id, inclusive_end=False):
            self.predecessor = node

    def check_predecessor(self):
        pass


# Now, we need to integrate ChordNode with the existing server functionality
# Let's start by creating a global ChordNode instance

chord_node = None  # This will be initialized when the server starts

# Next steps will be to integrate ChordNode's join, stabilization, and other methods with the existing server functions.
