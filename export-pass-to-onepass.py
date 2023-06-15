import os
import subprocess

# Change this!
password_store_path = ""
# Change this! Leave empty if exporting root dir
password_store_subdir = ""
# Change this!
separator_char = ";"
# Change this!
export_file = "export.csv"
# Change this!
tags = ""

directory = os.fsencode(os.path.join(password_store_path, password_store_subdir))



# Print header row
header = "title" + separator_char + "url" + separator_char + "username" + separator_char + "password" + separator_char + "email" + separator_char + "tags"
f = open(export_file, "a")
f.write(header + "\n")

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	entryname = os.path.splitext(filename)[0]
	print("Hadling " + entryname)

	email = ""
	# Skipedi skip hidden files
	if filename.startswith('.'):
		continue
	# Skip subfolder
	if os.path.isdir(os.path.join(password_store_path, file.decode('utf-8'))):
		continue

	#Get title
	title = entryname
	entry = str(subprocess.check_output('pass ' + password_store_subdir + entryname.replace(' ', '\ '), shell=True, stdin=open(os.devnull)).decode('utf-8')).replace("\\n", "\n")
	# Get URL
	if "url: " in entry:
		url = entry.split('url: ')[1].splitlines()[0]
	elif "site: " in entry:
		url = entry.split('site: ')[1].splitlines()[0]
	else:
		url = entryname
	# Get email and username
	if "email: " in entry:
		email = entry.split('email: ')[1].splitlines()[0]
	# Get username
	if "username: " in entry:
		username = entry.split('username: ')[1].splitlines()[0]
	# Use email if username not found but email is
	elif email:
		username = email
	# Get password if exists, otherwise use the first row of entry
	if "password: " in entry:
		password = entry.split('password: ')[1].splitlines()[0]
	else:
		password = entry.splitlines()[0]
	
	# Check if there are commas fucking up with us
	for check in [title, url, username, password, email]:
		if separator_char in check:
			print("SOS!! " + title + " contains a bad character")
	
	csv_row = title + separator_char + url + separator_char + username + separator_char + password + separator_char + email + separator_char + tags
	f.write(csv_row + "\n")

f.close()