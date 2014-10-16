#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import subprocess


class CompileAutomator(object):
    
    def __init__(self):
        self.vcupgrade_path = '"C:\\Program Files (x86)\\Microsoft Visual Studio 10.0\\Common7\\Tools\\VCUpgrade.exe"'
        self.msbuild_path = 'C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\MSBuild.exe'
    
    def __del__(self):
        pass
    
    def search_build_file(self, project_dir_path):
        vcproj_file_list = []
        vcxproj_file_list = []
        
        pattern_vcproj = '.+\.vcproj'
        pattern_vcxproj = '.+\.vcxproj'
        
        p_vcproj = re.compile(pattern_vcproj)
        p_vcxproj = re.compile(pattern_vcxproj)
        
        for dir_path, dir_names, file_names in os.walk(project_dir_path):
            for file_name in file_names:
                if p_vcproj.search(file_name) is not None:
                    vcproj_file_list.append(os.path.join(dir_path, file_name))
                elif p_vcxproj.search(file_name) is not None:
                    vcxproj_file_list.append(os.path.join(dir_path, file_name))
                    
        return vcproj_file_list, vcxproj_file_list
    
    def upgrade_vcproj_file(self, file_path):
        command = self.vcupgrade_path + ' ' + file_path
        subprocess.check_output(command, shell=True)
        
        return os.path.splitext(file_path)[0] + '.vcxproj'
        
    def build_vcxproj(self, file_path):
        command = self.msbuild_path + ' ' + file_path
        print command
        subprocess.check_output(command, shell=True)
        
if __name__ == '__main__':
    root_dir_path = 'D:\\Workspace\\buildtest'
            
    automator = CompileAutomator()
    
    for project_dir_name in os.listdir(root_dir_path):
        print project_dir_name
        project_dir_path = os.path.join(root_dir_path, project_dir_name)
        
        # search .vcproj, .vcxproj file in the project
        vcproj_path_list, vcxproj_path_list = automator.search_build_file(project_dir_path)
        
        # upgrade .vcproj file into .vcxproj file if exists
        if vcproj_path_list != []:
            for vcproj_path in vcproj_path_list:
                print vcproj_path
                vcxproj_path = None
                try:
                    vcxproj_path = automator.upgrade_vcproj_file(vcproj_path)
                except:
                    print 'Exception'
                if vcxproj_path is not None and vcxproj_path in vcxproj_path_list is False:
                    vcxproj_path_list.append(vcxproj_path)
                    
        # build project with .vcxproj file if exists
        if vcxproj_path_list != []:
            for vcxproj_path in vcxproj_path_list:
                print vcxproj_path
                try:
                    automator.build_vcxproj(vcxproj_path)
                    print 'Success'
                except:
                    print 'Exception'