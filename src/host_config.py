#-*- coding:utf-8 -*-
import os

"""
host切换工具
@author: thebye85
@date: 2013-06-06


host.conf配置内容格式如下：

[msp开发]
127.0.0.1   xxx
[msp日常]
10.10.10.11   xxx
[msp预发]
174.1.1.1  xxx

"""
class HostConfig:
    
    #配置文件
    default_config_file = os.path.expanduser("~") + "/.hosttweak/host.conf"
    #系统host文件
    system_host_path = "/etc/hosts"
    
    def __init__(self):
        self.configMap = {}
        #判断配置文件是否存在，不存在则初始配置文件
        self.__init_config()
        #加载配置文件
        self.__load_config()
    
            
    #第一次运行，初始配置文件
    def __init_config(self):
        if(os.path.isfile(self.default_config_file)):
            file = open(self.default_config_file)
            fileContent = file.read()
            if(fileContent.count("[") > 0 and fileContent.count("]") > 0):
                return
            
                
        #创建配置文件
        self.__create_config_file()
        #将系统host内容复制到配置文件中
        self.__copy_system_host_to_config()
        
        
    #将系统host内容复制到配置文件中
    def __copy_system_host_to_config(self):
        self.add_or_update_config("default", self.get_system_host())
        
    
    #创建配置文件~/.hosttweak/host.conf
    def __create_config_file(self):
        basedir = os.path.dirname(self.default_config_file)
        if(not os.path.exists(basedir)):
            os.makedirs(basedir)
        if(not os.path.isfile(self.default_config_file)):
            file = open(self.default_config_file, "w")
            file.write("")
            file.close()
            print "create config file success [%s] " %self.default_config_file
    
    
    #获取全部host配置内容
    def __load_config(self):
        file = open(self.default_config_file, "r")
        #key=host名称，value=host内容
        hostName = ""
        hostContent= ""
        for line in file:
            #解析host文件名称
            if(line.startswith("[") and line.endswith("]\n")):
                if(hostName and hostContent):
                    self.configMap[hostName] = hostContent
                hostName = line[1:-2]
                hostContent = ""
            #解析host内容
            else:
                hostContent = hostContent + line
        #添加文件最后一块host配置
        self.configMap[hostName] = hostContent
        
    
    #重新加载配置文件，在配置文件发布变化时调用
    def __reload_config(self):
        self.__load_config()
    
    #将configMap写入到配置文件
    def __write_config_to_file(self):
        if(not self.configMap):
            raise Exception("self.configMap is empty")
        
        fileContent = ""
        #按key排序后写入文件
        keyList = self.configMap.keys()
        keyList.sort()
        for hostName in keyList:
            hostBlock = "[" + hostName + "]\n" + self.configMap[hostName]
            if(not hostBlock.endswith("\n")):
                hostBlock = hostBlock + "\n"
            fileContent = fileContent + hostBlock
        
        #覆盖配置文件内容
        file = open(self.default_config_file, "w")
        file.write(fileContent)
        file.close()
    
    
    #返回hostName列表（已排序）
    def get_host_name_list(self):
        #按key排序
        keyList = self.configMap.keys()
        keyList.sort()
        return keyList
    
    def delete_host(self, hostName):
        #最后一个host不能删除
        if(len(self.configMap) == 1):
            return
        if(self.configMap.has_key(hostName)):
            del self.configMap[hostName]
            self.__write_config_to_file()
            self.__reload_config()
        
    #保存或更新host内容
    def add_or_update_config(self, hostName, hostContent):
        #更新
        if(self.get_config(hostName)):
            self.__update_config_map(hostName, hostContent)
        #新增
        else:
            self.__add_config_map(hostName, hostContent)
        
        #保存配置文件
        self.__write_config_to_file()
        #重新加载配置文件
        self.__reload_config()
    
    
    #返回指定host名称配置内容
    def get_config(self, hostName):
        if(self.configMap.has_key(hostName)):
            return self.configMap[hostName]
        else:
            return ""
    
    
    #返回host配置map
    def get_config_map(self):
        return self.configMap
    
    
    #添加host配置
    def __add_config_map(self, hostName, hostContent):
        #追加到配置文件尾
        self.configMap[hostName] = hostContent
    
    
    #更新指定host配置
    def __update_config_map(self, hostName, hostContent):
        if(self.configMap.has_key(hostName)):
            self.configMap[hostName] = hostContent
        else:
            raise Exception("hostName is not exised|hostName=%s" %hostName)
        
    #获取系统host
    def get_system_host(self):
        file = open(self.system_host_path, "r")
        system_host = file.read()
        file.close()
        return system_host
    
    #写入系统host
    def write_system_host(self, hostContent):
        file = open(self.system_host_path, "w")
        file.write(hostContent)
        file.close()
        
                
if(__name__ == "__main__"):
    hostConfig = HostConfig()
    
    """
    #查询host全部配置
    self.configMap = hostConfig.get_config_map()
    keyList = self.configMap.keys()
    keyList.sort()
    for key in keyList:
        print key + "\n" + self.configMap[key]
    """
    
    
    """
    #修改host配置
    print hostConfig.get_config("msp日常")
    #修改host内容
    hostConfig.add_or_update_config("msp日常", "10.10.10.10    xxx")
    #修改后
    print hostConfig.get_config("msp日常")
    """
    
    
    """
    #增加host配置
    hostConfig.add_or_update_config("msp项目环境", "20.20.20.20    xxx")
    self.configMap = hostConfig.get_config_map()
    keyList = self.configMap.keys()
    keyList.sort()
    for key in keyList:
        print key + "\n" + self.configMap[key]
    """        
    
    
    """
    #获取host名称列表
    keyList = hostConfig.get_host_name_list()
    for hostName in keyList:
        print hostName
    """
    
    HostConfig()
    
    
    
    
