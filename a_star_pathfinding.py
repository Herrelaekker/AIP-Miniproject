import math


class Node:
    def __init__(self, state=None, parent=None):
        self.state = state
        self.parent = parent
        self.hCost = 0
        self.gCost = 0
        self.fCost = 0

    def __eq__(self, other):
        return self.state == other.state


def a_star_search(initial_state, goal_state, obs, size):
    startNode = Node(initial_state, None)
    startNode.gCost, startNode.hCost, startNode.fCost = 0,0,0
    endNode = Node(goal_state, None)
    endNode.gCost, endNode.hCost, endNode.fCost = 0,0,0

    openSet = []
    closedSet = []

    openSet.append(startNode)

    while openSet:
        currentNode = openSet[0]

        for node in openSet:
            if node.fCost < currentNode.fCost:
                currentNode = node

        current_node = openSet[0]
        current_index = 0
        for index, item in enumerate(openSet):
            if item.fCost < current_node.fCost:
                current_node = item
                current_index = index

        closedSet.append(currentNode)
        openSet.pop(current_index)

        if currentNode == endNode:
            return construct_path(currentNode)

        for child in successors(currentNode, obs, size):
            if child in closedSet:
                continue

            child.gCost = currentNode.gCost +1
            child.hCost = math.sqrt((child.state[0] - endNode.state[0]) ** 2) + ((child.state[1] - endNode.state[1]) ** 2)
            child.fCost = child.gCost + child.hCost

            for node in openSet:
                if child == node and child.gCost > node.gCost:
                    continue
            openSet.append(child)

    return []


def successors(parent, obs, size):
    valid_successors = []
    actions = [(0,1), (0,-1), (1,0), (-1,0)]
    for action in actions:
        child_state = get_child_state(parent, action)
        if is_valid_state(child_state, obs, size):
            valid_successors.append(Node(child_state, parent))

    return valid_successors


def get_child_state(parent, action) -> ():
    child_state = (parent.state[0] + action[0], parent.state[1] + action[1])

    return child_state


def is_valid_state(child_state, obs, size) -> bool:
    if child_state[0] < 0 or child_state[1] < 0 or child_state[0] > size-1 or child_state[1] > size-1:
        return False

    for o in obs:
        if child_state == o:
            return False

    return True


def construct_path(current_node):
    state_path = []
    while current_node is not None:
        state_path.append(current_node.state)
        current_node = current_node.parent
    return state_path[::-1]


def search(initial_state, goal_state, obs, size):
    state_path = a_star_search(initial_state, goal_state, obs, size)
    return state_path


if __name__ == '__main__':
    obstacles = []
    search((0,0), (5,5), obstacles, 15)

