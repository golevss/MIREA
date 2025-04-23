import re
import sys
import argparse

def convert_quotes_in_markdown(text):
    def replace_quotes(text):
        result = []
        in_quotes = False
        for char in text:
            if char == '"':
                if in_quotes:
                    result.append('»')
                else:
                    result.append('«')
                in_quotes = not in_quotes
            else:
                result.append(char)
        return ''.join(result)


    def replace_quotes_in_code_block(text):
        code_block_pattern = r'```[\s\S]*?```'
        code_blocks = re.findall(code_block_pattern, text)
        text = replace_quotes(text)

        for code_block in code_blocks:
            text = text.replace(code_block, f'###CODEBLOCK###{code_block}###CODEBLOCK###')

        for code_block in code_blocks:
            text = text.replace(f'###CODEBLOCK###{code_block}###CODEBLOCK###', code_block)

        return text

    return replace_quotes_in_code_block(text)

def main():
    parser = argparse.ArgumentParser(description="Convert normal quotes to guillemets in Markdown, preserving quotes in code blocks.")
    parser.add_argument("file", nargs="?", type=argparse.FileType('r'), default=sys.stdin, help="Markdown file to process (or use stdin if not specified)")
    
    args = parser.parse_args()
    text = args.file.read()
    converted_text = convert_quotes_in_markdown(text)
    sys.stdout.write(converted_text)

if __name__ == "__main__":
    main()
