#encoding: utf-8
"""
@project=01temp
@file=read
@author=xiaoru
@create_time=2019/1/6 14:57
"""
from xml.dom.minidom import parse
import xml.dom.minidom

class Read_xml(object):
    """读取XML文件类"""
    def __init__(self):
        self.xml_dic = {}

    def read_second_tag(self,parent,daughter):
        """读取二层标签函数"""
        daughter_tag = parent.getElementsByTagName(daughter)[0].childNodes[0].data
        self.xml_dic[daughter] = daughter_tag
        #print(self.xml_dic)

    def read_third_tag(self,parent,daughter,*grandsons):
        """读取三层标签函数"""
        daughters = parent.getElementsByTagName(daughter)
        daughter_tag_list = []
        for daughteri in daughters:
            daughter_tag_dic = {}
            for grandson in grandsons:
                daughter_tag_dic[grandson] = daughteri.getElementsByTagName(grandson)[0].childNodes[0].data
            daughter_tag_list.append(daughter_tag_dic)
        #print(daughter_tag_list)
        self.xml_dic[daughter] = daughter_tag_list
        #print(self.xml_dic)

def read_xml(path,xml_name):
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(path+'/'+xml_name)
    TestReport = DOMTree.documentElement

    #创建读取xml对象
    read_xml = Read_xml()
    #读取车站文档信息配置
    read_xml.read_second_tag(TestReport, 'TestReportName')
    read_xml.read_second_tag(TestReport, 'DocumentNum')
    read_xml.read_second_tag(TestReport, 'ProjectNum')
    read_xml.read_second_tag(TestReport, 'ChangeOrder')
    #读取测试申请单
    read_xml.read_third_tag(TestReport,'TestRequestList','req_name','req_way','req_svn_num')
    #读取测试输入文档
    read_xml.read_third_tag(TestReport, 'TestInputDocument', 'input_doc_name', 'input_doc_way', 'input_doc_svn_num')
    #读取测试对象
    read_xml.read_third_tag(TestReport, 'TestObject', 'lower_computer_way', 'maintain_terminal_way', 'lower_computer_data_01','maintain_terminal_data_01')
    #读取测试配合项
    read_xml.read_second_tag(TestReport, 'AppSoftware')
    read_xml.read_second_tag(TestReport, 'MaintainTerminalSoftware')
    #读取测试过程
    read_xml.read_third_tag(TestReport, 'TestProcess', 'tester', 'test_time','test_method_01','test_method_02','bug_num','test_conclusion')
    #读取测试结果
    read_xml.read_second_tag(TestReport,'TestResult01')
    read_xml.read_second_tag(TestReport, 'TestResult02')
    return read_xml.xml_dic

if __name__ == '__main__':
    print(read_xml('C://Users\zhaox\Desktop\GitHub\lxpython\lxpython\\01temp','test_report.xml'))
