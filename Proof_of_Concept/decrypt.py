import os
from Crypto.Cipher import AES

# Read SBK and NV-MEK from Result.txt file
with open('Result.txt', 'r') as f:
    lines = f.readlines()

key1_hex = lines[26].strip().split(': ')[1]  # 27th line key

key1 = bytes.fromhex(key1_hex)
iv = b'\x00' * 16  

# Create output directory
decrypted_dir = 'decrypted_mb1_firmware'
os.makedirs(decrypted_dir, exist_ok=True)

# Process all .rcm files
rcm_folder = 'rcm_message'
for filename in os.listdir(rcm_folder):
    if not filename.endswith('.rcm'):
        continue
    base_name = os.path.splitext(filename)[0]
    
    name_parts = base_name.split('_', 1)

    if len(name_parts) > 1:
        modified_base = f'mb1_{name_parts[1]}' 
    else:
        modified_base = base_name  
    
    output_name = f'decrypted_{modified_base}.bin' 


    # Read encrypted payload
    with open(os.path.join(rcm_folder, filename), 'rb') as f:
        encrypted_data = f.read()[0x17B0:]  # Skip first 0x17B0 bytes
    
    # SBK decryption layer
    cipher1 = AES.new(key1, AES.MODE_CBC, iv=iv)
    decrypted_once = cipher1.decrypt(encrypted_data)
    
    
   # Save decrypted result
    with open(os.path.join(decrypted_dir, output_name), 'wb') as f:
        f.write(decrypted_twice)
print("Decryption completed!")