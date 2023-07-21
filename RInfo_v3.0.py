# 导入需要的库
from webbrowser import get
from re import I
from turtle import title
from xml.sax.xmlreader import AttributesImpl
from numpy import count_nonzero
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import func_timeout
# 构造函数
def getLinkList(end=5):
    '''输入想要获取的页面范围，返回一个列表wholeOrgList，包含指定页面范围内全部的事件链接，默认为前5页'''
    def makeNewOrganizationList(mainPageLink,end=end):
        '''输入机构主页链接，获取一个列表，包含该机构后续事件页的链接，默认为前5页'''
        # 构造链接列表 organizationWholeList
        organizationWholeList = []
        organizationWholeList.append(mainPageLink)
        if end > 1:
            for i in range(end-1):
                followingPageLink = mainPageLink.replace('common_list_gd','common_list_gd_'+str(i+2))
                organizationWholeList.append(followingPageLink)
        return organizationWholeList
            
    organizationList= ['http://www.csrc.gov.cn/csrc/c106259/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100045/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100046/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100047/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100048/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100049/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100050/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100051/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100052/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100053/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100054/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100055/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100056/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100057/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100058/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100059/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100060/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100061/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100062/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100063/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100064/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100065/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100066/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100067/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100068/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100069/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100070/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100071/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100072/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100073/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100074/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100075/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100076/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100077/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100078/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100079/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100080/common_list_gd.shtml']
    wholeOrgList = []
    for i in organizationList:
        [wholeOrgList.append(str(link)) for link in makeNewOrganizationList(i)]
    return wholeOrgList

def getContent(pageUrl):
    '''输入网址，返回监管页面通报内容'''
    headers= {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/90.0.664.47"
    }#模拟的服务器头
    url = pageUrl
    proxy = {
        'http':'171.35.171.247:9989',
        'https':'171.35.171.247:9989'
    }
    res=requests.get(url=url,headers=headers,timeout=1)
    Html=res.text.encode('iso-8859-1').decode('utf-8')#对编码格式为utf-8方式读取
    soup=BeautifulSoup(Html,features="lxml")  # BeautifulSoup打看网页
    contentTagList = soup.find_all(attrs={'class':'detail-news'})
    content =''
    for i in contentTagList:
        content += i.text
    return content


def getLinks(pageLink):
    '''输入证监会分支机构网址，返回一个列表，包含当前机构页面首页全部公告的标题、发布时间、链接'''
    headers= {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/90.0.664.47"
    }#模拟的服务器头
    url = pageLink
    proxy = {
        'http':'171.35.171.247:9999',
        'https':'171.35.171.247:9999'
    }
    res=requests.get(url=url,headers=headers)
    Html=res.text.encode('iso-8859-1').decode('utf-8')#对编码格式为utf-8方式读取
    soup=BeautifulSoup(Html)  # BeautifulSoup打看网页
    contentTagList = soup.find_all(attrs={'id':"list"})
    # 获取发布时间列表 dateList
    dateTagList = soup.find_all(attrs={'class':"date"})
    dateList = []
    for dateTag in dateTagList:
        dateList.append(dateTag.text)
    # 获取详情页链接列表 linkList
    soup = contentTagList[0]
    linkList = []
    for link in soup.find_all('a'):
        fulllink = 'http://www.csrc.gov.cn'+ link.get('href')
        linkList.append(fulllink)
    # 获取事件标题列表 titleList
    aTagSoup = contentTagList[0]
    titleTagList = aTagSoup.find_all('a')
    titleList = []
    for titleTag in titleTagList:
        titleList.append(titleTag.text)
    # 构造列表包含'标题-发布时间-链接'
    pageContent = [titleList,dateList,linkList]
    return pageContent
# 调用函数，获取全部机构最近两页的 '事件-时间-链接'
organizationList= ['http://www.csrc.gov.cn/csrc/c106259/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100045/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100046/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100047/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100048/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100049/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100050/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100051/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100052/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100053/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100054/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100055/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100056/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100057/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100058/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100059/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100060/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100061/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100062/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100063/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100064/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100065/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100066/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100067/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100068/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100069/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100070/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100071/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100072/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100073/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100074/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100075/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100076/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100077/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100078/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100079/common_list_gd.shtml', 'http://www.csrc.gov.cn/csrc/c100080/common_list_gd.shtml']
organizationList = getLinkList(2)
titleList=[]
dateList=[]
linkList=[]
orgTitleContentList = [[titleList,dateList,linkList]]
organizationListFailed = []
for orgLink in organizationList:
    try:
        pageContent = getLinks(orgLink)
        for i in pageContent[0]:
            titleList.append(i)
        for i in pageContent[1]:
            dateList.append(i)
        for i in pageContent[2]:
            linkList.append(i)
    except:
        organizationListFailed.append(orgLink)
    else:
        print(i)

data = {
    'title':titleList,
    'date':dateList,
    'link':linkList
}
# 根据获取的链接，爬取对应界面的通报详情，汇总至contentList
contentList = []
errorLinkList = []
finishedLink = []
for link in data['link']:
    try:
        contentList.append(getContent(link))
    except:
        errorLinkList.append(link)
    else:
        finishedLink.append(link)
        print(str(len(finishedLink))+"/"+str(len(data['link'])))
# 构建字典 finishedLinkDic
finishedLinkDic={
    'link':finishedLink,
    'contentList':contentList
}
df2 = pd.DataFrame(finishedLinkDic)

# 更新字典data
data['content'] = contentList
data['errorLink'] = errorLinkList
data['finishedLink'] = linkList

# 构建df，填充空值
df = pd.concat(
    [
    pd.DataFrame({'title':titleList}),
    pd.DataFrame({'date':dateList}),
    pd.DataFrame({'link':linkList}),
    # pd.DataFrame({'content':contentList}),
    pd.DataFrame({'errorLink':errorLinkList})
    ],
    axis=1
)
df.fillna(0)
# 合并两个df
mergedPd = pd.merge(df,df2,on='link',how='left')

# 输出数据
fileName = input('请输入文件标题：') + '.xlsx'
mergedPd.to_excel(fileName,encoding='utf-8')