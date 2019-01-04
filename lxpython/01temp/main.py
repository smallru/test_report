#encoding: utf-8
"""
@project=01temp
@file=main
@author=xiaoru
@create_time=2018/12/26 12:58
"""
from docx import Document
from docxtpl import DocxTemplate

def main():

    tpl = DocxTemplate('模板.docx')

    context = {
    'req_list':[
        {'req_name' : '2018.07.04.测试申请单-宁西线（郑州局）-WC183829X',
        'req_way' : '/svn/ApplicationDesign/tags/88 宁西线（郑州局）_AG18014A_A/2018年7月4日数据测试申请-WC183829X',
        'req_svn_num' : 37473},
        {'req_name' : '2018.07.04.测试申请单-宁西线（郑州局）-WC183829X',
        'req_way' : '/svn/ApplicationDesign/tags/88 宁西线（郑州局）_AG18014A_A/2018年7月4日数据测试申请-WC183829X',
        'req_svn_num' : 37473},
    ],
    'input_doc': [
        {'input_doc_name':'宁西线（郑州局）区间综合监控系统应用设计方案.docx',
         'input_doc_way': '/svn/ApplicationDesign/controled/88 宁西线（郑州局）_AG18014A_A/1南阳西站/Document/',
         'input_doc_svn_num':20230},
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
    'test_result_1' : 'mounoodfgjd',
    'test_result_2' : 'gsgsgsfse'
    }

    tpl.render(context)
    tpl.save('test1.docx')

    """
    f = open('模板.docx', 'rb')
    document = Document(f)
    f.close()
    document.save('test1.docx')
    """

if __name__ == '__main__':
    main()