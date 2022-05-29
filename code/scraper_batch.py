
# -*- coding: utf-8 -*-
import requests
import time
import random
import re
import csv
import os
import pandas as pd
import numpy as np


class Spider(object):
    def get_ua(self):
      first_num = random.randint(70, 88)
      third_num = random.randint(0, 3800)
      fourth_num = random.randint(0, 140)
      os_type = [
      '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
      '(Macintosh; Intel Mac OS X 10_14_5)'
      ]
      chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

      ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
            '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
            )
      headers = {"user-agent": ua}
      return headers
    
    def stmp_date(self, stmp):  
      """
      Turn seconds into %Y-%m-%d date.
      """
      stmp = float(str(stmp)[:10])
      stmp1 = stmp + 604800
      timeArray = time.localtime(stmp)
      start_date = time.strftime("%Y-%m-%d", timeArray)
      timeArray1 = time.localtime(stmp1)
      end_date = time.strftime("%Y-%m-%d", timeArray1)
      #date = '%s~%s' % (otherStyleTime, otherStyleTime1)
      return (start_date,end_date)
	
    def get_detail(self, url, name):
      """
      url: a string containing the url to be scraped.
      name: a string containing the name of the youtube channel as shown in the url.
      """
      text = requests.get(url, headers=self.get_ua(), timeout=10).text
      # the pattern containing the data of interest
      pattern="series: \[\{ name: '"+name+"',.*?data: (\[.*?)navigation"
      p1 = re.compile(pattern, re.S)
      t1 = re.findall(p1, text)[0].strip()[:-1]
      n1 = re.findall(p1, text)[1].strip()[:-1]
      p2 = re.compile('\[(\d+?),(\d+?)\]')
      # weekly subscribers
      t2 = re.findall(p2, t1)
      # weekly views
      n2 = re.findall(p2, n1)
      start_dates = []
      end_dates=[]
      a = []
      b = []
      for i in t2:
        start_date,end_date = self.stmp_date(i[0])
        value = i[1]
        
        start_dates.append(start_date)
        end_dates.append(end_date)
        a.append(value)
      for j in n2:
        value = j[1]
        b.append(value)
      title = ['start_date','end_date', 'weekly_subscribers', 'weekly_views']
      aa = [title]
      length = np.min([len(start_dates),len(end_dates),len(a),len(b)])
      for i in range(length):
        tmp = [start_dates[i], end_dates[i], a[i], b[i]]
        #print(tmp)
        aa.append(tmp)
      return aa

    def write_data(self):
      # get directory of the current file
      file_dir = os.path.dirname(os.path.realpath(__file__))
      # switch working directory to data directory
      main_dir = os.path.dirname(file_dir)
      os.chdir(main_dir + '/data')
      # read library.csv that contains all the urls/names to be scraped
      library = pd.read_csv('library.csv')
      for index, row in library.iterrows():
        url = row['url']
        name = row['name']
        category = row['category']
        category_path = main_dir+'/data/'+category
        # make a folder for each category of youtubers
        if not os.path.isdir(category_path):
          os.makedirs(category)
        data = self.get_detail(url,name)
        print(f'{category}_{name} is scraped.')
        # write to csv
        if not os.path.exists(category_path+'/'+name+'.csv'):
          with open('{}/{}.csv'.format(category,name), 'w', encoding='utf-8-sig') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(data)


if __name__ == "__main__":
  spider = Spider()
  spider.write_data()
