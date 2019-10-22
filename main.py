#!/usr/bin/python
# -- coding: utf-8 --

from database.database import Database
from database.expa import ExpaService

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
additionalIDs = []

db = Database("ba3ed2678ed81779e582848a4690da3dafbb9bc34933f4e2a7c24e68812e5864", additionalIDs if len(additionalIDs) > 0 else None)

#db.get()
#db.push()

#db.moveFromAssigned()
expa = ExpaService("7ff684f1636708fed3ba2fb266020b3320edc0a88cc87ee87a3cf9dd0d9e9bff")
expa.exportAllMembers("all_members.xls")
