import os
import re

def find_files_with_line(pattern, search_line):
    """
    Function for finding files with a line that is supposed to be wrong
    In this case, files containing the line: "1   58.69340000             # Ni" are wrong and need to be adjusted
    """
    # Create a regex pattern for the search line (escaping special characters)
    escaped_search_line = re.escape(search_line.strip())  # Escape special regex characters
    line_pattern = re.compile(rf"^\s*{escaped_search_line}\s*$")  # Match the exact line

    # Loop through the current directory to find matching files
    for root, dirs, files in os.walk(os.getcwd()):  # Search in the current working directory
        for file in files:
            # Check if the file matches the pattern (NiAl3*.lmp)
            if file.startswith(pattern) and file.endswith('.lmp'):
                file_path = os.path.join(root, file)
                try:
                    # Open and read the file
                    with open(file_path, 'r') as f:
                        for line in f:
                            # Check if the line matches the search pattern
                            if line_pattern.match(line.strip()):
                                print(f"File: {file_path} contains the line: {search_line}")
                                break  # Stop after finding the first matching line
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}")

def main():
    # Set the search pattern for filenames (NiAl3*.lmp)
    pattern = "NiAl3"  # Prefix of files to search for
    
    # Accept a search line from the user
    search_line = input("Enter the line to search for: ").strip()

    # Call the function to find matching files
    find_files_with_line(pattern, search_line)

if __name__ == "__main__":
    main()
