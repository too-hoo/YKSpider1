import requests
import json
import os
import random
import time
import matplotlib.pyplot as plt
import numpy
import jieba
from wordcloud import WordCloud
from PIL import Image



# 弹幕数据存放文件
DANMU_FILE_PATH = 'casesc_danmu.txt'
# 字体位置
WC_FONT_PATH = 'SimHei.ttf'

def spider_danmu(mat, vid):
    """
    抓取某酷指定页的弹幕
    :param vid：每集数
    :param page:页数
    :return :1爬取成功，0爬取失败或者结束
    """
    url = 'https://service.danmu.youku.com/list?jsoncallback=jQuery111206828742264426537_1564796071443&mat=%s&mcount=1&ct=1001&iid=%s&aid=322943&cid=97&lid=0&ouid=0&_=1564796071462' %(mat, vid)
    headers = {
        'referer': 'https://v.youku.com/v_show/id_XNDI0NDYyNjk1Mg==.html?spm=a2h0j.11185381.listitem_page1.5~A&&s=efbfbd78efbfbd5cefbf',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    r=None
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except:
        print('爬取失败！')
    # 找到jsonp数据的左括号位置并+1
    json_start_index = r.text.index('(') + 1
    # 截取json数据的字符串
    r_json_str = r.text[json_start_index:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    # 5、如果请求的总数count=0则说明这一集的弹幕爬取完成
    if not r_json_obj['count']:
        return 0
    # 获取弹幕列表数据
    r_json_result = r_json_obj['result']
    # 遍历评论对象列表
    for r_json_danmu in r_json_result:
        # 以追加的模式换行写入每条评论
        with open(DANMU_FILE_PATH, 'a+') as file:
            file.write(r_json_danmu['content'] + '\n')
        # 打印弹幕对象中的评论内容
        print(r_json_danmu['content'])
    return 1

def batch_spider_comment():
    """
    批量抓取某酷弹幕
    """
    # 写入数据之前先清空之前的数据
    if os.path.exists(DANMU_FILE_PATH):
        os.remove(DANMU_FILE_PATH)
    # 爬取所有的集数的vid
    vids = spider_vid()
    # 第一层循环遍历集数
    for vid in vids:
        print(vid)
        i = 0
        # 第二层循环遍历次数（分钟数）
        while spider_danmu(i, vid):
            # 模拟用户浏览，设置一个爬虫的间隔，防止IP被封
            time.sleep(random.random()*5)
            i += 1
def spider_vid():
    """
    爬取所有的集数的vid
    """
    url = 'https://acs.youku.com/h5/mtop.youku.play.ups.appinfo.get/1.1/?jsv=2.4.16&appKey=24679788&t=1564821581228&sign=e04a53b7f9d58c631efe98f5a5fee604&api=mtop.youku.play.ups.appinfo.get&v=1.1&timeout=20000&YKPid=20160317PLF000211&YKLoginRequest=true&AntiFlood=true&AntiCreep=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22steal_params%22%3A%22%7B%5C%22ccode%5C%22%3A%5C%220502%5C%22%2C%5C%22client_ip%5C%22%3A%5C%22192.168.1.1%5C%22%2C%5C%22utid%5C%22%3A%5C%22txvtFDjNACACATr8gw4HrP4t%5C%22%2C%5C%22client_ts%5C%22%3A1564821581%2C%5C%22version%5C%22%3A%5C%221.7.2%5C%22%2C%5C%22ckey%5C%22%3A%5C%22DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu%2F86PR1u%2FWh1Ptd%2BWOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1%2FY6hLK0OnCNxBj3%2Bnb0v72gZ6b0td%2BWOZsHHWxysSo%2F0y9D2K42SaB8Y%2F%2BaD2K42SaB8Y%2F%2BahU%2BWOZsHcrxysooUeND%5C%22%7D%22%2C%22biz_params%22%3A%22%7B%5C%22vid%5C%22%3A%5C%22XNDI0NDQ0ODEwNA%3D%3D%5C%22%2C%5C%22play_ability%5C%22%3A1280%2C%5C%22current_showid%5C%22%3A%5C%22322943%5C%22%2C%5C%22master_m3u8%5C%22%3A1%2C%5C%22media_type%5C%22%3A%5C%22standard%2Csubtitle%5C%22%2C%5C%22app_ver%5C%22%3A%5C%221.7.2%5C%22%7D%22%2C%22ad_params%22%3A%22%7B%5C%22vs%5C%22%3A%5C%221.0%5C%22%2C%5C%22pver%5C%22%3A%5C%221.7.2%5C%22%2C%5C%22sver%5C%22%3A%5C%222.0%5C%22%2C%5C%22site%5C%22%3A1%2C%5C%22aw%5C%22%3A%5C%22w%5C%22%2C%5C%22fu%5C%22%3A0%2C%5C%22d%5C%22%3A%5C%220%5C%22%2C%5C%22bt%5C%22%3A%5C%22pc%5C%22%2C%5C%22os%5C%22%3A%5C%22win%5C%22%2C%5C%22osv%5C%22%3A%5C%2210%5C%22%2C%5C%22dq%5C%22%3A%5C%22auto%5C%22%2C%5C%22atm%5C%22%3A%5C%22%5C%22%2C%5C%22partnerid%5C%22%3A%5C%22null%5C%22%2C%5C%22wintype%5C%22%3A%5C%22interior%5C%22%2C%5C%22isvert%5C%22%3A0%2C%5C%22vip%5C%22%3A0%2C%5C%22emb%5C%22%3A%5C%22AjEwNjExMTIwMjYCdi55b3VrdS5jb20CL3Zfc2hvdy9pZF9YTkRJME5EWXlOamsxTWc9PS5odG1s%5C%22%2C%5C%22p%5C%22%3A1%2C%5C%22rst%5C%22%3A%5C%22mp4%5C%22%2C%5C%22needbf%5C%22%3A2%7D%22%7D'
    headers = {
        'Referer': 'https://v.youku.com/v_show/id_XNDI0NDQ0ODEwNA==.html?spm=a2h0j.11185381.listitem_page1.5!2~A&&s=efbfbd78efbfbd5cefbf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Cookie':'__ysuid=1550338454558Rxz; cna=txvtFDjNACACATr8gw4HrP4t; juid=01d79i1ij52ncj; __yscnt=1; __ayft=1564795949272; __aysid=15647959492728vN; __ayscnt=1; P_ck_ctl=0412BE8E7431F6DDB9B2076737FD9CFB; ycid=0; __arycid=dz-3-00; __arcms=dz-3-00; referhost=https%3A%2F%2Fv.youku.com; yseid=1564816809278IhKrKW; yseidcount=5; seid=01dhb7tcbddkh; seidtimeout=1564822200488; _m_h5_tk=6c93e9030c885f7b038b9e3bdd62ceb3_1564825411928; _m_h5_tk_enc=e3d0a018724a23d03b8208bddbf30cae; ypvid=1564820403453XLsous; ysestep=4; yseidtimeout=1564827603455; ystep=10; __ayvstp=35; __aysvstp=35; isg=BC4udV9O_1x8JQpdA-AlyodKf4Qwh_JNDBZDmlj2szEGO86VwL8POdR68-dy4-pB; __arpvid=1564821575446xFqUQf-1564821575477; __aypstp=10; __ayspstp=10'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except:
        print('爬取失败！')
    print(r.text)
    # 获取json数据并转换为json对象
    r_json_obj = jsonp_func_to_json_obj(r.text)
    # 获取电视剧简介集数
    video_list = r_json_obj['data']['data']['videos']['list']
    # 创建一个生成器并返回
    return (video['vid'] for video in video_list)
    
def jsonp_func_to_json_obj(jsonp_func):
    """
    jsonp返回函数提取json并转化为对象
    """
    # 找到jsonp数据的左括号位置并+1
    json_start_index = jsonp_func.index('(') + 1
    # 找到最后一个）的位置
    json_end_index = jsonp_func.rindex(')')
    # 截取json数据字符串
    r_json_str = jsonp_func[json_start_index:json_end_index]
    # 字符串转json对象
    return json.loads(r_json_str)

def cut_word():
    """
    对数据分词
    :return :分词之后的数据
    """
    with open(DANMU_FILE_PATH) as file:
        comment_txt = file.read()
        wordlist = jieba.cut(comment_txt, cut_all=False)
        wl = " ".join(wordlist)
        print(wl)
        return wl

def create_word_cloud():
    """
    生成词云
    """
    # 设置词云的形状图片
    # wc_mask = np.array(Image.open(WC_MASK_IMG))
    # 设置词云的一些配置，如：字体，背景色，词云形状，大小
    # 数据清洗停用词列表
    stop_words = ['哈哈', '哈哈哈', '哈哈哈哈', '啊啊啊', '什么', '为什么', '不是', '就是', '还是', '真是', '这是', '是不是',
                  '应该', '不能', '这个', '电视','电视剧', '怎么',
                  '这么', '那么', '那个', '没有', '不能', '不知', '知道']
    wc = WordCloud(
        background_color = "white",
        max_words = 2000,
        width = 940,
        height = 680,
        max_font_size = 50,
        random_state = 42,
        stopwords = stop_words,
        font_path = WC_FONT_PATH)
    # 生成词云
    wordcloud=wc.generate(cut_word())
    # 将图片保存
    wordcloud.to_file('casesc_pic2.jpg')
    # 在只设置mask的情况下，你将会得到一个拥有图片形状的词云
    plt.imshow(wc,interpolation="bilinear")
    plt.axis("off")
    plt.figure()
    
    plt.show()

if __name__ == '__main__':
    # batch_spider_comment()
    # spider_vid()
    create_word_cloud()
