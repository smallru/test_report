#encoding: utf-8
"""
@project=01temp
@file=test
@author=xiaoru
@create_time=2019/1/6 15:42
"""
import wx
import re

from dealWithDict import *
from getTestReport import *

def GenerateTestReports(dict):
    new_dic = DealDict(dict)
    TestReport(new_dic)

class MainFrame(wx.Frame):
    def __init__(self):
        self.system_doc_path = ''
        self.system_doc_svn = ''
        self.station_doc_path = ''
        self.station_doc_svn = ''
        self.io_list_svn = ''
        self.dish_face_svn = ''
        self.bom_list_svn = ''
        self.test_data_path = ''
        self.test_data_path_list = []
        self.test_data_svn = ''
        #self.test_man = ''
        #self.test_time = ''
        self.test_method = ''
        self.test_data = []
        self.test_num = 0
        self.the_num = [x for x in range(2, 10)]
        #self.doc_name = ''
        #self.doc_num = ''
        #self.item_num = ''
        #self.change_order = ''
        #self.app_software = ''
        #self.terminal_Software = ''

        super().__init__(None, -1, "自动生成测试报告V1.1", size=(960, 500))
        #self.SetBackgroundColour('white')
        panel = wx.Panel(self, -1)
        panel2 = wx.Panel(panel, -1,pos=(10,30),size=(300,380))
        panel3 = wx.Panel(panel, -1, pos=(320, 30), size=(300, 380))
        panel4 = wx.Panel(panel, -1, pos=(630, 30), size=(300, 380))
        panel2.SetBackgroundColour('white')
        panel3.SetBackgroundColour('white')
        panel4.SetBackgroundColour('white')
        #系统方案路径窗口
        self.systemDocPathText = wx.StaticText(panel2, label="系统方案路径：", pos=(10, 20))
        self.systemDocPath = wx.TextCtrl(panel2, -1, value="请选择系统方案路径", pos=(10, 40), size=(240, 25),
                                         style=wx.TE_READONLY)
        self.systemDocPathOption = wx.Button(panel2, -1, "浏览", pos=(250, 40), size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.OnClick_systemDocPath, self.systemDocPathOption)

        #系统方案SVN号窗口
        self.systemDocSvnText = wx.StaticText(panel2, label="系统方案SVN号：", pos=(10, 80))
        self.systemDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 80), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_system_doc_svn, self.systemDocSvn)

        #车站方案路径窗口
        self.stationDocPathText = wx.StaticText(panel2, label="车站方案路径：", pos=(10, 140))
        self.stationDocPath = wx.TextCtrl(panel2, -1, value="请选择车站方案路径", pos=(10, 160), size=(240, 25),
                                         style=wx.TE_READONLY)
        self.stationDocPathOption = wx.Button(panel2, -1, "浏览", pos=(250, 160), size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.OnClick_stationDocPath, self.stationDocPathOption)

        #SVN号窗口
        self.stationDocSvnText = wx.StaticText(panel2, label="车站方案SVN号：", pos=(10, 200))
        self.stationDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 200), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_station_doc_svn, self.stationDocSvn)

        self.ioListSvnText = wx.StaticText(panel2, label="IO配线表SVN号：", pos=(10, 240))
        self.ioListDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 240), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_io_list_svn, self.ioListDocSvn)

        self.dishFaceSvnText = wx.StaticText(panel2, label="盘面图SVN号：", pos=(10, 280))
        self.dishFaceSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 280), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_dish_face_svn, self.dishFaceSvn)

        self.bomListSvnText = wx.StaticText(panel2, label="BOM表SVN号：", pos=(10, 320))
        self.bomListSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 320), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_bom_list_svn, self.bomListSvn)

        # 测试路径窗口
        self.testDataPathText = wx.StaticText(panel3, label="测试申请单测试路径：", pos=(10, 20))
        self.testDataPath = wx.TextCtrl(panel3, -1, value="请选择第1轮测试路径", pos=(10, 40), size=(240, 25),
                                         style=wx.TE_READONLY)
        self.testDataPathOption = wx.Button(panel3, -1, "浏览", pos=(250, 40), size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.OnClick_testDataPath, self.testDataPathOption)
        #测试申请单SVN
        self.testDataSvnText = wx.StaticText(panel3, label='第1轮测试申请单SVN： ', pos=(40, 80))
        self.testDataSvn = wx.TextCtrl(panel3, -1, value="", pos=(180, 80), size=(80, 25))
        self.Bind(wx.EVT_TEXT, self.EvtText_test_data_svn, self.testDataSvn)
        self.testDataSvn.Enable(False)
        #测试人，时间，方法
        self.testManText = wx.StaticText(panel3, label="第1轮测试人：", pos=(40, 120))
        self.testMan = wx.TextCtrl(panel3, -1, value="", pos=(180, 120), size=(80, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_test_man, self.testMan)
        self.testTimeText = wx.StaticText(panel3, label="第1轮测试时间：", pos=(40, 160))
        self.testTime = wx.TextCtrl(panel3, -1, value="2019.11.11", pos=(180, 160), size=(80, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_test_time, self.testTime)
        self.testMethodText = wx.StaticText(panel3, label="第1轮测试方法：", pos=(40, 200))
        self.testMethodList = ['执行两项检查表', '执行变更记录单', '执行回归记录单',]
        self.testMethod = wx.Choice(panel3,pos=(170, 200), size=(100, -1), choices=self.testMethodList)
        self.testBugNumText = wx.StaticText(panel3, label="第1轮测试BUG：", pos=(40, 240))
        self.testBugNum = wx.TextCtrl(panel3, -1, value="0", pos=(170, 240), size=(100, 25))
        # self.Bind(wx.EVT_TEXT, self.EvtText_bug_num, self.testBugNum)
        self.testResultText = wx.StaticText(panel3, label="第1轮测试结果：", pos=(10, 270))
        self.testResultList = ['维护终端数据通过，下位机数据通过', '维护终端数据不通过，下位机数据不通过',
                           '维护终端数据通过，下位机数据不通过','维护终端数据不通过，下位机数据通过',
                           '维护终端数据不通过','维护终端数据通过','下位机数据不通过','下位机数据通过']
        self.testResult = wx.Choice(panel3, pos=(20, 290), size=(260, -1), choices=self.testResultList)
        #轮数确定按钮
        self.num_ensure = wx.Button(panel3, -1, "确定", pos=(170, 330), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Num_ensure, self.num_ensure)
        self.num_ensure.Enable(False)
        #轮数清空按钮
        self.num_clear = wx.Button(panel3, -1, "重置", pos=(20, 330), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_num_clear, self.num_clear)
        self.num_clear.Enable(False)

        #零散信息
        self.docNameText = wx.StaticText(panel4, label="方案名称：", pos=(10, 20))
        self.docName = wx.TextCtrl(panel4, -1, value="", pos=(10, 40), size=(280, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_doc_name, self.docName)
        self.docNumText = wx.StaticText(panel4, label="文档编号：", pos=(10, 80))
        self.docNum = wx.TextCtrl(panel4, -1, value="", pos=(80, 80), size=(100, 25))
        self.itemNumText = wx.StaticText(panel4, label="项目编号：", pos=(10, 120))
        self.itemNum = wx.TextCtrl(panel4, -1, value="", pos=(80, 120), size=(100, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_doc_num, self.docNum)
        self.changeOrderText = wx.StaticText(panel4, label="变更单名称：", pos=(10, 160))
        self.changeOrder = wx.TextCtrl(panel4, -1, value="", pos=(10, 180), size=(280, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_change_order, self.changeOrder)
        self.appSoftwareText = wx.StaticText(panel4, label="下位机软件版本：", pos=(10, 220))
        self.appSoftware = wx.TextCtrl(panel4, -1, value="V1.0.14", pos=(120, 220),size=(100, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_app_software, self.appSoftware)
        self.terminalSoftwareText = wx.StaticText(panel4, label="维护终端软件版本：", pos=(10, 260))
        self.terminalSoftware = wx.TextCtrl(panel4, -1, value="V2.0.9", pos=(120, 260), size=(100, 25))
        #self.Bind(wx.EVT_TEXT, self.EvtText_terminal_software, self.terminalSoftware)

        #开始生成测试报告按钮
        self.start = wx.Button(panel4, -1,"开始生成报告", pos=(60, 320), size=(150, 50))
        self.Bind(wx.EVT_BUTTON, self.OnClick_start, self.start)

    def OnClick_systemDocPath(self, event):
        dialog = wx.DirDialog(None, "请选择系统方案路径", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.system_doc_path = dialog.GetPath()
            self.systemDocPath.SetValue(self.system_doc_path)
        dialog.Destroy()
        #self.ExecuteBtn.SetLabel("开始")

    def OnClick_stationDocPath(self, event):
        dialog = wx.DirDialog(None, "请选择车站方案路径", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.station_doc_path = dialog.GetPath()
            self.stationDocPath.SetValue(self.station_doc_path)
        dialog.Destroy()
        item_name = re.sub("[A-Za-z0-9\!\%\[\]\,\_]", "", self.station_doc_path.split('\\')[-2])
        station_name = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", self.station_doc_path.split('\\')[-1])
        self.docName.SetValue('区间综合监控系统工程数据测试报告'+'('+item_name.strip()+'-'+station_name+')')

    def OnClick_testDataPath(self, event):
        self.num_clear.Enable(True)
        dialog = wx.DirDialog(None, "请选择测试申请单路径", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.test_data_path = dialog.GetPath()
            self.testDataPath.SetValue(dialog.GetPath())
        dialog.Destroy()
        if self.test_data_path in self.test_data_path_list:
            self.testDataPath.SetValue('选择重复路径，请重新选择')
        else:
            self.testDataSvn.Enable(True)
            self.num_ensure.Enable(True)

    def EvtText_system_doc_svn(self, event):
        self.system_doc_svn = event.GetString()
    def EvtText_station_doc_svn(self, event):
        self.station_doc_svn = event.GetString()
    def EvtText_io_list_svn(self, event):
        self.io_list_svn = event.GetString()
    def EvtText_dish_face_svn(self, event):
        self.dish_face_svn = event.GetString()
    def EvtText_bom_list_svn(self, event):
        self.bom_list_svn = event.GetString()
    def EvtText_test_data_svn(self, event):
        self.test_data_svn = event.GetString()
        self.num_ensure.Enable(True)
    '''def EvtText_doc_name(self, event):
        self.doc_name = event.GetString()
    def EvtText_doc_num(self, event):
        self.doc_num = event.GetString()
    def EvtText_change_order(self, event):
        self.change_order = event.GetString()
    def EvtText_app_software(self, event):
        self.app_software = event.GetString()
    def EvtText_terminal_software(self, event):
        self.terminal_software = event.GetString()'''

    def OnClick_Num_ensure(self, event):
        self.test_data_path_list.append(self.test_data_path)
        self.test_data.append([self.test_data_path,self.test_data_svn,self.testMan.GetValue(),self.testTime.GetValue(),
                               self.testMethod.GetStringSelection(),self.testBugNum.GetValue(),self.testResult.GetStringSelection()])
        self.testDataPath.SetValue('请选择第' + str(self.the_num[self.test_num]) + '轮测试路径')
        self.testDataSvnText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试申请单SVN： ')
        self.testManText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试人')
        self.testTimeText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试时间')
        self.testMethodText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试方法')
        self.testBugNumText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试BUG')
        self.testResultText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试结果')
        self.test_num += 1
        self.testDataSvn.Enable(False)
        self.num_ensure.Enable(False)

    def OnClick_num_clear(self, event):
        self.test_data_path = ''
        self.test_data_path_list = []
        self.test_data = []
        #self.test_data_svn = ''
        self.test_num = 0
        self.doc_name = ''
        self.doc_num = ''
        self.testDataPath.SetValue('请选择第1轮测试路径')
        self.testDataSvnText.SetLabel('第1轮测试申请单SVN： ')
        self.testManText.SetLabel('第1轮测试人： ')
        self.testTimeText.SetLabel('第1轮测试时间： ')
        self.testMethodText.SetLabel('第1轮测试方法： ')
        self.testBugNumText.SetLabel('第1轮测试BUG： ')
        self.testResultText.SetLabel('第1轮测试结果： ')
        self.testDataSvn.Enable(False)
        self.num_ensure.Enable(False)

    def OnClick_start(self, event):
        self.item_num = self.itemNum.GetValue()
        dic = {'system_doc_path':self.system_doc_path,'system_doc_svn':self.system_doc_svn,'station_doc_path':self.station_doc_path,
                'station_doc_svn':self.station_doc_svn, 'io_list_svn':self.io_list_svn,'dish_face_svn':self.dish_face_svn,
                'bom_list_svn':self.bom_list_svn,'test_data':self.test_data,'doc_name':self.docName.GetValue(),
                'doc_num':self.docNum.GetValue(),'item_num':self.itemNum.GetValue(),'change_order':self.changeOrder.GetValue(),'app_software':self.appSoftware.GetValue(),
                'terminal_Software':self.terminalSoftware.GetValue()}
        print('界面程序输入信息字典:%s'%dic)
        self.start.SetLabel("正在生成报告")
        GenerateTestReports(dic)
        self.start.SetLabel("开始生成报告")

if __name__ == '__main__':
    app = wx.App()
    g_Frame = MainFrame()
    g_Frame.Show()
    app.MainLoop()