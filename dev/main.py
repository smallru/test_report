#encoding: utf-8
"""
@project=01temp
@file=test
@author=xiaoru
@create_time=2019/1/6 15:42
"""
import wx
import os

from testReport import *

def GenerateTestReports(path):
    #print(os.listdir(path))
    for xml_name in os.listdir(path):
        if xml_name[-3:] == 'xml':
            print(xml_name)
            TestReport(path,xml_name)

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
        self.test_data_svn_list = []
        self.test_num = 0
        self.the_num = [x for x in range(2, 10)]
        super().__init__(None, -1, "自动生成测试报告", size=(800, 500))
        #self.SetBackgroundColour('white')
        panel = wx.Panel(self, -1)
        panel2 = wx.Panel(panel, -1,pos=(0,0),size=(250,350))
        panel3 = wx.Panel(panel, -1, pos=(250, 0), size=(300, 350))
        panel2.SetBackgroundColour('white')
        panel3.SetBackgroundColour('white')
        #系统方案路径窗口
        self.systemDocPathText = wx.StaticText(panel2, label="系统方案路径：", pos=(20, 20))
        self.systemDocPath = wx.TextCtrl(panel2, -1, value="请选择系统方案路径", pos=(20, 40), size=(150, 20),
                                         style=wx.TE_READONLY)
        self.systemDocPathOption = wx.Button(panel2, -1, "浏览", pos=(170, 40), size=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick_systemDocPath, self.systemDocPathOption)

        #系统方案SVN号窗口
        self.systemDocSvnText = wx.StaticText(panel2, label="系统方案SVN号：", pos=(20, 80))
        self.systemDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 80), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_system_doc_svn, self.systemDocSvn)

        #车站方案路径窗口
        self.stationDocPathText = wx.StaticText(panel2, label="车站方案路径：", pos=(20, 140))
        self.stationDocPath = wx.TextCtrl(panel2, -1, value="请选择车站方案路径", pos=(20, 160), size=(150, 20),
                                         style=wx.TE_READONLY)
        self.stationDocPathOption = wx.Button(panel2, -1, "浏览", pos=(170, 160), size=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick_stationDocPath, self.stationDocPathOption)

        #SVN号窗口
        self.stationDocSvnText = wx.StaticText(panel2, label="车站方案SVN号：", pos=(20, 200))
        self.stationDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 200), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_station_doc_svn, self.stationDocSvn)

        self.ioListSvnText = wx.StaticText(panel2, label="IO配线表SVN号：", pos=(20, 240))
        self.ioListDocSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 240), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_io_list_svn, self.ioListDocSvn)

        self.dishFaceSvnText = wx.StaticText(panel2, label="盘面图SVN号：", pos=(20, 280))
        self.dishFaceSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 280), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_dish_face_svn, self.dishFaceSvn)

        self.bomListSvnText = wx.StaticText(panel2, label="BOM表SVN号：", pos=(20, 320))
        self.bomListSvn = wx.TextCtrl(panel2, -1, value="", pos=(120, 320), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_bom_list_svn, self.bomListSvn)

        # 测试路径窗口
        self.testDataPathText = wx.StaticText(panel3, label="测试申请单测试路径：", pos=(20, 20))
        self.testDataPath = wx.TextCtrl(panel3, -1, value="请选择第1轮测试路径", pos=(20, 40), size=(200, 30),
                                         style=wx.TE_READONLY)
        self.testDataPathOption = wx.Button(panel3, -1, "浏览", pos=(220, 40), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_testDataPath, self.testDataPathOption)
        #测试申请单SVN
        self.testDataSvnText = wx.StaticText(panel3, label='第1轮测试申请单SVN： ', pos=(20, 80))
        self.testDataSvn = wx.TextCtrl(panel3, -1, value="", pos=(170, 80), size=(60, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_test_data_svn, self.testDataSvn)
        self.testDataSvn.Enable(False)
        #轮数确定按钮
        self.num_ensure = wx.Button(panel3, -1, "确定", pos=(170, 120), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Num_ensure, self.num_ensure)
        self.num_ensure.Enable(False)
        #轮数清空按钮
        self.num_clear = wx.Button(panel3, -1, "重置", pos=(20, 120), size=(50, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_num_clear, self.num_clear)
        self.num_clear.Enable(False)



        self.ExecuteBtn = wx.Button(panel2, -1,"开始生成报告", pos=(600, 400), size=(100, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Execute, self.ExecuteBtn)

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

    def OnClick_Num_ensure(self, event):
        self.test_data_path_list.append(self.test_data_path)
        self.test_data_svn_list.append(self.test_data_svn)
        self.testDataPath.SetValue('请选择第' + str(self.the_num[self.test_num]) + '轮测试路径')
        self.testDataSvnText.SetLabel('第' + str(self.the_num[self.test_num]) + '轮测试申请单SVN： ')
        self.test_num += 1
        self.testDataSvn.Enable(False)
        self.num_ensure.Enable(False)

    def OnClick_num_clear(self, event):
        self.test_data_path = ''
        self.test_data_path_list = []
        self.test_data_svn = ''
        self.test_data_svn_list = []
        self.test_num = 0
        self.testDataPath.SetValue('请选择第1轮测试路径')
        self.testDataSvnText.SetLabel('第1轮测试申请单SVN： ')




    def OnClick_Execute(self, event):
        if self.system_doc_path == '':
            return
        GenerateTestReports(self.system_doc_path)
        self.ExecuteBtn.SetLabel("结束")

    def __str__(self):
        return self.station_doc_svn


if __name__ == '__main__':
    app = wx.App()
    g_Frame = MainFrame()
    g_Frame.Show()
    app.MainLoop()
    print(g_Frame.test_data_path_list,g_Frame.test_data_svn_list)