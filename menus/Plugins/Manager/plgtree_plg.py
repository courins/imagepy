# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 01:00:02 2017

@author: yxl
"""

from core.engines import Free
import wx
import IPy
from core.loader import loader
from wx.py.editor import EditorFrame

class TreeFrame ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Plugins Tree", pos = wx.DefaultPosition, size = wx.Size( 452,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.tre_plugins = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        self.tre_plugins.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer1.Add( self.tre_plugins, 0, wx.ALL|wx.EXPAND, 5 )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Plugin Infomation:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer4.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"[SourceCode]", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        
        bSizer4.Add( self.m_staticText3, 0, wx.ALL, 5 )
        bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
        
        self.txt_info = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        bSizer3.Add( self.txt_info, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.tre_plugins.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.on_run )
        self.tre_plugins.Bind( wx.EVT_TREE_SEL_CHANGED, self.on_select )
        self.m_staticText3.Bind( wx.EVT_LEFT_DOWN, self.on_source )
        self.plg = None
        self.load()
        
    def addnode(self, parent, data):
        for i in data:
            if i=='-':continue
            if isinstance(i, tuple):
                item = self.tre_plugins.AppendItem(parent, i[0].title)
                self.tre_plugins.SetItemPyData(item, i[0])
                self.addnode(item, i[1])
            else:
                item = self.tre_plugins.AppendItem(parent, i.title)
                self.tre_plugins.SetItemPyData(item, i)
                
    def load(self):
        data = loader.build_plugins('menus')
        root = self.tre_plugins.AddRoot('Plugins')
        self.addnode(root, data[1])
    
    def __del__( self ):
        pass
    
    # Virtual event handlers, overide them in your derived class
    def on_run( self, event ):
        plg = self.tre_plugins.GetItemPyData(event.GetItem())
        if hasattr(plg, 'start'):plg().start()
    
    def on_select( self, event ):
        plg = self.tre_plugins.GetItemPyData(event.GetItem())
        print type(plg)
        if plg!=None:
            self.plg = plg
            if plg.__doc__!=None:
                self.txt_info.SetValue(plg.__doc__)
            elif hasattr(plg, '__module__'): 
                self.txt_info.SetValue('plugin at %s'%plg.__module__)
            else: self.txt_info.SetValue('package at %s'%plg.__name__)
        
    def on_source(self, event):
        path = self.plg.__module__.replace('.','/')+'.py'
        EditorFrame(filename=path).Show()
    
class PlgTree(Free):
    title = 'Plugin Tree View'
        
    def run(self, para=None):
        TreeFrame(IPy.curapp).Show()
        
plgs = [PlgTree]