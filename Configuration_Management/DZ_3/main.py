import json
import argparse
import sys
import re

name = r'[_a-z]+'
consts = []

def process_array(arr,d):
    result = "(list"
    for item in arr:
        result += f" {process_value(item,d)}"
    result += " )"
    return result

def process_object(obj,d):
    vars = []
    result = "struct {\n"
    for key, value in obj.items():
        if key == "constants":
            result = f"{process_cons(value)}" + result
        elif key == "coments":
            result = f"{process_coms(value)}" + result
        elif re.match(name,key):
            if key in vars:
                raise ValueError(f"Wrong var: {key}")
            else:
                result += '\t'*d
                result += f"{key} = {process_value(value,d+1)},\n"
                vars.append(key)
        else:
            raise ValueError(f"Unsupported name: {key}")
    result = result[:-2] + '\n' + '\t'*(d-1) + '}'
    return result

def process_cons(obj):
    result = ""
    for key, value in obj.items():
        if re.match(name,key):
            if key in consts:
                raise ValueError(f"Wrong var: {key}")
            else:
                result += f"def {key} := {process_value(value,1)};\n"
                consts.append(key)
        else:
            raise ValueError(f"Unsupported name: {key}")
    return result

def process_coms(obj):
    result = ""
    for key, value in obj.items():
        result += f'\ {key} = {process_value(value,1)}\n'
    return result

def process_value(value,d):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return process_array(value,d)
    elif isinstance(value, dict):
        return process_object(value,d)
    else:
        raise ValueError(f"Unsupported type: {type(value)}")

def main(input_file,output_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = process_object(data,1)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print("Translation completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translator")
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output
    main(input_file,output_file)