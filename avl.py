import random
from avl_helpers import *
from node import Node

# Global variables for 4 AVL cases
LL, LR, RR, RL = 1, 2, 3, 4

class AVLBinarySearchTree:
    def __init__(self, root=None):
        self.root = root

    def __str__(self):
        if self.root:
            return self.root.display(show_heights=False)
        else:
            return 'Empty binary search tree'

    def __contains__(self, value):
         node = self.root

         while node:
              if node.value > value:
                   node = node.left
              elif node.value < value:
                   node = node.right
              else:
                   return True

         return False

    def validate(self):
        return AVLBST_validator(self.root)

    def updateParent(self, old_child, new_child):
        ''' Updates the parent by replacing old_child with new_child '''
        if not old_child.parent:
            self.root = new_child
        elif isLeft(old_child):
            old_child.parent.left = new_child
        elif isRight(old_child):
            #assert isRight(old_child)
            old_child.parent.right = new_child

        if new_child: 
            new_child.parent = old_child.parent

    def rotateLeft(self, node):
        # Step 1: rotate the node to the left of itself
        parent=node.parent
        self.updateParent(old_child=parent, new_child=node)
        old_left=node.left
        node.left=parent
        parent.parent=node
        if old_left:
            parent.right=old_left
            old_left.parent=parent
        else:
            parent.right=None

        
    
    def rotateRight(self, node):
        # Step 2: rotate the node to the right of itself
        parent=node.parent
        self.updateParent(old_child=parent, new_child=node)
        old_right=node.right
        node.right=parent
        parent.parent=node
        if old_right:
            parent.left=old_right
            old_right.parent=parent
        else:
            parent.left=None

    def rebalance(self, z, y, x, case):
        if case==LL:
            self.rotateRight(y)
            updateHeights(y)
            return y
        elif case==LR:
            self.rotateLeft(x)
            self.rotateRight(x)
            updateHeights(x)
            return x
        elif case==RR:
            self.rotateLeft(y)
            updateHeights(y)
            return y
        elif case==RL:
            self.rotateRight(x)
            self.rotateLeft(x)
            updateHeights(x)
            return x


    def inspect(self, node):
        # Step 4: Implement the method inspect. The method performs a bottom-up traversal given a node.
        # For each node, it checks for an imbalance and/or updates the height.
        # Stop the bottom-up traversal if there is no need for it.
        # negative always means the right
        while node:
            old_height=getHeight(node)
            balancefactor= getBalanceFactor(node)
            if balancefactor<-1:
                y=node.right
                if getBalanceFactor(y) <=0:
                    x=y.right
                    node = self.rebalance(node,y,x,case=RR)        
                else:
                    x=y.left
                    node = self.rebalance(node,y,x,case=RL)
            elif balancefactor>1:
                y=node.left
                if getBalanceFactor(y)>=0:
                    x=y.left
                    node = self.rebalance(node,y,x,case=LL)
                else:
                    x=y.right
                    node = self.rebalance(node,y,x,case=LR)
            else:
                    node.height=max(getHeight(node.left), getHeight(node.right)) + 1
            if node.height==old_height:
                break
            else:
                node = node.parent

    def insert(self, value, data=None):
        if not self.root:
            self.root = Node(value)
            return self.root

        parent = self.root

        while True:
            if value < parent.value:
                if parent.left:
                    parent = parent.left
                else:
                    parent.left = Node(value, parent=parent)
                    if not parent.right:
                        self.inspect(parent)
                    return parent.left
            else:
                if parent.right:
                    parent = parent.right
                else:
                    parent.right = Node(value, parent=parent)
                    if not parent.left:
                        self.inspect(parent)                    
                    # Step 5.2: call the inspect method on the parent of the newly inserted node (if needed)
                    return parent.right

    def deleteNode(self, node):
        if not self.root or not node:
            return

        # Step 6.1: Identify and initilize node_to_inspect for all 4 cases
        
        # Case 1: no children
        if not node.left and not node.right:
            self.updateParent(old_child=node, new_child=None)
            node_to_inspect=node.parent
        # Case 2: no left child
        elif not node.left:
            self.updateParent(old_child=node, new_child=node.right)
            node_to_inspect=node.parent
        # Case 3: no right child
        elif not node.right:
            self.updateParent(old_child=node, new_child=node.left)
            node_to_inspect=node.parent
        # Case 4: Both children exist
        else:
            successor = node.right
            while successor.left:
                successor = successor.left
            node.value = successor.value
            self.updateParent(old_child=successor, new_child=successor.right)
            node_to_inspect=successor.parent
        


        
        self.inspect(node_to_inspect)

    def deleteValue(self, value):
        node = self.findNode(value)
        if node:
            self.deleteNode(node)

    def get_sorted_list(self):
        stack = []
        lst = []
        node = self.root

        while True:
            if node:
                stack.append(node)
                node = node.left
            elif len(stack) > 0:
                node = stack.pop()
                lst.append(node.value)
                node = node.right
            else:
                break

        return lst                          

    def findNode(self, value):
         node = self.root

         while node:
              if node.value > value:
                   node = node.left
              elif node.value < value:
                   node = node.right
              else:
                   return node

         return None

if __name__ == '__main__':
    b = AVLBinarySearchTree()

    test = 8

    if test == 1:
        for n in [10, 1, 15, 12, 20, 25]:
            b.insert(n)
        print(b) 
    elif test == 2:
        for n in [10, 5, 15, 3, 8, 4]:
            b.insert(n)
        print(b)
    elif test == 3:
        for n in [10, 1, 15, 12, 20, 13]:
            b.insert(n)
        print(b)
    elif test == 4:
        for n in [10, 5, 15, 3, 8, 9]:
            b.insert(n)
        print(b)
    elif test == 5:
        for i in range(1, 31):
            b.insert(i)
        print(b)
    elif test == 6:
        for n in [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 55, 31, 28]:
            b.insert(n)
        print(b)
    elif test == 7:
        for n in [10, 7, 30, 6, 8, 35, 5, 9]:
            b.insert(n)
        print(b)
        b.deleteValue(35)
        print('After deleting 35:')
        print(b)
        b.insert(1)
        print('After inserting 1:')
        print(b)        
    elif test == 8:
        print('Testing tree ', end='')
        for j in range(200):
            print(f'{j+1}...', end='')
            for i in range(25):
                b.insert(random.randint(-100, 100))
                assert b.validate()

            lst = b.get_sorted_list()

            random.shuffle(lst)
            
            for n in lst:
                b.deleteValue(n)
                assert b.validate()

            assert b.root == None





    


