#!/usr/bin/python

def readText():

    mess = [];

    try:
        fo = open("data/messages.txt", "r+");

        for i in range(0,5):
            mess.append(fo.readline());
        # Close opend file
        fo.close();
    except:
        pass

    return mess

mess=[];
while True:
    temp=readText();
    if temp!=mess and temp!=[] :
        mess=temp;
        for i in range(0,5):
            print mess[i];