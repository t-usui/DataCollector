#!/usr/bin/env python
#-*- coding:utf-8 -*-

import commands
import os
import re
import time
import types
import urllib2


class GitCrawler(object):
    
    def __init__(self):
        self.project_dir = '../project'
    
    def __del__(self):
        pass
    
    def crawl_and_clone(self, language, page, query):
        clone_url_list, repo_name_list = self.crawl(language, page, query)
        print clone_url_list
        self.clone_repositry_from_list(clone_url_list, repo_name_list)
    
    def crawl(self, language, page, query):
        clone_url_list = []
        repo_name_list = []
                
        if isinstance(page, types.ListType):
            page_list = page
            for page in page_list:
                search_result = self.search(language, page, query)
                repo_url_list = self.parse_search_result(search_result)
                       
                for url in repo_url_list:
                    clone_url_list.append(self.fetch_clone_url(url))
                    repo_name_list.append(self.lookup_repo_name(url))
                           
        else:
            search_result = self.search(language, page, query)
            repo_url_list = self.parse_search_result(search_result)
            
            for url in repo_url_list:
                self.clone_url_list.append(self.fetch_clone_url(url))
                repo_name_list.append(self.lookup_repo_name(url))
                
        return clone_url_list, repo_name_list
            
    @classmethod
    def search(cls, language, page, query):
        base_url = 'https://github.com/search?l=%s&o=desc&p=%d&q=%s&s=stars&type=Repositories'
        
        search_url = base_url % (language, page, query)
        response = urllib2.urlopen(search_url)
        
        time.sleep(1)
        
        return response.read()
    
    @classmethod
    def parse_search_result(cls, html):
        repo_url_list = []
        
        pattern = '<a href="(.+)" class="css-truncate css-truncate-target">'
        p = re.compile(pattern)
        
        for m in p.findall(html):
            repo_url_list.append('https://github.com' + m)
            
        return repo_url_list
    
    @classmethod
    def fetch_clone_url(cls, repo_url):
        response = urllib2.urlopen(repo_url)
        html = response.read()
        
        time.sleep(1)
        
        pattern = '<input type="text" class="clone js-url-field".+value="(.+)" readonly="readonly">'
        p = re.compile(pattern, re.DOTALL)
        
        m = p.search(html)
        if m is not None:
            return m.group(1)
        else:
            return None
        
    @classmethod    
    def lookup_repo_name(cls, repo_url):
        return repo_url.split('/')[-1]
    
    def clone_repositry(self, clone_url, repo_name):
        clone_command = 'git clone ' + clone_url + ' ' + self.project_dir + os.sep + repo_name
        
        print commands.getoutput(clone_command)
        
    def clone_repositry_from_list(self, clone_url_list, repo_name_list):
        if len(clone_url_list) != len(repo_name_list):
            print 'Error: crawl (clone_repositry_from_list)'
            sys.exit()
        else:
            for clone_url, repo_name in zip(clone_url_list, repo_name_list):
                self.clone_repositry(clone_url, repo_name)
