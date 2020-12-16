# -*- coding:utf-8 -*-
'''
----------------------------
@Author: Hairong Wu
@time: 11/23/2020
----------------------------
'''

# ## This make sure you login your steam account :)
# import steam_login
# steam_login.main()

import time
import re
import csv
import requests as rq
from bs4 import BeautifulSoup as bs

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
HEADERS = {
    "Referer": "https://steamcommunity.com/id/AMD_Shanghai/games/?tab=all",
    # "sec-ch-ua": "\"Chromium\";v=\"86\", \"\\\"Not\\\\A;Brand\";v=\"99\", \"Google Chrome\";v=\"86\"",
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

def file_initialization(account_name):
    '''
    This function initialize an output file for an account.
    - @INPUT: a Steam account name
    - @OUTPUT PATH: "./outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''
    output_file = open("./outputs/" + account_name + ".csv", "w", newline="")
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["app_id", "name", "time", "API", "DEV_Build"])
    return csv_writer

def single_crawler(account):
    '''
    This function do web crawling on a single Steam account.
    It will initialize the output file using file_initialization() function and then right infos in the output file.
    - @INPUT: a Steam account name
    - @OUTPUT PATH: "./outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''
    csv_writer = file_initialization(account)

    url = "https://steamcommunity.com/id/%s/games/?tab=all"%account

    # Start Crawler
    try:
        # html = urllib2.urlopen(url, timeout=12)
        html = rq.get(url, headers=HEADERS).text

        soup = bs(html, "html.parser")

        for div in soup.find_all("div", class_="gameListRow"):
            # Get APP id
            app_id = div["id"]
            app_id = re.findall(r"\d+", app_id)

            div_tmp = div.find("div", class_="gameListRowItem")
            game_name = div_tmp.find("div", class_="gameListRowItemName ellipsis ").text
            game_time = div_tmp.find("h5", class_="ellipsis hours_played ").text
            game_time = re.findall(r"\d+.\d+|\d+", game_time)
            csv_writer.writerow([app_id, game_name, game_time, "", ""])
    except Exception as e:
        mistaken(e)
        time.sleep(1)

def list_crawler():
    '''
    This Function would crawl a list of Steam accounts.
    THis function utilize single_crawler() to analysis each Steam accounts
    - @OUTPUT PATH: "./outputs/"
    - @OUTPUT NAME: {SteamAccountName}.csv
    '''
    tar_file = input("Please ENTER the text file with Steam account names you want to crawl: ")

    try:

        with open("data.txt","r") as f:    #设置文件对象
            for line in f.readline():
                line=line.strip("\n")
                if line is None or line == "":
                    continue
                else:
                    single_crawler(line)
    except Exception as e:
        mistaken(e)
        time.sleep(1)

def end_program():
    '''
    This program is simply using a while loop to as for user's interaction on whether to quit the program.
    '''
    print("\n\n** Do you want to crawl again? **\n")
    print("Press \"y/Y\" to crawl again;")
    print("Press \"q/Q\" to QUIT;")
    inputs = input("INPUT: ")
    while True:
        if inputs == "y" or inputs == "Y":
            return True;
        elif inputs == "q" or inputs == "Q":
            return False;
        else:
            # TODO
            print("\n** Incorrect inputs !!! Please enter again :( **\n\n")
            print("Press \"y/Y\" to crawl again;")
            print("Press \"q/Q\" to QUIT;")
            inputs = input("INPUT: ")

def start():
    '''
    This function start the all program features.
    '''
    print("****************************************")
    print("This program can craw a single Steam Account's INFO, or a list or Steam Accounts")
    print("****************************************\n\n")

    print("# If you want to crawl a SINGLE Steam Account's INFO, please ENTER \"1\";")
    print("# If you want to crawl a LIST Steam Accounts, please ENTER \"2\";")
    print("# If you want to QUIT the program, please ENTER \"q/Q\";")
    target_type = input("INPUT: ")

    if target_type == "q" or target_type == "Q":
        return None

    program_flag = True
    while program_flag:
        if target_type == "1":
            print("\n********** You"ve chosen to crawl a single account !!! **********\n")
            account = input("\nEnter the account name you want to analysis: ")
            single_crawler(account)
            end_program()
        elif target_type == "2":
            print("\n********** You"ve chosen to crawl a list of account !!! **********\n")
            list_crawler()
        else:
            # TODO
            print("\n** Incorrect inputs !!! Please enter again :( **\n\n")
            print("# If you want to crawl a SINGLE Steam Account's INFO, please ENTER \"1\";")
            print("# If you want to crawl a LIST Steam Accounts, please ENTER \"2\";")
            program_flag = input("INPUT: ")

def main():
    '''
    This is a main function for this web Crawling program.
    '''
    start()

if __name__ == "__main__":
    main()

# https://steamcommunity.com/id/{Account_Name}}/games/?tab=all