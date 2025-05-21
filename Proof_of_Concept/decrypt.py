import os
from Crypto.Cipher import AES
# ------------------------- Error Handling for Result.txt -------------------------
try:
    with open('Result.txt', 'r') as f:
        lines = f.readlines()
except FileNotFoundError:
    print("[Critical Error] Result.txt not found. Check file path.")
    exit(1)
except IOError as e:
    print(f"[File Error] Failed to read Result.txt: {str(e)}")
    exit(1)
# Check line count
if len(lines) < 27:
    print(f"[Format Error] Insufficient lines in Result.txt (expected ≥27, got {len(lines)})")
    exit(1)
line_27 = lines[26].strip()  
# Validate line format "key: value"
if ": " not in line_27:
    print(f"[Format Error] Line 27 format invalid (expected 'AES Cipher Key : value'): '{line_27}'")
    exit(1)
# Extract HEX value
try:
    key1_hex = line_27.split(": ", 1)[1]  # Split only once to avoid colon in value
except IndexError:
    print(f"[Format Error] No value found after colon in line 27: '{line_27}'")
    exit(1)
# Validate HEX string
try:
    key1 = bytes.fromhex(key1_hex)
except ValueError as e:
    print(f"[HEX Error] Invalid HEX value on line 27: '{key1_hex}'\nDetail: {str(e)}")
    exit(1)
# ------------------------- Decryption Process -------------------------
iv = b'\x00' * 16  
# Create output directory
decrypted_dir = 'decrypted_mb1'
os.makedirs(decrypted_dir, exist_ok=True)
# Validate RCM folder
rcm_folder = 'rcm_message'
if not os.path.exists(rcm_folder):
    print(f"[Path Error] Directory '{rcm_folder}' does not exist")
    exit(1)
if not os.path.isdir(rcm_folder):
    print(f"[Path Error] '{rcm_folder}' is not a valid directory")
    exit(1)
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
    
    try:
        with open(os.path.join(rcm_folder, filename), 'rb') as f:
            encrypted_data = f.read()[0x17B0:]  # Skip header
    except IOError as e:
        print(f"[Read Error] Failed to read '{filename}': {str(e)}")
        continue  # Skip problematic file
    # AES decryption
    cipher1 = AES.new(key1, AES.MODE_CBC, iv=iv)
    decrypted_once = cipher1.decrypt(encrypted_data)
    
    # Optional: Check decrypted data length (AES-CBC requires multiples of 16)
    if len(decrypted_once) % 16 != 0:
        print(f"[Warning] {filename}: Decrypted data length {len(decrypted_once)} is not block-aligned")
    # Write output
    output_path = os.path.join(decrypted_dir, output_name)
    try:
        with open(output_path, 'wb') as f:
            f.write(decrypted_once)
    except IOError as e:
        print(f"[Write Error] Failed to write '{output_path}': {str(e)}")
print("Decryption completed successfully!")