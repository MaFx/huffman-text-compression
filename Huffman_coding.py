import heapq
import wx
import os
from numpy import *

HuffAlphabeth = []
LZWAlphabeth = ""

class Example(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.args = args
        self.kwargs = kwargs
        self.fname=""    
        self.InitUI()        
        self.SetIcon(wx.Icon('favicon.ico',wx.BITMAP_TYPE_ICO))
        self.cMode = 0
        
    def InitUI(self):    

        #### MENU BAR ###
        menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        fitem = self.fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        menubar.Append(self.fileMenu, '&File')
        self.modeMenu = wx.Menu()
        self.fHuff = self.modeMenu.Append(21,'Huffman coding','Compression using Huffman coding', kind=wx.ITEM_CHECK)
        self.modeMenu.Check(self.fHuff.GetId(), True)
        self.Bind(wx.EVT_MENU,self.OnHuff,self.fHuff)
        self.fLZW = self.modeMenu.Append(22,'Lempel-Ziv-Welch coding','Compression using LZW coding', kind=wx.ITEM_CHECK)
        self.Bind(wx.EVT_MENU,self.OnLZW,self.fLZW)
        
        menubar.Append(self.modeMenu, '&Compression algorithm')
        menuAbout = wx.Menu()
        menuAbout.Append(2, "&About...", "About this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=2)
        menubar.Append(menuAbout, '&Help')
        self.SetMenuBar(menubar)

        ### Input fields & button ###
        self.panel = wx.Panel(self,-1)
        font = wx.Font(10,wx.ROMAN,wx.NORMAL,wx.NORMAL)
        statictext = wx.StaticText(self.panel,-1,"Uncompressed input text:",(15,5))        
        statictext = wx.StaticText(self.panel,-1,"Coding alphabeth:",(375,5))        
        statictext = wx.StaticText(self.panel,-1,"Coding output:",(605,5))        
        self.text = wx.TextCtrl(self.panel, -1, 'Insert your coding text here!',pos=(10,20),size=(350,250), style=wx.TE_MULTILINE )
        self.outText = wx.TextCtrl(self.panel, -1, 'OUTPUT WILL BE GENERATED HERE',pos=(600,20),size=(350,220), style=wx.TE_MULTILINE )
        self.abc = wx.TextCtrl(self.panel, -1, 'CODING ALPHABETH WILL BE GENERATED HERE',pos=(370,20),size=(200,220), style=wx.TE_MULTILINE )
        button = wx.Button(self.panel, 13, "Compress", pos=(600,250), size=(350,20))
        self.Bind(wx.EVT_BUTTON,self.OnCompress,id=13)

        ### OTHER OPTIONS ###
        self.SetSize((1000, 340))
        self.SetTitle('Datu kompresija')
        self.Centre()
        self.Show(True)

    def OnHuff(self,event):
        self.cMode = 0
        self.modeMenu.Check(self.fHuff.GetId(), True)
        self.modeMenu.Check(self.fLZW.GetId(), False)

    def OnLZW(self,event):
        self.cMode = 1
        self.modeMenu.Check(self.fHuff.GetId(), False)
        self.modeMenu.Check(self.fLZW.GetId(), True)

    def OnCompress(self,event):
        global HuffAlphabeth
        global LZWAplhabeth
        ### Huffman coding ###
        txt = self.text.GetValue()
        totalLen = len(txt)
        if self.cMode == 0 :
            self.List = None
            self.List = [[ 0,' ']]
            remove = False
            ### Symbol count in string ###
            for i in range(totalLen):
                isnew = True
                for j in range(len(self.List)):
                    if self.List[j][1] == txt[i] :
                        isnew = False
                        self.List[j][0] = self.List[j][0] + 1
                if isnew == True :
                    self.List.append([1,txt[i]])
                    if remove == False :
                        self.List.pop(0)
                        remove = True
    
            ### Sorting data ###
            for i in range(len(self.List)):
                for j in range(len(self.List)-i):
                    if self.List[i][0]>self.List[j][0] :
                        tmp = self.List[i]
                        self.List[i]=self.List[j]
                        self.List[j]=tmp
            ### Propability list calculation ###
            proplist = None
            proplist = []
            for i in range(len(self.List)):
                proplist.append((float(1.0 * self.List[i][0] / totalLen), self.List[i][1]))
            ### Huffman Alphabeth/Tree construction ###
            HuffAlphabeth = None
            HuffAlphabeth = []
            huffTree = makeHuffTree(proplist)
            printHuffTree(huffTree)
            ### Construct Huffman binary string ###
            output = ""
            length = 0
            for i in range(totalLen):
                for j in range(len(HuffAlphabeth)):
                    if txt[i] == HuffAlphabeth[j][0] :
                        output += HuffAlphabeth[j][1]+" "
                        length += len(HuffAlphabeth[j][1])
            self.outText.SetValue(output)
            length = int(100.0-100.0*(length/(8.0*totalLen)))
        if self.cMode == 1 :
            ### Call for the compression algorithm ###
            compressed,size = LZWcompress(txt)
            #self.outText.SetValue(compressed)
            self.abc.SetValue(LZWAlphabeth)
            output = ""
            for i in range(len(compressed)):
                output += str(compressed[i])
            self.outText.SetValue(output)
            if size < 512 :
                totalSize = 9*len(compressed)
            if size < 1024 :
                totalSize = 10*len(compressed)
            if size < 2048 :
                totalSize = 11*len(compressed)
            if size < 4096 :
                totalSize = 12*len(compressed)
            length = int(100.0-100.0*(totalSize/(8.0*totalLen)))
        self.OnPrint(length)
            
                

    def OnPrint(self,length):
        global HuffAlphabeth
        compression = "                                                       "
        wx.StaticText(self.panel, -1, compression, (370, 250), style=wx.TE_RIGHT)
        compression = "Compression Ratio:"+str(length)+"%"
        outtext = ""
        if self.cMode == 0:
            for i in range(len(HuffAlphabeth)):
                outtext += '"'+HuffAlphabeth[i][0]+'" - '+HuffAlphabeth[i][1]+'\n' 
                self.abc.SetValue(outtext)
        wx.StaticText(self.panel, -1, compression, (370, 250), style=wx.TE_RIGHT)
            
        

    def OnAbout(self, event):
        AboutFrame().Show()

    def OnQuit(self, e):
        self.Close()

class AboutFrame(wx.Frame):

    title = "About"

    def __init__(self):
        wx.Frame.__init__(self, wx.GetApp().TopWindow, title=self.title)
        panel = wx.Panel(self,-1)
        text = "Created by\nMartins Fridenbergs\n2012\nDeveloped in Python"
        font = wx.Font(10,wx.ROMAN,wx.NORMAL,wx.NORMAL)
        statictext = wx.StaticText(panel,-1,text,(30,20),style = wx.ALIGN_CENTRE)
        statictext.SetFont(font)
        self.Center()
        self.SetSize((200,150))

### LZW Coding algorithm ###
def LZWcompress(uncompressed):
    global LZWAlphabeth
    LZWAlphabeth = ""
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), chr(i)) for i in xrange(dict_size))
    # in Python 3: dictionary = {chr(i): chr(i) for i in range(dict_size)}
    LZWAlphabeth += "0-255: Default ANSI charset\n"        
 
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
            LZWAlphabeth += str(dict_size)+" - '"+wc+"'\n"
    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return [result,dict_size]

### HUFFMAN Coding functions ###        
def makeHuffTree(symbolTupleList):
    trees = list(symbolTupleList)
    heapq.heapify(trees)
    while len(trees) > 1:
        childR, childL = heapq.heappop(trees), heapq.heappop(trees)
        parent = (childL[0] + childR[0], childL, childR)
        heapq.heappush(trees, parent)
    return trees[0]
def printHuffTree(huffTree, prefix = ''):
    global HuffAlphabeth
    if len(huffTree) == 2:
        HuffAlphabeth.append([ huffTree[1], prefix ])
    else:
        printHuffTree(huffTree[1], prefix + '0')
        printHuffTree(huffTree[2], prefix + '1')
        
if __name__ == '__main__':
    ex = wx.App()
    main = Example(None)
    ex.MainLoop()
