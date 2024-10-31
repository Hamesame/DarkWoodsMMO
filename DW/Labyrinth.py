

class LabyrinthLocation:
    '''
        Class that represent the player location in a Labyrinth

        Parameters:
            start_location_name(str): name of the location to start
    '''
    def __init__(self, start_location_name):
        self.node_name = start_location_name
        self.target_node = ""
        self.altitude = 0
        self.progress = 0
        self.distance = 0


class LabyrinthNode:
    '''
        Class that represents a node in the Labyrinth

        Parameters:
            name(str): Name of the node

        The connections is a list of LabyrinthConnection objects,
        indicating the distance and name to respective nodes.

        The description is given later.
    '''
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.description = ""

class LabyrinthConnection:
    '''
        Class the represents a connection between two LabyrinthNode

        Parameters:
            distance(int): Number of minutes indicating the length of the path
            connection(str): Name of the target node
    '''
    def __init__(self, distance, connection):
        self.distance = distance
        self.connection = connection
