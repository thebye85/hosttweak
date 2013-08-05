#-*- coding:utf-8 -*-
import os
from host_config import HostConfig
from encrypt_util import EncryptUtil

"""
host切换工具
@author: thebye85
@date: 2013-06-06
"""
class HostTweakHandler:
	
	def __init__(self):
		#配置文件处理类
		self.hostConfig = HostConfig()
		
	#返回当前系统host
	def get_system_host(self):
		return self.hostConfig.get_system_host()
	
	#写入当前系统host
	def set_system_host(self, hostContent):
		self.hostConfig.write_system_host(hostContent)
	
	#获取全部host选项
	def get_all_host_select_options(self):
		return self.hostConfig.get_host_name_list()
	
	#使用当前host，将内容写入系统host文件
#	def use_host(self, hostContent):
#		self.hostConfig.write_system_host(hostContent)
	
	#删除host
	def delete_host(self, hostName):
		self.hostConfig.delete_host(hostName)
		
	
	#读取目标host内容
	def read_host(self, hostName):
		hostContent = self.hostConfig.get_config(hostName)
		print "read_host: %s\n%s" %(hostName, hostContent)
		self.hostConfig.write_system_host(hostContent)
		return hostContent
	
	
	#保存host内容
	def save_host(self, hostName, hostContent):
		print "save host: %s\n%s" %(hostName, hostContent)
		#保存到配置文件
		self.hostConfig.add_or_update_config(hostName, hostContent)
		#保存到系统host
		self.hostConfig.write_system_host(hostContent)
	
	
	#另存为新host内容，返回True保存成功，False保存失败
	def save_new_host(self, hostName, hostContent):
		print "save new host: %s\n%s" %(hostName, hostContent)
		self.hostConfig.add_or_update_config(hostName, hostContent)
	
	#查询与系统host相同的host配置名称
	def get_host_name_equals_system_host(self):
		systemHostMd5 = EncryptUtil.md5(self.get_system_host())
		configMap = self.hostConfig.get_config_map()
		keyList = configMap.keys()
		keyList.sort()
		for hostName in keyList:
			hostConent= configMap[hostName]
			hostContentMd5 = EncryptUtil.md5(hostConent)
			print "hostName: %s, md5: %s" %(hostName, hostContentMd5)
			if(systemHostMd5 == hostContentMd5):
				return hostName
		return None
		
		
		
	