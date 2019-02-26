# -*- coding: UTF-8 -*-
import os

def DealDict(dict):
    """处理输入的字典，至xml形字典（因修改xml至Word已成模块）"""
    new_dict = {}
    new_dict["TestReportName"] = dict['doc_name']
    new_dict["DocumentNum"] = dict['doc_num']
    new_dict["ProjectNum"] = dict['item_num']
    new_dict["AppSoftware"] = dict['app_software']
    new_dict["MaintainTerminalSoftware"] = dict['terminal_Software']

    #导入测试申请单，导入测试过程，导入测试结果
    TestRequestList = []
    TestObject = []
    stationName = dict['doc_name'][dict['doc_name'].find('-')+1:-1]
    new_dict["TestResult01"] = ''
    new_dict["TestResult02"] = ''
    test_num = 1
    for TestNum in dict['test_data']:
        req_path = os.path.abspath(os.path.dirname(TestNum[0]))
        req_name = ''
        for req in os.listdir(req_path):
            if req.find('申请单') != -1:
                req_name = req
        if '.pdf' in req_name:
            req_name = req_name[:-4]
        #req_name = os.path.basename(req_path)
        print('第%s轮测试申请单名称:%s' % (test_num, req_name))
        print('第%s轮数据申请单位置：%s'%(test_num,req_path))
        req_way = '/svn/ApplicationDesign/tags/'+str(req_path.split("\\")[-2])+'/'+str(req_path.split('\\')[-1])
        station_data_way = '/svn/ApplicationDesign/tags' + TestNum[0].split("tags")[-1].replace('\\','/')
        station_computer_data_way = station_data_way+'/目标文件'
        station_terminal_data_way = station_data_way + '/维护终端数据'
        req_svn_num = TestNum[1]
        TestRequestList.append({'req_name':req_name,'req_way':req_way,'req_svn_num':req_svn_num})
        lower_computer_way = TestNum[0]+'/目标文件'
        maintain_terminal_way = TestNum[0]+'/新版维护终端数据'
        lower_computer_data_01 = ''
        maintain_terminal_data_01 = ''
        try:
            for data in os.listdir(lower_computer_way):
                if data.find('PLAT') != -1:
                    lower_computer_data_01 = data
                    print('第%s轮车站下位机数据导入'%test_num)
        except FileNotFoundError:
            print('第%s轮车站下无目标文件文件夹'%test_num)
            station_computer_data_way = ''
        try:
            for data in os.listdir(maintain_terminal_way):
                if data.find('App') != -1:
                    maintain_terminal_data_01 = data
                    print('第%s轮车站维护终端数据导入'%test_num)
        except FileNotFoundError:
            print('第%s轮车站下维护终端数据'%test_num)
            station_terminal_data_way = ''
        TestObject.append({'lower_computer_way':station_computer_data_way,'maintain_terminal_way':station_terminal_data_way,
                           'lower_computer_data_01':lower_computer_data_01,'maintain_terminal_data_01':maintain_terminal_data_01})
        #导入测试结果
        if TestNum[6] == '维护终端数据通过，下位机数据通过':
            new_dict["TestResult01"] = '对'+req_name+'提交的'+stationName+'进行测试，'+stationName+'下位机数据无问题，维护终端数据无问题'
        if TestNum[6].find('维护终端数据通过') != -1 and TestNum[6] != '维护终端数据通过，下位机数据通过':
            new_dict["TestResult01"] = '对'+req_name+'提交的'+stationName+'进行测试，'+stationName+'维护终端数据无问题'
        if TestNum[6].find('下位机数据通过') != -1 and TestNum[6] != '维护终端数据通过，下位机数据通过':
            new_dict["TestResult02"] = '对'+req_name+'提交的'+stationName+'进行测试，'+stationName+'下位机数据无问题'
        test_num+=1
    new_dict["TestRequestList"] = TestRequestList
    new_dict["TestObject"] = TestObject

    #导入测试过程
    TestProcess = []
    test_method_01 = ''
    test_method_02 = ''
    for TestNum in dict['test_data']:
        if TestNum[4].find('检查') != -1:
            test_method_01 = '1、执行QJK-JS区间综合监控系统维护终端数据测试检查表'
            test_method_02 = '2、执行QJK-JS区间综合监控系统下位机数据测试检查表'
        elif TestNum[4].find('变更') != -1:
            test_method_01 = '1、执行QJK-JS工程数据变更测试记录单'
            test_method_02 = ''
        elif TestNum[4].find('回归') != -1:
            test_method_01 = '1、执行QJK-JS工程数据回归测试记录单'
            test_method_02 = ''
        TestProcess.append({'tester':TestNum[2],'test_time':TestNum[3],
                            'test_method_01':test_method_01,'test_method_02':test_method_02,
                            'bug_num':TestNum[5],'test_conclusion':TestNum[6]})
    new_dict["TestProcess"] = TestProcess

    #抽取方案到字典
    TestInputDocument = []
    system_doc_path = dict['system_doc_path']
    system_doc_path_Doc = system_doc_path+'\\Document'
    system_doc_way = '/svn/ApplicationDesign/controled'+system_doc_path_Doc.split("controled")[-1].replace('\\','/')
    #print(os.listdir(system_doc_path_Doc))
    system_doc_name = ''
    try:
        for system_name in os.listdir(system_doc_path_Doc):
            if system_name.find(system_doc_path.split("\\")[-1][-3:-1]) == -1\
                    and system_name.find('应用设计方案.doc') != -1 :
                system_doc_name = system_name
                print('找到系统方案:%s，并导入'%system_doc_name)
    except FileNotFoundError:
        print('系统方案路径下无Document文件，无法读取系统方案')
    if system_doc_name != '':
        TestInputDocument.append({'input_doc_name':system_doc_name,'input_doc_way':system_doc_way,
                                      'input_doc_svn_num':dict['system_doc_svn']})

    station_doc_path = dict['station_doc_path']
    station_doc_path_Doc = station_doc_path + '\\Document'
    station_doc_way = '/svn/ApplicationDesign/controled' + station_doc_path_Doc.split("controled")[-1].replace('\\','/')
    #print(os.listdir(station_doc_path_Doc))
    station_doc_name = ''
    io_list__name = ''
    dish_face_name = ''
    bom_list_name = ''
    try:
        for doc_name in os.listdir(station_doc_path_Doc):
            if doc_name.find('应用设计方案.doc') != -1 and doc_name.find(station_doc_path.split("\\")[-1][-3:-1]) != -1:
                station_doc_name = doc_name
                print('找到车站方案:%s，并导入'%station_doc_name)
            elif doc_name.find('配线表.dwg') != -1:
                io_list__name = doc_name
                print('找到IO配线表:%s，并导入'%io_list__name)
            elif doc_name.find('盘面图.dwg') != -1:
                dish_face_name = doc_name
                print('找到盘面图:%s，并导入'%dish_face_name)
            elif doc_name.find('(BOM表).xlsx') != -1:
                bom_list_name = doc_name
                print('找到BOM表:%s，并导入'%bom_list_name)
    except FileNotFoundError:
        print('车站方案路径下无Document文件，无法读取车站文档')
    if station_doc_name != '':
        TestInputDocument.append({'input_doc_name':station_doc_name,'input_doc_way':station_doc_way,
                                      'input_doc_svn_num':dict['station_doc_svn']})
    if io_list__name != '':
        TestInputDocument.append({'input_doc_name': io_list__name, 'input_doc_way': station_doc_way,
                                      'input_doc_svn_num': dict['io_list_svn']})
    if dish_face_name != '':
        TestInputDocument.append({'input_doc_name': dish_face_name, 'input_doc_way': station_doc_way,
                                      'input_doc_svn_num': dict['dish_face_svn']})
    if bom_list_name != '':
        TestInputDocument.append({'input_doc_name': bom_list_name, 'input_doc_way': station_doc_way,
                                      'input_doc_svn_num': dict['bom_list_svn']})
    new_dict['TestInputDocument'] = TestInputDocument

    if dict['change_order'] != '':
        new_dict["ChangeOrder"] = str(len(TestInputDocument)+1)+'.'+dict['change_order']
    return new_dict

if __name__ == '__main__':

    dic = {'system_doc_path': 'C:\\Users\\zhaox\\Desktop\\cangku\\lxpython\\dev\\ApplicationDesign\\controled\\17京广线\\1岳阳站',
           'system_doc_svn': '1111',
           'station_doc_path': 'C:\\Users\\zhaox\\Desktop\\cangku\\lxpython\\dev\\ApplicationDesign\\controled\\17京广线\\12白马垅站',
           'station_doc_svn': '1', 'io_list_svn': '2', 'dish_face_svn': '3', 'bom_list_svn': '4',
           'test_data': [['C:\\Users\\zhaox\\Desktop\\cangku\\lxpython\\dev\\ApplicationDesign\\tags\\17京广线\\2018年8月26日数据测试申请-WC185443X\\白马垅站',
                          '11', '牟林杰', '2019.11.11', '执行检查表', '0', '维护终端数据通过，下位机数据通过'],
                         ['C:\\Users\\zhaox\\Desktop\\cangku\\lxpython\\dev\\ApplicationDesign\\tags\\17京广线\\2018年10月12日数据测试申请-WC186688X\\白马垅站',
                          '22', '牟林杰', '2019.11.11', '执行变更记录单', '1', '维护终端数据不通过，下位机数据通过']],
           'doc_name': '区间综合监控系统维护终端工程数据变更测试报告1（苏抚线-榆树台站）',
           'doc_num': 'WC189242X', 'item_num':'GC-QJK-SF-16-024','change_order': '2018.08.23设计变更单-京广线.wps-WB184724X',
           'app_software': 'V2.0.9', 'terminal_Software': 'V2.0.9'}
    new_dic = DealDict(dic)
    print(new_dic)

