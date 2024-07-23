import shutil

# Get the disk usage statistics
total, used, free = shutil.disk_usage("/")

# Print the results in bytes
print(f"Total: {total} bytes")
print(f"Used: {used} bytes")
print(f"Free: {free} bytes")

# Print the results in a more readable format
print(f"Total: {total // (2**30)} GiB")
print(f"Used: {used // (2**30)} GiB")
print(f"Free: {free // (2**30)} GiB")
