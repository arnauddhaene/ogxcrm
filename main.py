#!/usr/bin/python
# -- coding: utf-8 --

from database import Database

# initialise the dabatase
expaToken = "27b81dfbff4ff8e8424786ff84f74f97e84e82cc013bacbb9cdc576fcae025da"

# constant token variables
trelloToken = "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
trelloKey = "448b14b4374aaa9429f4a8b979936e2b"
idBoard = "5cb1f5a13ae5f15b88be935d"

db = Database(expaToken, trelloToken, trelloKey, idBoard)