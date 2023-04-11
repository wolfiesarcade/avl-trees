def AVLBST_validator(node, min_value=None, max_value=None):
    # preorder traversal
    if not node:
        return True

    if (min_value and node.value < min_value) or (max_value and node.value > max_value) or abs(getBalanceFactor(node)) > 1:
         return False
     
    left = AVLBST_validator(node.left, min_value, max_value=node.value)
    right = AVLBST_validator(node.right, min_value=node.value, max_value=max_value)
    
    return left and right

def getHeight(node):
    ''' Return 0 if node does not exist, otherwise return node.height '''
    if node:
        return node.height
    else:
        return 0

def isLeft(node):
    if not node.parent:
        return False

    return node.parent.left == node

def isRight(node):
    if not node.parent:
        return False

    return node.parent.right == node

def updateHeights(node):
    node.left.height = max(getHeight(node.left.left), getHeight(node.left.right)) + 1
    node.right.height = max(getHeight(node.right.left), getHeight(node.right.right)) + 1

    node.height = max(getHeight(node.left), getHeight(node.right)) + 1

def getBalanceFactor(node):
    return getHeight(node.left) - getHeight(node.right)
