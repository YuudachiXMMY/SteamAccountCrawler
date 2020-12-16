# coding=utf-8
'''
----------------------------
@Author: Hairong Wu
@time: 11/23/2020
----------------------------
'''

# ## This make sure you login your steam account :)
# import steam_login
# steam_login.main()

import os
from sys import flags
import time
import re
import csv
import requests as rq
from bs4 import BeautifulSoup as bs

version = "0.1.2"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
HEADERS = {
    "method": "GET",
    # "path": "/calculator/76561198025085898", # name2
    "Referer": "https://steamdb.info/",
    "User-Agent": USER_AGENT,
    "X-Requested-With": "XMLHttpRequest"
    }

def mistaken(e):
    '''
    This function make sure the program will keep running while an exception occurred
    '''
    print ("a", str(e))
    # try:
    #     print("*****循环跳过，本页无内容*****")
    #     ######采集代码##########
    #     print ("a", str(e))
    #     ########################
    #     print("——————————正常运行——————————")
    # except:
    #     mistaken()

def chooseLanguage():
    '''
    This function allows user to choose program language
    '''
    global language
    language = "en"
    print("Which language do you prefer?")
    print("ENTER \"1\" for ENGLISH")
    print("输入 \"2\" 使用中文")
    tmp = input("> ")
    if tmp == "1":
        language = "en"
    elif tmp == "2":
        language = "cn"
    return language

def whtsNew():
    if language == "en":
        print("- fix a small bug;")
        print("- add Chinese User Interface.")
        print("- add instructions for crawling a file of accounts.")
    elif language == "cn":
        print("- 修复了几个小bug；")
        print("- 实装了中文界面。")
        print("- 新增了文件爬取指引。")

def printHear():
    if language == "en":
        print("\n********************************************************************************")
        print("THIS PROGRAM IS FOR AMD INTERNAL USE ONLY")
        print("version:%s\n"%version)
        print("This program can craw a single Steam Account's INFO, or a list or Steam Accounts\n")
        whtsNew()
        print("********************************************************************************\n")
    elif language == "cn":
        print("\n********************************************************************************")
        print("！！！此程序仅供AMD内部使用！！！")
        print("版本:%s\n"%version)
        print("此程序可以爬取SteamDB上的账号信息，可以输入单个账号进行爬取，或者爬取一个文件(.txt)内所有账号的信息。\n")
        print("本次更新内容:")
        whtsNew()
        print("********************************************************************************\n")

def crawlAgain():
    if language == "en":
        print("\n\n** Do you want to crawl again? **\n")
        print("Press \"y/Y\" to crawl again;")
        print("Press \"q/Q\" to QUIT.")
    elif language == "cn":
        print("\n\n** 是否再次爬取? **\n")
        print("输入 \"y/Y\" 再次爬取;")
        print("输入 \"q/Q\" 推出程序。")

def crawlType():
    if language == "en":
        print("# If you want to crawl a SINGLE Steam Account's INFO, please ENTER \"1\";")
        print("# If you want to crawl a LIST Steam Accounts, please ENTER \"2\";")
        print("# If you want to QUIT the program, please ENTER \"q/Q\";")
    elif language == "cn":
        print("# 爬取单个账户的信息，请输入 \"1\";")
        print("# 爬取一个文件(.txt)内所有账号的信息，请输入 \"2\";")
        print("# 若要退出程序，请输入 \"q/Q\";")

def invalidInput():
    if language == "en":
        print("\n\n****************************************")
        print("** Invalid inputs !!! Please enter again :( **\n")
    elif language == "cn":
        print("\n\n****************************************")
        print("** 非法输入！！！请重新输入 :( **\n")

def file_initialization(account_name):
    '''
    This function initialize an output file for an account.
    - @INPUT: a Steam account name
    - @OUTPUT PATH: "../outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''
    # output_path = os.path.dirname(os.getcwd())
    output_path = os.getcwd()
    output_file = open(output_path+"\\\\outputs\\%s.csv"%(account_name), "w", encoding="utf-8", newline="")
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["app_id", "name", "time", "API", "DEV_Build", "Rating", "Price", "Price / Hour"])
    return csv_writer

def single_crawler(account, list_crawling=False):
    '''
    This function do web crawling on a single Steam account.
    It will initialize the output file using file_initialization() function and then right infos in the output file.
    - @INPUT: a Steam account name
    - @OUTPUT PATH: "./outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''

    url = "https://steamdb.info/calculator/?player=%s&cc=cn"%(account)

    # Start Crawler
    try:
        html = rq.get(url, headers=HEADERS)
        # html.encoding = 'gb2312'
        html = html.text

        soup = bs(html, "html.parser")
        csv_writer = file_initialization(account)

        c = 1

        for tr in soup.find_all("tr", class_="app"):
            # Get APP id
            app_id = tr["data-appid"]
            game_name = str.strip(tr.find("td", class_="text-left").text)
            game_time = tr.find_all("td")[4 :: 5][0].text

            game_rating = tr.find_all("td")[5 :: 6][0].text

            game_price = tr.find_all("td")[3 :: 4][0].text
            game_price_hour = tr.find_all("td")[2 :: 3][0].text

            if not list_crawling:
                print("......Writing {c}th row on: {account}".format(c=c, account=account) )
            csv_writer.writerow([app_id, game_name, game_time, "", "", game_rating, game_price, game_price_hour])
            if not list_crawling:
                print("{game_name} was written on {c} row !!!".format(game_name=game_name, c=c))

            c = c + 1

        print("\n\nSuccessfull Crawlled for account: %s !!!\n\n"%(account))
    except Exception as e:
        mistaken(e)
        time.sleep(1)

def list_crawler(tar_file):
    '''
    This Function would crawl a list of Steam accounts.
    THis function utilize single_crawler() to analysis each Steam accounts
    - @OUTPUT PATH: "./outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''
    try:
        with open(tar_file,"r") as f:    #设置文件对象
            for line in f.readlines():
                line=line.strip("\n")
                if line is None or line == "":
                    continue
                else:
                    single_crawler(line)
    except Exception as e:
        mistaken(e)
        time.sleep(1)

def end_program():
    '''`
    This program is simply using a while loop to as for user's interaction on whether to quit the program.
    '''
    crawlAgain()
    inputs = input("> ")
    while True:
        if str.lower(inputs) == "y":
            return True;
        elif str.lower(inputs) == "q":
            return False;
        else:
            # TODO
            invalidInput()

            crawlAgain()
            inputs = input("> ")

def start():
    '''
    This function start the all program features.
    '''
    printHear()

    program_flag = True
    while program_flag:

        target_type = ""

        crawlType()

        target_type = input("> ")

        if str.lower(target_type) == "q":
            return None
        if target_type == "1":
            if language == "en":
                print("\n********** You've chosen to crawl a single account !!! **********\n")
                account = input("Enter the account name you want to analysis: ")
            elif language == "cn":
                print("\n********** 您选择了爬取单个账户信息！！！ **********\n")
                account = input("请输入您Steam的用户名: ")
            single_crawler(account)
            program_flag = end_program()
        elif target_type == "2":
            tar_file = ""
            if language == "en":
                print("\n********** You've chosen to crawl a list of account !!! **********\n")
                print("可输入：")
                print("  1.accounts.txt (content within this file can be updated with your own accounts)；")
                print("  2.A file with a relative path under current working directory;")
                print("  3.A file under an absolute path。\n")
                cur_path = os.getcwd()
                print("Current Path：%s"%cur_path)
                tar_file = input("Please ENTER the text file with Steam account names you want to crawl: ")
            elif language == "cn":
                print("\n********** 您选择了爬取一个文件内所有账号的信息！！！ **********\n")
                print("可输入：")
                print("  1.accounts.txt(可更新此文件内的账号信息)；")
                print("  2.一个当前路径下相对路径内的文件;")
                print("  3.一个绝对路径下的文件。\n")
                cur_path = os.getcwd()
                print("当前路径：%s"%cur_path)
                tar_file = input("请选择您要爬取的文件名(.txt): ")
            list_crawler(tar_file)
            program_flag = end_program()
        else:
            invalidInput()
            crawlType()
            program_flag = input("> ")

def main():
    '''
    This is a main function for this web Crawling program.
    '''
    language = chooseLanguage()
    start()

if __name__ == "__main__":
    main()

# https://steamcommunity.com/id/{Account_Name}}/games/?tab=all