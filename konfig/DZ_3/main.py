import json
import argparse
import sys
import re

name = r'[_a-z]+'
consts = []

def process_array(arr):
    result = "(list"
    for item in arr:
        result += f" {item}"
    result += " )"
    return result

def process_object(obj):
    result = "struct {\n"
    for key, value in obj.items():
        if key == "constants":
            result += f"{process_cons(value)}"
        elif re.match(name,key):
            result += f"\t{key} = {process_value(value)},\n"
        else:
            raise ValueError(f"Unsupported name: {key}")
    result += "}"
    return result

def process_cons(obj):
    result = ""
    for key, value in obj.items():
        if re.match(name,key) and isinstance(value, (int, float)):
            if key in consts:
                raise ValueError(f"Unsupported name: {key}")
            else:
                result += f"\tdef {key} := {value};\n"
                consts.append(value)
        else:
            raise ValueError(f"Unsupported name: {key}")
    return result

def process_value(value):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        return process_array(value)
    elif isinstance(value, dict):
        return process_object(value)
    else:
        raise ValueError(f"Unsupported type: {type(value)}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translator")
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = process_object(data)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print("Translation completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)






