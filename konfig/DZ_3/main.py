import json
import sys
import re


def process_array(arr):
    result = "(list"
    for item in arr:
        result += f" {item}"
    result += " )"
    return result

def process_object(obj):
    name = r'[_a-z]+'
    result = "struct {\n"
    for key, value in obj.items():
        if re.match(name,key):
            result += f"    {key} = {process_value(value)},\n"
        else:
            raise ValueError(f"Unsupported name: {key}")
    result += "}"
    return result

def process_value(value):
    if isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return f"\"{value}\""
    elif isinstance(value, list):
        return process_array(value)
    elif isinstance(value, dict):
        return process_object(value)
    else:
        raise ValueError(f"Unsupported type: {type(value)}")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

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






