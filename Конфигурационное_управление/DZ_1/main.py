import tarfile
import argparse
import datetime
import os
import logging

class VM:
    def __init__(self, filesystem_archive: str):
        self.currentpath = ""
        self.filesystem = tarfile.TarFile(filesystem_archive)
        self.filesystemlist = list()
        for file in self.filesystem:
                self.filesystemlist.append(file.name)

    def start(self):
        while True:
            if len(self.currentpath) == 0:
                cmd = input(f'usr:~$ ').split(" ")
            else:
                cmd = input(f'usr:{self.currentpath}$ ').split(" ")
            logger_main.info(f'INPUT script : "{cmd}"')
#-------------------------ls-------------------------
            if cmd[0].lower() == "ls":
                try:
                    if not self.ls(cmd[1]):
                        logger_main.error(f'ls command cause an error : Directory "{cmd[1]}" does not exist.')
                        print(f'Directory "{cmd[1]}" does not exist.')
                except:
                    self.ls("")
#-------------------------cd-------------------------
            elif cmd[0].lower() == "cd":
                try:
                    if not self.cd(cmd[1]):
                        logger_main.error(f'cd command cause an error : Directory "{cmd[1]}" does not exist.')
                        print(f'Directory "{cmd[1]}" does not exist.')
                except:
                    self.cd("")
#-------------------------pwd------------------------
            elif cmd[0].lower() == "pwd":
                self.pwd()
#-------------------------cat------------------------
            elif cmd[0].lower() == "cat":
                try:
                    if not self.cat(cmd[1]):
                        logger_main.error(f'cat command cause an error : Error while opening {cmd[1]}.')
                        print(f'Error while opening {cmd[1]}.')
                except:
                    self.cat("")
#-------------------------date-----------------------
            elif cmd[0].lower() == "date":
                self.date()
#------------------------clear-----------------------
            elif cmd[0].lower() == "clear" or cmd[0].lower() == "cls":
                self.clear()
#-------------------------exit-----------------------
            elif cmd[0].lower() == 'exit':
                break
            else:
                logger_main.error(f"Unknown command")
                print('Unknown command.')
    
    def pwd(self):
        if self.currentpath != "":
            print(f'/root/{self.currentpath}/')
            logger_main.info(f'/root/{self.currentpath}/')
        else:
            print(f'/root{self.currentpath}/')
            logger_main.info(f'/root{self.currentpath}/')
    
    def ls(self, newpath: str):
        path = self.currentpath

        if "/root" in newpath:
            path = newpath.replace('/root/', '')
        elif newpath == "~" or newpath == "/":
            path = ""
        elif newpath == "..":
                if (self.currentpath != ''):
                    path = self.currentpath[:self.currentpath.rfind('/')]
        else:
            if newpath != "":
                if newpath[:2] == "./":
                    newpath = newpath[2:]
                elif newpath[0] == "/":
                    newpath = newpath[1:]
            path += "/" + newpath
                    
        if path != "":
            if path[0] == "/":
                path = path[1:]
        
        flag = False
        for file in self.filesystemlist:
            if path in file:
                flag = True
        if flag == False: 
            return False;
    
        all_files = list()
        for file in self.filesystemlist:
                if path in file:
                    files = file[len(path):].split('/')
                    files = list(filter(None, files))
                    if files[0] in all_files:
                        continue
                    all_files.append(files[0])
                    print(files[0])
                    logger_main.info(files[0])
        return True 
    
    def cd(self, newpath: str):

        if newpath == "~" or newpath == "/":
            self.currentpath = ""
            return True
    
        elif "/root/" in newpath:
            newpath = newpath.replace('/root/', '')
            if newpath != "":
                if newpath[-1] == '/':
                    newpath = newpath[:-1]
                if newpath[0] == '/':
                    newpath = newpath[1:]
            for file in self.filesystemlist:
                if newpath in file:
                    self.currentpath = newpath
                    return True
                    
        elif newpath[:2] == "./":
            newpath = newpath[2:]
            if newpath[-1] == '/':
                newpath = newpath[:-1]
            for file in self.filesystemlist:
                if newpath in file:
                    self.currentpath += "/" + newpath
                    return True
        
        elif newpath == "..":
            if (self.currentpath != ''):
                self.currentpath = self.currentpath[:self.currentpath.rfind('/')]
            return True
        
        elif newpath != "":        
            if newpath[0] == '/':
                newpath = newpath[1:]
                if newpath[-1] == '/':
                    newpath = newpath[:-1]
                for file in self.filesystemlist:
                    if newpath in file:
                        self.currentpath = "/" + newpath
                        return True
        return False
    
    def cat(self, filename: str):
        path = self.currentpath

        if filename != "":
            if filename[0] == "/":
                path = filename
            else:
                path += "/" + filename
        elif "/root" in filename:
            filename = filename.replace('/root/', '')
            for file in self.filesystemlist:
                if filename in file.filename:
                    path = "/" + filename
        else:
            path += "/" + filename
        if path != "":
            if path[0] == "/":
                path = path[1:]
        try:
            f = self.filesystem.extractfile(path)
            if f is not None:
                lines = [x.decode('utf8').strip() for x in f.readlines()]
                for line in lines:
                    print(line)
                    logger_main.info(line)
                
            return True
        except KeyError:
            return False

    def date(self):
        date = datetime.date.today()
        print("DATE: ");print(date)
        logger_main.info(date)
        time = datetime.datetime.now().time()
        print("TIME: ");print(time)
        logger_main.info(time)
    
    def clear(self):
        os.system('cls||clear')

    def test_commands(self):
        logger_main.info(f"Testing commands")
        print("======================================")

#----------------Test ls----------------
        logger_main.info(f"Testing ls command:")
        print("Testing ls command:")
        self.ls("")
        self.ls("/root/Right")
        self.ls("/Right/Test/")
        print("======================================")

#----------------Test cd----------------
        print("Testing cd command:")
        logger_main.info(f"Testing cd command:")
        self.cd("")
        self.cd("/root/Left")
        self.cd("..")
        self.cd("/")
        print("======================================")

#----------------Test pwd----------------
        print("Testing pwd command:")
        logger_main.info(f"Testing pwd command:")
        self.cd("/root/Right/Test")
        self.pwd()
        self.cd("~")
        self.pwd()
        print("======================================")
        
#----------------Test cat----------------
        print("Testing cat command:")
        logger_main.info(f"Testing cat command:")
        self.cat("/root/Left/xd.txt")
        self.cat("/root/Right/main.py")
        print("======================================")

#----------------Test date----------------
        print("Testing date command:")
        logger_main.info(f"Testing date command:")
        self.date()
        print("======================================")

    def run_script(self, script_file: str):
        try:
            with open(script_file, 'r') as file:
                logger_main.info(f"script was successfuly started")
                for line in file:
                    logger_main.info(f'INPUT script : "{line.strip()}"')
                    self.execute_command(line.strip())
        except FileNotFoundError:
            print(f"Script file '{script_file}' not found.")
            logger_main.error(f"Script file '{script_file}' not found.")
    
    def execute_command(self, command: str):
        cmd = command.split(" ")
        print("Executing command: ", cmd)
#-------------------------ls-------------------------
        if cmd[0].lower() == "ls":
            try:
                if not self.ls(cmd[1]):
                    logger_main.error(f'ls command cause an error : Directory "{cmd[1]}" does not exist.')
                    print(f'Directory "{cmd[1]}" does not exist.')
            except:
                self.ls("")
#-------------------------cd-------------------------
        elif cmd[0].lower() == "cd":
            try:
                if not self.cd(cmd[1]):
                    logger_main.error(f'cd command cause an error : Directory "{cmd[1]}" does not exist.')
                    print(f'Directory "{cmd[1]}" does not exist.')
            except:
                self.cd("")
#-------------------------date-----------------------
        elif cmd[0].lower() == "date":
            self.date()
#-------------------------pwd------------------------
        elif cmd[0].lower() == "pwd":
            self.pwd()
#-----------------------clear----------------------- 
        elif cmd[0].lower() == "cls" or cmd[0].lower() == "clear":
            self.clear()
#-------------------------cat-------------------------    
        elif cmd[0].lower() == "cat":
            try:
                if not self.cat(cmd[1]):
                    logger_main.error(f'cat command cause an error : Error while opening {cmd[1]}.')
                    print(f'Error while opening {cmd[1]}.')
            except:
                self.cat("")
#-------------------------exit-------------------------
        elif cmd[0].lower() == 'exit':
            exit()
        else:
                logger_main.error(f"Unknown command")
                print('Unknown command.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="VM")
    parser.add_argument('--archive', help="Path to the filesystem archive.")
    parser.add_argument('--script', help="Path to a script file containing commands.")
    parser.add_argument('--logging', help="Path to a logger file.")
    parser.add_argument('--test', help="Start test commands.")
    args = parser.parse_args()
    
    logger_main = logging.getLogger(__name__)
    logger_main.setLevel(logging.INFO)
    handler_main = logging.FileHandler(args.logging, mode='w')
    formatter_main = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_main.setFormatter(formatter_main)
    logger_main.addHandler(handler_main)
    
    vm = VM(args.archive)
    if args.script:
        vm.run_script(args.script)
    elif args.test:
        vm.test_commands()
    else:
        vm.start()