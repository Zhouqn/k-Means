import typing
from tkinter import filedialog, IntVar, StringVar
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import pandas as pd
import kMeans
import pre_data

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
pd.set_option('display.max_rows', None)

window = ttk.Window()
window.title("基于K-Means++的股票预测系统")
window.geometry(f"{int(window.winfo_screenwidth() / 2)}x{int(window.winfo_screenheight() / 2)}")

# info colored notebook style - inactive tab color
nb = ttk.Notebook(window, bootstyle=SECONDARY)
nb.pack(fill=BOTH, expand=True)

f1 = ttk.Frame(window)
nb.add(f1, text="获取股票数据")

f2 = ttk.Frame(window)
nb.add(f2, text="计算kdj及聚类")
file_select_line = ttk.Frame(f2)
file_select_line.grid(row=0, column=0, sticky=W, padx=10)

lbl = ttk.Label(file_select_line, text="股票代码文件:")
lbl.grid(row=0, column=0, pady=10, sticky=W)
txt_code = ttk.Entry(file_select_line, width=50)
txt_code.grid(row=0, column=1, pady=10)
ttk.Button(file_select_line, text="点击选择", command=lambda: select_file(txt_code)).grid(row=0, column=2, padx=10,
                                                                                          pady=10)

lbl = ttk.Label(file_select_line, text="历史数据文件:")
lbl.grid(row=1, column=0, padx=1, pady=10)
txt_his = ttk.Entry(file_select_line, width=50)
txt_his.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(file_select_line, text="点击选择", command=lambda: select_file(txt_his)).grid(row=1, column=2, padx=10,
                                                                                         pady=10)


def run():
    stock_data_file = txt_code.get()
    daily_data_file = txt_his.get()
    kdj_centroids_data = kMeans.clustering(stock_data_file, daily_data_file)
    info.delete(1.0, END)
    info.insert(END, f"执行完成，数据已写入至kdj_centroids_data.csv\n{kdj_centroids_data}")


ttk.Button(file_select_line, text="开始执行", bootstyle=DANGER, command=run).grid(row=1, column=3, padx=10, pady=10)

window.update()

lf = ttk.Labelframe(f2, bootstyle=PRIMARY, text="数据预览")
lf.grid(sticky=NSEW, padx=10, pady=10)
info = ttk.Text(lf, height=20, bd=-1)
info.grid(row=0, column=0, sticky=NSEW)

# 第三个tab
f3 = ttk.Frame(window)
nb.add(f3, text="准确率分析", sticky=NW)
ttk.Label(f3, text="kdj聚类结果:").grid(row=0, column=0, pady=10, sticky=NW)
kdj_result = ttk.Entry(f3, width=55)
kdj_result.grid(row=0, column=1, pady=10)

zd = [-1, -1]
kdj_centroids_data: pd.DataFrame


def cluster_list():
    global kdj_centroids_data
    file = filedialog.askopenfile(filetypes=(("Text file", "csv"),))
    kdj_centroids_data, j_dict = pre_data.kdj_centroids(file.name)
    cluster_chk_btn: typing.Dict[int, typing.Tuple[IntVar, IntVar]] = {}

    def command(_cluster, btn):
        zv, dv = cluster_chk_btn[_cluster]
        if btn == "涨":
            if zv.get() == 1:
                for c, (zv, _) in cluster_chk_btn.items():
                    if c != _cluster:
                        zv.set(0)
                zd[0] = _cluster
            else:
                zd[0] = -1
        elif btn == "跌":
            if dv.get() == 1:
                for c, (_, dv) in cluster_chk_btn.items():
                    if c != _cluster:
                        dv.set(0)
                zd[1] = _cluster
            else:
                zd[1] = -1
        print("zd =", zd)

    row = 1
    for cluster, j_list in j_dict.items():
        ttk.Label(f3, text=f"簇{cluster}：").grid(row=row, column=0, padx=5, pady=10)
        j = ttk.Entry(f3, width=55)
        j.grid(row=row, column=1, padx=5, pady=10)
        j.insert(0, f"{j_list}")
        zint = IntVar()
        dint = IntVar()

        def f(_c):
            z = ttk.Checkbutton(
                f3, text="涨", variable=zint,
                command=lambda: command(_c, "涨"), bootstyle=DANGER
            )
            z.grid(row=row, column=2, padx=5, pady=10)
            d = ttk.Checkbutton(
                f3, text="跌", variable=dint,
                command=lambda: command(_c, "跌"), bootstyle=SUCCESS
            )
            d.grid(row=row, column=3, padx=5, pady=10)

        f(cluster)
        cluster_chk_btn[cluster] = (zint, dint)
        row += 1
    run_pre_btn()


ttk.Button(f3, text="点击选择", command=cluster_list).grid(row=0, column=2, padx=10, pady=10)


def run_pre_btn():
    scale_frame = ttk.Frame(f3)
    scale_frame.grid(row=4, column=1, sticky=W, pady=10)
    pre_day_num = IntVar()
    pre_day_num.set(3)
    pre_day_text = StringVar()
    pre_day_text.set("请选择要计算的天数：")
    ttk.Label(scale_frame, textvariable=pre_day_text).grid(row=0, column=0)
    ttk.Scale(
        scale_frame, variable=pre_day_num, from_=1, to=10, length=300,
        command=lambda x: pre_day_text.set(f"请选择要计算的天数({pre_day_num.get()})：")
    ).grid(row=0, column=1)

    str_var = StringVar()
    str_var.set("准确率: 待计算")

    ttk.Label(f3, textvariable=str_var).grid(row=5, column=1, sticky=W, pady=10)

    def run_pre():
        n = pre_data.run_pre(kdj_centroids_data, zd[0], zd[1], pre_day_num.get())
        str_var.set(f"准确率：{n}")

    ttk.Button(
        f3, text="点击计算", command=lambda: run_pre()
    ).grid(row=5, column=2, padx=10, sticky=W, pady=10)


def select_file(txt: ttk.Entry):
    files = filedialog.askopenfiles(filetypes=(("Text file", "csv"),))
    txt.delete(0, END)
    txt.insert(0, ",".join([file.name for file in files]))
    csvs = pd.concat([pd.read_csv(file.name) for file in files])
    csvs = csvs.iloc[:, :3]
    info.delete(1.0, END)
    info.insert(END, f"{csvs}")


if __name__ == '__main__':
    window.mainloop()
