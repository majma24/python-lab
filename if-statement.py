#!/usr/bin/env python

# if_statement 1st
print("=========================")
print("if_statement 1st")
print("=========================")

friends = "Rolf"
user_name = input("Enter Your Name: ")

if user_name == friends:
    print("Hello, friends")
else:
    print("Hello, strange")

print("=========================")


# if_statement 2nd
print("=========================")
print("if_statement 2nd")
print("=========================")


friends = {"Rob", "Anne", "Rudi"}
user_name = input("Enter Your Name : ")

if user_name in friends:
    print("Hello, friends")
else:
    print("Hello, Stranger")

print("=========================")