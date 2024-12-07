from asyncio import current_task
from http.cookiejar import cut_port_re
from os.path import curdir
from typing import List, Any, Dict, Set, Generator

class StaticArray:
    def __init__(self, capacity: int):
        if capacity<=0:
            raise ValueError("Capacity must be more than 0")
        self._arr=[None]*capacity
        self.capacity=capacity

    def set(self, index: int, value: int) -> None:
        if index<0 or index>self.capacity:
            raise IndexError("Index can't be more than capacity or less than zero")
        self._arr[index]=value

    def get(self, index: int) -> int:
        if index<0 or index>self.capacity:
            raise IndexError("Incorrect index")
        return self._arr[index]

class DynamicArray:
    def __init__(self):
        self.arr=[]

    def append(self, value: int) -> None:
        self.arr.append(value)

    def insert(self, index: int, value: int) -> None:
        if index<0 and index>len(self.arr)-1:
            raise IndexError("Index error")
        self.arr.insert(index,value)

    def delete(self, index: int) -> None:
        if index<0 and index>len(self.arr)-1:
            raise IndexError("Index out of range")
        del self.arr[index]
    def get(self, index: int) -> int:
        if index < 0 and index > len(self.arr) - 1:
            raise IndexError("Index out of range")
        return self.arr[index]
class Node:
    def __init__(self, value: int):
        self.value=value
        self.next=None


class SinglyLinkedList:
    def __init__(self):
        self.head=None
        self.count=0

    def append(self, value: int) -> None:
        new_node=Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.count+=1

    def insert(self, position: int, value: int) -> None:
        if position < 0 or position > self.count:
            raise IndexError("Index out of range")

        new_node = Node(value)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for it in range(position - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.count += 1

    def delete(self, value: int) -> None:
        current=self.head
        prev=None
        while current:
            if current.value==value:
                if prev is None:
                    self.head=current.next
                else:
                    prev.next=current.next
                self.count-=1
                return
            prev=current
            current=current.next
        raise ValueError(f'{value} not found')

    def find(self, value: int) -> Node:
        current=self.head
        if current.value==value:
            return current
        while current:
            if current.value==value:
                return current
            current=current.next
        raise ValueError(f'{value} nor found')

    def size(self) -> int:
        return self.count

    def is_empty(self) -> bool:
        if self.count==0:
            return True
        else:
            return False

    def print_list(self) -> None:
        ans=[]
        current=self.head
        while current.next:
            ans.append(current.value)
            current=current.next
        print(ans)
    def reverse(self) -> None:
        current=self.head
        prev=None
        while current:
            next=current.next
            current.next=prev
            prev=current
            current=next
        self.head=prev

    def get_head(self) -> Node:
        return self.head

    def get_tail(self) -> Node:
        current =self.head
        if not current:
            return None
        while current.next:
            current=current.next
        return  current

class DoubleNode:
    def __init__(self, value: int, next_node = None, prev_node = None):
        self.value=value
        self.next_node=next_node
        self.prev_node=prev_node

class DoublyLinkedList:
    def __init__(self):
        self.head=None
        self.count=0
        self.tail=None


    def append(self, value: int) -> None:
        new_node=DoubleNode(value)
        if self.head is None:
            self.head=new_node
            self.tail=new_node
        else:
            self.head.next_node=new_node
            new_node.prev_node=self.head
            self.tail=new_node
        self.count+=1

    def insert(self, position: int, value: int) -> None:
        if position<0 or position>self.count:
            raise IndexError("Index out of range")
        new_node=DoubleNode(value)
        if position==0:
            if self.head is None:
                self.head=new_node
                self.tail=new_node
            else:
                new_node.next_node=self.head
                self.head.prev_node=new_node
                self.head=new_node
        elif position==self.count-1:
                self.append(value)
        else:
            current=self.head
            for j in range(position):
                current=current.next_node
            new_node.prev_node=current.prev_node
            new_node.next_node=current
            if current.prev_node:
                current.prev_node.next_node=new_node
            current.prev_node=new_node
            self.count+=1
    def delete(self, value: int) -> None:
        current=self.head
        while current:
            if current.value==value:
                if current.prev_node:
                    current.next_node.prev_node=current.next_node
                else:
                    self.head=current.next_node
                if current.next_node:
                    current.next_node.prev_node=current.prev_node
                else:
                    self.tail=current.prev_node
                self.count-=1
                return
            current=current.next_node
        raise ValueError(f'{value} not found')


    def find(self, value: int) -> DoubleNode:
        if self.head.value==value:
            return self.head
        elif self.tail.value==value:
            return self.tail
        current = self.head
        while current:
            if current.value==value:
                return current
            current=current.next_node
        raise ValueError(f'{value} not found')

    def size(self) -> int:
        return self.count

    def is_empty(self) -> bool:
        if self.count==0:
            return True
        return False

    def print_list(self) -> None:
        ans=[]
        current=self.head
        while current:
            ans.append(current.value)
            current=current.next_node
        print(ans)

    def reverse(self) -> None:
        current = self.head
        self.head, self.tail = self.tail, self.head
        while current:
            current.next_node, current.prev_node = current.prev_node, current.next_node
            current = current.prev_node

    def get_head(self) -> DoubleNode:
        return self.head

    def get_tail(self) -> DoubleNode:
        return self.tail

class Queue:
    def __init__(self):
        self.arr=[]

    def enqueue(self, value: int) -> None:
        self.arr.append(value)

    def dequeue(self) -> int:
        if len(self.arr)>0:
            return self.arr.pop(0)
        else:
            raise IndexError("queue is empty")
    def peek(self) -> int:
        if len(self.arr)>0:
            return  self.arr[0]
        raise IndexError("queue is empty")
    def is_empty(self) -> bool:
        return len(self.arr)==0

class TreeNode:
    def __init__(self, value: int):
        self.value=value
        self.left=None
        self.right=None

class BinarySearchTree:
    def __init__(self):
        self.root=None

    def insert(self, value: int) -> None:
        new_TreeNode=TreeNode(value)
        if self.root is None:
            self.root=new_TreeNode
            return
        current=self.root
        while True:
            if value<current.value:
                if current.left is None:
                    current.left=new_TreeNode
                    return
                current=current.left
            else:
                if current.right is None:
                    current.right=new_TreeNode
                    return
                current=current.right
    def delete(self, value: int) -> None:
        if self.root is None:
            return
        parent=None
        current=self.root
        while current and current.value!=value:
            parent=current
            if value<current.value:
                current=current.left
            else:
                current=current.right
        if current is None:
            return
        if current.left is None and current.right is None:
            if current==self.root:
                self.root=None
            elif parent.left==current:
                parent.left=None
            else:
                parent.right=None
        elif current.left is None or current.right is None:
            if current.left:
                child=current.left
            else:
                child=current.right
            if current==self.root:
                self.root=child
            elif current==parent.left:
                parent.left=child
            else:
                parent.right=child
        else:
            r_parent=current
            r=current.right
            while r.left:
                r_parent=r
                r=r.left
            current.value=r.value
            if r_parent.left==r:
                r_parent.left=r.right
            else:
                r_parent.right=r.right


    def search(self, value: int) -> TreeNode:
        current=self.root
        while current:
            if current.value==value:
                return current
            elif value<current.value:
                current=current.left
            else:
                current=current.right
        return None

    def inorder_traversal(self) -> List[int]:
        def traverse(node, result):
            if node:
                traverse(node.left, result)
                result.append(node.value)
                traverse(node.right, result)

        result = []
        traverse(self.root, result)
        return result

    def size(self) -> int:
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        return count_nodes(self.root)

    def is_empty(self) -> bool:
        return self.root is None

    def height(self) -> int:
        def calculate_height(node):
            if not node:
                return 0
            return 1 + max(calculate_height(node.left), calculate_height(node.right))
        return calculate_height(self.root)

    def preorder_traversal(self) -> List[int]:
        def traverse(node, result):
            if node:
                result.append(node.value)
                traverse(node.left, result)
                traverse(node.right, result)

        result = []
        traverse(self.root, result)
        return result

    def postorder_traversal(self) -> List[int]:
        def traverse(node, result):
            if node:
                traverse(node.left, result)
                traverse(node.right, result)
                result.append(node.value)

        result = []
        traverse(self.root, result)
        return result

    def level_order_traversal(self) -> List[int]:
        if not self.root:
            return []

        queue = [self.root]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current.value)
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

        return result

    def minimum(self) -> TreeNode:
        current = self.root
        while current and current.left:
            current = current.left
        return current

    def maximum(self) -> TreeNode:
        current = self.root
        while current and current.right:
            current = current.right
        return current

    def is_valid_bst(self) -> bool:
        def validate(node, min_val, max_val):
            if not node:
                return True
            if not (min_val < node.value < max_val):
                return False
            return validate(node.left, min_val, node.value) and validate(node.right, node.value, max_val)

        return validate(self.root, float('-inf'), float('inf'))

def insertion_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    for i in range(1, n):
        x = lst[i]
        j = i

        while j > 0 and lst[j - 1] > x:
            lst[j] = lst[j - 1]
            j -= 1

        lst[j] = x

    return lst

def selection_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if lst[j] < lst[min_index]:
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
    return lst

def bubble_sort(lst: List[int]) -> List[int]:
    for i in range(len(lst)):
        for j in range(len(lst)-1):
            if lst[j]>lst[j+1]:
                lst[j],lst[j+1]=lst[j+1],lst[j]
    return lst

def shell_sort(lst: List[int]) -> List[int]:
    n = len(lst)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = lst[i]
            j = i
            while j >= gap and lst[j - gap] > temp:
                lst[j] = lst[j - gap]
                j -= gap
            lst[j] = temp
        gap //= 2
    return lst
def merge_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    leftHalf = lst[:mid]
    rightHalf = lst[mid:]
    sortedLeft = merge_sort(leftHalf)
    sortedRight = merge_sort(rightHalf)
    return merge(sortedLeft, sortedRight)
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
def quick_sort(lst: List[int]) -> List[int]:
    if len(lst) <= 1:
        return lst
    else:
        pivot = lst[len(lst) // 2]
        left = [x for x in lst if x < pivot]
        middle = [x for x in lst if x == pivot]
        right = [x for x in lst if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)

