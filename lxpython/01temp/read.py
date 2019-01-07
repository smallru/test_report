#encoding: utf-8
"""
@project=01temp
@file=read
@author=xiaoru
@create_time=2019/1/6 14:57
"""
from xml.dom.minidom import parse
import xml.dom.minidom

def get(parent,child):
    return parent.getElementsByTagName(child)[0].childNodes[0].data

def main():

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse("test_report.xml")
    TestReport = DOMTree.documentElement

    # 在集合中获取所有测试申请单
    TestRequestLists = TestReport.getElementsByTagName('TestRequestList')
    # 在集合中获取所有测试结果
    TestResults = TestReport.getElementsByTagName('TestResult')

    for TestRequestList in TestRequestLists:
        req_name = get(TestRequestList,'req_name')
        print(req_name)

    for TestResult in TestResults:
        test_result_1 = TestResult.getElementsByTagName('test_result_1')[0].childNodes[0].data
        print(test_result_1)
        test_result_2 = TestResult.getElementsByTagName('test_result_2')[0]
        print("test_result_2: %s" % test_result_2.childNodes[0].data)
if __name__ == '__main__':
    main()
