#!/usr/bin/env python

# Lists 1
print("=========================")
print("Lists 1st")
print("=========================")
friends = ["Adi" , "Dedi" , "Budi"]

print(friends)
print(friends[0])
print(friends[1])
print(friends[2])
print(len(friends))

friends.append("Rudi")
print(friends)
print("=========================")

# Lists 2
print("=========================")
print("Lists 2nd")
print("=========================")

friends = [
    ["Bob" , 27],
    ["Anne" , 28],
    ["Rudi" , 29]
]

print(friends[0][0])
print(friends[0][1])
print(friends[0])

print("=========================")


# Lists 3
print("=========================")
print("Lists 3rd")
print("=========================")

friends = ["Bob", "Anne" , "Rudi"]
add1 = input("Enter Name : ")
friends.append(add1)
print(friends)

print("=========================")

