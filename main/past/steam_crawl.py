# -*- coding: utf-8 -*-
"""
File Name：     main
Description :
Author : mengzhihao
date：          2018/11/20
淘宝地址 :https://shop560916306.taobao.com/?spm=2013.1.1000126.2.3418ab83wv5Ai2
"""


# from crawl_tool_for_py3 import crawlerTool # 自己写的一个工具类
import pdb
#import multiprocessing
#import gevent
#from gevent import socket,monkey,pool    #导入pool
import time
import queue
import re
#monkey.patch_all()
#gevent.monkey.patch_all(thread=False, socket=False, select=False) # gevent和multiprocessing同时使用时
ct = crawlerTool()
#pool=gevent.pool.Pool(10) # 有个问题处理不了，queue写文件问题
result_queue = queue.Queue()
task_flag=True

import csv

output_csv = open('steam_result.csv','w',newline='')
csv_writer =  csv.writer(output_csv)
csv_writer.writerow(['name','url','languages','require_os','achievements','types','types_num','score'])
def main():
    global task_flag
    urls=[]
    for page in range(1,1298,1):
        url = 'https://store.steampowered.com/search/?sort_by=&sort_order=0&special_categories=&tags=492&page=%s&l=english'%page
        #urls.append(url)
        print('page=%s'%page)
        try:
            search_page(url)
        except Exception as e:
            print(e)


def search_page(url):
    page_buf = ct.sget(url).decode('utf8')
    segments = crawlerTool.getXpath('//div[@id="search_result_container"]/div/a', page_buf)
    for segment in segments:
        title = crawlerTool.getXpath('//span[@class="title"]/text()', segment)
        href = crawlerTool.getXpath('//a/@href', segment)[0]
        print(title, href)
        try:
            get_page_detail(href)
        except Exception as e:
            print(e)



def get_page_detail(url):
    page_buf = ct.sget(url,cookies={"Steam_Language":"english","birthtime":"725817601","lastagecheckage":"1-January-1993"})
    #print(page_buf)
    name =  crawlerTool.getXpath('//div[@class="apphub_AppName"]/text()', page_buf)[0]
    languages =  crawlerTool.getXpath('//a[@class="all_languages"]/text()', page_buf)
    if languages:
        languages = crawlerTool.getRegex('ee all\s+(\d+)',languages[0])
    else:
        languages = len(crawlerTool.getXpath("//table[@class='game_language_options']//tr[@class='']", page_buf))

    require_os = len(crawlerTool.getXpath('//div[contains(@class,"sysreq_tab" )]',page_buf))
    if not require_os:
        require_os = 1
    achievements = crawlerTool.getXpath("//div[@id='achievement_block']/div/text()", page_buf)
    if achievements:
        achievements = crawlerTool.getRegex('Includes\s+(\d+)',achievements[0])
    else:
        achievements = 0
    types =  crawlerTool.getXpath('//div[@id="category_block"]/div[@class="game_area_details_specs"]//text()', page_buf)
    types = [type.strip() for type in types if type]
    types_num = len(types)
    types= '|'.join(types)
    score =  crawlerTool.getXpath('//div[contains(@class,"score " )]/text()', page_buf)
    if score:
        score = score[0].strip()
    else:
        score = 0
    print(languages,require_os,achievements,types_num,types,score)
    csv_writer.writerow([name, url, languages, require_os, achievements, types, types_num, score])

if __name__ == '__main__':
   # rs = ct.session.get('https://store.steampowered.com/app/477160/Human_Fall_Flat/?snr=1_7_7_230_150_1',cookies={"Steam_Language":"english","birthtime":"725817601","lastagecheckage":"1-January-1993"}) #右上角切换语言
    #print(rs.text)
    #get_page_detail('https://store.steampowered.com/app/252490/Rust/?snr=1_7_7_230_150_1')
    main()