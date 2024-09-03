source_file_path = 'source.txt'  
destination_file_path = 'destination.txt' 


with open(source_file_path, 'r') as source_file, open(destination_file_path, 'w') as destination_file:
    content = source_file.read()
    upper_case_content = content.upper()
    destination_file.write(upper_case_content)

print("Content has been converted to uppercase and written to the destination file.")
