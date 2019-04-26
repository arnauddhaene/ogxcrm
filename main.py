#!/usr/bin/python
# -- coding: utf-8 --


from database.database import Database

# initialise the dabatase
expaToken = "b3a3520509a6dcf3b4da55c65b0b0659addd151983fcfaff4aadf29aecff2ae0"
trelloToken = "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
trelloKey = "448b14b4374aaa9429f4a8b979936e2b"

db = Database(expaToken, trelloToken, trelloKey)