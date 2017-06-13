#!/usr/bin/python

def readText():
    
    fo = open("data/messages.txt", "r+")
    # str = fo.read(10);
    mess = [];

    for i in range(0,5):
        mess.append(fo.readline());

    for i in range(0,5):
        print mess[i];

    # print "Read String is : ", mess1
    # print "Read String is : ", mess2
    # Close opend file
    fo.close()

readText()