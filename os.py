import os

# 1. Get the current working directory
print("Current Working Directory:", os.getcwd())

# 2. List all files and directories in the current path
print("Files and Directories:", os.listdir())

# 3. Make a new directory
os.mkdir("test_dir")
print("Directory 'test_dir' created.")

# 4. Change the working directory
os.chdir("test_dir")
print("Changed Directory to:", os.getcwd())

# 5. Create a file inside the new directory
with open("test_file.txt", "w") as f:
    f.write("Hello, this is a test file.")

# 6. Rename the file
os.rename("test_file.txt", "renamed_file.txt")
print("File renamed to 'renamed_file.txt'.")

# 7. Get file statistics
file_stat = os.stat("renamed_file.txt")
print("File Size:", file_stat.st_size, "bytes")

# 8. Remove the file
os.remove("renamed_file.txt")
print("File removed.")

# 9. Move back to the parent directory
os.chdir("..")
print("Changed Directory back to:", os.getcwd())

# 10. Remove the directory
os.rmdir("test_dir")
print("Directory 'test_dir' removed.")

# 11. Get the environment variables
print("Home Directory:", os.environ.get("HOME", "Not Available"))

# 12. Execute a system command (List files)
os.system("ls" if os.name != "nt" else "dir")

# 13. Get the process ID
print("Process ID:", os.getpid())

# 14. Get the parent process ID
print("Parent Process ID:", os.getppid())

# 15. Get the user ID (For Unix-like systems)
if hasattr(os, "getuid"):
    print("User ID:", os.getuid())

# 16. Get the system name
print("OS Name:", os.name)

# 17. Check if a path exists
print("Does '/etc' exist?:", os.path.exists("/etc"))

# 18. Join paths
print("Joined Path:", os.path.join("folder1", "folder2", "file.txt"))

# 19. Split a file path
print("Split Path:", os.path.split("/home/user/file.txt"))

# 20. Get absolute path
print("Absolute Path:", os.path.abspath("file.txt"))

# 21. Check if a path is a directory
print("Is '/home' a directory?:", os.path.isdir("/home"))

# 22. Check if a path is a file
print("Is '/home/user/file.txt' a file?:", os.path.isfile("/home/user/file.txt"))

# 23. Change file permissions (only on Unix-like systems)
if hasattr(os, "chmod"):
    os.chmod(".", 0o755)
    print("Changed permissions of current directory.")

# 24. Get the system login name
if hasattr(os, "getlogin"):
    print("Logged-in User:", os.getlogin())

# 25. Get CPU count
print("CPU Count:", os.cpu_count())

# 26. Get system load average (only on Unix-like systems)
if hasattr(os, "getloadavg"):
    print("System Load Average:", os.getloadavg())

# 27. Walk through a directory
for root, dirs, files in os.walk("."):
    print("Walking through:", root, "Dirs:", dirs, "Files:", files)
    break  # Avoid deep traversal

# 28. Create symbolic link (Unix-like systems only)
if hasattr(os, "symlink"):
    os.symlink("folder1", "symlink_to_folder1")
    print("Symbolic link created.")

# 29. Remove symbolic link (Unix-like systems only)
if hasattr(os, "unlink"):
    os.unlink("symlink_to_folder1")
    print("Symbolic link removed.")
