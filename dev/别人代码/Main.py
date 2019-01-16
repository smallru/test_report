#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
import wx.grid

from _codecs import decode
import configparser
import os

from StationData import *
from IOChecker.IOChecker import *
from IOChecker.ReadIO import *

from RJPChecker.ReadRJP import *
from RJPChecker.RJPChecker import *

from WriteDIOSheets import *

from RecordCreator.ClientRecordCreator import *
from RecordCreator.SeverRecordCreator import *

from RJPChecker.PreliminaryRJP import *

import sys
reload(sys) 
sys.setdefaultencoding('utf8')

#PATH_IO = "D:\\检查IO表\\IO配线表数据\\".decode("utf8")
PATH_RJP = "D:\\RJPTable\\"
PATH_DIO_SIMU = "D:\\检查IO表\\仿真DIO配置表\\".decode("utf8")
PATH_CLIENT = "D:\\client\\"
PATH_SERVER = "D:\\server\\"
g_listStation = []
g_dicIOTableInfo = {}
g_CheckResult = {}
g_Frame = None

#读取IO配线表数据
def ExecuteReadIO(rootPath):
    for IOList in os.listdir(rootPath + u'//IO//'):
        if IOList.startswith('~'):
            continue
        stationName = IOList[:-5]
        dicDr, dicGa,listInfo = ReadIOSheet(rootPath + u'//IO//' + IOList,stationName)
        #print '%s 采集板信息：%s'%(stationName,dicGa)
        g_dicIOTableInfo[stationName] = [dicDr,dicGa]
        WriteTxtContent(stationName,listInfo,rootPath)

#执行IO配线表校对
def ExecuteCheckIO(rootPath,formerLineBool):
    for station in g_listStation:
        listInfo = []
        dicStation = g_CheckResult.get(station.name,{})
        dicIO = {"result":False,"info":listInfo}         
        if not g_dicIOTableInfo.has_key(station.name):
            #print 'wei zhao dao %s IO pei xian biao shuju '%station.name
            listInfo.append(u'未找到%s IO配线表数据\n'%station.name)
        else:   
            bCheck,listInfo1 = CheckIO(station,g_dicIOTableInfo[station.name][0],g_dicIOTableInfo[station.name][1],formerLineBool) 
            listInfo.extend(listInfo1)
            dicIO["result"] = bCheck
            dicIO["info"] = listInfo
        dicStation["IO"] = dicIO
        g_CheckResult[station.name] = dicStation

        WriteTxtContent(station.name,listInfo,rootPath)
    if g_Frame:
        g_Frame.OutputIOCheckResult()

#读取解锁盘盘面图
def ExecuteReadRJP(rootPath):
    
    listInfoPre = []
    global g_listStation
    #print "车站数量%s"%len(g_listStation)
    for station in g_listStation:
        listInfo = []
        tablePath = rootPath + u'/RJP/'  +station.name + ".xlsx"
        if not os.path.exists(tablePath):
            #print "未找到解锁盘盘面图表格,请重新操作\n".decode("utf8")
            listInfo.append(u"未找到%s 解锁盘盘面图表格,请重新操作\n"%station.name)
            WriteTxtContent(station.name,listInfo,rootPath)
            continue
        
        listInfoPre.append('********************************************************************')
        listInfoPre.append(u'-------------%s-----检验盘面图闭塞分区名称修改的情况---开始----------'%station.name)
        listInfo1 = Preliminary(tablePath)
        if listInfo1:
            listInfoPre.extend(listInfo1)
            listInfoPre.append(u'-------------%s-----检验盘面图闭塞分区名称修改的情况---结束----------'%station.name)
            WriteTxtContent(station.name,listInfoPre,rootPath)
            msgDialog = wx.MessageDialog(None, u'%s 盘面图 闭塞分区名称存在修改的情况或者内容存在为空，请确认!'%station.name, u'信息警示', wx.YES_DEFAULT | wx.ICON_QUESTION)
            if msgDialog.ShowModal() == wx.ID_YES:
                pass
            msgDialog.Destroy()  
        
        listInfo.append('********************************************************************')
        listInfo.append(u'-------------%s-----盘面图闭塞分区名称核对---开始----------'%station.name) 
        dicRJPTableInfo,listInfo2 = ReadRJPTableInfor(tablePath)
        listInfo.extend(listInfo2)
        listInfo.append(u'-------------%s-----盘面图闭塞分区名称核对---结束----------'%station.name)
        listInfo.append('********************************************************************')
        station.dicRJPInfo = dicRJPTableInfo
        WriteTxtContent(station.name,listInfo,rootPath)
        
        
#执行解锁盘盘面图校对
def ExecuteCheckRJP(rootPath):
    listInfo = []
    for station in g_listStation:
        dicStation = g_CheckResult.get(station.name,{})
        dicRJP = {"result":False,"info":[]}
       
        if station.dicRJPInfo != {}:
            bCheck,listInfo = CheckRJP(station.dicRJPInfo,station)

            dicStation = g_CheckResult.get(station.name,{})
            dicRJP["result"] = bCheck
            dicRJP["info"] = listInfo
        else:
            listInfo.append(u"未读取到%s RJP表格内容\n"%station.name)
            dicRJP["info"] = listInfo
        dicStation["RJP"] = dicRJP
        g_CheckResult[station.name] = dicStation
        

        WriteTxtContent(station.name,listInfo,rootPath)
        listInfo = []
    if g_Frame:
        g_Frame.OutputRJPCheckResult()    

#执行生成IO仿真数据表
def ExecuteCreateIOSimuData(pathIO):
    WHZDWriteDIOSheets().CreateSimuDataByIO(pathIO,g_dicIOTableInfo)

def ExecuteReadWHZDData(WHZDRootPath):
    WHZDPath = WHZDRootPath + u"/Client/"
    global g_listStation
    g_listStation = []
    deviceFile = ""
    appFile = ""
    for parent, dirnames, filenames in os.walk(WHZDPath, topdown=True):
        if "新版维护终端数据".decode("utf8") in parent:
            listInfo = []
            listInfo.append('********************************************************************')
            listInfo.append('-----------------维护终端数据文件读取---开始-------------')
            station,listInfo1 = ReadStationInfo(parent)
            listInfo.extend(listInfo1)
            listInfo.append('-----------------维护终端数据文件读取---结束-------------')
            listInfo.append('********************************************************************')
            g_listStation.append(station)
            WriteTxtContent(station.name,listInfo,WHZDRootPath)

def WriteTxtContent(stationName, listInfo,rootPath):
    logPath = rootPath + '\\Log\\'
    if not os.path.exists(logPath):
        os.makedirs(logPath)
    logFile = logPath + '%s.txt'%stationName
    CheckMisstxt = open(logFile, "a+")
    CheckMisstxt.write("\n")
    CheckMisstxt.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    CheckMisstxt.write("\n")
    CheckMisstxt.write("\n".join(listInfo))
    CheckMisstxt.close()
    
    
class Grid(wx.grid.Grid):
    def __init__(self,parent,Pos,size):
        wx.grid.Grid.__init__(self,parent,-1,Pos,size)

        self.CreateGrid(100,5)
        self.SetColLabelValue(0,"站名".decode("utf8"))
        self.SetColSize(0,100)
        self.SetColLabelValue(1,"IO校验结果".decode("utf8"))
        self.SetColSize(1, 100)      
        self.SetColLabelValue(2,"RJP校验结果".decode("utf8"))
        self.SetColSize(2, 100)  
        self.SetColLabelValue(3,"IO备注".decode("utf8"))
        self.SetColSize(3, 200)          
        self.SetColLabelValue(4,"RJP备注".decode("utf8"))
        self.SetColSize(4, 200)

class MainFrame(wx.Frame):
    def __init__(self):                                                                                                                                                                                
        self.check = {}
        self.m_RootLineName = ""
        self.LineNameList = []
        self.m_BasePath = ''
        #self.ReadChoiceListConfig()
        
        wx.Frame.__init__(self, None, -1, "QJK自动对点和生成检查表 V1.1.7".decode("utf8"), size=(1000,700))
        self.SetBackgroundColour('white')
        panel = wx.Panel(self, -1)
        panel1 = wx.Panel(panel, -1,pos=(0,25),size=(1000,35))
        panel2 = wx.Panel(panel, -1,pos=(100,90),size=(800,80))
        panel3 = wx.Panel(panel2, -1,pos=(10,10),size=(780,60))
        panel4 = wx.Panel(panel, -1,pos=(100,180),size=(800,80))
        panel5 = wx.Panel(panel4, -1,pos=(10,10),size=(780,60))
        panel1.SetBackgroundColour((239, 239, 239, 255))
        panel2.SetBackgroundColour((239, 239, 239, 255))
        panel4.SetBackgroundColour((239, 239, 239, 255))
        panel3.SetBackgroundColour('white')
        panel5.SetBackgroundColour('white')
        self.Table = None
        self.Table = Grid(panel,(100,280),(800,350))
        #self.Table.EnableEditing(False)

        self.formerLineText = wx.StaticText(panel1,-1,u"陈旧线路".decode("utf8"),pos=(170,10),size=(50,20))
        self.checkBox_formerLine = wx.CheckBox(panel1, -1,  pos=(145,10))
        self.InputLineAddressText = wx.TextCtrl(panel1, -1,value=u"请选择测试线路路径",pos=(285,5),size=(565,25),style=wx.TE_READONLY)
        self.ChooseLinePathBtn = wx.Button(panel1,-1,"浏览".decode("utf-8"),pos=(850,5),size=(50,26))
        self.scheduleText = wx.StaticText(panel,-1,"".decode("utf8"),pos=(420,70),size=(190,20))
        self.checkBox_ReadWHZDBtn = wx.CheckBox(panel3, -1,  pos=(150,20))
        self.checkBox_ReadIOBtn = wx.CheckBox(panel3, -1,  pos=(450,20))
        self.checkBox_ReadRJPBtn = wx.CheckBox(panel3, -1,  pos=(750,20))        
        self.ReadWHZDBtn = wx.Button(panel3, -1, "读取维护终端".decode("utf8"), pos=(25,15),size=(120,30))
        self.ReadIOBtn = wx.Button(panel3, -1, "读取IO配线表".decode("utf8"), pos=(325,15),size=(120,30))
        self.ReadRJPBtn = wx.Button(panel3, -1, "读取RJP盘面图".decode("utf8"),  pos=(625,15),size=(120,30))
        self.CheckIOBtn = wx.Button(panel5, -1, "校验IO数据".decode("utf8"), pos=(25,15),size=(120,30))
        self.CheckRJPBtn = wx.Button(panel5, -1, "校验RJP数据".decode("utf8"), pos=(175, 15),size=(120,30))
        self.CreateIOConfigBtn = wx.Button(panel5, -1, "生成仿真IO配置表".decode("utf8"),  pos=(325,15),size=(120,30))
        self.CreateClientRecordBtn = wx.Button(panel5, -1, "生成维护终端检查表".decode("utf8"), pos=(475,15),size=(120,30))
        self.CreateSeverRecordBtn = wx.Button(panel5, -1, "生成下位机检查表".decode("utf8"),pos=(625,15),size=(120,30))
        self.scheduleText.SetForegroundColour('Blue')
        self.ReadWHZDBtn.Enable(False)
        self.ReadIOBtn.Enable(False)
        self.ReadRJPBtn.Enable(False)
        self.CheckIOBtn.Enable(False)
        self.CheckRJPBtn.Enable(False)
        self.CreateIOConfigBtn.Enable(False)
        self.CreateClientRecordBtn.Enable(False)
        self.CreateSeverRecordBtn.Enable(False)
        self.checkBox_ReadWHZDBtn.Enable(False)
        self.checkBox_ReadIOBtn.Enable(False)
        self.checkBox_ReadRJPBtn.Enable(False)
               
        self.Bind(wx.EVT_BUTTON,self.OnClick_Path, self.ChooseLinePathBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_ReadWHZD,self.ReadWHZDBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_ReadIO,self.ReadIOBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_ReadRJP,self.ReadRJPBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_CheckIO,self.CheckIOBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_CheckRJP,self.CheckRJPBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_CreateDIOConfig,self.CreateIOConfigBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_CreateClientRecord,self.CreateClientRecordBtn)
        self.Bind(wx.EVT_BUTTON,self.OnClick_CreateSeverRecord,self.CreateSeverRecordBtn)
        
    def SetTitleText(self,panel,title):
        Title = wx.StaticText(panel,-1,title,(400,30),(100,30),wx.ALIGN_CENTER)
        font = wx.Font(15,wx.ROMAN,wx.NORMAL,wx.BOLD)
        Title.SetFont(font)    
    
    def InitialState(self):
        #self.m_BasePath = ''
        #self.InputLineAddressText.SetValue(self.m_BasePath)
        self.ReadWHZDBtn.Enable(False)
        self.ReadIOBtn.Enable(False)
        self.ReadRJPBtn.Enable(False)       
        self.CheckIOBtn.Enable(False)
        self.CheckRJPBtn.Enable(False)
        self.CreateIOConfigBtn.Enable(False)
        self.CreateClientRecordBtn.Enable(False)
        self.CreateSeverRecordBtn.Enable(False)  
        self.checkBox_ReadWHZDBtn.SetValue(False)
        self.checkBox_ReadIOBtn.SetValue(False)
        self.checkBox_ReadRJPBtn.SetValue(False)
        self.scheduleText.SetLabel(u"")
        
        self.Table.ClearGrid()
        g_listStation = []
        g_CheckResult.clear()
        g_dicIOTableInfo.clear()        
        
    def OnClick_Path(self,event):
        self.InitialState()
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)  
        if dialog.ShowModal() == wx.ID_OK:  
            self.m_BasePath = dialog.GetPath()
            self.InputLineAddressText.SetValue(self.m_BasePath)
        dialog.Destroy()
        self.ReadWHZDBtn.Enable(True)
        self.ReadIOBtn.Enable(True)
                
        
    def OnClick_ReadWHZD(self,event):
        self.scheduleText.SetLabel(u"正在读取维护终端，请稍等......")
        path = self.m_BasePath + u"/Client/"
        if not os.path.exists(path):
            msgDialog = wx.MessageDialog(None, u'未找到维护终端数据文件夹/Client/ !', u'信息警示', wx.YES_DEFAULT | wx.ICON_QUESTION)
            if msgDialog.ShowModal() == wx.ID_YES:
                pass
            msgDialog.Destroy()
            self.scheduleText.SetLabel(u"")
            return  
        ExecuteReadWHZDData(self.m_BasePath)

        self.checkBox_ReadWHZDBtn.SetValue(True)
        self.ReadRJPBtn.Enable(True)
        self.CreateClientRecordBtn.Enable(True)
        self.CreateSeverRecordBtn.Enable(True)        
        if self.checkBox_ReadWHZDBtn.IsChecked() and self.checkBox_ReadIOBtn.IsChecked():
            self.CheckIOBtn.Enable(True)        
        if self.checkBox_ReadWHZDBtn.IsChecked() and self.checkBox_ReadRJPBtn.IsChecked():
            self.CheckRJPBtn.Enable(True)
        self.scheduleText.SetLabel(u"      读取维护终端完成")
    
    def OnClick_ReadIO(self,event):
        self.scheduleText.SetLabel(u"正在读取IO配线表，请稍等......")
        path = self.m_BasePath + u"/IO/"
        if not os.path.isdir(path):
            msgDialog = wx.MessageDialog(None, u'未找到IO配线表文件夹/IO/ !', u'信息警示', wx.YES_DEFAULT | wx.ICON_QUESTION)
            if msgDialog.ShowModal() == wx.ID_YES:
                pass
            msgDialog.Destroy()
            self.scheduleText.SetLabel(u"")
            return
        ExecuteReadIO(self.m_BasePath)
        
        self.checkBox_ReadIOBtn.SetValue(True)
        if self.checkBox_ReadWHZDBtn.IsChecked() and self.checkBox_ReadIOBtn.IsChecked():
            self.CheckIOBtn.Enable(True)
        if self.checkBox_ReadIOBtn.IsChecked():
            self.CreateIOConfigBtn.Enable(True)
        self.scheduleText.SetLabel(u"      读取IO配线表完成")
        
    def OnClick_CheckIO(self,event):
        formerLineBool = self.checkBox_formerLine.IsChecked()
        self.scheduleText.SetLabel(u"正在校验IO数据，请稍等......")
        ExecuteCheckIO(self.m_BasePath,formerLineBool)
        self.scheduleText.SetLabel(u"      校验IO数据完成")
        
    def OnClick_ReadRJP(self,event):
        self.scheduleText.SetLabel(u"正在读取RJP盘面图，请稍等......")
        path = self.m_BasePath + u"/RJP/"
        if not os.path.isdir(path):
            msgDialog = wx.MessageDialog(None, u'未找到解锁盘盘面图文件夹/RJP/ !', u'信息警示', wx.YES_DEFAULT | wx.ICON_QUESTION)
            if msgDialog.ShowModal() == wx.ID_YES:
                pass
            msgDialog.Destroy()
            self.scheduleText.SetLabel(u"")
            return
        #print u"\n******开始自动读取RJP盘面图数据*******"      
        ExecuteReadRJP(self.m_BasePath)
        
        self.checkBox_ReadRJPBtn.SetValue(True)
        if self.checkBox_ReadWHZDBtn.IsChecked() and self.checkBox_ReadRJPBtn.IsChecked():
            self.CheckRJPBtn.Enable(True)
        self.scheduleText.SetLabel(u"      读取RJP盘面图完成")
    
    def OnClick_CheckRJP(self,event):
        self.scheduleText.SetLabel(u"正在校验RJP数据，请稍等......")
        ExecuteCheckRJP(self.m_BasePath)        
        self.scheduleText.SetLabel(u"      校验RJP数据完成")
        
    def OnClick_CreateDIOConfig(self,event):
        self.scheduleText.SetLabel(u"正在生成仿真IO配置表，请稍等......")
        ExecuteCreateIOSimuData(self.m_BasePath + u'/IOSimuConfig/')
        self.scheduleText.SetLabel(u"   生成仿真IO配置表完成")
    
    def OnClick_CreateClientRecord(self,event):
        self.scheduleText.SetLabel(u"正在生成维护终端检查表，请稍等......")
        for station in g_listStation:
            listInfo = []
            listInfo.append('********************************************************************')
            listInfo.append(u'-------------%s-----生成维护终端检查表核对---开始----------'%station.name)
            WriteClientRecordFile(station,self.m_BasePath + u'/ClientRecord/',listInfo)
            listInfo.append(u'-------------%s-----生成维护终端检查表核对---结束----------'%station.name)
            listInfo.append('********************************************************************')
            WriteTxtContent(station.name, listInfo, self.m_BasePath)
        self.scheduleText.SetLabel(u"   生成维护终端检查表完成")
    
    def OnClick_CreateSeverRecord(self,event):
        self.scheduleText.SetLabel(u"正在生成下位机检查表，请稍等......")
        for station in g_listStation:
            listInfo = []
            listInfo.append('********************************************************************')
            listInfo.append(u'-------------%s-----生成下位机检查表核对---开始----------'%station.name)            
            WriteServerRecordFile(station,self.m_BasePath + u'/ServerRecord/',listInfo)
            listInfo.append(u'-------------%s-----生成下位机检查表核对---结束----------'%station.name)
            listInfo.append('********************************************************************')
            WriteTxtContent(station.name, listInfo, self.m_BasePath)
        self.scheduleText.SetLabel(u"    生成下位机检查表完成")
    
    def OutputRJPCheckResult(self):
        i = 0
        for key,value in g_CheckResult.items():
            self.Table.SetCellValue(i, 0, key)
            strResult = ''
            if value.has_key("RJP"):
                strResult = str(value["RJP"]["result"])
                self.Table.SetCellValue(i, 4, "\t".join(value["RJP"]["info"])) 
                self.Table.SetCellValue(i, 2, strResult)
            i += 1    
    def OutputIOCheckResult(self):
        i = 0
        for key,value in g_CheckResult.items():
            self.Table.SetCellValue(i, 0, key)
            strResult = ''
            if value.has_key("IO"):
                strResult = str(value["IO"]["result"])
                self.Table.SetCellValue(i, 1, strResult)
                self.Table.SetCellValue(i, 3, "\t".join(value["IO"]["info"])) 
            i += 1
        

if __name__ == '__main__':
    print 'start'
    '''
    from array import array
    fp = open('D://a//4_OBJ_XGX_GCZ_V1.0.0.bin','rb')
    allDta = array('B')
    fsize = os.path.getsize('D://a//4_OBJ_XGX_GCZ_V1.0.0.bin')
    print fsize
    allDta.fromfile(fp,fsize)
    print allDta

    qds = allDta[23:]
    pureData = []
    
    print len(qds)
    for i in range(0,len(qds),1030):
        if i + 1026 > len(qds):
            pureData.extend(qds[i+2:-4])
        else:
            pureData.extend(qds[i+2:i+1026])

    print len(pureData)
    
    shiftNo = 0
    sectionNum = pureData[shiftNo + 1]<<8 + pureData[shiftNo]
    shiftNo = 2
    #pureData = pureData[2:]
    for i in range(shiftNo,14*sectionNum + shiftNo,14):
        print pureData[i:i+14]
        print pureData[i+1]*256 + pureData[i]
    
    shiftNo += 14*sectionNum
    
    blockNum = pureData[shiftNo + 1]*256 + pureData[shiftNo]
    shiftNo += 2
    print blockNum,'block'
    for i in range(shiftNo,29*blockNum+ shiftNo,29):
        print pureData[i:i+29]
        print pureData[i+1]*256 + pureData[i]    
    shiftNo += 29*blockNum
    
    zoneNum = pureData[shiftNo]
    shiftNo += 1
    print zoneNum,'zone'
    for i in range(zoneNum):
        zjzNo = pureData[shiftNo+4]
        print pureData[shiftNo+1]*256 + pureData[shiftNo] 
        print pureData[shiftNo:shiftNo+30+14*zjzNo]
        shiftNo += 30+14*zjzNo
    '''
    app = wx.App()
    g_Frame = MainFrame()
    g_Frame.Show()
    app.MainLoop()
