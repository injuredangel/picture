# coding:utf-8
# 第一页： 'http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=0'
# 第二页：'http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=50'
#
# 100张图片
# 1、打开列表页
# 2、从列表页里面获取每一个帖子的链接
# 3、打开每一个帖子的链接，获取每一张图片的链接
# 4、打开图片的链接，下载图片

import urllib.request
import re
from PIL import Image
from io import BytesIO
# import requests
url1 = 'http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=0'
url2 = 'http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=50'
# http://tieba.baidu.com/f?kw=%E6%A0%A1%E8%8A%B1&pn=450

second_href = []
second_href1 = []
# 完成第一步，打开列表页

headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Mobile Safari/537.36',
        'Connection': 'keep - alive',
        'Cookie':'BAIDUID=B3BD8D0A241066B6D4C7C3620E1077F4:FG=1; BIDUPSID=B3BD8D0A241066B6D4C7C3620E1077F4; PSTM=1535971092; rpln_guide=1; bdshare_firstime=1540179487814; TIEBAUID=7357fc7f6a2da001bae32d2a; TIEBA_USERTYPE=c1fb10688b54c1de682c2b01; BDUSS=Q4TmlVanVzTk1sZWhWTEFsd2NEZHhDN3dQVkN5d3RUZH42ZFRWdWNqZlRJUFZiQVFBQUFBJCQAAAAAAAAAAAEAAACKMRCjyrjjyQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANOTzVvTk81bQW; STOKEN=96ab3c8a12e84a730ce09b4e59866c8dbac633025690907de5ac7b03bc7654b1; MCITY=-179%3A; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[EqubiKLEhIc]=-tUPB7bzJE6uZNBmi4WUvY; delPer=0; PSINO=5; H_PS_PSSID=; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1540127162,1540176884,1540199357,1540450368; 2735747466_FRSVideoUploadTip=1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1540450439'

    }




def create_request(url):
    '''这个函数用来构建请求对象'''
    request = urllib.request.Request(url=url,headers=headers)
    return request

def send_request(request):
    '''这个函数用来发送请求'''
    response = urllib.request.urlopen(request).read()
    # response = response.decode('gbk', 'ignore')
    return response

def write_html_page(response,page_name):
    '''这个函数用来将爬取的网页写入文件'''
    # response = response.decode('gbk','ignore')
    with open(page_name,'wb+') as file:
        file.write(response)

def tiqu_href(html):
    '''这个函数专门用来负责二级页面的超链接提取'''
    html = html.decode('utf-8')
    obj = re.findall(r'<a href="(.*?)\?lp=\d+&amp;mo_device=1&amp;is_jingpost=0"  class="j_common ti_item" tid="\d+">', html)
    second_href.extend(obj[1:])

def tiqu_href1(html):
    '''这个函数专门用来负责二级页面的超链接提取'''
    html = html.decode('utf-8')
    obj = re.findall(r"data-url='(.*?)jpg", html)
    second_href1.extend(obj[0:])

def open_detail(xxx):
    # for i in range(0,len(xxx)):
        url = 'http://tieba.baidu.com'+xxx[0]
        data = urllib.request.urlopen(url).read()
        return data

if __name__ == '__main__':
    tieba_name = input('请输入需要爬取的贴吧名字')
    print(tieba_name)
    start = int(input('请输入起始页码：'))
    end = int(input('请输入结束页'))
    # 将贴吧名字进行url编码
    tieba_name = urllib.parse.urlencode({'kw': tieba_name})
    print(tieba_name)
    for i in range(start, end + 1):
        # 'http://tieba.baidu.com/f?' + tieba_name + '&pn=' + str((i - 1) * 50)
        url = 'http://tieba.baidu.com/f?' + tieba_name + '&ie=utf-8&pn=' + str((i - 1) * 50)
        request = create_request(url)
        response = send_request(request)
        print(type(response))
        tiqu_href(response)
        file_name = '这是第' + str(i) + '页的内容'
        write_html_page(response, file_name)
        open_detail(second_href)
        print(second_href[0])
        for i in range(0,len(second_href)):
            url2 ='http://tieba.baidu.com'+str(second_href[i])
            request1 = create_request(url2)
            response1  = send_request(request1)
            tiqu_href1(response1)
            file_name = '这是第1条的内容'
            write_html_page(response1,file_name)
            for i in range(0,len(second_href1)):
                url3 = str(second_href1[i])+'jpg'
                print(url3)
                # request2 = create_request(url2)
                # response2 = send_request(request2)
                urllib.request.urlretrieve(url3,'./11/这是第%s张照片.jpg'%i)
        print(len(second_href1))
    # print(len(second_href))
    # print(second_href)




