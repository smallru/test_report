# coding:'utf-8'

from docx import Document
from docxtpl import DocxTemplate

from read import *

#处理xml数据为doc内标签内容，并抽取重叠数据
def process_data(dict):
    #提取信息部分
    dict['station_name'] = dict['TestReportName'][dict['TestReportName'].rfind("-")+1:-1]
    for obj in dict["TestObject"]:
        obj['lower_computer_data_ver'] = obj['lower_computer_data_01'][-10:-4]
        obj['maintain_terminal_data_ver'] = obj['maintain_terminal_data_01'][-10:-4]
        if obj['lower_computer_data_01'] != ' ':
            obj['lower_computer_data_02'] = '2_STN'+obj['lower_computer_data_01'][6:]
            obj['lower_computer_data_03'] = '3_FUNC'+obj['lower_computer_data_01'][6:]
            obj['lower_computer_data_04'] = '4_OBJ'+obj['lower_computer_data_01'][6:]
            obj['lower_computer_data_05'] = '5_POOL'+obj['lower_computer_data_01'][6:]
            obj['lower_computer_data_06'] = '6_INTF'+obj['lower_computer_data_01'][6:]
        if obj['maintain_terminal_data_01'] != ' ':
            obj['maintain_terminal_data_02'] = 'Canvas'+obj['maintain_terminal_data_01'][6:]
            obj['maintain_terminal_data_03'] = 'DeviceLogic'+obj['maintain_terminal_data_01'][6:]
    for process in range(0,(len(dict['TestProcess']))):
        dict['TestProcess'][process]['req_list'] = dict['TestRequestList'][process]['req_name']
        dict['TestProcess'][process]['doc_num'] = dict['TestRequestList'][process]['req_name'][-9:]
    if dict['AppSoftware'] == ' ':
        dict['platform_software_ver'] =''
        dict['Commun01_board_ver'] = ''
        dict['Commun03_board_ver'] = ''
    else:
        dict['platform_software_ver'] ='V1.0.1'
        dict['Commun01_board_ver'] = 'V1.0.2'
        dict['Commun03_board_ver'] = 'V0.0.3'

    #修改名称部分
    dict["doc_name"] = dict.pop('TestReportName')
    dict["document_num"] = dict.pop('DocumentNum')
    dict["PM_num"] = dict.pop('ProjectNum')
    dict["test_req"] = dict.pop('TestRequestList')
    dict["input_doc"] = dict.pop('TestInputDocument')
    dict["test_obj"] = dict.pop('TestObject')
    dict["lower_computer_ver"] = dict.pop('AppSoftware')
    dict["maintain_terminal_ver"] = dict.pop('MaintainTerminalSoftware')
    dict["test_process"] = dict.pop('TestProcess')
    dict["test_result_1"] = dict.pop('TestResult01')
    dict["test_result_2"] = dict.pop('TestResult02')
    return  dict

def TestReport(path,xml_name):
    tpl = DocxTemplate('工程数据测试报告模板.docx')
    xml = read_xml(path,xml_name)
    #print(xml)
    content = process_data(xml)
    #print(content)

    context = content
    tpl.render(context)
    tpl.save(path+'/'+content['doc_name']+'.docx')

#-----------------主程序内容-------------------------#
if __name__ == '__main__':
    TestReport()