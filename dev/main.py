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
        super().__init__(None, -1, "自动生成测试报告", size=(800, 500))
        panel = wx.Panel(self, -1)

        #系统方案路径窗口
        self.systemDocPathText = wx.StaticText(panel, label="系统方案路径：", pos=(20, 20))
        self.systemDocPath = wx.TextCtrl(panel, -1, value="请选择系统方案路径", pos=(20, 40), size=(150, 20),
                                         style=wx.TE_READONLY)
        self.systemDocPathOption = wx.Button(panel, -1, "浏览", pos=(170, 40), size=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick_systemDocPath, self.systemDocPathOption)

        #系统方案SVN号窗口
        self.systemDocSvnText = wx.StaticText(panel, label="系统方案SVN号：", pos=(20, 80))
        self.systemDocSvn = wx.TextCtrl(panel, -1, value="", pos=(120, 80), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_system_doc_svn, self.systemDocSvn)

        #车站方案路径窗口
        self.stationDocPathText = wx.StaticText(panel, label="车站方案路径：", pos=(20, 140))
        self.stationDocPath = wx.TextCtrl(panel, -1, value="请选择车站方案路径", pos=(20, 160), size=(150, 20),
                                         style=wx.TE_READONLY)
        self.stationDocPathOption = wx.Button(panel, -1, "浏览", pos=(170, 160), size=(50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick_stationDocPath, self.stationDocPathOption)

        #SVN号窗口
        self.stationDocSvnText = wx.StaticText(panel, label="车站方案SVN号：", pos=(20, 200))
        self.stationDocSvn = wx.TextCtrl(panel, -1, value="", pos=(120, 200), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_station_doc_svn, self.stationDocSvn)

        self.ioListSvnText = wx.StaticText(panel, label="IO配线表SVN号：", pos=(20, 240))
        self.ioListDocSvn = wx.TextCtrl(panel, -1, value="", pos=(120, 240), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_io_list_svn, self.ioListDocSvn)

        self.dishFaceSvnText = wx.StaticText(panel, label="盘面图SVN号：", pos=(20, 280))
        self.dishFaceSvn = wx.TextCtrl(panel, -1, value="", pos=(120, 280), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_dish_face_svn, self.dishFaceSvn)

        self.bomListSvnText = wx.StaticText(panel, label="BOM表SVN号：", pos=(20, 320))
        self.bomListSvn = wx.TextCtrl(panel, -1, value="", pos=(120, 320), size=(100, 20))
        self.Bind(wx.EVT_TEXT, self.EvtText_bom_list_svn, self.bomListSvn)



        self.ExecuteBtn = wx.Button(panel, -1,"开始生成报告", pos=(600, 400), size=(100, 30))
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
    print(g_Frame.station_doc_svn,g_Frame.system_doc_svn,g_Frame.io_list_svn,g_Frame.dish_face_svn,g_Frame.bom_list_svn)