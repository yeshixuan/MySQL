'''

'''
__author__ = 'Yebiyun'
__time__ = '2019/2/4'
import requests
from pypinyin import lazy_pinyin
from lxml import etree
from SPider_2.baiduMap_API.MySQLAPI_demo.MySQLAPI_demo import MysqlDemo
from SPider_2.baiduMap_API.Demos.UA_Proxy import get_headers,get_proxies



#获取具体url地址
def get_url(city,search_name):
    city_str_list = lazy_pinyin(city)
    city_str = city_str_list[0][0] + city_str_list[1][0]
    return city_str,search_name

#获取所有详情链接
def get_Info(data):
    url = 'https://{}.58.com/shangchaoshb/?'.format(data[0])
    # print(url)
    data = {
        'key':data[1]
    }
    headers = get_headers()
    proxies = get_proxies()
    rsp = requests.get(url,params=data,headers=headers,proxies=proxies)

    html = etree.HTML(rsp.text)
    #获取详情链接
    detail_urls = html.xpath("//div[@class='tdiv']/a/@href")
    return detail_urls


#获取详情信息,插入数据库
def get_Detail(urls,mysql,table_name):
    #存放所有发布的信息
    info_list = []
    for url in urls:
        #存放单个发布者的信息
        info = {}
        headers = get_headers()
        proxies = get_proxies()
        rsp = requests.get(url,headers=headers,proxies=proxies)
        html = etree.HTML(rsp.text)

        #获取标题
        title = html.xpath('//div[@class="detail-title"]/h1/text()')
        title = title[0].strip('\r\n').strip(' ')

        # print(title)

        #获取联系人和地址
        name_info = html.xpath('//div[@class="infocard__container__item__main"]/text()')

        #联系人
        name = name_info[1].strip('\r\n').strip()

        #地址
        address = name_info[-1].strip('\r\n').strip().strip('- ')
        #
        #详情介绍
        details = html.xpath('//article[@class="description_con"]/text()|//article[@class="description_con"]//span/text()|//article[@class="description_con"]//p/text()')
        # print(detail)
        detail = ''
        for d in details:
            detail += d

        try:
            #获取图片链接
            imgs = html.xpath('//ul/li//img/@src')
        except:
            imgs= ''
        if title == '':
            title = None
        info['TITLE'] = title
        if name == '':
            name = None
        info['NAME'] = name
        if address == '':
            address = None
        info['ADDRESS'] = address
        if detail == '':
            detail = None
        info['DETAIL'] = detail
        if imgs == '':
            imgs = None
        info['IMG_URL'] = str(imgs)
        # print(info)
        #插入数据
        mysql.insert(table_name, info)
        print('{}插入成功'.format(info['TITLE']))
#创建表
def create_table(mysql):

    datas = [('TITLE', 'CHAR', '200', 'NOT NULL'), ('NAME', 'CHAR', '200', 'NOT NULL'), ('ADDRESS', 'CHAR', '200', ''),
             ('DETAIL', 'TEXT', '1000', ''), ('IMG_URL', 'TEXT', '1000', '')]

    table_name = 'huojia_58'

    mysql.create_tab(table_name, datas)
    return table_name

def main():
    data = get_url('杭州','货架')
    urls = get_Info(data)
    mysql = MysqlDemo('127.0.0.0', 'root', '123456', 'HUOJIA')
    table_name = create_table(mysql)
    get_Detail(urls,mysql,table_name)



if __name__ == '__main__':
    main()