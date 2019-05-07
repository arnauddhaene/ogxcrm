#!/usr/bin/python
# -- coding: utf-8 --


from database import Database

# initialise the dabatase
expaToken = "f0249c34905d31f22165b21b075a11e71ecbac8535c17abc0837012afbc83f19"

# constant token variables
trelloToken = "c9d4a9e119e80ad8b763a129418a9f534b7fc8abceee642538083b87f2d65077"
trelloKey = "448b14b4374aaa9429f4a8b979936e2b"
idBoard = "5cb1f5a13ae5f15b88be935d"

db = Database(expaToken, trelloToken, trelloKey, idBoard)