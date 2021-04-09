#! /bin/usr/env python

cities = ['New York', 'Dallas', 'San Antonio', 'Houston', 'San Francisco'];

stack = []

for i in range(len(cities)) :
    stack.append(i)

    while len(stack) :
        print(stack.pop())
