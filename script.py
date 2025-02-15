import os
import hashlib
import subprocess
import time
directory = "/Users/tatiana/Desktop/test"
files = {}
duplicates = []

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

for root, _, filenames in os.walk(directory):
    for filename in filenames:
        filepath = os.path.join(root, filename)
        file_hash = calculate_sha256(filepath)
        if file_hash in files:
            files[file_hash].append(filepath)
        else:
            files[file_hash] = [filepath]

for file_list in files.values():
    if len(file_list) > 1:
        duplicates.append(file_list)

if duplicates:
    for duplicate_group in duplicates:
        print("Оригинал:")
        for i, duplicate in enumerate(duplicate_group, start=0):
            command = ["open", duplicate]
            if not i:
                subprocess.check_output(command)
                time.sleep(2)
                subprocess.run(['osascript', '-e', f'tell application "Preview" to close (first document whose name is "{os.path.basename(duplicate)}")'])
                print(f"    Дубликат {i+1} - {duplicate}")
            else:
                print(f"    Дубликат {i+1} - {duplicate}")
        
        for i, duplicate in enumerate(duplicate_group, start=1):
            command = ["open", duplicate]
            subprocess.check_output(command)
            user_input = input(f"    Удалить дубликат {i} - {duplicate}?(д/н) ")
            while True:
                if user_input.lower() == "д":
                    os.remove(duplicate)  
                    print(f"    Файл {duplicate} удален.")
                    print("    " + "-" * 90)
                    subprocess.run(['osascript', '-e', f'tell application "Preview" to close (first document whose name is "{os.path.basename(duplicate)}")'])
                    break
                elif user_input.lower() == "н":
                    print(f"    Файл {duplicate} сохранен.")
                    print("    " + "-" * 90)
                    subprocess.run(['osascript', '-e', f'tell application "Preview" to close (first document whose name is "{os.path.basename(duplicate)}")'])
                    break
                else:
                    user_input = input(f"    Удалить дубликат {i} - {duplicate}?(д/н) ")
else:
    print("Дубликаты не найдены.")
