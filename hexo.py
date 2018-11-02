import tkinter
import os
from win32api import GetSystemMetrics
from threading import Thread


class Hexo:
    command_dict = {'g': 'hexo g', 's': 'hexo s', 'd': 'hexo d', 'clean': 'hexo clean'}
    over_dict = {'g': '初始化成功~', 's': 'Hexo已开启~', 'd': 'Hexo已提交~', 'clean': 'Hexo已重置~'}

    def __init__(self, blog_path):
        self.path = blog_path
        # 分辨率
        self.x = GetSystemMetrics(0)
        self.y = GetSystemMetrics(1)
        self.root = tkinter.Tk()
        self.root.wm_attributes('-topmost', 1)
        self.show()

    def show(self):

        # 创建385×200大的窗口,并移动到屏幕400,300位置
        self.root.geometry("467x200+%d+%d" % ((self.x - 385) // 2, (self.y - 200) // 2))
        # 无边框启动
        self.root.overrideredirect(True)

        # 花色
        tkinter.Frame(self.root, width=50, height=10, bg='blue').grid(row=0, column=0)
        tkinter.Frame(self.root, width=50, height=10, bg='blue').grid(row=0, column=5)
        tkinter.Frame(self.root, width=50, height=10, bg='red').grid(row=1, column=0)
        tkinter.Frame(self.root, width=50, height=10, bg='red').grid(row=1, column=5)
        tkinter.Frame(self.root, width=50, height=10, bg='black').grid(row=1, column=2)
        tkinter.Frame(self.root, width=50, height=10, bg='black').grid(row=1, column=3)

        # 窗体标题,使用布局排版,第一行第三列开始占两列
        tkinter.Label(self.root, text='hexo-see', font=('Segoe Print', 22)).grid(row=0, column=2, columnspan=2)

        # 留白
        tkinter.Label(self.root, text=' ', ).grid(row=1, column=4)

        tkinter.Button(text='重新生成静态文件', command=lambda: self.transfer('g')).grid(row=2, column=2, padx=5)
        tkinter.Button(text='清除本地public文件', command=lambda: self.transfer('clean')).grid(row=2, column=3, padx=5)

        tkinter.Label(self.root, text='', ).grid(row=3)

        tkinter.Button(text='创建文章', command=lambda: self.n()).grid(row=4, column=1, padx=5)
        tkinter.Button(text='提交仓库', command=lambda: self.transfer('d')).grid(row=4, column=2, padx=5)
        tkinter.Button(text='本地预览', command=lambda: self.transfer('s')).grid(row=4, column=3, padx=5)
        tkinter.Button(text=' 退出 ', command=lambda: os._exit(0)).grid(row=4, column=4, padx=5)

        # 为窗口绑定无界面时可拖动的相关函数
        self.root.bind("<B1-Motion>", self.root_move)
        self.root.bind("<Button-1>", self.mouse)

        self.root.mainloop()

    def n(self):

        # 创建窗体
        self.pub_tk = tkinter.Toplevel()
        self.pub_tk.bind("<B1-Motion>", self.pub_move)
        self.pub_tk.bind("<Button-1>", self.mouse)
        self.pub_tk.wm_attributes('-topmost', 1)
        self.pub_tk.geometry("279x300+%d+%d" % ((self.x - 260) // 2, (self.y - 300) // 2))
        self.pub_tk.overrideredirect(True)

        # 窗体标题
        tkinter.Label(self.pub_tk, text='hexo-see', font=('Segoe Print', 22)).grid(row=0, column=1, columnspan=2)

        # 留白与布局专用
        tkinter.Frame(self.pub_tk, width=50, height=10, bg='blue').grid(row=0, column=0)
        tkinter.Frame(self.pub_tk, width=50, height=10, bg='blue').grid(row=0, column=3)
        tkinter.Frame(self.pub_tk, width=50, height=10, bg='red').grid(row=1, column=0)
        tkinter.Frame(self.pub_tk, width=50, height=10, bg='red').grid(row=1, column=3)
        tkinter.Frame(self.pub_tk, width=10, height=50, bg='black').grid(row=11, column=0)
        tkinter.Frame(self.pub_tk, width=10, height=50, bg='black').grid(row=11, column=3)

        # 标题
        tkinter.Label(self.pub_tk, text='标题', font=('黑体', 16)).grid(row=2, column=1, columnspan=2)
        title_text = tkinter.Entry(self.pub_tk, relief='flat', width=25)
        title_text.grid(row=3, column=1, columnspan=2)

        # 留白/空行
        tkinter.Frame(self.pub_tk, width=50, height=10).grid(row=4, column=3)

        # 标签
        tkinter.Label(self.pub_tk, text='标签', font=('黑体', 16)).grid(row=5, column=1, columnspan=2)
        tags_text = tkinter.Entry(self.pub_tk, relief='flat', width=25)
        tags_text.grid(row=6, column=1, columnspan=2)

        # 留白/空行
        tkinter.Frame(self.pub_tk, width=50, height=10).grid(row=7, column=2)  # 留白

        # 分类
        tkinter.Label(self.pub_tk, text='分类', font=('黑体', 16)).grid(row=8, column=1, columnspan=2)
        cats_text = tkinter.Entry(self.pub_tk, relief='flat', width=25)
        cats_text.grid(row=9, column=1, columnspan=2)

        # 留白/空行
        tkinter.Frame(self.pub_tk, width=50, height=10).grid(row=10, column=2)  # 留白

        tkinter.Button(self.pub_tk, text='开始创建',
                       command=lambda: self.transfer('n', title_text, tags_text, cats_text)).grid(row=11, column=1)
        tkinter.Button(self.pub_tk, text='放弃创建', command=lambda: self.pub_tk.destroy()).grid(row=11, column=2)

    def publish_blog(self, title_text, tags_text, cats_text):
        title = title_text.get().replace(' ', '')
        tags = [tag for tag in tags_text.get().split(' ') if tag != '']
        cats = [cat for cat in cats_text.get().split(' ') if cat != '']

        # 创建文章
        os.chdir(self.path)
        os.system('hexo n %s ' % title)

        # 为文章加上标签和分类
        os.chdir('.\source\_posts')
        with open('./%s.md' % title, 'rb') as f:
            md = f.read().decode()

        md = md.replace('tags:', 'tags: %s' % tags)
        md = md.replace('categories:', 'categories: %s' % cats)

        with open('./' + title + '.md', 'wb') as f:
            f.write(md.encode())

        # 创建成功弹窗并销毁创建文章的窗口
        self.pub_tk.destroy()
        self.warn = tkinter.Toplevel()
        self.warn.overrideredirect(True)
        self.warn.wm_attributes('-topmost', 1)
        self.warn.geometry("330x120+%d+%d" % ((self.x - 260) // 2, (self.y - 110) // 2))
        self.warn.bind("<B1-Motion>", self.warn_move)
        self.warn.bind("<Button-1>", self.mouse)

        # 留白与布局专用
        tkinter.Frame(self.warn, width=50, height=10).grid(row=0, column=0)
        tkinter.Frame(self.warn, width=50, height=10, bg='blue').grid(row=1, column=0)
        tkinter.Frame(self.warn, width=50, height=10, bg='blue').grid(row=1, column=4)
        tkinter.Frame(self.warn, width=25, height=10).grid(row=1, column=1)
        tkinter.Frame(self.warn, width=25, height=10).grid(row=1, column=3)
        tkinter.Frame(self.warn, width=50, height=10, bg='red').grid(row=3, column=0)
        tkinter.Frame(self.warn, width=50, height=10, bg='red').grid(row=3, column=4)
        tkinter.Frame(self.warn, width=10, height=50, bg='black').grid(row=5, column=0)
        tkinter.Frame(self.warn, width=10, height=50, bg='black').grid(row=5, column=4)

        tkinter.Label(self.warn, text='新文章创建成功!', font=('黑体', 12)).grid(row=2, column=2)

        tkinter.Frame(self.warn, height=20).grid(row=4, column=3)  # 留白好看

        tkinter.Button(self.warn, text='打开文件', command=lambda: os.startfile(title + '.md')).grid(row=5, column=1)
        tkinter.Button(self.warn, text='继续创建', command=lambda: self.continue_publish()).grid(row=5, column=2)
        tkinter.Button(self.warn, text=' 确 定 ', command=lambda: self.warn.destroy()).grid(row=5, column=3)

    def transfer(self, command, *args):
        if command in Hexo.command_dict.keys():
            Thread(target=self.exec_cmd, args=(command,)).start()
        if command == 'n':
            Thread(target=self.publish_blog, args=(args[0], args[1], args[2])).start()

    def exec_cmd(self, command):
        os.chdir(self.path)
        if command != 's':
            os.system(Hexo.command_dict[command])
        self.over = tkinter.Toplevel()
        self.over.overrideredirect(True)
        self.over.wm_attributes('-topmost', 1)
        self.over.geometry("214x110+%d+%d" % ((self.x - 260) // 2, (self.y - 110) // 2))
        self.over.bind("<B1-Motion>", self.over_move)
        self.over.bind("<Button-1>", self.mouse)

        tkinter.Frame(self.over, width=40, height=10).grid(row=0, column=0)
        tkinter.Frame(self.over, width=40, height=10, bg='blue').grid(row=1, column=0)
        tkinter.Frame(self.over, width=40, height=10, bg='blue').grid(row=1, column=4)
        tkinter.Frame(self.over, width=20, height=10).grid(row=1, column=1)
        tkinter.Frame(self.over, width=20, height=10).grid(row=1, column=3)
        tkinter.Frame(self.over, width=40, height=10, bg='red').grid(row=3, column=0)
        tkinter.Frame(self.over, width=40, height=10, bg='red').grid(row=3, column=4)
        tkinter.Frame(self.over, width=10, height=40, bg='black').grid(row=5, column=0)
        tkinter.Frame(self.over, width=10, height=40, bg='black').grid(row=5, column=4)

        tkinter.Label(self.over, text=Hexo.over_dict[command], font=('黑体', 12)).grid(row=2, column=2)

        tkinter.Frame(self.over, height=20).grid(row=4, column=3)  # 留白好看

        tkinter.Button(self.over, text=' 确 定 ', command=lambda: self.over.destroy()).grid(row=5, column=2)

        if command == 's':
            self.kill_port(4000)
            os.system(Hexo.command_dict[command])



    def continue_publish(self):
        self.n()
        self.warn.destroy()

    @staticmethod
    def kill_port(port):
        # 查找端口的pid
        find_port = 'netstat -aon | findstr %s' % port
        result = os.popen(find_port)
        pid = result.read().split(' ')[-1]
        # 占用端口的pid
        find_kill = 'taskkill -f -pid %s' % pid
        os.popen(find_kill)

    @staticmethod
    def mouse(event):
        global x, y
        x, y = event.x, event.y

    def root_move(self, event):
        global x, y
        new_x = (event.x - x) + self.root.winfo_x()
        new_y = (event.y - y) + self.root.winfo_y()
        s = "467x200+" + str(new_x) + "+" + str(new_y)
        self.root.geometry(s)

    def pub_move(self, event):
        global x, y
        new_x = (event.x - x) + self.pub_tk.winfo_x()
        new_y = (event.y - y) + self.pub_tk.winfo_y()
        s = "279x300+" + str(new_x) + "+" + str(new_y)
        self.pub_tk.geometry(s)

    def warn_move(self, event):
        global x, y
        new_x = (event.x - x) + self.warn.winfo_x()
        new_y = (event.y - y) + self.warn.winfo_y()
        s = "276x120+" + str(new_x) + "+" + str(new_y)
        self.warn.geometry(s)

    def over_move(self, event):
        global x, y
        new_x = (event.x - x) + self.over.winfo_x()
        new_y = (event.y - y) + self.over.winfo_y()
        s = "214x110+" + str(new_x) + "+" + str(new_y)
        self.over.geometry(s)


if __name__ == '__main__':
    Hexo('E:\工具\Git\Hexo')
