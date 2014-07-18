import wx
import  wx.lib.scrolledpanel as scrolled
import wx.lib.inspection

import ListingsPanel
from ListingsPanel import *
import Sequence
from Sequence import *
import SequenceListing
from SequenceListing import *

wx.ID_EXIT = 1

class GUI(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(GUI, self).__init__(*args, **kwargs) 
        
        
        self.OriginalList = SeqListing();
        self.RevisionList = SeqListing();

        #self.panels = ListingsPanel(self)
        self.ListingsPanel = ListingsPanel (self)
        self.MenuAndToolbar()
        
        #elf.SetSize((750, 500))
        self.SetTitle('Falcatrua & Co')
        self.Centre()
        self.Show()
    

    def MenuAndToolbar(self):
        #self.SetIcon(wx.Icon('P-icon.jpg', wx.BITMAPIMG_ICO))
        menubar = wx.MenuBar()
        
        ## File
        fileMenu = wx.Menu()    
        fileMenu.Append(wx.ID_NEW, '&New')
        fileOpen = fileMenu.Append(wx.ID_OPEN, "&Open\tCtrl+O"," Open a file to edit")
        self.Bind(wx.EVT_MENU, self.OnOpen )
        fileMenu.Append(wx.ID_ANY, '&Save')
        fileMenu.AppendSeparator()

        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mail...')

        fileMenu.AppendMenu(wx.ID_ANY, '&Import', imp)

        qmi = wx.MenuItem(fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(qmi)
        self.Bind(wx.EVT_MENU, self.OnQuit, qmi)

        menubar.Append(fileMenu, '&File')

        ## View
        viewMenu = wx.Menu()
        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar', 
            'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar', 
            'Show Toolbar', kind=wx.ITEM_CHECK)
            
        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        menubar.Append(viewMenu, '&View')
        
        
        ## MenuBar
        self.SetMenuBar(menubar)
        

        ## Status Bar
        self.toolbar = self.CreateToolBar()
        self.toolbar.AddLabelTool(1, '', wx.Bitmap ('exit2.png') )
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')


        ## Undo & Redo
        self.count = 5
        image = self.resizePic ( 'undo.png')
        tundo = self.toolbar.AddLabelTool(wx.ID_UNDO, '', image, wx.NullBitmap, 0, 
            'Desfazer' )
        image = self.resizePic ( 'redo.png')
        tredo = self.toolbar.AddLabelTool(wx.ID_REDO, '', image, wx.NullBitmap, 0,
            'Refazer' )
        self.toolbar.EnableTool(wx.ID_REDO, False)
             
        self.Bind(wx.EVT_TOOL, self.OnUndo, tundo)
        self.Bind(wx.EVT_TOOL, self.OnRedo, tredo)


        ## Import File
        self.toolbar.AddSeparator()
        image = self.resizePic ( 'import_file.png' )
        import_file = self.toolbar.AddLabelTool (4, '', image, wx.NullBitmap, 0, 
            'Importar Listagem de Sequencias' )
        #self.Bind(wx.EVT_TOOL, self.OnImportarSequencias, import_file)
        self.Bind(wx.EVT_MENU, self.OnOpen, fileOpen)
        

        ## Mirror File
        image = self.resizePic ( 'mirror_file.png' )
        mirror_file = self.toolbar.AddLabelTool (5, '', image, wx.NullBitmap, 0, 
            'Copiar Listagem para arquivo novo' )
        self.Bind(wx.EVT_TOOL, self.OnMirror, mirror_file)
        self.toolbar.EnableTool(5, False)
        

        self.toolbar.Realize()

    def OnImportarSequencias (self, import_file):
        print "Importar Sequencias"


    def OnMirror (self, e):
        #self.toolbar.EnableTool(5, False)  
        self.ListingsPanel.Mirror ()


    def resizePic (self, filename ):
        image = wx.Image( filename ) 
        image.Rescale(32, 32) 
        image = wx.BitmapFromImage(image)
        return image
        
    def OnQuit(self, e):
        self.Close()

    def ToggleStatusBar(self, e):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self, e):
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def OnUndo(self, e):
        if self.count > 1 and self.count <= 5:
            self.count = self.count - 1

        if self.count == 1:
            self.toolbar.EnableTool(wx.ID_UNDO, False)

        if self.count == 4:
            self.toolbar.EnableTool(wx.ID_REDO, True)

    def OnRedo(self, e):
        if self.count < 5 and self.count >= 1:
            self.count = self.count + 1

        if self.count == 5:
            self.toolbar.EnableTool(wx.ID_REDO, False)

        if self.count == 2:
            self.toolbar.EnableTool(wx.ID_UNDO, True)

    def OnOpen(self, e):
        wildcard = "All files (*.*)|*.*" 
        dlg = wx.FileDialog(
            self, message="Abrir arquivo",
            defaultFile="",
            wildcard=wildcard,
            #style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # checar se e um sequence listing mesmo
            self.OriginalList.Clear()
            self.OriginalList.importSeqListing (path)
            self.ListingsPanel.fillOriginalListing(self.OriginalList)
        dlg.Destroy()
        self.toolbar.EnableTool(5, True)


def main():
    ex = wx.App(False, 'Falcatrua & Co')
    GUI(None, size=(750,520))
    #wx.lib.inspection.InspectionTool().Show()     
    ex.MainLoop()


if __name__ == '__main__':
    main()