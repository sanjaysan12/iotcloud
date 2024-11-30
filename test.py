from src.User import User
from src.Database import Database


s = User.register("Ramya","Ramya@123","Ramya@123")
print(str(s))

# if User.login("Thabu","Thabu@123"):
#     print("Login Success")
# else:
#     print("Login Failed")