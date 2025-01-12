#file  -- pages.py --
# import time
# import docx
#import io
import os
# import json
# import re
# import UI_layout

# from docx.shared import Inches
global pages
pages = []
def setPages(xmlFiles__):
    try:
        for root_, dirs, files in xmlFiles__:
            for item_ in dirs:
                if item_ == 'data':
                    d_path = os.path.join(root_, item_)
                    for path in os.listdir(d_path):
                        if path == 'js':
                            getDirPath = os.path.join(d_path, path)
                        # check if current path is a file
                            for dir_ in os.listdir(getDirPath):
                                jsName = dir_
                                str1 = ''
                                if jsName == 'data.js':
                                    with open(os.path.join(getDirPath, jsName), 'r', encoding='utf-8', errors='ignore') as file:
                                        for line in file:
                                            data_js = str1.join(line)
                                            data_js = data_js.split('"html5url":"')
                                            for i, data in enumerate(data_js):
                                                if i != 0:
                                                    pages.append(data.split('","title":')[0])
                                                    #print(data.split('","title":')[0])
    except Exception as e:
        print(f'issue in lesscss{e}')