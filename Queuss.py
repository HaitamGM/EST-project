from collections import deque

queue = deque()

queue.appendleft("Jobi")
queue.appendleft("Joba")
queue.appendleft("Hoba")

print(queue)

print(queue[-1])

queue.pop()

print(queue[-1])