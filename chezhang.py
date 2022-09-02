import os
import zipfile
import time


class chezhang():
    def __init__(self, rootPath):
        self.rootPath = rootPath
        self.oldStr = '下载完成后用其他软件重命名把最后字母pdf改回压缩包格式即可.pdf'
        self.newStr = '.zip'
        self.txtName = '视频标题在这里.txt'
        self.tempVideoName = '重命名这个文件把abc改回mp4即可播放.abc'

    def invokeFiles(self):
        for file in os.listdir(self.rootPath):
            if os.path.isfile(os.path.join(self.rootPath, file)) == True:
                if file.endswith('.pdf') :
                    if file.find(self.oldStr) > -1:
                        zipfile_name = file.replace(self.oldStr, self.newStr)
                        oldpath = os.path.join(self.rootPath, file)
                        newpath = os.path.join(self.rootPath, zipfile_name)
                        os.rename(oldpath, newpath)
                        self.extraZipFile(newpath)
                        subpath = newpath.replace('.zip', '')
                        self.renFiles(subpath)
                        self.clear(newpath, subpath)
        time.sleep(1000)
        #        print file.split('.')[-1]

    def extraZipFile(self, zipfile_name):
        zip_file = zipfile.ZipFile(zipfile_name)
        try:

            '''
            if os.path.isdir(file_name.split(".")[0]):  
                pass  
            else:  
                os.mkdir(file_name.split(".")[0])
            '''
            for fname in zip_file.namelist():
                if (fname.find(self.txtName) > -1 or fname.find(self.tempVideoName) > -1):
                    zip_file.extract(fname)
                    # 加入到某个文件夹中 zip_file.extract(names,file_name.split(".")[0])
            print('extra done')
            
        except:
            print('ex')
        finally:
            zip_file.close()
            print('zipfile closed')

    def renFiles(self, subpath):
        print(subpath)
        oldVideoPath = os.path.join(subpath, self.tempVideoName)
        newVideoPath = os.path.join(subpath, self.readVname(subpath))+'.mp4'
        print('newVideoPath: ' + newVideoPath)
        os.rename(oldVideoPath, newVideoPath)

    def readVname(self, subpath):
        txtPath = os.path.join(subpath, self.txtName)
        vname = ''
        '''
        if (os.path.isfile(txtPath)):
            with open(txtPath, "r") as f:
                for line in f.readlines():
                    line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                    if (line.find('文件标题') > 0):
                        line.replace('：', ':')
                        vname = line.split("#", 1)[1]
                        print(vname)
                        break
        '''
        f = open(txtPath, 'r')
        try:
            line = f.readline()
            while line:
                line = line.strip('\n')
                #print(line)  # line后面的‘，’将忽略换行符
                if (line.find('文件标题') > -1):
                    line = line.replace('：', ':')
                    list = line.split(":", 1)
                    if(len(list) > 1):
                        vname = list[1]
                    break
                line = f.readline()
        except:
            print('ex2')
        finally:
            f.close()
        if(vname==''):
            vname = os.path.split(subpath)[1]
        return vname

    def clear(self, newpath, subpath):
        txtPath = os.path.join(subpath, self.txtName)
        os.remove(txtPath)
        
        tempDir = os.path.join(self.rootPath, 'temp')
        if not(os.path.exists(tempDir)):
            os.makedirs(tempDir)
        tempFile = os.path.join(tempDir, os.path.split(newpath)[1])
        print(tempFile)
        os.rename(newpath, tempFile)
        
if __name__ == '__main__':
    rootPath = os.getcwd()
    cz = chezhang(rootPath)
    cz.invokeFiles()
