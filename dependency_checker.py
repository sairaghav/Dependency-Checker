import os
from shutil import copyfile

def getAllFiles(root_dir):
    global allFiles
    allFiles = []
    
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            allFiles.append(os.path.join(root,filename))

    allFiles = set(allFiles)
    

def getDependentHeaderFiles(root_dir):
    global allFiles
    headers = []

    try:
        len(allFiles)
    except:
        getAllFiles(root_dir)

    for filename in allFiles:
        if filename.endswith('.c') or  filename.endswith('.cpp') or filename.endswith('.h') or filename.endswith('.hpp'):
            with open(filename,'r') as f:
                for line in f.readlines():
                    if line.strip().startswith('#include'):
                        header = line.split('#include')[1].strip().split()[0]

                        if '"' in header:
                            header = header.replace('"','')
                        if '<' in header:
                            header = header.replace('<','')
                            header = header.replace('>','')
                        if '\\\\' in header:
                            header = header.replace('\\\\','\\')
                        if '//' in header:
                            header = header.replace('//','')
                        if '*/' in header:
                            header = header.replace('*/','')
                        if '/*' in header:
                            header = header.replace('/*','')
                        if header.strip() not in headers:
                            headers.append(header.strip())

    return set(headers)


def copyHeaderFiles(root_dir,headers=[],out_dir=''):
    if headers == []:
        headers = getDependentHeaderFiles(root_dir)

    if out_dir == '':
        out_dir = os.getcwd()

    if os.name == 'nt':
        path_separator = '\\'
    else:
        path_separator = '/'

    for header in headers:
        head = header.replace('/',path_separator).strip()
        prefix = out_dir
        actual_header = head

        if '..'+path_separator in head:
            index = -(head.count('..'+path_separator)+1)
            prefix = path_separator.join(out_dir.split(path_separator)[:index])
            actual_header = head.replace('..'+path_separator,'')

        outpath = prefix +''+path_separator+''+ actual_header

        for filename in allFiles:
            if filename.endswith(path_separator+''+actual_header):
                try:
                    os.makedirs(path_separator.join(outpath.split(path_separator)[:-1]))
                except:
                    pass
                copyfile(filename,outpath)


def findHeaderFiles(root_dir,headers=[]):
    global allFiles
    foundHeaders = []
    
    if headers == []:
        headers = getDependentHeaderFiles(root_dir)

    try:
        len(allFiles)
    except:
        getAllFiles(root_dir)

    if os.name == 'nt':
        path_separator = '\\'
    else:
        path_separator = '/'

    for header in headers:
        head = header.replace('/',path_separator).strip()
        actual_header = head.replace('..'+path_separator,'')

        for filename in allFiles:
            if filename.endswith(path_separator+''+actual_header):
                foundHeaders.append(header)
                break

    return set(foundHeaders)

 

def findMissingHeaderFiles(root_dir,headers=[]):
    if headers == []:
        headers = getDependentHeaderFiles(root_dir)
        
    foundHeaders = findHeaderFiles(root_dir,headers)
    missingHeaders = set(headers) - set(foundHeaders)

    return set(missingHeaders)

