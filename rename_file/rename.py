import os,sys

if __name__ == '__main__':
    for dirPath, dirNames, fileNames in os.walk("."):
        for f in fileNames:
            if(str(f)=='rename.py'):
               print('')
            else:
               if(str(sys.argv[1])=='del'):
                   oscmd = 'rm '+str(f)
               else:
                   oscmd = 'mv '+str(f)+' TEG-'+str(f)
               os.system(oscmd)
    print('all finish')
