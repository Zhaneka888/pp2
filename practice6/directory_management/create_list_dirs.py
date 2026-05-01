import os

os.makedirs("myfolders/folder1/folder2", exist_ok=True)
print("Nested directories created.")

print("Current working directory:")
print(os.getcwd())

print("Files and folders in current directory:")
print(os.listdir())

os.mkdir("single_folder")
print("single_folder created.")

os.rmdir("single_folder")
print("single_folder removed.")