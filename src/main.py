#!/usr/bin/env python
#-*- coding:utf-8 -*-

from git_crawler import GitCrawler

if __name__ == '__main__':
    crawler = GitCrawler()
    
    language = 'C'
    page = range(1, 101)
    query = 'Windows'
    
    crawler.crawl_and_clone(language, page, query)