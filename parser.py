import os
import sys
import re
from collections import Counter, defaultdict
from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


class Parser:

    def __init__(self, path_to_the_file):
        self.t = 0
        self.filename = path_to_the_file
        self.sep = '\n'
        self.filename_version = "version_pip.txt"

    def read_csv(self):
        self.lst=[]
        with open(self.filename, 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                buf = line
                self.lst.append(buf)
                self.res[buf[0]] = buf[1]
        # print(self.lst)
     
    def parse_library(self, val, html_soup):
        lib = html_soup.find('h1', class_="package-header__name").text
        return lib

    def parse_data(self, val, html_soup):
        data = html_soup.find('p', class_="package-header__date").text
        return data

    def parsing(self):
        c = Counter()
        li=self.lst
        li = [line.rstrip() for line in li]
        info = []
        sl = {}
        for val in li:
            # ib = self.lst[val]
            try:
                url = f'https://pypi.org/project/{val}/'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            dir = self.parse_library(val, html_soup)
            data = self.parse_data(val, html_soup)
            data =data.replace("\n        Released: \n  ", "")
            data =data.replace("\n\n", "")
            c[dir] = +1
            dir =dir.rstrip("\n        ")
            dir =dir.replace("\n        ", "")
            info.append(dir)
            sl[dir] = data
            print(dir, "," ,data)
            # print(dir)
        # print(c.most_common(n))
        return sl
    
    def read_txt(self):
        self.version=[]
        with open(self.filename_version, 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                buf = line.split(" , ")
                self.version.append(buf[0])
        for val in self.version:
            print(val)
    
    def version_and_name(self):
        self.vers=[]
        self.names=[]
        with open("text1.txt", 'r') as csv_file:
            self.res = {}
            i = 1
            for line in csv_file:
                buf = line.split(" ")
                self.vers.append(buf[1])
                self.names.append(buf[0])
        # for val in self.vers:
        #     print(val)
        # for val in self.names:
        #     print(val)
        # print(self.vers)

    def parse_install_url(self, val, html_soup):
        lib = html_soup.find('div', id="files")
        return lib

    def parse_html_req(self, dir):
        mylist = []
        links = []
        with open("t.txt", 'r') as csv_file:
            for line in csv_file:
                r = re.compile('(?<=href=").*?(?=")')
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
                mylist.append(urls)
        for x in mylist:
            for l in x:
                if len(l) >  1:
                    links.append(l)
        return(links)
            
    def parsing_version(self):
        ver = self.vers
        name = self.names
        ver = [line.rstrip() for line in ver]
        name = [line.rstrip() for line in name]
        info = []
        i = 0
        for ver_ in ver:
            # ib = self.lst[val]
            try:
                url = f'https://pypi.org/project/{name[i]}/{ver_}/#files'
            except:
                raise ValueError("404")
            response = requests.get(url)
            html_soup = BeautifulSoup(response.text, 'html.parser')
                # print(html_soup)
            self.dir = self.parse_install_url(ver_, html_soup)
                # print(self.dir)
            self.data = self.parse_html_req(self.dir)
                # data =data.replace("\n        Released: \n  ", "")
                # data =data.replace("\n\n", "")
                # dir =dir.rstrip("\n        ")
                # dir =dir.replace("\n        ", "")
            info.append(dir)
            print(name[i], ", ", ver_)
            for line in self.data:
                print(line)
            if (len (ver) < i):
                i += 1
            # print(dir)
        # print(c.most_common(n))
    
if __name__ == "__main__":

    l = Parser("names.csv")
    # l.read_csv()
    # l.parsing()
    # l.read_txt()
    l.version_and_name()
    l.parsing_version()
