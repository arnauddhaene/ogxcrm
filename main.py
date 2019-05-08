#!/usr/bin/python
# -- coding: utf-8 --


from database import Database

# initialise the dabatase
expaToken = "f10c1152388a3b0525db0c80be36e2c2670a0fd5e951bf8ce6f58d3775a7067c"

SpecialIDtoAdd = ['2614893']

# constant token variables
trelloToken = "c9d4a9e119e80ad8b763a129418a9f534b7fc8abceee642538083b87f2d65077"
trelloKey = "448b14b4374aaa9429f4a8b979936e2b"
idBoard = "5cb1f5a13ae5f15b88be935d"

db = Database(expaToken, trelloToken, trelloKey, idBoard, SpecialIDtoAdd)


