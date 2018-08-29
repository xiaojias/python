#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
# testing yield to read a file

def readFileWithBlock(filepath):
    BLOCK_SIZE=30
    with open(filepath, 'rb') as f:
        while True:
            block=f.read(BLOCK_SIZE)
            if block:
                yield block
            else:
                return


def readFileWithLine(filepath):
    with open(filepath, "r") as f:
        for line in f.readlines():
            newLine=line.upper().replace("\t", "  ")
            # process on the line
            yield newLine

fileContent=readFileWithBlock("/tmp/aa.out")
print("Read file with block:")
for i in fileContent:
    print(i)

fileLines=readFileWithLine("/tmp/aa.out")
print("Read file with line:")
j=1
for i in fileLines:
    print("line %s: %s" % (j, i), end="")
    j+=1
