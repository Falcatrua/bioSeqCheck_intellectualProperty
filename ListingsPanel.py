# -*- coding: utf-8 -*-
import wx
import  wx.lib.scrolledpanel as scrolled
import wx.lib.inspection
import SequenceListing
from SequenceListing import *
import Sequence
from Sequence import *

import tags
from tags import * 

FONT_A = 'Lucida Console'
FONT_B = 'Liberation Mono'
mChoices = ['']
ERROR_COLOUR = '#eb4c42'
REVISION_COLOUR = '#0D5BA8'

########################################################################
#class MyPanel(wx.Panel):
class MyPanel (scrolled.ScrolledPanel):
 
    #----------------------------------------------------------------------
    def __init__(self, parent, ListingsObj, opt):
        """Constructor"""
        #wx.Panel.__init__(self, parent)
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.number_of_boxxes = 0
        self.parent = parent
        self.ListingsObj = ListingsObj
        self.opt = opt
        

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.listSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.mainSizer.Add(self.listSizer, 0, wx.EXPAND|wx.ALL, 10)
 
        self.SetSizer(self.mainSizer)
        self.boxxes = []
        self.SetupScrolling()
 
    #----------------------------------------------------------------------
    def AddBoxx(self, sequenceObj):
        if self.opt == 1:
            b = Boxx (self, self.listSizer, self.number_of_boxxes, sequenceObj)
            self.boxxes.append (b)
            
        elif self.opt == 2:
            b = EditBoxx (self, self.listSizer, self.number_of_boxxes, sequenceObj)
            self.boxxes.append (b)
            
        
        self.number_of_boxxes += 1
        self.SetupScrolling()    
        
    #----------------------------------------------------------------------
    def RemoveBoxx(self, event):
        if len(self.boxxes) > 0:
            self.listSizer.Hide(self.boxxes[len(self.boxxes)-1].header)
            self.listSizer.Hide(self.boxxes[len(self.boxxes)-1].info)
            self.listSizer.Remove(self.boxxes[len(self.boxxes)-1].header)
            self.listSizer.Remove(self.boxxes[len(self.boxxes)-1].info)
            self.boxxes[len(self.boxxes)-1].header.Destroy()
            self.boxxes[len(self.boxxes)-1].info.Destroy()   
            del self.boxxes[len(self.boxxes)-1] 
            self.number_of_boxxes -= 1
            
            self.mainSizer.Layout()
            self.SetupScrolling()

    def ClearAll (self):
        while (len(self.boxxes) > 0):
            self.RemoveBoxx(None)
        
        self.mainSizer.Layout()
        self.SetupScrolling()

class Boxx (object):
    def __init__(self, parent, parentSizer, number, sequenceObj):
        self.parent = parent
        self.parentSizer = parentSizer
        self.number = number
        self.isOn = False
        self.seq = sequenceObj

        self.sizer = wx.BoxSizer (wx.VERTICAL)

        self.header = wx.Panel (parent)
        self.header.SetBackgroundColour('#e6e6fa')
        if sequenceObj.isSequence():
            label = "Sequencia "+ `parent.number_of_boxxes`
        else:
            label = "Header"

        headerFont = wx.FontFromPixelSize(pixelSize=(14,14), family=wx.SWISS, style=wx.NORMAL,
                weight=wx.NORMAL, face=FONT_A )
        headerText = wx.StaticText(self.header, -1, label,(-1, -1), (-1, -1), wx.ALIGN_LEFT|wx.TE_RICH)
        headerText.SetFont(headerFont)


        self.info = wx.Panel (parent)
        self.info.SetBackgroundColour ('WHITE')
        SeqInfo(self.info, self.seq)

        
        self.sizer.Add(self.header, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        self.sizer.Add(self.info, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        parentSizer.Add (self.sizer, 0, wx.EXPAND|wx.ALL, 0)
        self.header.Bind (wx.EVT_LEFT_UP, self.OnButton)
        
        self.sizer.Layout()
        parentSizer.Layout()

        #frame.Fit()
    
    def OnButton (self, event):
        if self.isOn == True :
            self.isOn = False
            for l in self.parent.ListingsObj.Lists:
                if len(l.boxxes) > self.number:
                    l.boxxes[self.number].sizer.Show (l.boxxes[self.number].info)
                    l.listSizer.Layout()                    
                #frame.Fit()
                l.SetupScrolling()
                    
        else:
            self.isOn = True
            for l in self.parent.ListingsObj.Lists:
                if len(l.boxxes) > self.number:
                    l.boxxes[self.number].sizer.Hide (l.boxxes[self.number].info)   
                    l.listSizer.Layout()                    
                #frame.Fit()
                l.SetupScrolling()

class SeqInfo (object):
    def __init__ (self, parent, sequenceObj):
        self.parent = parent
        self.font = wx.FontFromPixelSize(pixelSize=(14,14), family=wx.SWISS, style=wx.NORMAL,
                weight=wx.NORMAL, face=FONT_A )

        self.cumSumLines = [];

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        Infos = sequenceObj.info
        for i in range(len(Infos)):
            self.AddInfo (str(Infos[i][0]), str(Infos[i][1]), sequenceObj._infoError[i])

        
        if sequenceObj.isSequence():
            self.AddSeq (sequenceObj)

        self.parent.SetSizerAndFit(self.mainSizer)
        
        #for i in range(len(sequenceObj._infoError)):


    def AddInfo(self, text1, text2, infoError):
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        text1 = text1+"  "
        tex1 = wx.TextCtrl(self.parent, value=text1, style=wx.BORDER_NONE|wx.ALIGN_LEFT|wx.TE_READONLY|wx.TE_RICH|wx.TE_MULTILINE)
        tex1.SetFont(self.font)
        if infoError[0] == False:
            tex1.SetStyle(0, len(text1), wx.TextAttr('white',ERROR_COLOUR))
        h1.Add(tex1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        tex1.Bind (wx.EVT_LEFT_UP, self.TipOnClick)

        tex2 = wx.TextCtrl(self.parent, value=text2, style=wx.BORDER_NONE|wx.ALIGN_LEFT|wx.TE_READONLY|wx.TE_RICH|wx.TE_MULTILINE)
        tex2.SetFont(self.font)
        if infoError[1] == False:
            tex2.SetStyle(0, len(text2), wx.TextAttr('white',ERROR_COLOUR))
        lines = text2.split('\n')
        h1.Add(tex2, 3, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        #tex2.Bind (wx.EVT_LEFT_UP, self.SugestOnClick)
        
        h1.Add((1,1), 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        height = 1
        if len(lines) > 1:
            height = 0
        self.mainSizer.Add(h1, height, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)
        
            
    
    def AddSeq (self, sequenceObj):
        lines = sequenceObj.seq.split('\n')
        h1 = wx.BoxSizer(wx.VERTICAL)
        tex1 = wx.TextCtrl(self.parent, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE|wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_RICH)
        tex1.AppendText (sequenceObj.seq)
        tex1.SetFont(self.font)
        tex1.SetInsertionPoint(0)
        for error in sequenceObj._seqError:
            tex1.SetStyle(error[1], error[2], wx.TextAttr('white', ERROR_COLOUR))
            tex1.SetStyle(error[3], error[4], wx.TextAttr('white', ERROR_COLOUR))
        h1.Add(tex1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)
        self.mainSizer.Add(h1, len(lines)/2 +2, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)           
            

    def TipOnClick (self, event):
        obj = event.GetEventObject()
        Tip(obj)
      

        
class EditBoxx(object):
     def __init__(self, parent, parentSizer, number, sequenceObj):
        self.parent = parent
        self.parentSizer = parentSizer
        self.number = number
        self.isOn = False
        self.seq = sequenceObj

        self.sizer = wx.BoxSizer (wx.VERTICAL)

        self.header = wx.Panel (parent)
        self.header.SetBackgroundColour('#e6e6fa')
        if sequenceObj.isSequence():
            label = "Sequencia "+ `parent.number_of_boxxes`
        else:
            label = "Header"
        headerFont = wx.FontFromPixelSize(pixelSize=(14,14), family=wx.SWISS, style=wx.NORMAL,
                weight=wx.NORMAL, face=FONT_A )
        headerText = wx.StaticText(self.header, -1, label,(-1, -1), (-1, -1), wx.ALIGN_LEFT|wx.TE_RICH)
        headerText.SetFont(headerFont)
        
        
        self.info = wx.Panel (parent)
        self.info.SetBackgroundColour ('WHITE')
        EditSeqInfo (self.info, sequenceObj)

        self.sizer.Add(self.header, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        self.sizer.Add(self.info, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        parentSizer.Add (self.sizer, 0, wx.EXPAND|wx.ALL, 0)
        self.header.Bind (wx.EVT_LEFT_UP, self.OnButton)
        
        self.sizer.Layout()
        parentSizer.Layout()

     def OnButton (self, event):
        if self.isOn == True :
            self.isOn = False
            for l in self.parent.ListingsObj.Lists:
                l.boxxes[self.number].sizer.Show (l.boxxes[self.number].info)
                l.listSizer.Layout()
            l.SetupScrolling()   

        else:
            self.isOn = True
            for l in self.parent.ListingsObj.Lists:
                l.boxxes[self.number].sizer.Hide (l.boxxes[self.number].info)   
                l.Layout()
                #frame.Fit()
            l.SetupScrolling()

class EditSeqInfo (object):
    def __init__ (self, parent, sequenceObj):
        self.parent = parent

        self.font = wx.FontFromPixelSize(pixelSize=(14,14), family=wx.SWISS, style=wx.NORMAL,
                weight=wx.NORMAL, face=FONT_A)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        Infos = sequenceObj.info
        #print sequenceObj._infoError
        for i in range(len(Infos)):
            self.AddInfo (str(Infos[i][0]), str(Infos[i][1]), sequenceObj._infoError[i])
            s = str(Infos[i][1])
            if not s.isdigit():
                mChoices.append ( s ) 
        
        if sequenceObj.isSequence():
            self.AddSeq (sequenceObj)

        self.parent.SetSizer(self.mainSizer)


    def AddInfo(self, text1, text2, infoError ):
        h1 = wx.BoxSizer(wx.HORIZONTAL)
        text1 = text1+"  "
        tex1 = wx.TextCtrl(self.parent, value=text1, style=wx.BORDER_NONE|wx.ALIGN_LEFT|wx.TE_RICH|wx.TE_MULTILINE)
        tex1.SetFont(self.font)
        if infoError[0] == False:
            tex1.SetStyle(0, len(text1), wx.TextAttr('white',ERROR_COLOUR))
        h1.Add(tex1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        

        tex2 = wx.TextCtrl(self.parent, value=text2, style=wx.BORDER_NONE|wx.ALIGN_LEFT|wx.TE_RICH|wx.TE_MULTILINE)
        tex2.SetFont(self.font)
        lines = text2.split('\n')
        if infoError[1] == False:
            tex2.SetStyle(0, len(text2), wx.TextAttr('white',ERROR_COLOUR))
        h1.Add(tex2, 3, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        tex2.Bind (wx.EVT_SET_FOCUS, lambda event: self.focusText (event, text1.strip()) )
        
        h1.Add((1,1), 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)
        height = 1
        if len(lines) > 1:
            height = 0
        self.mainSizer.Add(h1, height, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)
        
    def AddSeq (self, sequenceObj):
        lines = sequenceObj.seq.split('\n')
        h1 = wx.BoxSizer(wx.VERTICAL)
        tex1 = wx.TextCtrl(self.parent, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.BORDER_NONE|wx.HSCROLL|wx.TE_DONTWRAP|wx.TE_RICH)
        tex1.AppendText (sequenceObj.seq)
        tex1.SetFont(self.font)
        tex1.SetInsertionPoint(0)
        for error in sequenceObj._seqError:
            tex1.SetStyle(error[1], error[2], wx.TextAttr('white', ERROR_COLOUR))
            tex1.SetStyle(error[3], error[4], wx.TextAttr('white', ERROR_COLOUR))
        h1.Add(tex1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)
        self.mainSizer.Add(h1, len(lines)/2 +2, wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)           
    
    def focusText (self, event, field):
        tc = event.GetEventObject()
        text = tc.GetValue()
        tc.Bind (wx.EVT_KILL_FOCUS, lambda event: self.changeText (event, text, field))

    def changeText (self, event, text, field):
        tc = event.GetEventObject()
        newtxt = tc.GetValue()
        listing = tc.GetParent().GetParent().ListingsObj.parent.RevisionList
        
        count = 0
        for info in listing.info:
            if info[0] == field:
                count = count + 1
        #buscar nas sequencias
        for s in listing.seqList:
            for info in s.info:
                if info[0] == field and info[1] == text:
                    count = count + 1
        if count > 1:
            sug = Sugestao(tc, field, text, newtxt)    
            if sug.active:
                for info in listing.info:
                    if info[0] == field:
                        info[1] = newtxt
                #buscar nas sequencias
                for s in listing.seqList:
                    for info in s.info:
                        if info[0] == field and info[1] == text:
                            info[1] = newtxt
                
                #Realizar as alterações de fato (achar os txtctrl buscando por childs)
                flag = 0
                counter = 0
                for pan in self.parent.GetParent().GetChildren():
                    for txtctrl in pan.GetChildren():
                        counter = counter + 1
                        if txtctrl.GetLabel().strip() == field:
                            flag = counter                            
                        elif txtctrl.GetLabel() == text and flag == counter-1:
                            txtctrl.SetLabel (newtxt)
                            txtctrl.SetStyle(0, len(newtxt), wx.TextAttr(REVISION_COLOUR, 'white'))
                            flag = 0                            

        event.Skip()

    def TipOnClick (self, event):
        obj = event.GetEventObject()
        Tip(obj)
    
    def SugestOnClick (self, event):
        obj = event.GetEventObject()
        Sugestao(obj)    


class ListingsPanel(object):
    def __init__(self, parentFrame ):
        self.parent = parentFrame
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(parentFrame, -1, style=wx.SP_LIVE_UPDATE|wx.SP_NOBORDER)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(splitter, -1)
        panel11 = wx.Panel(panel1, -1, size=(-1, 40))
        panel11.SetBackgroundColour('#53728c')
        headerText1 = wx.StaticText(panel11, -1, 'Listagem Original', (5, 5))
        headerText1.SetForegroundColour('WHITE')

        panel12 = wx.Panel(panel1, -1, style=wx.BORDER_SUNKEN)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.Lists = []
        self.Lists.append ( MyPanel(panel12, self, 1) )
        
        vbox.Add(self.Lists[0], 1, wx.EXPAND)
        panel12.SetSizer(vbox)
        panel12.SetBackgroundColour('WHITE')


        vbox1.Add(panel11, 0, wx.EXPAND)
        vbox1.Add(panel12, 1, wx.EXPAND)

        panel1.SetSizer(vbox1)
       
        
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        panel2 = wx.Panel(splitter, -1)
        panel21 = wx.Panel(panel2, -1, size=(-1, 40), style=wx.NO_BORDER)
        headerText2 = wx.StaticText(panel21, -1, 'Listagem Revisada', (5, 5))
        headerText2.SetForegroundColour('WHITE')
        panel21.SetBackgroundColour('#53728c')
        panel22 = wx.Panel(panel2, -1, style=wx.BORDER_RAISED)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        self.Lists.append ( MyPanel (panel22, self, 2))
        #self.list2 = MyPanel(panel22, self, 2)
        vbox3.Add(self.Lists[1], 1, wx.EXPAND)
        panel22.SetSizer(vbox3)


        panel22.SetBackgroundColour('WHITE')
        vbox2.Add(panel21, 0, wx.EXPAND)
        vbox2.Add(panel22, 1, wx.EXPAND)

        panel2.SetSizer(vbox2)
        
        splitter.SplitVertically(panel1, panel2, 375)
    
    def fillOriginalListing(self, seqListingObj):
        L = seqListingObj
        self.Lists[0].ClearAll()

        self.Lists[0].AddBoxx(L)
        for s in L.seqList:
            self.Lists[0].AddBoxx(s)

    def Mirror (self):
        originalL = self.Lists[0].ListingsObj.parent.OriginalList
        revisionL = self.Lists[1].ListingsObj.parent.RevisionList

        for i in range(1,len(self.Lists)):
            self.Lists[i].ClearAll()
            self.Lists[i].Refresh()
        
        revisionL.Clear()
        revisionL = revisionL.Clone (originalL)
        self.Lists[1].ListingsObj.parent.RevisionList = revisionL.Clone (originalL)
                
        self.Lists[1].AddBoxx(revisionL)
        self.Lists[1].opt = 2
        for s in revisionL.seqList:
            self.Lists[1].AddBoxx(s)

                    
            
              

########################################################################
class MyFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="Add / Remove Buttons")
        
        ListingsPanel (self)
        self.Center()
        self.Show()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    wx.lib.inspection.InspectionTool().Show() 
    app.MainLoop()