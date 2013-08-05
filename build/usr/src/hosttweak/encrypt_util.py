#-*- coding:utf-8 -*-
import hashlib

class EncryptUtil:
    
    @staticmethod
    def md5(str):
        md5 = hashlib.md5()
        md5.update(str)
        return md5.hexdigest()
    
    
if(__name__ == "__main__"):
    print EncryptUtil.md5("thebye85")