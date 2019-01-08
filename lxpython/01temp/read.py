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

    def __str__(self):
        return self.xml_dic

    def read_second_tag(self,parent,daughter):
        """读取二层标签函数"""
        a = {}
        daughter_tag = parent.getElementsByTagName(daughter)[0].childNodes[0].data
        print(daughter_tag)
        self.xml_dic[daughter] = daughter_tag
        #print(self.xml_dic)

    def read_third_tag(self,parent,daughter,*grandsons):
        """读取三层标签函数"""
        daughters = parent.getElementsByTagName(daughter)
        daughter_tag_list = []
        daughter_tag_dic = {}
        for daughter in daughters:
            for grandson in grandsons:
                daughter_tag_dic[grandson] = daughter.getElementsByTagName(grandson)[0].childNodes[0].data
            daughter_tag_list.append(daughter_tag_dic)
        self.xml_dic[daughter] = daughter_tag_list
        #print(self.xml_dic)

if __name__ == '__main__':
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("test_report.xml")
    TestReport = DOMTree.documentElement

    read_xml = Read_xml()
    read_xml.read_third_tag(TestReport,'TestRequestList','req_name','req_way','req_svn_num')
    read_xml.read_third_tag(TestReport, 'TestInputDocument', 'input_doc_name', 'input_doc_way', 'input_doc_svn_num')
    read_xml.read_second_tag(TestReport,'test_result_1')
    print(read_xml.xml_dic)
