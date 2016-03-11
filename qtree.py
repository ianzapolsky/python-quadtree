import math, sys

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx * dx + dy * dy)

class QTreeRect:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.nodes = []
        self.is_split = False

    def contains(self, node):
        if node.x >= self.x1 and node.x <= self.x2 and node.y >= self.y1 and node.y <= self.y2:
            return True
        return False

    # this will produce some false positives
    def intersects(self, target, radius):
        mid_x = self.x1 + ((self.x2 - self.x1) * .5)
        mid_y = self.y1 + ((self.y2 - self.y1) * .5)
        rect_rad = distance([self.x1, self.y1], [mid_x, mid_y])
        target_dist = distance([mid_x, mid_y], [target.x, target.y])

        if target_dist < (rect_rad + radius):
            return True
        return False

    def insert(self, new_node):
        if not self.is_split:
            #if len(self.nodes) == 0:
            if len(self.nodes) < 4:
                self.nodes.append(new_node)
            else:
                self.split()
                self.insert(new_node)
        else:
            for node in self.nodes:
                if node.contains(new_node):
                    node.insert(new_node)

    def split(self):
        new_width = (self.x2 - self.x1) * .5
        new_height = (self.y2 - self.y1) * .5
        children = self.nodes
        self.is_split = True
        self.nodes = []
        self.nodes.append(QTreeRect(self.x1, self.y1, self.x1+new_width, self.y1+new_height))
        self.nodes.append(QTreeRect(self.x1, self.y1+new_height, self.x1+new_width, self.y2))
        self.nodes.append(QTreeRect(self.x1+new_width, self.y1, self.x2, self.y1+new_height))
        self.nodes.append(QTreeRect(self.x1+new_width, self.y1+new_height, self.x2, self.y2))
        for child in children:
            for node in self.nodes:
                if node.contains(child):
                    node.insert(child)

    def find_closest_in_region(self, target):
        if not self.is_split:
            closest = None
            mindist = sys.maxint
            for node in self.nodes:
                dist = distance([node.x, node.y], [target.x, target.y])
                if dist < mindist:
                    mindist = dist
                    closest = node
            return closest
        else:
            for node in self.nodes:
                if node.contains(target):
                    return node.find_closest_in_region(target)

    def to_string(self):
        s = '[['+str(self.x1)+','+str(self.y1)+'],['+str(self.x2)+','+str(self.y2)+']] '
        for node in self.nodes:
            s += node.to_string()
        return s+'\n'


class QTreeNode:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def distance(self, node):
        dx = self.x - node.x
        dy = self.y - node.y
        return math.sqrt(dx * dx + dy * dy)

    def to_string(self):
        return '['+str(self.x)+','+str(self.y)+']'

class QTree:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = QTreeRect(0, 0, self.width, self.height)

    def insert(self, x, y, data=None):
        node = QTreeNode(x,y,data)
        self.root.insert(node)

    def to_string(self):
        return self.root.to_string()

    def find_closest_in_region(self, x, y):
        self.root.find_closest_in_region(QTreeNode(x,y))

    def find_closest(self, x, y, prev=None):
        closest = None
        target = QTreeNode(x=x,y=y)
        radius = sys.maxint
        if prev:
            radius = distance([prev.x, prev.y], [target.x, target.y])
        stack = [self.root]

        while len(stack) > 0:
            node = stack.pop()
            if node.is_split:
                for nnode in node.nodes:
                    if nnode.intersects(target, radius):
                        stack.append(nnode)
            else:
                if node.intersects(target, radius):
                    for nnode in node.nodes:
                        dist = distance([nnode.x, nnode.y], [target.x, target.y])
                        if dist <= radius:
                            radius = dist
                            closest = nnode
        return closest
