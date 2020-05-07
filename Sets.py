#!/usr/bin/env python

# Sets 1st
print("=========================")
print("Sets 1st")
print("=========================")

arts_friends = {"Rob" , "Anne"}
chart_friends = {"Jen" , "Bob"}

arts_friends.add("Jen")
chart_friends.remove("Jen")

print(arts_friends)
print(chart_friends)

print("=========================")

# Sets 2nd
print("=========================")
print("Sets 2nd")
print("=========================")

arts_friends = {"Rob" , "Anne" , "Jen"}
science_friends = {"Jen" , "charlie"}

arts_but_not_science = arts_friends.difference(science_friends)
print(arts_but_not_science)

science_but_not_arts = science_friends.difference(arts_friends)
print(science_but_not_arts)

not_in_both = arts_friends.symmetric_difference(science_friends)
print(not_in_both)

arts_and_science = arts_friends.intersection(science_friends)
print(arts_and_science)

all_friends = arts_friends.union(science_friends)
print(all_friends)

print("=========================")

# Sets 3rd
print("=========================")
print("Sets 3rd")
print("=========================")

nearby_people = {"Rob" , "Anne" , "Rudi" , "Bob"}
user_friends = set()
my_name = input("Enter Your Name : ")

user_friends.add(my_name)

nearby_and_user = nearby_people.intersection(user_friends)

print(nearby_and_user)

print("=========================")