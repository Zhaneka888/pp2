f = open("demofile.txt", "w")
f.write("Hello! Welcome to demofile.\n")
f.write("This file is for testing.\n")
f.close()

print("File written successfully.")

f = open("demofile.txt", "a")
f.write("Now the file has more content.\n")
f.close()

print("Content appended successfully.")