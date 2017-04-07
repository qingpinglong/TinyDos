# login name - fliu988
# This program is my own unaided work, and was not copied,
# (except some parts as allowed to base my work on that distributed
# by the lecturer)
# nor written in collaboration with any other person.
# name: FENG LIU
# UPI: 243390391

#!/usr/bin/env python3
import os
import drive
class Volume:
    """A drive with addtional information"""
    def __init__(self, name):
        """create a drive object by class Drive"""
        self.name = name
        self.count = 1
        dirc = Dir_entry()
        self.v_initial = dirc.volume_initial()  #initialise block 0 content
        self.d_initial = dirc.dir_initial() # initialise the directory entry
        self.vdrive = drive.Drive(self.name)
        self.file = ""
    def format(self):
        """call the drive.format function, add information into block 0"""
        try:
            self.vdrive.format()
            self.vdrive.disconnect()
            self.vdrive.reconnect()
            self.vdrive.file.seek(0)
            self.vdrive.file.write(self.v_initial)
            self.vdrive.disconnect()
        except PermissionError:  
            print("Bad drive name, please try again")
    def reconnect(self, file):
        """reconnect an existing file as a Drive object"""
        if not os.path.exists(file):
            raise IOError("drive does not exist.")
        self.vdrive = drive.Drive(file)
        self.vdrive.reconnect()
    def mkfile(self, file):
        """create a new file with pathname"""
        try:
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            the_bitmap = fn[:128]
            file_path = file.split("/")
            if len(file_path[-1])>8:
                raise IOError("file name too long.")
            real_file = "+".join(file_path)
            if len(file_path)>2: #file inside a nested directory
                with open(file_path[-2], "a+") as the_file:
                    the_file.write("f:"+file_path[-1].ljust(8)+" "+ " "*4+"\n")
                pos = fn.index("d:"+file_path[-2].ljust(8))
                block = fn[pos+16:pos+64].split()
                for i in range(12):
                    if block[i] == "000":
                        the_block = ""
                        for j in range(128):
                            if the_bitmap[j] == "-":
                                self.vdrive.file.seek(j)
                                self.vdrive.file.write("+")
                                the_block += str(j).rjust(3, "0")
                                pos1 = fn.index("** "+str(j-1).rjust(3)+" **")
                                self.vdrive.file.seek(pos1+10)
                                self.vdrive.file.write(str(self.d_initial))
                                self.vdrive.file.seek(pos1+10)
                                self.vdrive.file.write("f:"+file_path[-1].ljust(8))
                                break
                        d_size = int(fn[pos+11:pos+15])+512
                        self.vdrive.file.seek(pos+11)
                        self.vdrive.file.write(str(d_size).rjust(4, "0"))
                        self.vdrive.file.seek(pos+16+4*i)
                        self.vdrive.file.write(the_block)
                        break
                    else:
                        the_block = ""
                        for j in range(3):
                            if block[i][j] != "0":
                                the_block += block[i][j]
                        index1 = fn.index("** " + the_block.rjust(3)+" **")
                        fl = fn[index1-513:index1]
                        if "f:        " in fl:
                            index = len(fn[:index1-513])+fl.index("f:        ")
                            self.vdrive.file.seek(index)
                            self.vdrive.file.write("f:"+file_path[-1].ljust(8))
                            break  
            else: #file at the volume root level
                index = fn.index("f:        ")
                self.vdrive.file.seek(index)
                self.vdrive.file.write("f:"+file_path[-1].ljust(8))
            self.vdrive.disconnect()
            the_file = open(real_file, mode = 'w+')
            the_file.close()
        except PermissionError:
            print("Bad file name, please try again")
    def mkdir(self, file):
        """create a new dirctory"""
        try:
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            the_bitmap = fn[:128]
            file_path = file.split("/")
            if len(file_path[-1])>8:
                raise IOError("file name too long.")
            real_file = "+".join(file_path)
            if len(file_path)>2: #dirctory inside a nested directory
                if not os.path.exists(file_path[-2]):
                    raise IOError("Wrong directory path")
                with open(file_path[-2], "a+") as the_file:
                    the_file.write("d:"+file_path[-1].ljust(8)+" "+ " "*4+"\n")
                pos = fn.index("d:"+file_path[-2].ljust(8))
                block = fn[pos+16:pos+64].split()
                for i in range(12):
                    if block[i] == "000":
                        the_block = ""
                        for j in range(128):
                            if the_bitmap[j] == "-":
                                self.vdrive.file.seek(j)
                                self.vdrive.file.write("+")
                                the_block += str(j).rjust(3, "0")
                                pos1 = fn.index("** "+str(j-1).rjust(3)+" **")
                                self.vdrive.file.seek(pos1+10)
                                self.vdrive.file.write(str(self.d_initial))
                                self.vdrive.file.seek(pos1+10)
                                self.vdrive.file.write("d:"+file_path[-1].ljust(8))
                                break
                        d_size = int(fn[pos+11:pos+15])+512
                        self.vdrive.file.seek(pos+11)
                        self.vdrive.file.write(str(d_size).rjust(4, "0"))
                        self.vdrive.file.seek(pos+16+4*i)
                        self.vdrive.file.write(the_block)
                        break
                    else: 
                        the_block = ""
                        for j in range(3):
                            if block[i][j] != "0":
                                the_block += block[i][j]
                        index1 = fn.index("** " + the_block.rjust(3)+" **")
                        fl = fn[index1-513:index1]
                        if "f:        " in fl:
                            index = len(fn[:index1-513])+fl.index("f:        ")
                            self.vdrive.file.seek(index)
                            self.vdrive.file.write("d:"+file_path[-1].ljust(8))
                            break                            
            else: #directory at the volume root level
                index = fn.index("f:        ")
                self.vdrive.file.seek(index)
                self.vdrive.file.write("d:"+file_path[-1].ljust(8))                         
            self.vdrive.disconnect()
            the_file = open(real_file, mode = 'w+')
            the_file.write("current directory: "+file+"\n")            
            the_file.close()
        except PermissionError:
            print("Bad file name, please try again")        
    def append(self, file, data):
        """write the data into file"""
        try:
            if len(data)> 6144:
                raise IOError("data too many, file overflowed")
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            file_path = file.split("/")
            real_file = "+".join(file_path)
            with open(real_file, "a+") as the_file:
                the_file.write(data)            
            file_name = file_path[-1]
            if not os.path.exists(real_file):
                raise IOError("file does not exist")
            index = 0
            if len(file_path)>2:
                the_dir = file_path[-2]
                pos1 = fn.index("d:"+the_dir.ljust(8))
                block1 = fn[pos1+16:pos1+64].split()
                for h in range(12):
                    if block1[h] != "000":
                        file1 = self.vdrive.read_block(int(block1[h]))
                        if "f:"+file_name.ljust(8) in file1:
                            index = (int(block1[h]))*523 +file1.index("f:"+file_name.ljust(8))
                            break
            else:
                index = fn.index("f:"+file_name.ljust(8))
            block = fn[index+16:index+64].split()
            for i in range(12):
                if block[i] != "000" and len(data)>0:
                    content = self.vdrive.read_block(int(block[i])).rstrip()
                    if len(content)==512:
                        continue
                    elif len(content)+len(data)<=512:
                        self.vdrive.file.seek(0)
                        fn = self.vdrive.file.read()
                        f_size = int(fn[index+11:index+15])+len(data)
                        self.vdrive.file.seek(index+11)
                        self.vdrive.file.write(str(f_size).rjust(4, "0"))                        
                        content+=data + " "*(512-len(content)-len(data))
                        self.vdrive.write_block(int(block[i]), content)
                        data = ""
                        break
                    elif len(content)+len(data)>512:
                        self.vdrive.file.seek(0)
                        fn = self.vdrive.file.read()
                        f_size = int(fn[index+11:index+15])+512-len(content)
                        self.vdrive.file.seek(index+11)
                        self.vdrive.file.write(str(f_size).rjust(4, "0"))
                        temp = content
                        content += data[:512-len(content)]
                        data = data[512-len(temp):]
                        self.vdrive.write_block(int(block[i]), content)
                        continue
                elif block[i] == "000" and len(data)>0:
                    self.vdrive.file.seek(0)
                    the_bitmap = self.vdrive.file.read(128)
                    for j in range(128):
                        if the_bitmap[j] == "-":
                            self.vdrive.file.seek(j)
                            self.vdrive.file.write("+")
                            block[i] = str(j).rjust(3, "0")
                            if len(data)<=512:
                                self.vdrive.file.seek(0)
                                fn = self.vdrive.file.read()
                                f_size = int(fn[index+11:index+15])+len(data)
                                self.vdrive.file.seek(index+11)
                                self.vdrive.file.write(str(f_size).rjust(4, "0"))                                
                                data += " "*(512-len(data))
                                self.vdrive.write_block(j, data)
                                data = ""
                                break
                            else:
                                self.vdrive.file.seek(0)
                                fn = self.vdrive.file.read()
                                f_size = int(fn[index+11:index+15])+512
                                self.vdrive.file.seek(index+11)
                                self.vdrive.file.write(str(f_size).rjust(4, "0"))
                                self.vdrive.write_block(j, data[:512])
                                data = data[512:]
                                break
                else:
                    break
            the_block = ""
            for i in range(12):
                the_block += block[i]+" "
            self.vdrive.file.seek(index+16)
            self.vdrive.file.write(the_block)
            self.vdrive.disconnect()
        except PermissionError:
            print("Bad file name, please try again")
    def print_file(self, file):
        """print the contents of the file"""
        try:
            file_path = file.split("/")
            real_file = "+".join(file_path)            
            if not os.path.exists(real_file):
                raise IOError("file does not exist")
            with open(real_file, "r+") as file:
                line = file.read()
                if len(line) == 0:
                    print("file does not exist")
                else:
                    print(line)
        except PermissionError:
            print("Bad file name, please try again")                
    def ls(self, file):
        """list the directory. if it is empty, list the directory name"""
        try:
            print("\ncurrent directory:", file)
            print("type    name    size")
            print("----  --------  ----")
            file_path = file.split("/")
            file_name = file_path[-1]
            real_file = "+".join(file_path)
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            if file_name != "":
                if not os.path.exists(real_file):
                    raise IOError("directory does not exist")
                index = fn.index("d:"+file_name.ljust(8))            
                block = fn[index+16:index+64].split()            
                for i in range(12):
                    if block[i] != "000":
                        data = self.vdrive.read_block(int(block[i]))
                        for j in range(0, 512, 64):
                            if data[j:j+10] != "f:"+" "*8 and data[j:j+10] != "d:"+" "*8:
                                print("  {0}  {1}  {2}".format(
                                    data[j:j+2], data[j+2:j+10], data[j+11:j+15]))
            else:
                data = fn[128:512]
                for j in range(0, 384, 64):
                    if data[j:j+10] != "f:"+" "*8 and data[j:j+10] != "d:"+" "*8:
                        print("  {0}  {1}  {2}".format(
                            data[j:j+2], data[j+2:j+10], data[j+11:j+15]))
        except PermissionError:
            print("Bad file name, please try again") 
    def delfile(self, file):
        """delete the file"""
        try:
            file_path = file.split("/")
            file_name = file_path[-1]
            real_file = "+".join(file_path)
            if not os.path.exists(real_file):
                raise IOError("file does not exist")
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            the_bitmap = fn[:128]
            index = 0
            if len(file_path)>2:
                the_dir = file_path[-2]
                pos1 = fn.index("d:"+the_dir.ljust(8))
                block1 = fn[pos1+16:pos1+64].split()
                for h in range(12):
                    if block1[h] != "000":
                        file1 = self.vdrive.read_block(int(block1[h]))
                        if "f:"+file_name.ljust(8) in file1:
                            index = (int(block1[h]))*523 +file1.index("f:"+file_name.ljust(8))
                            break
            else:
                index = fn.index("f:"+file_name.ljust(8))
            k = fn[index:].index("\n** ")
            f_block = fn[k-512:k]
            file_block = fn[index+16:index+64].split()
            for i in range(12):
                if file_block[i] != "000":
                    self.vdrive.write_block(int(file_block[i]), " "*512)
                    self.vdrive.file.seek(int(file_block[i]))
                    self.vdrive.file.write("-")
            if len(file_path)>2:
                count = 0
                for m in range(0, 512, 64):
                    if f_block[m:m+10] != "d:"+" "*8 and f_block[m:m+10] != "f:"+" "*8:
                        count += 1
                if count != 1:
                    self.vdrive.file.seek(index)
                    self.vdrive.file.write("f:"+" "*9+"0000:"+"000 "*12)
                else:
                    self.vdrive.file.seek(index)
                    self.vdrive.file.write(" "*512)
                    n = fn[index-7:index-4]
                    self.vdrive.file.seek(int(n))
                    self.vdrive.file.write("-")
                    pos = fn.index("d:"+file_path[-2].rjust(8))
                    block = fn[pos+16:pos+64].split()
                    for i in range(12):
                        if block[i] == n:
                            pos = pos + 16 + i*4
                    self.vdrive.file.seek(pos)
                    self.vdrive.file.write("000")
            else:
                self.vdrive.file.seek(index)
                self.vdrive.file.write("f:"+" "*9+"0000:"+"000 "*12)
            self.vdrive.disconnect()
            os.remove(real_file)
        except PermissionError:
            print("Bad file name, please try again") 
    def deldir(self, file):
        """delete the dirctory"""
        try:
            dir_path = file.split("/")
            dir_name = dir_path[-1]
            real_file = "+".join(dir_path)
            if not os.path.exists(real_file):
                raise IOError("directory does not exist")
            self.vdrive.reconnect()
            fn = self.vdrive.file.read()
            the_bitmap = fn[:128]
            index = 0
            if len(dir_path)>2:
                the_dir = dir_path[-2]
                pos1 = fn.index("d:"+the_dir.ljust(8))
                block1 = fn[pos1+16:pos1+64].split()
                for h in range(12):
                    if block1[h] != "000":
                        file1 = self.vdrive.read_block(int(block1[h]))
                        if "d:"+dir_name.ljust(8) in file1:
                            index = (int(block1[h]))*523 +file1.index("d:"+dir_name.ljust(8))
                            break
            else:
                index = fn.index("d:"+dir_name.ljust(8))
            k = fn[index:].index("\n** ")
            f_block = fn[k-512:k]
            dir_block = fn[index+16:index+64].split()
            for i in range(12):
                if dir_block[i] != "000":
                    data = self.vdrive.read_block(int(dir_block[i]))
                    for j in range(0, 512, 64):
                        if data[j:j+10] != "d:"+" "*8 and data[j:j+10] != "f:"+" "*8:
                            if data[j] == "d":
                                self.deldir(file+"\\"+data[j+2:j+10].strip())
                                self.vdrive.reconnect()
                            elif data[j] == "f":
                                self.delfile(file+"\\"+data[j+2:j+10].strip())
                                self.vdrive.reconnect()
                    self.vdrive.write_block(int(dir_block[i]), " "*512)
                    self.vdrive.file.seek(int(dir_block[i]))
                    self.vdrive.file.write("-")
            if len(dir_path)>2:
                count = 0
                for m in range(0, 512, 64):
                    if f_block[m:m+10] != "d:"+" "*8 and f_block[m:m+10] != "f:"+" "*8:
                        count += 1
                if count != 1:
                    self.vdrive.file.seek(index)
                    self.vdrive.file.write("f:"+" "*9+"0000:"+"000 "*12)
                else:
                    self.vdrive.file.seek(index)
                    self.vdrive.file.write(" "*512)
                    n = fn[k+4:k+7]
                    self.vdrive.file.seek(int(n))
                    self.vdrive.file.write("-")
                    pos = fn.index("d:"+dir_path[-2].ljust(8))
                    block = fn[pos+16:pos+64].split()
                    for i in range(12):
                        if block[i] == n:
                            pos = pos + 16 + i*4
                    self.vdrive.file.seek(pos)
                    self.vdrive.file.write("000")
            else:
                self.vdrive.file.seek(index)
                self.vdrive.file.write("f:"+" "*9+"0000:"+"000 "*12)
            self.vdrive.disconnect()
            os.remove(real_file)
        except PermissionError:
            print("Bad file name, please try again")                         
class Dir_entry:
    """initialise the block content"""
    def __init__(self):
        self.bitmap = "+" + "-"*127
        self.file_name = " "*8
        self.length = "0000:"
        self.file_block = "000 "* 12
        self.file_type = "f:"
        self.dir_entry = self.file_type + self.file_name + " " + self.length +self.file_block
        self.directory = self.bitmap + self.dir_entry*6
    def volume_initial(self):
        """return the content of block 0"""
        return self.directory
    def dir_initial(self):
        """return the content of block of a new dirctory"""
        return self.dir_entry*8
if __name__ == '__main__':
    COMMANDS = ["format", "reconnect", "ls", "mkfile", "mkdir",
                "append", "print", "delfile", "deldir", "quit"]
    volume = None
    while True:
        try:
            command = input()
            if command == "":
                continue
            if " " not in command:
                if command == "quit":
                    break
                else:
                    print("Invalid command")
            else:
                if "\"" in command:
                    index1 = command.index("\"")
                    command1 = command[:index1-1].split()
                    data = command[index1+1:-1]
                else:
                    command1 = command.split()
                order = command1[0]
                file_name = command1[1]
                if order == "format":
                    the_drive = file_name
                    volume = Volume(the_drive)
                    volume.format()
                elif order == "reconnect":
                    the_drive = file_name
                    volume = Volume(the_drive)
                    volume.reconnect(the_drive)
                elif order == "mkfile":
                    volume.mkfile(file_name)
                elif order == "mkdir":
                    volume.mkdir(file_name)
                elif order == "append":
                    volume.append(file_name, data)
                elif order == "print":
                    volume.print_file(file_name)
                elif order == "ls":
                    volume.ls(file_name)
                elif order == "delfile":
                    volume.delfile(file_name)
                elif order == "deldir":
                    volume.deldir(file_name)
                else:
                    print("Invalid command")
        except EOFError:
            break
