import wx


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Box布局器', size=(300, 120))
        self.Center()  # 设置窗口屏幕居中
        panel = wx.Panel(parent=self)
        # 创建垂直方向box布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.statictext = wx.StaticText(parent=panel, label='Button1单击')
        # 添加静态文本到vbox布局管理器
        vbox.Add(self.statictext, proportion=2, flag=wx.FIXED_MINSIZE | wx.TOP | wx.CENTER, border=1)
        b1 = wx.Button(parent=panel, id=10, label='Button1')
        b2 = wx.Button(parent=panel, id=11, label='Button2')
        self.Bind(wx.EVT_BUTTON, self.on_click, id=10, id2=20)
        # 创建水平方向box布局管理器
        hbox = wx.BoxSizer()    # hbox = wx.BoxSizer(wx.HORIZONTAL),默认为水平方向
        hbox.Add(b1, 0, wx.EXPAND | wx.BOTTOM, 5)
        hbox.Add(b2, 0, wx.EXPAND | wx.BOTTOM, 5)
        # 将水平box添加到垂直box
        vbox.Add(hbox, proportion=1, flag=wx.CENTER)
        panel.SetSizer(vbox)

    def on_click(self):
        pass

class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True

    def OnExit(self):
        print('应用程序退出')
        return 0

if __name__ == '__main__':
    app = App()
    app.MainLoop()   #进入主循环事件