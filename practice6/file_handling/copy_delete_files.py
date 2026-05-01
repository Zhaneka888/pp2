from pathlib import Path
import shutil

source_file = Path("demofile.txt")
copy_file = Path("demofile_copy.txt")
backup_file = Path("demofile_backup.txt")

if source_file.exists():
    shutil.copy(source_file, copy_file)
    print("File copied.")

if source_file.exists():
    shutil.copy(source_file, backup_file)
    print("Backup created.")

if copy_file.exists():
    copy_file.unlink()
    print("Copied file deleted safely.")
else:
    print("File does not exist.")