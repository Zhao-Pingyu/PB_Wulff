import numpy as np

def read_lines_from_file(file_path, num_lines):
    """
    Function for reading lines from file and making appropriate adjustments
    This is for adjusting the contents of files that contain errors
    """
    lines = []
    try:
        with open(file_path, 'r') as file:
            for _ in range(num_lines):
                line = file.readline()
                if not line:  # Stop if the file has fewer lines than requested
                    break
                lines.append(line.strip())  # Strip newline characters
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    lines[11] = '1   26.98153860             # Al'
    lines[12] = '2   58.69340000             # Ni'
    return lines
    
def join_files(file1, num_lines, file2, output_file):
    """
    Function for joining the contents of two files
    """
    # Open the first file and read its contents
    head = read_lines_from_file(file1,num_lines)

    # Open the second file and read its contents
    with open(file2, 'r') as f2:
        content2 = f2.readlines()

    # Write the contents of both files into the output file
    with open(output_file, 'w') as out:
        for line in head:
            out.write(line + "\n")

        for line in content2:
            out.write(line)

            
if __name__ == "__main__":
    index = ['148','149','158','162','163','169','55','56','70','71','72','74','76','8','82','83','85','93']
    for i in index:
        data = np.loadtxt(f'Al3Ni-inbox-{i}.lmp',skiprows=16)
        xyz = data[:,:5]
        sorted_indices = np.argsort(xyz[:, 0])
        sorted_data = xyz[sorted_indices]
        atype = data[:,1]
        Al = np.where(atype == 2)
        Ni = np.where(atype == 1)
        sorted_data[Al,1] = 1
        sorted_data[Ni,1] = 2
        np.savetxt("pos.txt",sorted_data,fmt=' '.join(['%i']*2 + ['%1.11f']*3))
        join_files(f'Al3Ni-inbox-{i}.lmp', 16, 'pos.txt', f'Al3Ni-inbox-{i}-1.lmp')
