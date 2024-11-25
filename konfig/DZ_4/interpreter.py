import yaml
import argparse

def din_to_str(binary_file):
    with open(binary_file, 'rb') as f:
        binary_data = f.read()
    
    return ' '.join(f'{byte:08b}' for byte in binary_data).split(' ')
        

def interpret(binary_file, output_file, memory_range):
    memory = [0] * 1024
    registers = [0] * 1024

    all_bin = din_to_str(binary_file)
    while all_bin != []:
        bin_code = ""
        
        for i in range (6):
            bin_code += all_bin[i]
        all_bin = all_bin[6:]

        A = bin_code[:2]

        print()
        print(A,int(A,2))

        if int(A,2) == 1:  # LOAD
            B = bin_code[3:8]
            C = bin_code[9:21]
            #registers[B] = C
            print(B,int(B,2))
            print(C,int(C,2))
        elif int(A,2) == 0:  # READ
            B = bin_code[3:8]
            C = bin_code[9:21]
            print(B,int(B,2))
            print(C,int(C,2))
            #registers[B] = memory[registers[C]]
        elif int(A,2) == 2:  # WRITE
            B = bin_code[3:35]
            C = bin_code[35:41]
            print(B,int(B,2))
            print(C,int(C,2))
            #memory[registers[B]] = registers[C]
        elif int(A,2) == 3:  # MUL
            B = bin_code[3:8]
            C = bin_code[9:14]
            D = bin_code[15:45]
            print(B,int(B,2))
            print(C,int(C,2))
            print(C,int(D,2))
            #registers[B] = registers[C] * memory[D]
        else:
            raise ValueError(f"Unknown instruction with A={int(A,2)}")
    
    # Сохраняем диапазон памяти
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
