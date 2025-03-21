import numpy as np

def bunge_to_rotation_matrix(phi1, phi2, phi3):
    """Convert Bunge angles to a rotation matrix."""
    # Convert degrees to radians
    phi1_rad = np.radians(phi1)
    phi2_rad = np.radians(phi2)
    phi3_rad = np.radians(phi3)

    # Rotation matrices
    R_z1 = np.array([[np.cos(phi1_rad), -np.sin(phi1_rad), 0],
                     [np.sin(phi1_rad), np.cos(phi1_rad), 0],
                     [0, 0, 1]])

    R_x2 = np.array([[1, 0, 0],
                     [0, np.cos(phi2_rad), -np.sin(phi2_rad)],
                     [0, np.sin(phi2_rad), np.cos(phi2_rad)]])

    R_z3 = np.array([[np.cos(phi3_rad), -np.sin(phi3_rad), 0],
                     [np.sin(phi3_rad), np.cos(phi3_rad), 0],
                     [0, 0, 1]])

    # Combined rotation matrix
    R = R_z3 @ R_x2 @ R_z1
    return R

def rotation_matrix_to_xyz_euler(R):
    """Extract rotation angles (roll, pitch, yaw) from a rotation matrix in the XYZ convention."""
    assert R.shape == (3, 3), "Input must be a 3x3 matrix."

    # Extracting the angles
    roll = np.arctan2(R[2, 1], R[2, 2])  # Roll (phi)
    pitch = -np.arcsin(R[2, 0])          # Pitch (theta)
    yaw = np.arctan2(R[1, 0], R[0, 0])   # Yaw (psi)

    # Convert radians to degrees
    roll = np.degrees(roll)
    pitch = np.degrees(pitch)
    yaw = np.degrees(yaw)

    return roll, pitch, yaw

# create structure file
def create_Al3Ni(x_rot, y_rot, z_rot):
    deg = '°'
    incs = np.arange(0,181)
    for inc in incs:
        with open('Al3Ni-{}.txt'.format(inc), 'w',encoding="utf-8") as outfile:
            outfile.write(f'box 200 200 200\n')
            x = x_rot + inc
            outfile.write(f'node 0.5*box 0.5*box 0.5*box {x}{deg} {y_rot}{deg} {z_rot}{deg}\n')
        
def create_Al(x_rot, y_rot, z_rot):
    deg = '°'
    incs = np.arange(0,181)
    for inc in incs:
        with open('Al-{}.txt'.format(inc), 'w',encoding="utf-8") as outfile:
            outfile.write(f'box 200 200 200\n')
            x = x_rot + inc
            outfile.write(f'node 0.5*box 0.5*box 0.5*box {x}{deg} {y_rot}{deg} {z_rot}{deg}\n')
        
if __name__=="__main__":
    # Bunge angles for Al3Ni
    phi1 = 171  # degrees
    phi2 = 85  # degrees
    phi3 = 230  # degrees

    # Step 1: Compute the rotation matrix from Bunge angles
    rotation_matrix = bunge_to_rotation_matrix(phi1, phi2, phi3)
    # Step 2: Extract XYZ Euler angles from the rotation matrix
    roll, pitch, yaw = rotation_matrix_to_xyz_euler(rotation_matrix)
    create_Al3Ni3(roll, pitch, yaw)
    
    # Bunge angles for Al
    phi1 = 190  # degrees
    phi2 = 83  # degrees
    phi3 = 224  # degrees    
    
    rotation_matrix = bunge_to_rotation_matrix(phi1, phi2, phi3)
    roll, pitch, yaw = rotation_matrix_to_xyz_euler(rotation_matrix)
    create_Al(roll, pitch, yaw)