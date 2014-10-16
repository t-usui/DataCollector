#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import shutil
import sys


class ProjectDistinguisher(object):
    
    def __init__(self):
        self.mingw_project_dir = 'D:\\Workspace\\MinGW'
        self.msvc_project_dir = 'D:\\Workspace\\MSVC++'
        self.cmake_project_dir = 'D:\\Workspace\\CMake'
        self.bat_project_dir = 'D:\\Workspace\\bat'
        self.unknown_project_dir = 'D:\\Workspace\\Unknown'
    
    def __del__(self):
        pass
    
    def distinguish(self, parent_dir_name):
        dir_name_list = os.listdir(parent_dir_name)
        
        for dir_name in dir_name_list:
            self.classify_file(dir_name)
    
    def does_makefile_exist(self, dir_path):
        makefile_pattern = 'Makefile|makefile'
        return self.search_file_from_dir(dir_path,
                                         makefile_pattern)
        
    def does_cmakelists_exists(self, dir_path):
        cmakelists_pattern = 'CMakeLists'
        return self.search_file_from_dir(dir_path,
                                         cmakelists_pattern)
        
    def does_vcproj_file_exist(self, dir_path):
        vcproj_file_name_pattern = '.+\.vcproj|\.vcxproj'
        return self.search_file_from_dir(dir_path,
                                         vcproj_file_name_pattern)
        
    def does_bat_file_exist(self, dir_path):
        bat_file_name_pattern = '.+\.bat'
        return self.search_file_from_dir(dir_path,
                                         bat_file_name_pattern)
    
    def search_file_from_dir(self, root_dir_path, file_name_pattern):
        """
        search file_name_pattern from root_dir_path
        """
        p = re.compile(file_name_pattern)
        
        for dir_path, dir_names, file_names in os.walk(root_dir_path):
            for file_name in file_names:
                if p.search(file_name) is not None:
                    return True
        return False
    
    def classify_file(self, dir_path):
        dir_name = os.path.basename(dir_path)
        if self.does_vcproj_file_exist(dir_path):
            shutil.move(dir_path, os.path.join(self.msvc_project_dir, dir_name))
        elif self.does_makefile_exist(dir_path):
            shutil.move(dir_path, os.path.join(self.mingw_project_dir, dir_name))
        elif self.does_cmakelists_exists(dir_path):
            shutil.move(dir_path, os.path.join(self.cmake_project_dir, dir_name))
        elif self.does_bat_file_exist(dir_path):
            shutil.move(dir_path, os.path.join(self.bat_project_dir, dir_name))            
        else:
            shutil.move(dir_path, os.path.join(self.unknown_project_dir, dir_name))
            
if __name__ == '__main__':
    git_project_dir = 'D:\\Workspace\\git_project'
    
    distinguisher = ProjectDistinguisher()
    
    for dir_name in os.listdir(git_project_dir):
        distinguisher.classify_file(os.path.join(git_project_dir, dir_name))