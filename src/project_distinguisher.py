#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os


class ProjectDistinguisher(object):
    
    def __init__(self):
        self.useful_project_dir = '../project/useful'
        self.useless_project_dir = '../project/useless'
    
    def __del__(self):
        pass
    
    def distinguish(self, parent_dir_name):
        dir_name_list = os.listdir(parent_dir_name)
        
        for dir_name in dir_name_list:
            self.classify_file(dir_name)
            
    def is_useful(cls, dir_name):
        if cls.does_makefile_exist(dir_name):
            return True
        else:
            return False
    
    def does_makefile_exist(self, dir_name):
        file_list = os.listdir(self.project_dir + os.sep + dir_name)
        
        if 'Makefile' in file_list:
            return True
        else:
            return False
        
    def classify_file(self, dir_name):
        if self.is_useful(dir_name):
            shutil.move(dir_name, self.useful_project_dir + os.sep + dir_name)
        else:
            shutil.move(dir_name, self.useless_project_dir + os.sep + dir_name)