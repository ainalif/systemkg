# -*- coding: utf-8 -*-
import subprocess, os

softPath = r"C:\Program Files\Microsoft Visual Studio 10.0\VC\bin\dumpbin.exe"

def dumpbin(option, argv):
    if option is None or argv is None:
        return None
    proc = subprocess.Popen([softPath, option, argv],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)
    return proc.stdout.readlines()

def dependents(argv):
    if argv is None:
        return None
    lines = dumpbin('/DEPENDENTS', argv)
    res = []
    for line in lines:
        str = bytes.decode(line).strip()
        if str.endswith(('.dll', '.DLL')) and not str.startswith('Dump'):
            res.append(str.lower())
    return res

def exports(argv):
    if argv is None:
        return None
    lines = dumpbin('/EXPORTS', argv)
    res = []
    for line in lines:
        str = bytes.decode(line).strip()
        sp = str.split(' ')
        if sp.count('') == 3:
            res.append(sp[-1])
    return res

def imports(argv):
    if argv is None:
        return None
    lines = dumpbin('/IMPORTS', argv)
    res = {}
    arg = ''
    for line in lines:
        str = bytes.decode(line).strip()
        sp = str.split(' ')
        if len(sp) == 1 and str.endswith(('.dll', '.DLL')):
            res[str] = []
            arg = str
        elif sp.count('') == 3:
            res[arg].append(sp[-1])
    return res

def walk(folder):
    res = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.dll', '.DLL')):
                res[file] = os.path.join(root,file)
    return res

arg = r'C:\Windows\System32\acledit.dll'

# C:\Program Files\Microsoft Visual Studio 10.0\VC\bin
# >dumpbin /DEPENDENTS "C:\Windows\System32\acledit.dll"
if __name__ == '__main__':
    # res = exports(arg)
    # print(res)
    res = walk('C:\Windows')
    print(res)
    print(len(res))

