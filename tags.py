# -*- coding: utf-8 -*-
import wx
tags = {
            '<110>': 'Applicant name',
            '<120>': 'Title of invention',
            '<130>': 'File reference',
            '<140>': 'Current patent application',
            '<141>': 'Current filing date',
            '<150>': 'Earlier patent application',
            '<151>': 'Earlier application filing date',
            '<160>': 'Number of SEQ ID NOs',
            '<170>': 'Software',
            '<210>': 'Information for SEQ ID No: x',
            '<211>': 'Length',
            '<212>': 'Type',
            '<213>': 'Organism',
            '<220>': 'Feature',
            '<221>': 'Name/key',
            '<222>': 'Location',
            '<223>': 'Other information',
            '<300>': 'Publication information',
            '<301>': 'Authors',
            '<302>': 'Title',
            '<303>': 'Journal',
            '<304>': 'Volume',
            '<305>': 'Issue',
            '<306>': 'Pages',
            '<307>': 'Date',
            '<308>': 'Database accession number',
            '<309>': 'Database entry date',
            '<310>': 'Document number',
            '<311>': 'Filing date',
            '<312>': 'Publication date',
            '<313>': 'Relevant residues in SEQ ID No: x: from to',
            '<400>': 'Sequence'
        }


class Tip (object):
    def __init__ (self, parent):
        #parent tem que ser um TextCtrl
        self.infoPopup = wx.PopupWindow(parent, flags = wx.SIMPLE_BORDER)
        self.infoPopup.Bind (wx.EVT_LEAVE_WINDOW, self.goAway )
        label = self.getTip(parent)
        border = 1
        text = wx.StaticText(self.infoPopup, label = label, pos=(border,border))
        size = text.GetBestSize()
        self.infoPopup.SetSize ((size.width+2*border, size.height+2*border))
        self.infoPopup.Position(parent.ClientToScreen((0, 0)), (-1,1))
        self.infoPopup.Show()
        
    def getTip (self, parent):
        value = parent.GetValue()
        value = value.strip(' ')
        try:
            return tags[value]
        except:
            return 'Tag inexistente'
    def goAway (self, event):
        self.infoPopup.Show(False)
        self.infoPopup.Close()
        #self.infoPopup = None

class Sugestao (object):
    def __init__ (self, parent, field, text, newtxt):
        """
        self.active = False
        self.popup = wx.PopupWindow (parent)
        self.panel = wx.Panel(self.popup) 
        top_sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = "Ha mais campos"+field+" contendo \'"+text+"\'"
        txt = wx.StaticText(self.panel,wx.ID_ANY, label=label)
        top_sizer.Add(txt, 0, wx.EXPAND|wx.ALL, 2)
        #   parent.Bind (wx.EVT_LEAVE_WINDOW, self.goAway )    
        
        textctrl = wx.TextCtrl(self.panel, style=wx.BORDER_NONE|wx.TE_READONLY) 
        textctrl.AppendText ("O que voce deseja fazer?")
        top_sizer.Add(textctrl, 0, wx.EXPAND|wx.ALL, 2)

        top_sizer.Add((1,1), 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 0)

        textctrl = wx.TextCtrl(self.panel, style=wx.BORDER_SIMPLE|wx.TE_READONLY) 
        textctrl.AppendText ("Mudar todos para "+newtxt)
        top_sizer.Add(textctrl, 0, wx.EXPAND|wx.ALL, 2) 
        textctrl.Bind (wx.EVT_RIGHT_DOWN, self.doIt )
        
        ignore = wx.TextCtrl(self.panel, style=wx.BORDER_SIMPLE|wx.TE_READONLY) 
        ignore.AppendText ("Ignorar")
        top_sizer.Add(ignore, 0, wx.EXPAND|wx.ALL, 2) 
        ignore.Bind (wx.EVT_RIGHT_DOWN, self.goAway )        
        
        self.panel.SetSizer(top_sizer) 
        sizer = wx.BoxSizer() 
        sizer.Add(self.panel, 0, wx.EXPAND|wx.ALL, 3) 
        self.popup.SetSizerAndFit(sizer) 
        self.popup.Layout()

        self.popup.Position(parent.ClientToScreen((0, 0)), (-10,10))
        self.popup.Show()
       """
        self.active = False
        scrollw =  parent.GetParent().GetParent()
        #gui =  parent.GetParent().GetParent().GetParent().GetParent().GetParent().GetParent()
        
        self.panel = wx.Panel(scrollw)
        self.popup = wx.Menu()  
        self.popup.Append(-1, "Ha mais campos"+field+" contendo \'"+text+"\'")
        self.popup.Append(-1, "O que voce deseja fazer?")        
        
        mudar = self.popup.Append(-1, "Mudar todos para "+newtxt)
        self.panel.Bind(wx.EVT_MENU, self.doIt)
        ignorar = self.popup.Append(-1, "Ignorar")
        #self.panel.Bind(wx.EVT_MENU, self.goAway)
        #self.panel.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        pos = self.panel.ScreenToClient(wx.GetMousePosition())
        self.panel.PopupMenu(self.popup, pos)

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        pos = self.panel.ScreenToClient(pos)
        self.panel.PopupMenu(self.popupmenu, pos)
        
    
    def goAway (self, event):
        self.popup.Show(False)
        self.popup.Close()

    def doIt (self, event):
        self.active = True
    

            
