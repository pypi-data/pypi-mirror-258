import argparse
import json
import yaml
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Translate JSON/YAML to Apple Pkl.')
    parser.add_argument('--input', required=True, help='Input file path (JSON or YAML).')
    parser.add_argument('--output', required=True, help='Output file path (Pkl).')
    return parser.parse_args()

def read_input_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension in ['.json']:
        with open(file_path, 'r') as file:
            return json.load(file)
    elif file_extension in ['.yaml', '.yml']:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or YAML file.")

def translate_yaml_to_pkl(data, indent=0, is_top_level=True):
    pkl_string = ""
    indent_space = "  " * indent
    entries = []
    if isinstance(data, dict):
        for key, value in data.items():
            entry = f"{indent_space}{key} = {translate_yaml_to_pkl(value, indent+1, False)}"
            entries.append(entry)
        pkl_string += "\n".join(entries)
        if is_top_level:
            pkl_string += "\n"  # Add a newline after top-level blocks
    elif isinstance(data, list):
        entries = [f"{indent_space}{translate_yaml_to_pkl(item, indent+1, False)}" for item in data]
        pkl_string += "\n".join(entries)
    elif isinstance(data, str):
        return f'"{data}"'
    elif data is None:
        return "nil"
    elif isinstance(data, bool):
        return "true" if data else "false"
    else:
        return str(data)
    if indent > 0:
        return "{\n" + pkl_string + "\n" + indent_space + "}"
    else:
        return pkl_string


def translate_json_to_pkl(data, indent=0, is_top_level=True):
    pkl_string = ""
    indent_space = "  " * indent
    entries = []
    if isinstance(data, dict):
        for key, value in data.items():
            entry = f"{indent_space}{key} = {translate_json_to_pkl(value, indent+1, False)}"
            entries.append(entry)
    elif isinstance(data, list):
        entries = [f"{indent_space}- {translate_json_to_pkl(item, indent+1, False)}" for item in data]
    elif isinstance(data, str):
        return f'"{data}"'
    elif data is None:
        return "nil"
    elif isinstance(data, bool):
        return "true" if data else "false"
    else:  # Covers integers, floats
        return str(data)
    pkl_string += "\n".join(entries)
    if indent > 0:
        return "{\n" + pkl_string + "\n" + indent_space + "}"
    else:
        # Add a newline after the top-level structure if it's the top level
        return pkl_string
    
    
def add_newline_after_blocks(pkl_data):
    lines = pkl_data.split('\n')
    processed_lines = []
    total_lines = len(lines)
    
    for i, line in enumerate(lines):
        processed_lines.append(line)
        # Check if the current line ends with a '}' and is not the last line
        if line.strip().endswith('}') and i + 1 < total_lines:
            # If the next line is not '}', add an empty line
            if not lines[i + 1].strip().startswith('}'):
                processed_lines.append('')
    
    return '\n'.join(processed_lines)


def write_output_file(file_path, pkl_data):
    with open(file_path, 'w') as file:
        file.write(pkl_data)


def main():
    args = parse_arguments()
    data = read_input_file(args.input)
    if args.input.endswith(('.yaml', '.yml')):
        pkl_data = translate_yaml_to_pkl(data, is_top_level=True)
    elif args.input.endswith('.json'):
        pkl_data = translate_json_to_pkl(data, is_top_level=True)
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or YAML file.")

    # Call the updated post-processing function to adjust the output formatting
    pkl_data = add_newline_after_blocks(pkl_data)

    write_output_file(args.output, pkl_data)

if __name__ == "__main__":
    main()