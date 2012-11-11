import os
import wx
import wx.lib.inspection
import wx.gizmos
from nltk.tree import *
 
wildcard = "All files (*.*)|*.*"
            

class Annotator(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY)
        self.currentDirectory = os.getcwd()
        
        #create menubar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()
        toolMenu = wx.Menu()    

        # fileMenu items and bindings
        newFileItem = fileMenu.Append(wx.ID_NEW, "New")
        self.Bind(wx.EVT_MENU, self.OnNew, newFileItem)

        openFileItem = fileMenu.Append(wx.ID_OPEN, "Open")
        self.Bind(wx.EVT_MENU, self.OnOpenFile, openFileItem)
 
        saveFileItem = fileMenu.Append(wx.ID_SAVE, "Save")
        self.Bind(wx.EVT_MENU, self.OnSaveFile, saveFileItem)

        # menu separator
        fileMenu.AppendSeparator()

        quitFileItem = fileMenu.Append(wx.ID_EXIT, "Quit")
        self.Bind(wx.EVT_MENU, self.OnQuit, quitFileItem)

        # attach menus to menubar    
        menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        menubar.Append(toolMenu, '&Tools')
        
        # attach menubar to frame
        self.SetMenuBar(menubar)
        
        # listbox widget to display strings from opened file
        panel1 = wx.Panel(self, -1)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel1, -1)
        hbox1.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.NLTKTree)
        self.Bind(wx.EVT_LISTBOX, lambda event: self.MakeTree(event, hbox1))
        
        # Annotator tree main interface
        self.annotree = wx.TreeCtrl(panel1, 1, wx.DefaultPosition, (-1,-1), 
            wx.TR_EDIT_LABELS|wx.TR_HAS_BUTTONS|wx.TR_FULL_ROW_HIGHLIGHT)
        self.annotree.Bind(wx.EVT_TREE_SEL_CHANGED, self.TreeSelect, id=1)
        
        hbox1.Add(self.annotree, 1, wx.EXPAND, 20)
        
        self.annotree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag)
        self.annotree.Bind(wx.EVT_TREE_END_DRAG, self.OnEndDrag)

        vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel1.SetSizer(hbox1)

        self.SetSize((700,400))
        self.SetTitle('Annotator')
        self.Centre()
        self.Show(True)    


        #rootID = self.annotree.AddRoot("S", -1, -1, None)
            #npId = self.annotree.AppendItem(rootID, "NP")
            #vpId = self.annotree.AppendItem(rootID, "VP")
            
            # WILL COME FROM TREE PARSE ON THE LEFT
            # noun phrase subtree
            #a1 = self.annotree.AppendItem(npId, "A")
            #npId2 = self.annotree.AppendItem(npId, "NP")
            #a2 = self.annotree.AppendItem(npId2, "A")
            #n1 = self.annotree.AppendItem(npId2, "N")
            #self.annotree.AppendItem(a1, "Colorless")
            #self.annotree.AppendItem(a2, "green")
            #self.annotree.AppendItem(n1, "ideas")
            
            
            # verb phrase subtree
            #verbId = self.annotree.AppendItem(vpId, "V")
            #AdvId = self.annotree.AppendItem(vpId, "Adv")
            #self.annotree.AppendItem(verbId, "sleep")
            #self.annotree.AppendItem(AdvId, "furiously")
                #btnPanel = wx.Panel(panel, -1)
                
                #new = wx.Button(btnPanel, ID_NEW, 'New', size=(90, 30))
                #ren = wx.Button(btnPanel, ID_RENAME, 'Rename', size=(90, 30))
                #dlt = wx.Button(btnPanel, ID_DELETE, 'Delete', size=(90, 30))
                #clr = wx.Button(btnPanel, ID_CLEAR, 'Clear', size=(90, 30))    

                #self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
                #self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
                #self.Bind(wx.EVT_BUTTON, self.OnDelete, id=ID_DELETE)
                #self.Bind(wx.EVT_BUTTON, self.OnClear, id=ID_CLEAR)
                #self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

                #vbox.Add((-1, 20))
                #vbox.Add(new)
                #vbox.Add(ren, 0, wx.TOP, 5)
                #vbox.Add(dlt, 0, wx.TOP, 5)
                #vbox.Add(clr, 0, wx.TOP, 5)

                #btnPanel.SetSizer(vbox)
                #hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
            

            # toolbar
            #toolbar = self.CreateToolBar()
            #makeTreeItem = toolbar.AddLabelTool(wx.ID_ANY, 'Make tree', wx.Bitmap('/home/arish/Downloads/ptree.png'))
            #toolbar.Realize()


    
#--------------------- Annotator class methods -----------------------#


        
    def MakeTree(self, event, rf_widget):
        """Create Annotator tree from selected s-expression"""
        
        sentence = self.listbox.GetStringSelection()
        parsed_sentence = Tree.parse(sentence, remove_empty_top_bracketing=True)
        # list of productions as tuples
        production_list = parsed_sentence.productions()
        
        # add root (as string) first
        root = production_list[0].lhs().__str__()
        parentID = self.annotree.AddRoot(root, -1, -1, None)
        
        seen_nodes = {root:parentID}
        
        # now add subsequent nodes individually
        for production in production_list:
            parent = production.lhs().__str__()
            for node in production.rhs():
                
                # if we've already seen the parent of current node, use that ID
                if seen_nodes.has_key(parent):
                    nodeID = self.annotree.AppendItem(seen_nodes[parent], node.__str__())
                    print parent.__str__()
                    # add current node to list of seen nodes
                    seen_nodes[node.__str__()] = nodeID
        
           
    #    rf_widget.fSizer.Layout()
    #    rf_widget.Fit()


         
    def NLTKTree(self, event):
        """Draw NLTK tree and display in Tk window"""
        
        sentence = self.listbox.GetStringSelection()
        parse = Tree.parse(sentence, remove_empty_top_bracketing=True)
        parse.draw()

        
    def TreeSelect(self, event):

        item =  event.GetItem()
        print self.annotree.GetItemText(item)

        
    def OnBeginDrag(self, event):
        
        if self.annotree.GetChildrenCount(event.GetItem()) == 0:
            event.Allow()
            self.dragItem = event.GetItem()
        else:
            pass
            

 
    def OnEndDrag(self, event):
        
        try:
            old = self.dragItem
        except:
            return
        # Get the other IDs that are involved
        new = event.GetItem()
        parent = self.annotree.GetItemParent(new)
        if not parent.IsOk():
            return
 
        text = self.annotree.GetItemText(old)
        self.annotree.Delete(old)
        self.annotree.InsertItem(parent, new, text)

 
    def OnNew(self, event):
        pass

    
    def OnOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlog = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        
        if dlog.ShowModal() == wx.ID_OK:
            path = dlog.GetPath()
            #print type(path)
            f = open(path)

            # to be generalized across files/CHILDES format
            text = f.readlines(1)
            filtered_text = [item for item in text if item != '\n']
            stripped_text = [item.replace('\n', '').strip() for item in filtered_text]
            for sentence in stripped_text[:6]:
                self.listbox.Append(sentence)    

        dlog.Destroy()


    def OnSaveFile(self, event):
        """
        Create and show the Save FileDialog
        """
        dlog = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=self.currentDirectory, 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )
        if dlog.ShowModal() == wx.ID_OK:
            path = dlog.GetPath()
            print "You chose the following filename: %s" % path
        dlog.Destroy()


    def OnQuit(self, event):
        self.Close()


#------------------------- Main loop -----------------------------#
                        


def main():

    app = wx.App(False)
    frame = Annotator()
    frame.Show()
    #wx.lib.inspection.InspectionTool().Show() 
    app.MainLoop()
 

if __name__ == "__main__":
    main()