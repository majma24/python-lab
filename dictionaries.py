#!/usr/bin/env python

# dictionary 1st
print("=========================")
print("Dict 1st")
print("=========================")

friend_ages = {"Rob" : 24 , "Bob" : 25 , "Andi" : 27}
print(friend_ages["Rob"])
print(friend_ages["Bob"])
print(friend_ages["Andi"])

print("=========================")

# dictionary 2nd
print("=========================")
print("Dict 2nd")
print("=========================")

friend_ages = {"Rob" : 24 , "Bob" : 25 , "Andi" : 27}

friend_ages["Deni"] = 28
friend_ages["Rob"] = 31

print(friend_ages)

print("=========================")

# dictionary 3rd
print("=========================")
print("Dict 3rd")
print("=========================")

friends = (
    {"name" : "Rudi Corona", "Age" : 25},
    {"name" : "Hendi Sanity", "Age" : 26},
    {"name" : "Hazmat", "Age" : 27}
)

print(friends[0]["name"])
print(friends[0]["Age"])
print(friends[1]["name"])
print(friends[1]["Age"])
print(friends[2]["name"])
print(friends[2]["Age"])

print("=========================")

# dictionary 4th
print("=========================")
print("Dict 4th")
print("=========================")

lottery_numbers = {13, 21, 22, 5, 8}
players = [
    {"name" : "Rudi",
    "numbers" : {1, 2, 13, 4, 5}
    },
    {
    "name" : "Bob",
    "numbers" : {6, 7, 8, 9, 10}
    }
]
name = players[0]['name']
numbers = players[0]['numbers'].intersection(lottery_numbers)
print('Player {name} got {amount} numbers right.'.format(name=name, amount=len(numbers)))
 
name = players[1]['name']
numbers = players[1]['numbers'].intersection(lottery_numbers)
print('Player {name} got {amount} numbers right.'.format(name=name, amount=len(numbers)))  
