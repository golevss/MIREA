import os
import argparse

def list_directory(path, all_files, long_format):
    entries = os.listdir(path)
    
    if not all_files:
        entries = [entry for entry in entries if not entry.startswith('.')]
    
    if long_format:
        for entry in entries:
            entry_path = os.path.join(path, entry)
            stats = os.stat(entry_path)
            print(f"{stats.st_mode} {stats.st_size:10} {entry}")
    else:
        print("\n".join(entries))

def main():
    parser = argparse.ArgumentParser(description="A simple ls clone")
    parser.add_argument("path", nargs="?", default=".", help="Path to list (default is current directory)")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files")
    parser.add_argument("-l", "--long", action="store_true", help="Use long listing format")
    
    args = parser.parse_args()
    
    list_directory(args.path, args.all, args.long)

if __name__ == "__main__":
    main()
