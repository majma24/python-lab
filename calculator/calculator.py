#! /usr/bin/env python

from operator import add,sub,mul,floordiv

class calculator:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def add(self):
        print("Add : ", add(self.x,self.y))
    def sub(self):
        if self.x <= self.y:
           print("Sub : ", sub(self.y,self.x))
        else:
            print("Sub : ", sub(self.x,self.y))
    def mul(self):
        print("Mul : ", mul(self.x,self.y))
    def div(self):
        print("Div : ", floordiv(self.x,self.y))

a = int(input("Enter Your Number -1: "))
b = int(input("Enter Your Number -2: "))
calc = calculator(a,b)
calc.add()
calc.sub()
calc.mul()
calc.div()