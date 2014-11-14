# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 14:59:26 2014

@author: Robert
"""

import wx

class Cell(wx.Button):
  def __init__(self, *args, **kwargs):
    super(Cell, self).__init__(*args, **kwargs)

a = wx.Frame()
wx.EVT_COMMAND
class Example(wx.Frame):
  
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, 
            size=(300, 250))
        self.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.onLeftButtonCellClick)            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

 
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.display = wx.TextCtrl(self, style=wx.TE_RIGHT)
        vbox.Add(self.display, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=4)

        rows = 10
        columns = 10
        
        gs = wx.GridSizer(rows, columns, 1, 1)
        buttons=[]
        for r in range(0, rows):
          for c in range(0, columns):
            button=Cell(self, label='')
            buttons.append((button, 0, wx.EXPAND))
        gs.AddMany(buttons)

        vbox.Add(gs, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def onLeftButtonCellClick(self, e):
      self.display.SetText('botton pressed')
      print 'button pressed'
    
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title='Kakuro Solver')
    app.MainLoop()
    