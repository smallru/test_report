# coding:'utf-8'

#from docx import Document
from docxtpl import DocxTemplate


#import read
#import write

class Output(object):
    def __init__(self):
        self.PM_name = '京九线'
        self.station_name = '白马垅站'
        self.document_num = 'WC12345'
        self.PM_num = '12345'
    def test_req(self):


#-----------------主程序内容-------------------------#
req_list_dic = {'req_name' : '2018.07.04.测试申请单-宁西线（郑州局）-WC183829X',
        'req_way' : '/svn/ApplicationDesign/tags/88 宁西线（郑州局）_AG18014A_A/2018年7月4日数据测试申请-WC183829X',
        'req_svn_num' : 37473}
def req_list_wirte(req_list_dic):
    req_list = []
    req_list.append(req_list_dic)


def main():
    tpl = DocxTemplate('工程数据测试报告模板.docx')
    output = Output()

    context = {'PM_name':output.PM_name,
               'station_name' : output.station_name,
               'document_num':output.document_num,
               'PM_num': output.PM_num,
               'test_req': [
                   {'req_name' : '2018.08.25测试申请单-京广线-WC185443X',
                    'req_way' : '/svn/ApplicationDesign/tags/17京广线/2018年8月26日数据测试申请-WC185443X',
                    'req_svn_num': 41259,},
                   {'req_name': '2018.10.11测试申请单-京广线-WC186688X',
                    'req_way': '/svn/ApplicationDesign/tags/17京广线/2018年10月12日数据测试申请-WC186688X',
                    'req_svn_num' : 45525,},
               ],
               'input_doc': [
                   {'input_doc_name': '宁西线（郑州局）区间综合监控系统应用设计方案.docx',
                    'input_doc_way': '/svn/ApplicationDesign/controled/88 宁西线（郑州局）_AG18014A_A/1南阳西站/Document/',
                    'input_doc_svn_num': 20230},
                   {'input_doc_name': '18宁西线屈原岗站区间综合监控系统应用设计方案.doc',
                    'input_doc_way': '/svn/ApplicationDesign/controled/88 宁西线（郑州局）_AG18014A_A/1南阳西站/Document/',
                    'input_doc_svn_num': 20234},
                   {'input_doc_name': '18宁西线屈原岗站解锁盘盘面图.dwg',
                    'input_doc_way': '/svn/ApplicationDesign/controled/88 宁西线（郑州局）_AG18014A_A/1南阳西站/Document/',
                    'input_doc_svn_num': 24340},
                   {'input_doc_name': '18宁西线屈原岗站区间综合监控系统配置清单(BOM表).xlsx',
                    'input_doc_way': '/svn/ApplicationDesign/controled/88 宁西线（郑州局）_AG18014A_A/1南阳西站/Document/',
                    'input_doc_svn_num': 23432},
               ],
               'test_obj' : [
                   {'low_data_way' : '/svn/ApplicationDesign/tags/17京广线/2018年8月26日数据测试申请-WC185443X/白马垅站/目标文件',
                    'display_data_way' : '/svn/ApplicationDesign/tags/17京广线/2018年8月26日数据测试申请-WC185443X/白马垅站/新版维护终端数据',
                    'low_data_ver' : 'V1.0.0',
                    'dsiplay_data_ver' : 'V1.1.1'},
                ],
               'low_soft_ver' : 'V1.0.13',
               'display_soft_ver' : 'V2.0.9',
               'test_process' : [
                   {'req_list' : '2018.08.25测试申请单-京广线-WC185443X',
                    'doc_num' : 'WC185443X',
                    'test_man' : '收款单发货',
                    'test_time' : '2112-09-22',
                    'test_sum' :  '维护终端数据不通过、下位机数据通过'},
                   {}
               ],
               'test_result_1': '对2018.08.25测试申请单-京广线-WC185443X提交的白马垅站数据进行测试，白马垅站下位机数据无问题。',
               'test_result_2': '对2018.11.05.测试申请单-京广线-WC187777X提交的白马垅站数据进行测试，白马垅站维护终端数据无问题。'
    }

    tpl.render(context)
    tpl.save('test.docx')

# 用python-docx模块只能添加重写文档，不能用以修改模板
"""
    document = Document('测试报告模板.docx')
    
    paragraph = document.add_paragraph('测试报告')
    paragraph = document.add_paragraph('测试报告')
    prior_paragraph = paragraph.insert_paragraph_before('附加险')
    document.add_heading('The REAL meaning of the universe', level=2)
    table = document.add_table(rows=2, cols=2)

    document.save('test1.docx')
"""

#-----------------主程序运行------------------------#
main()