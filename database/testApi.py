from apiService import *
from database import Database
from getpass import getpass
import xlwt

"""
loginService = ExpaLoginService()

username = input("EXPA email: ")
pwd = getpass()

result = loginService.sign_in(username, pwd)
"""

"""
token =
expaService = ExpaService()

print(result)
print(result.text)
print(result.status_code)
print(result.cookies)
print(result.request)
"""

#expaService = ExpaService("4812f7da1cab6855b96edeaf2072d2adb6713966e90d29405953a1e0b26275e3")
#expaService.getAndExportCurrentMembers("members.xls", verbose=True)

db = Database("4812f7da1cab6855b96edeaf2072d2adb6713966e90d29405953a1e0b26275e3", None, None, None)
db.moveFromAssigned()
