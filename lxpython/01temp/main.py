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
        super().__init__(None, -1, "自动生成测试报告", size=(600, 150))
        self.m_BasePath = ''
        panel = wx.Panel(self, -1)
        self.ChoosePathBtn = wx.Button(panel, -1, "浏览", pos=(500, 15), size=(50, 26))
        self.InputLineAddressText = wx.TextCtrl(panel, -1, value="请选择读取xml路径", pos=(50, 15), size=(450, 25),
                                                style=wx.TE_READONLY)
        self.ExecuteBtn = wx.Button(panel, -1,"请选择", pos=(240, 60), size=(120, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick_Path, self.ChoosePathBtn)
        self.Bind(wx.EVT_BUTTON, self.OnClick_Execute, self.ExecuteBtn)

    def OnClick_Path(self, event):
        dialog = wx.DirDialog(None, "选择车站报告xml路径", style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            self.m_BasePath = dialog.GetPath()
            self.InputLineAddressText.SetValue(self.m_BasePath)
        dialog.Destroy()
        self.ExecuteBtn.SetLabel("开始")

    def OnClick_Execute(self, event):
        if self.m_BasePath == '':
            return
        GenerateTestReports(self.m_BasePath)
        self.ExecuteBtn.SetLabel("结束")


if __name__ == '__main__':
    app = wx.App()
    g_Frame = MainFrame()
    g_Frame.Show()
    app.MainLoop()
