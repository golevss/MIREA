import yaml
import argparse

def din_to_str(binary_file):
    with open(binary_file, 'rb') as f:
        binary_data = f.read()
    
    return ' '.join(f'{byte:08b}' for byte in binary_data).split(' ')

def interpret(binary_file, output_file, memory_range):
    memory = [0] * 1024
    registers = [0] * 32

    all_bin = din_to_str(binary_file)
    while all_bin != []:
        bin_code = ""

        for i in range (6):
            bin_code += all_bin[i]
        all_bin = all_bin[6:]

        A = int(bin_code[:3],2)
        if A == 1:  # LOAD
            B = int(bin_code[3:8],2)
            C = int(bin_code[8:21],2)
            registers[B] = C
        elif A == 7:  # READ
            B = int(bin_code[3:8],2)
            C = int(bin_code[8:21],2)
            registers[B] = memory[registers[C]]
        elif A == 2:  # WRITE
            B = int(bin_code[3:35],2)
            C = int(bin_code[35:41],2)
            memory[registers[B]] = registers[C]
        elif A == 3:  # MUL
            B = int(bin_code[3:8],2)
            C = int(bin_code[8:13],2)
            D = int(bin_code[13:45],2)
            registers[B] = registers[C] * memory[D]
        else:
            raise ValueError(f"Unknown instruction with A={int(A,2)}")
    
    start, end = memory_range
    with open(output_file, 'w') as f:
        yaml.dump({'memory': memory[start:end]}, f)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interpreter")
    parser.add_argument('--bin')
    parser.add_argument('--out')
    parser.add_argument('--range', nargs=2, type=int)
    args = parser.parse_args()

    interpret(args.bin, args.out, tuple(args.range))
