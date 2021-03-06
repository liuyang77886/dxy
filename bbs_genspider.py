import requests
from lxml import etree


base_url = 'http://www.dxy.cn/bbs/topic/'


class bbs_genspider(object):
    def __init__(self, id):
        self.url = base_url + id

    def get_html(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '填写自己的cookie',
            'Host': 'www.dxy.cn',
            'Referer': 'https://auth.dxy.cn/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        req = requests.get(self.url, headers=headers).text
        return req

    def get_BbsInfo(self):
        raw_html = self.get_html()
        selector = etree.HTML(raw_html)
        # 提取bbs标题
        bbs_title = selector.xpath('//table[@class="title tbfixed"]/tbody/tr/th/h1/text()')[0]
        bbs_title = bbs_title.strip() # 去除字符串左右的空格

        print(bbs_title)
        # 头像
        bbs_other_avater = selector.xpath('//td[@class="tbs"]//div[@class="avatar"]/div/span/a/img/@src')
        print(bbs_other_avater)
        # 用户名
        bbs_other_id = selector.xpath('//td[@class="tbs"]//div[@class="auth"]//a/text()')
        print(bbs_other_id)


        # bbs_id = []
        # bbs_avater = []
        # bbs_data= dict(zip(bbs_other_id,bbs_other_avater)) # 两列表合并成字典
        #
        # data_bbs = {}
        # for key in bbs_data:
        #     if key not in data_bbs:
        #         data_bbs[key] = bbs_data[key]
        # for key in data_bbs:
        #     bbs_id.append(key)
        #     bbs_avater.append(data_bbs[key])
        # [bbs_id.append(i) for i in bbs_other_id if not i in bbs_id]
        # [bbs_avater.append(i) for i in bbs_other_avater if not i in bbs_avater]
        try:
            page = selector.xpath('//div[@class="pages"]/div[@class="num"]/a[last()]/text()')[0]
            print(page)
        except IndexError as e:
            page = 1
        '''
            到这里，我们得到了当前bbs的所有回复用户的信息
            bbs_other_avater  用户的头像地址
            bbs_other_id      用户的用户名
            page              页面数量
        '''
        return bbs_other_id,bbs_other_avater,page

    # 获取所有页面的Url
    def get_AllPageUrl(self, raw_id):
        bbs = bbs_genspider(raw_id)
        bbs_other_id, bbs_other_avater, page = bbs.get_BbsInfo()
        page_list = []
        for i in range(1, int(page) + 1):
            page_url = raw_id + '?ppg=' + str(i)
            page_list.append(page_url)
        return page_list

    # 删除重复的用户
    def del_common(self,raw_id):
        page_list = self.get_AllPageUrl(raw_id)
        data_bbs = {}
        for url in page_list:
            bbs = bbs_genspider(url)
            bbs_id, bbs_avater, page = bbs.get_BbsInfo()
            bbs_data = dict(zip(bbs_id, bbs_avater))  # 两列表合并成字典
            for key in bbs_data:
                if key not in data_bbs:
                    data_bbs[key] = bbs_data[key]

        bbs_id = []
        bbs_avater = []
        for key in data_bbs:
            bbs_id.append(key)
            bbs_avater.append(data_bbs[key])


        return bbs_id,bbs_avater


raw_id = '12345'
bbs = bbs_genspider(raw_id)
bbs_id,bbs_avater = bbs.del_common(raw_id)
print("----------------------------------")
print(bbs_id)
print(len(bbs_id))
print(bbs_avater)
print(len(bbs_avater))