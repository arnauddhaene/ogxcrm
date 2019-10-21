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

#expaService = ExpaService("dadae54a94265f18ae6d6dafb4fa5047ceadb22c3dddc682b6b66323a304d6be")
#expaService.getAndExportCurrentMembers("members.xls", verbose=True)

db = Database("ae29bf9d23f972c8031afa4de2f6fc1af5946514739f2f0fecf79bfdd8105689")
db.get()
db.push()
