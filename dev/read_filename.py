# -*- coding: UTF-8 -*-
import os


read_dict = {}
TestReportName = '区间综合监控系统维护终端工程数据变更测试报告1(京广线-白马垅站）'
# 从报告名称中获取项目名称
item_name = TestReportName[TestReportName.find('(') + 1:TestReportName.find('-')]
# 从报告名称中获取车站名称
station_name = TestReportName[TestReportName.find('-') + 1:TestReportName.find(')')]
DocumentNum = 'WC189242X'
ProjectNum = 'GC-QJK-SF-16-024'
ChangeOrder = '6.2018.08.23设计变更单-京广线.wps-WB184724X'

def ReadFile(read_path):
    """读取文件名称"""

    TestInputDocument = []
    #进入到文档信息处，并进行读取
    controled_path = read_path+'/controled'
    #在controled文件夹下找到该项目的文件夹并进入
    for controled_item_name in os.listdir(controled_path):
        if controled_item_name.find(item_name) != -1:
            controled_project_path = controled_path+'/'+controled_item_name
    #print(controled_project_path)
    #print(os.listdir(controled_project_path))

    #在该项目文件夹下到第一个文件中寻找系统方案
    controled_system_path = controled_project_path+'/'+os.listdir(controled_project_path)[0]
    #print(controled_system_path)
    #print(os.listdir(controled_system_path))
    for system_name in os.listdir(controled_system_path):
        if system_name.find(item_name+'区间') != -1:
            TestInputDocument.append({'input_doc_name': system_name, 'input_doc_way': controled_system_path})
            print('找到系统方案，并导入')
    if TestInputDocument == []:
        print('未找到系统方案，请尝试手动输入')
    # print(TestInputDocument)

    #在该项目文件夹下找到该车站的文件夹并导入输入文档
    for controled_station_name in os.listdir(controled_project_path):
        if controled_station_name.find(station_name) != -1:
            controled_station_path = controled_project_path+'/'+controled_station_name
    #print(controled_station_path)
    #print(os.listdir(controled_station_path))
    for doc_name in os.listdir(controled_station_path):
        if doc_name.find('设计方案.doc') != -1:
            TestInputDocument.append({'input_doc_name' : doc_name,'input_doc_way' : controled_station_path})
            print('找到车站方案，并导入')
        elif doc_name.find('配线表.dwg') != -1:
            TestInputDocument.append({'input_doc_name': doc_name, 'input_doc_way': controled_station_path})
            print('找到IO配线表，并导入')
        elif doc_name.find('盘面图.dwg') != -1:
            TestInputDocument.append({'input_doc_name': doc_name, 'input_doc_way': controled_station_path})
            print('找到盘面图，并导入')
        elif doc_name.find('(BOM表).xlsx') != -1:
            TestInputDocument.append({'input_doc_name': doc_name, 'input_doc_way': controled_station_path})
            print('找到BOM表，并导入')
    print(TestInputDocument)

    #进入到申请数据处，并进行读取
    tags_path = read_path+'/tags'
    # 在tags文件夹下找到该项目的文件夹并进入
    for tags_item_name in os.listdir(tags_path):
        if tags_item_name.find(item_name) != -1:
            tags_project_path = tags_path + '/' + tags_item_name
    print(tags_project_path)
    print(os.listdir(tags_project_path))

    tags_project_path = tags_path+'/17京广线'
    tags_reqlist_path = tags_project_path+'/2018年8月26日数据测试申请-WC185443X'
    tags_station_path = tags_reqlist_path+'/白马垅站'
    print(os.listdir(tags_reqlist_path))
    TestRequestList = []
    for req_name in os.listdir(tags_reqlist_path):
        reqlist_path = os.path.join(tags_reqlist_path,req_name)
        if os.path.isfile(reqlist_path):
            TestRequestList.append({'req_name': req_name,'req_way':tags_reqlist_path})
    print(TestRequestList)


if __name__ == '__main__':

    read_path = 'C:/Users/zhaox/Desktop/ApplicationDesign'
    ReadFile(read_path)
