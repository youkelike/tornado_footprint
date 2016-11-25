
class Node(object):
    def __init__(self,val,left,right):
        self.val = val
        self.left = left
        self.right = right

def visit_post(node):
    if node.left:
        yield from visit_post(node.left)
    if node.right:
        yield from visit_post(node.right)
    yield node.val

if __name__ == '__main__':
    node = Node(-1,None,None)
    for val in range(100):
        node = Node(val,None,node)
    print(list(visit_post(node)))