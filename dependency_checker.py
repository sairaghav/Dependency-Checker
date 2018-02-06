import os
import subprocess

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


def copyHeaderFile(srcpath,outpath):
    try:
        os.makedirs('\\'.join(outpath.split('\\')[:-1]))
    except:
        pass
    subprocess.Popen(['copy', srcpath, outpath], shell=True)


def findHeaderFiles(root_dir,headers=[],out_dir=''):
    global allFiles
    foundHeaders = []
    
    if headers == []:
        headers = getDependentHeaderFiles(root_dir)

    try:
        len(allFiles)
    except:
        getAllFiles(root_dir)

    for header in headers:
        head = header.replace('/','\\').lower().strip()
        prefix = out_dir
        actual_header = head

        if '..\\' in head:
            index = -(head.count('..\\')+1)
            prefix = '\\'.join(out_dir.split('\\')[:index])
            actual_header = head.replace('..\\','')

        for filename in allFiles:
            try:
                if filename.endswith('\\'+actual_header):
                    if not out_dir == '':
                        outpath = prefix +'\\'+ actual_header
                        copyHeaderFile(filename,outpath)
                    foundHeaders.append(header)
                    break
                
            except:
                pass

    return set(foundHeaders)

 

def findMissingHeaderFiles(root_dir,headers=[]):
    if headers == []:
        headers = getDependentHeaderFiles(root_dir)
        
    foundHeaders = findHeaderFiles(root_dir,headers)
    missingHeaders = set(headers) - set(foundHeaders)

    return set(missingHeaders)
