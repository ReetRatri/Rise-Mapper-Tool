import difflib
from difflib import Differ
import re
import os
import time
import read_SB
import webbrowser
import pages
import exportContent
import server
from bs4 import BeautifulSoup

# location = read_SB.downloads_path
slideCount = pages.pages
global idx
global video_check
video_check= False
idx = 0
a=[]
def compareText(courseTxt, storyboardTxt, file_path):
            print(file_path)
    # start = time.time()
            #print(courseTxt)
            #print(storyboardTxt)
            # a.append(idx)
            # # print(idx)
            # sg.popup(a)
            path = os.getcwd() + '/' + file_path
            #print(slideCount)
            SBPath = storyboardTxt
            StoryPath = courseTxt

            # SBPath = path + 'Storyboard_slide_1.txt'
            # StoryPath = path + 'Storyline_slide_1.txt'


            try:
                sf = open(SBPath,'r', encoding='UTF8').readlines()
                print('-------------------this is  sb--------------------------')
                # print(sf)
            except FileNotFoundError:
                print(f"The file '{SBPath}' does not exist.")
                return "This screen is not part of SB"
            try:
                ff = open(StoryPath,'r+', encoding='utf-8').readlines()
                # if "(opens in a new tab)\n" in ff or "(opens in a new tab)" in ff:
                #     ff = [item.replace("(opens in a new tab)\n", "").replace("(opens in a new tab)", "") for item in ff]





            except FileNotFoundError:
                print(f"The file '{StoryPath}' does not exist.")
                return "This screen is not part of SB"

            #ff = open(SBPath,'r').readlines()
            #ff_is_video=ff
            #ff_is_video=set(ff_is_video)
            #ff_is_video=list(ff_is_video)

            #ff_is_video.remove('Storyline Content\n')
            #ff_is_video.remove('\n')
            #ff_is_video.remove("slide_"+str(idx+1)+'\n')
            # if ff_is_video==[]:
            #     val_4_test=exportContent.val_4_test
            #     val_4_test=val_4_test.split('/')[-1]
            #     video_check=True
            #     ff.remove('\n')
            #     ff.append('VIDEO')



            html = difflib.HtmlDiff()

            html._styles = html._styles + """
            .diff_next {background-color:#c0c0c0}
            .diff_add {background-color:#fff26a}
            .diff_chg {background-color:#ffffff}
            .diff_sub {background-color:#ffaaaa}
            td[nowrap="nowrap"] {
                white-space:normal !important;
                word-break: break-word;
                min-width: 700px;
                max-width: 800px;
                font-family: Coda, sans-serif !important;
                padding:5px 5px 5px 10px;;
                }
                table tr:first-child td {
                    font-weight: bold;
                    font-size: 18px;

                }
                table tr:first-child td .diff_sub {
                    background:none;
                }
                table tr:first-child td:last-child .diff_add{
                    background:none;
                }
                table[summary="Legends"]{
                    display:none;
                }
                .diff_next{
                    display:none;
                }
                td.diff_header{
                padding:5px;
                background:#ffffff !important;
                }
                table.diff{
                width:100%;
                }
                table {
                    border-collapse: collapse;
                }
                table, tr, td {
                    border-left: 1px solid #fff;
                    border-right: 1px solid #fff;
                }
                table{
                    border-top: 1px solid #fff !important;
                    border-bottom: 1px solid #fff !important;
                }
            """
            def chunks(l,n):
                for i in range(0, len(l), n):
                    yield l[i:i+n]

            if len(ff) or len(sf) > 100:
                ff_len = len(ff)
                sf_len = len(sf)

                if ff_len != sf_len:
                    if ff_len >sf_len:
                        for x in range(ff_len - sf_len):
                            sf.append('\n')
                    else:
                        for x in range(sf_len - ff_len):
                            ff.append('\n')

                listC=[]
                bestMatch = [[] for Null in range(len(ff))]
                reOrdered_ff = []
                shortList = []
                for index, value in enumerate(ff):
                # # if(value != '\n' or value != 'Storyline Content' or 'slide_' in value):
                #     # if '\n' in value:
                #     #     value = value.split('\n')[0]
                #     # if value == '' or value == ' ':
                #     #     value = '\n'
                     for idxe, vlue in enumerate(sf):
                         value = value.strip()
                         vlue = vlue.strip()
                         s = difflib.SequenceMatcher(None, value, vlue).ratio()
                         bestMatch[index].append(s)
                for i, v in enumerate(bestMatch):
                     listC.append(v.index(max(v)))
                     reOrdered_ff.append('\n')
                     shortList.append(ff[i])

                for i, v in enumerate(listC):
                     if(v != 0 and v!= 1):
                         reOrdered_ff[v] = ff[i]
                     elif v == 0:
                         reOrdered_ff[i] = ff[i]
                for i, v in enumerate(reOrdered_ff):
                     if v in shortList:
                         shortList.remove(v)
                for i, v in enumerate(shortList):
                    reOrdered_ff.append(v)
                # if len(reOrdered_ff) != len(sf):
                #     if len(sf) > len(reOrdered_ff):
                #         margin = len(sf) - len(reOrdered_ff)
                #         for i in range(margin):
                #             reOrdered_ff.append('\n')
                #     if len(sf) < len(reOrdered_ff):
                #         margin = len(reOrdered_ff) - len(sf)
                #         for i in range(margin):
                #             sf.append('\n')
                reOrdered_ff_len = len(reOrdered_ff)
                reOrdered_sf_len = len(sf)
                if reOrdered_ff_len != reOrdered_sf_len:
                    if reOrdered_ff_len >reOrdered_sf_len:
                         for x in range(reOrdered_ff_len - reOrdered_sf_len):
                             sf.append('\n')
                    else:
                        for x in range(reOrdered_sf_len - reOrdered_ff_len):
                            reOrdered_ff.append('\n')
                diffrence0 = html.make_file(ff,sf)
                print('worked')
                    # else:
                    #     diffrence = html.make_file(ff[i],sf[i],first_chunk,second_chunk)#wrapcolumn=10)

                        # tbody = diffrence[diffrence.find('<tbody>')+len('<tbody>'):diffrence.find('</tbody>')]
                        # tbody_list = tbody.split('\n')
                        # n=1
                        # for line in tbody_list[1:-1]:
                        #     no = re.search('id="from(.*)_'+str(n)+'">'+str(n)+'<',line).group(1)
                        #     # no = re.search('id="from(.*)_'+str(n)+'">'+str(n)+'<',line).group(1)
                        #     line = line.replace('id="form'+str(no)+'_'+str(n)+'">'+str(n)+'<','id="form'+str(no)+'_'+str(n+i*100)+'">'+str(n+i*100)+'<',1)
                        #     tbody_list[n] = line.replace('id="to'+str(no)+'_'+str(n)+'">'+str(n)+'<','id="to'+str(no)+'_'+str(n+i*100)+'">'+str(n+i*100)+'<',1)
                        #     n+=1
                        # tbody = '\n'.join(tbody_list)
                        # diff_split = diffrence0.split('</tbody>')
                        # diffrence0 = diff_split[0]+tbody+'</tbody>'+diff_split[1]

                with open(path+'/diff_'+str(idx+1)+'.html','w', encoding='utf-8') as f:
                    f.write(diffrence0)
            createdHtmlPath = path+'/diff_'+str(idx+1)+'.html'
            return createdHtmlPath
            # for f in os.list
            # end = time.time()
            # print('Time Taken: ' + str(end-start))
            #----webbrowser.open_new_tab(path+'diff.html')





def mergeFinalFile():
    strHTML = []
    masterData=exportContent.masterData
    with open(location+'mergeFinalFile.html','w') as f:
        headerText = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><title></title><style type="text/css">table.diff {font-family:Courier;}.diff_header {background-color:#ffffff;min-width:25px;}td.diff_header {text-align:right;padding:5px;}.diff_next {background-color:#c0c0c0}.diff_add {background-color:#fff26a}.diff_chg {background-color:#ffff77}.diff_sub {background-color:#ffff77}td[nowrap="nowrap"] {    white-space:normal !important;    word-break: break-word;    min-width: 724px;    max-width: 724px;    }    table tr:first-child td {        font-weight: bold;        text-align: center;        font-size: 18px;            }    table tr:first-child td .diff_sub {        background:none;    }    table tr:first-child td:last-child .diff_add{        background:none;    }table[summary="Legends"]{ display:none; } a{display:none;}body{margin-bottom:30px;}</style></head><body>'
        f.write(headerText)
        for idx, val in enumerate(slideCount):
            file = location + 'diff_'+str(idx+1)+'.html'
            HTMLFile = open(file, "r")
            index = HTMLFile.read()
            S = BeautifulSoup(index, 'lxml')
            strHTML.append(S.select('table:nth-of-type(1)')[0])
            textString = str(S.select('table:nth-of-type(1)')[0])
            textString = textString.replace(u'\xa0', u' ')
            f.write(textString)

        f.write('<table><tr><td>')
        f.write('<h1>Master Data:</h1>')
        f.write('<ul style="font-family: courier;font-size: 16px;font-weight: normal;text-align:left">')
        for data in masterData:
            f.write(f'<li>{data}</li>')
        f.write('</ul>')
        f.write('</td></tr></table>')

        f.write('</body></html>')

    webbrowser.open_new_tab(location+'mergeFinalFile.html')
