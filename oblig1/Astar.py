import math

import Map

"""
Implementation of a grid based A-star algorithm
"""


class Node:
    """
    Node is a position on the grid, with corresponding children / neighbours and parent
    """
    def __init__(self, coordinates=None, parent=None):
        """
        :param coordinates: x, y coordinates for Node on the grid
        """
        # Initially we do not want a specific node to have a parent node
        self.parent = parent
        self.coordinates = coordinates
        self.children = []
        self.weight = 0
        self.cost = 0

    def get_f(self):
        return self.cost + self.h

    def __eq__(self, other):
        # a node is equal to another if and only if their coordinates match
        return self.coordinates == other.coordinates

    def __gt__(self, other):
        # the estiamted cost determines the sorting order in the queue
        return self.cost > other.cost

    def define_children(self, map):
        """
        Since we have a grid based map, we can define a nodes children (neighbours) as adjacent cells in grid
        :param map: defines the task to be solved
        :return:
        """
        up, down, left, right = \
            [self.coordinates[0], self.coordinates[1]+1], \
            [self.coordinates[0], self.coordinates[1]-1], \
            [self.coordinates[0]-1, self.coordinates[1]], \
            [self.coordinates[0]+1, self.coordinates[1]],

        children = []
        for direction in up, down, left, right:
            # need to try catch as the index may be out of bounds
            try:
                x = map.get_cell_value(direction)
                if x >= 0:
                    children.append(Node(direction))
            except IndexError:
                continue
        self.children = children


def est_dist(current, end):
    """
    calculates the estimated distance (aerial distance) between current and end nodes
    :param current: coordinates of current node
    :param end: coordinates of goal
    :return: distance
    """
    # the absolute value may be used on such a simple example, but may not be very applicable on more complicated tasks
    # return abs(current[0]-end[0])+abs(current[1]-end[1])

    # the euclidian distance may be a more scalable option, but is substantially slower
    x = current[0]-end[0]
    y = current[1]-end[1]
    return math.sqrt(x*x + y*y)


def calc_cost(current, to, end, map):
    """
    calculating the cost for the current node, we need to use the weighted path to next node
    the total cost will den be the estimated distance to the end coordinates
    :param current: current node
    :param to: node to check
    :param end: target node
    :param map: task
    :return: cost
    """
    current.parent = to
    current.weight = to.weight + map.get_cell_value(current.coordinates)
    return current.weight + est_dist(current.coordinates, end.coordinates)


def improve_path(current, end, map):
    """
    improves the path if possible
    :param current: current node
    :param end: goal node
    :param map: task
    :return:
    """
    for x in current.children:
        # updates the cost if the current weight and cell value of child is less than the childs weight
        if current.weight + map.get_cell_value(x.coordinates) < x.weight:
            x.parent = current
            x.cost = calc_cost(x, current, end, map)
            improve_path(x, end, map)


def a_star(map):
    """
    Astar algorith using estimated distance
    :param start:
    :param end:
    :return:
    """
    n = Node(map.get_start_pos())  # starting node
    end = Node(map.get_goal_pos()) # goal node
    checked = []  # at the start no nodes are checked
    queue = [n]  # a queue is initialized with the starting node
    while not n.__eq__(end):
        if not queue:
            return "failed"
        n = queue.pop()  # pops top element of queue
        checked.append(n)  # appends the popped node to checked list
        if n.__eq__(end):  # if the current node is equal to the end node, we return
            return n
        n.define_children(map)
        for child in n.children:
            current = child
            for c in checked:
                if c.__eq__(child):  # checks if any children are in checked, then sets current and break
                    current = c
                    break

            if current not in checked:
                current.cost = calc_cost(current, n, end, map)
                queue.append(current)  # appends the current to the queue
                # Sort the list by the total cost defined by overridden __gt__
                queue.sort(reverse=True)
            elif n.weight + map.get_cell_value(current.coordinates) < current.weight:
                current.cost = calc_cost(current, n, end, map)  # sets the currents cost
                if current in checked:
                    improve_path(current, end, map)  # improves path if current is checked


def backtrack(current, map):
    """
    method to backtrack, drawing the map to show
    :param current: current node
    :param map: task
    """
    x = current
    while x.parent is not None:
        map.set_cell_value(x.coordinates, 5)
        x = x.parent
    map.show_map()


def main(task):
    """
    :param tasl_ task number
    """
    map = Map.Map_Obj(task=task)
    x = a_star(map)
    try:
        backtrack(x, map)
    except AttributeError:
        print("Failed")


main(4)
