#!/usr/bin/python
# -- coding: utf-8 --


from database import Database

# manager library
# key is the expa ID, label is the trello ID --> { 'expa ID' :  'Trello ID' }
# Anais, Daniella, Gwenaelle, Jonas, Lucas, Adrien, Dylan, Jeremy, Morgane
# TODO integrate this somewhere (doesn't seem useful as of now in our code?)
ogxTeam = {'1856304': '5cbae2c59d966941df8d9b5f',
           '2108256': '5cb5dae61646158e92621248',
           '2209383': '5cb739286550d048542b0081',
           '2709530': '5cb4418c84476835eb75e95b',
           '2154457': '5cb73b6e19cff548f71ca5b2',
           '2064165': '5cb71e2e16cb0e546c301cef',
           '1803727': '5cb71e2f7f653c623d9aaa1f',
           '996944': '5cb85bdf02feea45bc7f89e1',
           '3001465': '5cbae37ccb202f790b6d9297'}

# initialise the dabatase
expaToken = "3bdedc112ffe486b6d422520540ebe394f118b8d4f406934f4918bb6ba6f5fa8"

additionalIDs = []

# constant token variables
trelloToken = "9f9de4286e6a5f627f083dc3ca8fdf6dceae7307a06c5e9dcedda4212491a4e3"
trelloKey = "448b14b4374aaa9429f4a8b979936e2b"
idBoard = "5cb1f5a13ae5f15b88be935d"

db = Database(expaToken, trelloToken, trelloKey, idBoard, additionalIDs if len(additionalIDs) != 0 else None)
db.get()
db.push()