#!/usr/bin/python
# -*- coding: utf-8 -*-
# testing yield

# iterables
mylist = [x*x for x in range(3)]

print("Values of list:")
for i in mylist:
    print(i)

# generators
mygenerator = (x*x for x in range(3))

print("Values of generator:")
for i in mygenerator:
    print(i)

# yield
def createGenerator():
    mylist = range(3)
    for i in mylist:
        yield i*i

mygenerator = createGenerator()    # create a generator

print("Type of mygenerator:")
print(mygenerator)

print("Values of Yield:")
for i in mygenerator:
    print(i)