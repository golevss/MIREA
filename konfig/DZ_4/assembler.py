import yaml
import argparse
import sys

def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        instructions = f.readlines()
    
    binary_file = bytearray()
    log_data = []

    for line in instructions:
        if not line:
            continue
        
        parts = line.split()
        command = parts[0].upper()

        if command == "LOAD":
            A, B, C = 1, int(parts[1]), int(parts[2])
            instr = (A << 46) | (B << 40) | (C << 27)
        elif command == "READ":
            A, B, C = 0, int(parts[1]), int(parts[2])
            instr = (A << 46) | (B << 40) | (C << 27)
        elif command == "WRITE":
            A, B, C = 2, int(parts[1]), int(parts[2])
            instr = (A << 46) | (B << 13) | (C << 8)
        elif command == "MUL":
            A, B, C, D = 3, int(parts[1]), int(parts[2]), int(parts[3])
            instr = (A << 46) | (B << 40) | (C << 35) | (D << 4)
        else:
            raise ValueError(f"Unknown command: {command}")

        binary_file.extend(instr.to_bytes(6, byteorder='big'))
        log_data.append({ 'cmd_line': line.strip(),'binary': bin(instr)[2:].zfill(48), 'hex': hex(instr)[2:].zfill(12)})

    with open(output_file, 'wb') as f:
        f.write(binary_file)

    with open(log_file, 'w') as f:
        yaml.dump(log_data, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assembler")
    parser.add_argument('--input')
    parser.add_argument('--bin')
    parser.add_argument('--log')
    args = parser.parse_args()
    assemble(args.input, args.bin, args.log)
