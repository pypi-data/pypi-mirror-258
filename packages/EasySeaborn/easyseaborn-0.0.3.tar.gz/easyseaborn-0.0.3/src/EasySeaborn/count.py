import matplotlib.pyplot as plt
from matplotlib import font_manager
from pathlib import Path
import seaborn as sns
import warnings
# 禁用警告
warnings.filterwarnings("ignore")

# 获取包所在的路径
current_PACKAGE_PATH = Path(__file__).resolve().parent


def count(
        df=None,
        xvarname=None,
        yvarname=None,
        groupby=None,
        xlabel=None,
        ylabel=None,
        title=None,
        xlabelsize=12,
        ylabelsize=12,
        titlesize=12,
        xticklabelsize=12,
        yticklabelsize=12,
        xticklabelrotation=0,
        yticklabelrotation=0,
        colormap=None,
        fig_length=6.4,
        fig_width=4.8,
        layout="tight",
        hue_order=None,
        order=None,
        fontfamily="华文楷体",
        isshowplot=1,
        savefilename=None,
        snsstyle="darkgrid",
        removeleftspine=0,
        removerightspine=1,
        removetopspine=1,
        removebottomspine=0,
        offset=None,
        trim=0,
        contextstyle="notebook",
        matplotlibstyle=None,
        countparamsdict={
            "orient": None,
            "color": None,
            "isfill": 1,
            "saturation": 0.75,
            "stat": "count",
            "width": 0.8,
            "dodge": "auto",
            "gap": 0,
            "islog": 0,
            "legend": "auto"},
        **kwargs):
    """
    这是一个Seaborn绘指字符变量计数柱状图函数的文档字符串。

    参数:
    df (pd.DataFrame object): dataframe。
    xvarname (str): X轴变量名。
    yvarname (str): Y轴变量名。
    groupby (str): 分组变量名。
    xlabel (str): X轴标签。
    ylabel (str): Y轴标签。
    title (str): 图形标题。
    xlabelsize (numeric): X轴标签字体大小。
    ylabelsize (numeric): Y轴标签字体大小。
    titlesize (numeric): 图形标题字体大小。
    xticklabelsize (numeric): X轴刻度标签字体大小。
    yticklabelsize (numeric): Y轴刻度标签字体大小。
    xticklabelrotation (numeric): X轴刻度标签旋转角度。
    yticklabelrotation (numeric): Y轴刻度标签旋转角度。
    colormap (str): 颜色映射名称。
    fig_length (numeric): 图形长度。
    fig_width (numeric): 图形宽度。
    layout (str ; None): 图形在画布上的布局机制{"constrained", "compressed", "tight", None}。
    hue_order (list or array-like): 分组变量的顺序。
    order (list or array-like): 图形主体的顺序。
    fontfamily (str): 支持的中英文字体名称{"方正舒体", "方正姚体", "仿宋", "黑体", "华文彩云", "华文仿宋", "华文琥珀", "华文楷体", "华文隶书", "华文宋体", "华文细黑", "华文新魏", "华文行楷", "华文中宋", "楷体", "隶书", "宋体", "微软雅黑", "新宋体", "幼圆", "TimesNewRoman", "Arial"}。
    isshowplot (binary): 是否显示图形{1,0}。
    savefilename (str): 保存的图形文件名（带后缀）{".pdf", ".png", ".jpg"}。
    snsstyle (str): seaborn绘图风格样式{"darkgrid", "whitegrid", "dark", "white", "ticks"}。
    isremoveleftspine (binary): 是否移除左轴线{1,0}。
    isremoverightspine (binary): 是否移除右轴线{1,0}。
    isremovetopspine (binary): 是否移除上轴线{1,0}。
    isremovebottomspine (binary): 是否移除下轴线{1,0}。
    offset (numeric): 轴线距离图形的距离。
    trim (binary): 是否设置R风格轴线{1,0}。
    contextstyle (str): 图形元素大小风格调整{"paper", "notebook", "talk", "poster"}。
    matplotlibstyle (str): matplotlib支持的绘图风格{"Solarize_Light2", "_classic_test_patch", "_mpl-gallery", "_mpl-gallery-nogrid", "bmh", "classic", "dark_background", "fast", "fivethirtyeight", "ggplot", "grayscale", "seaborn-v0_8", "seaborn-v0_8-bright", "seaborn-v0_8-colorblind", "seaborn-v0_8-dark", "seaborn-v0_8-dark-palette", "seaborn-v0_8-darkgrid", "seaborn-v0_8-deep", "seaborn-v0_8-muted", "seaborn-v0_8-notebook", "seaborn-v0_8-paper", "seaborn-v0_8-pastel", "seaborn-v0_8-poster", "seaborn-v0_8-talk", "seaborn-v0_8-ticks", "seaborn-v0_8-white", "seaborn-v0_8-whitegrid", "tableau-colorblind10"}。
    countparamsdict (dict): 控制分类变量计数柱状图的参数。
    {
        orient (str): 柱状图的方向{"v", "h"}。
        color (colorname str ; tuple of RGB(A) with value range between 0 and 1 ; hex color str): 柱子的颜色。Matplotlib支持的颜色名称字符串；缩放到01范围内的RGB(A)三元组；十六进制颜色字符串。
        isfill (binary): 是否填充颜色{1,0}。
        saturation (float): 颜色透明度。
        stat (str): 柱子的含义{"count", "percent", "proportion", "probability"}。
        width (numeric): 柱子的宽度。
        dodge (str or binary): 是否设置分组柱状图的排列方式为并排排列{"auto", 1, 0}。
        gap (numeric): 分组柱状图的排列方式为并排排列时柱子之间的间隔。
        islog (binary or positive numeric): 是否对数化(以10为底)后再绘制箱线图{1,0}或者是对数的底数。
        legend (str): 指定图例的样式{"auto", "brief", "full", False}。
    }

    返回值：
    Axes对象或者是Axes构成的二维数组

    示例：
    ===============================================================================0
    导入模块
    >>> import sys
    >>> sys.path.append(r"D:\document\statistics\TidyStatsProject")
    >>> from EasySeaborn import count
    >>> import matplotlib.pyplot as plt
    >>> from SoEasyData import GetSeabornData
    >>> import numpy as np
    >>> titanic = GetSeabornData("titanic")
    >>> print(titanic)
    ===============================================================================1
    测试df参数(绘制整个dataframe中字符变量的计数柱状图)
    >>> ax = count(titanic, savefilename="./image/count1.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================2
    测试xvarname(竖直分类变量柱状图)
    >>> ax = count(titanic, xvarname="class", savefilename="./image/count2.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================3
    测试yvarname参数(水平分类变量柱状图)
    >>> ax = count(titanic, xvarname="class", savefilename="./image/count3.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================4
    测试groupby参数(分组分类变量柱状图)
    >>> ax = count(titanic, xvarname="class", groupby="survived", savefilename="./image/count4.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================5
    测试一般标签参数
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="x", ylabel="y", title="count", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, savefilename="./image/count5.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================6
    测试colormap参数(绘图颜色)
    >>> ax = count(titanic, xvarname="class", groupby="survived", colormap="Accent", savefilename="./image/count6.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================7
    测试fig_length和fig_width参数(图形大小)
    >>> ax = count(titanic, xvarname="class", groupby="survived", fig_length=6, fig_width=6, savefilename="./image/count7.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================8
    测试layout参数(图形布局方式)
    >>> ax = count(titanic, xvarname="class", groupby="survived", layout="tight", savefilename="./image/count8.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", layout="compressed", savefilename="./image/count9.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", layout="constrained", savefilename="./image/count10.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", layout=None, savefilename="./image/count11.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================9
    测试hue_order参数(分组排列顺序)
    >>> ax = count(titanic, xvarname="class", groupby="survived", hue_order=[1, 0], savefilename="./image/count12.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================10
    测试order参数(柱子排列顺序)
    >>> ax = count(titanic, xvarname="class", groupby="survived", order=["First", "Third", "Second"], savefilename="./image/count13.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================11
    测试fontfamily参数(字体)
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="方正舒体", savefilename="./image/count14.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="方正姚体", savefilename="./image/count15.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="仿宋", savefilename="./image/count16.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="黑体", savefilename="./image/count17.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文彩云", savefilename="./image/count18.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文仿宋", savefilename="./image/count19.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文琥珀", savefilename="./image/count20.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文楷体", savefilename="./image/count21.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文隶书", savefilename="./image/count22.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文宋体", savefilename="./image/count23.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文细黑", savefilename="./image/count24.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文新魏", savefilename="./image/count25.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文行楷", savefilename="./image/count26.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="华文中宋", savefilename="./image/count27.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="楷体", savefilename="./image/count28.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="隶书", savefilename="./image/count29.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="宋体", savefilename="./image/count30.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="新宋体", savefilename="./image/count31.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="X轴", ylabel="Y轴", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="幼圆", savefilename="./image/count32.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="class", ylabel="y轴", title="count Plot", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="TimesNewRoman", savefilename="./image/count33.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", xlabel="class", ylabel="y轴", title="count Plot", xlabelsize=10, ylabelsize=16, titlesize=14, xticklabelsize=9, yticklabelsize=15, xticklabelrotation=30, yticklabelrotation=45, fontfamily="Arial", savefilename="./image/count34.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================12
    测试isshowplot参数(是否显示图形)
    >>> ax = count(titanic, xvarname="class", groupby="survived", isshowplot=0, savefilename="./image/count35.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", isshowplot=1, savefilename="./image/count36.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================13
    测试snsstyle参数(使用seaborn的风格)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="darkgrid", savefilename="./image/count37.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="whitegrid", savefilename="./image/count38.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="dark", savefilename="./image/count39.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="white", savefilename="./image/count40.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", savefilename="./image/count41.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================14
    测试isremoveleftspine参数(移除左轴线，snsstyle为ticks或者white时才有用)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="white", removeleftspine=1, savefilename="./image/count42.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", removeleftspine=0, savefilename="./image/count43.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================15
    测试isremoverightspine参数(移除右轴线，snsstyle为ticks或者white时才有用)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="white", removerightspine=1, savefilename="./image/count44.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", removerightspine=0, savefilename="./image/count45.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================16
    测试isremovetopspine参数(移除上轴线，snsstyle为ticks或者white时才有用)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="white", removetopspine=1, savefilename="./image/count46.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", removetopspine=0, savefilename="./image/count47.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================17
    测试isremovebottomspine参数(移除下轴线，snsstyle为ticks或者white时才有用)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="white", removebottomspine=1, savefilename="./image/count48.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", removebottomspine=0, savefilename="./image/count49.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================18
    测试offset参数(图形与轴线距离)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", offset=3, savefilename="./image/count50.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", offset=3, savefilename="./image/count51.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================19
    测试trim参数(设置R风格轴线)
    >>> ax = count(titanic, xvarname="class", groupby="sex", snsstyle="ticks", trim=1, savefilename="./image/count52.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", trim=1, savefilename="./image/count53.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================20
    测试contextstyle参数(绘图风格)
    >>> ax = count(titanic, xvarname="class", groupby="sex", contextstyle="notebook", savefilename="./image/count54.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", contextstyle="paper", savefilename="./image/count55.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", contextstyle="talk", savefilename="./image/count56.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", contextstyle="poster", savefilename="./image/count57.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================21
    测试matplotlibstyle参数(matplotlib支持的绘图风格)
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="Solarize_Light2", savefilename="./image/count58.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="_classic_test_patch", savefilename="./image/count59.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="_mpl-gallery", savefilename="./image/count60.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="_mpl-gallery-nogrid", savefilename="./image/count61.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="bmh", savefilename="./image/count62.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="classic", savefilename="./image/count63.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="dark_background", savefilename="./image/count64.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="fast", savefilename="./image/count65.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="fivethirtyeight", savefilename="./image/count66.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="ggplot", savefilename="./image/count67.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="grayscale", savefilename="./image/count68.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8", savefilename="./image/count69.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-bright", savefilename="./image/count70.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-colorblind", savefilename="./image/count71.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-dark", savefilename="./image/count72.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-dark-palette", savefilename="./image/count73.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-darkgrid", savefilename="./image/count74.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-deep", savefilename="./image/count75.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-muted", savefilename="./image/count76.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-notebook", savefilename="./image/count77.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-paper", savefilename="./image/count78.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-pastel", savefilename="./image/count79.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-poster", savefilename="./image/count80.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-talk", savefilename="./image/count81.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-ticks", savefilename="./image/count82.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-white", savefilename="./image/count83.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="seaborn-v0_8-whitegrid", savefilename="./image/count84.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="sex", matplotlibstyle="tableau-colorblind10", savefilename="./image/count85.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================22
    测试countparamsdict参数中的stat参数(设置Y轴含义)
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"stat": "count"}, savefilename="./image/count86.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"stat": "percent"}, savefilename="./image/count87.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"stat": "proportion"}, savefilename="./image/count88.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"stat": "probability"}, savefilename="./image/count89.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================23
    测试countparamsdict参数中的color参数(改变柱子颜色)
    >>> ax = count(titanic, xvarname="class", countparamsdict={"color": "green"}, savefilename="./image/count90.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================24
    测试countparamsdict参数中的saturation参数(设置饱和度)
    >>> ax = count(titanic, xvarname="class", groupby="sex", countparamsdict={"color": "green", "saturation": 0.4}, savefilename="./image/count91.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================25
    测试countparamsdict参数中的isfill参数(不填充颜色)
    >>> ax = count(titanic, xvarname="class", countparamsdict={"isfill": 0}, savefilename="./image/count92.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================26
    测试countparamsdict参数中的width参数(柱子宽度)
    >>> ax = count(titanic, xvarname="class", countparamsdict={"width": 0.4}, savefilename="./image/count93.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================27
    测试countparamsdict参数中的dodge参数(分组排列方式)
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 0}, savefilename="./image/count94.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1}, savefilename="./image/count95.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": "auto"}, savefilename="./image/count96.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================28
    测试countparamsdict参数中的gap参数(并排排列柱子之间的距离)
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1, "gap": 0.5}, savefilename="./image/count97.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================29
    测试countparamsdict参数中的legend参数(图例设置样式)
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1, "legend": "auto"}, savefilename="./image/count98.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1, "legend": "brief"}, savefilename="./image/count99.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1, "legend": "full"}, savefilename="./image/count100.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    >>> ax = count(titanic, xvarname="class", groupby="survived", countparamsdict={"dodge": 1, "legend": False}, savefilename="./image/count101.png", block=False)
    >>> plt.pause(2)
    >>> plt.close()
    ===============================================================================30
    """
    # 字体对应
    fontfamily_dic = {
        "方正舒体": "FZSTK.TTF",
        "方正姚体": "FZYTK.TTF",
        "仿宋": "simfang.ttf",
        "黑体": "simhei.ttf",
        "华文彩云": "STCAIYUN.TTF",
        "华文仿宋": "STFANGSO.TTF",
        "华文琥珀": "STHUPO.TTF",
        "华文楷体": "STKAITI.TTF",
        "华文隶书": "STLITI.TTF",
        "华文宋体": "STSONG.TTF",
        "华文细黑": "STXIHEI.TTF",
        "华文新魏": "STXINWEI.TTF",
        "华文行楷": "STXINGKA.TTF",
        "华文中宋": "STZHONGS.TTF",
        "楷体": "simkai.ttf",
        "隶书": "SIMLI.TTF",
        "宋体": "simsun.ttc",
        "微软雅黑": "msyhl.ttc",
        "新宋体": "simsun.ttc",
        "幼圆": "SIMYOU.TTF",
        "TimesNewRoman": "times.ttf",
        "Arial": "arial.ttf"
    }
    # 设置字体路径
    fontpath = Path(
        current_PACKAGE_PATH, "fonts/{}".format(fontfamily_dic[fontfamily]))
    fontobj = font_manager.FontProperties(fname=fontpath)
    # 默认的字典
    countparamsdictdefault = {
        "orient": None,
        "color": None,
        "isfill": 1,
        "saturation": 0.75,
        "stat": "count",
        "width": 0.8,
        "dodge": "auto",
        "gap": 0,
        "islog": 0,
        "legend": "auto"}
    # 更新字典
    countparamsdictdefault.update(countparamsdict)
    if matplotlibstyle is None:
        with sns.axes_style(snsstyle):
            sns.set_context(contextstyle)
            # 开始绘图，画布参数
            fig, ax = plt.subplots(
                figsize=(fig_length, fig_width), layout=layout)
            # 核心变量参数，颜色参数，图形参数
            sns.countplot(data=df, x=xvarname, y=yvarname, hue=groupby, ax=ax, palette=colormap,
                            hue_order=hue_order, order=order, orient=countparamsdictdefault[
                                "orient"],
                            color=countparamsdictdefault["color"], fill=bool(
                                countparamsdictdefault["isfill"]),
                            saturation=countparamsdictdefault["saturation"],
                            stat=countparamsdictdefault["stat"],
                            width=countparamsdictdefault["width"],
                            dodge=countparamsdictdefault["dodge"] if countparamsdictdefault["dodge"] == "auto" else bool(
                                countparamsdictdefault["dodge"]),
                            gap=countparamsdictdefault["gap"],
                            log_scale=bool(countparamsdictdefault["islog"]) if countparamsdictdefault[
                                "islog"] == 0 or countparamsdictdefault["islog"] == 1 else countparamsdictdefault["islog"],
                            legend=countparamsdictdefault["legend"]
                            )
    else:
        with plt.style.context(matplotlibstyle):
            # 开始绘图，画布参数
            fig, ax = plt.subplots(
                figsize=(fig_length, fig_width), layout=layout)
            # 核心变量参数，颜色参数，图形参数
            sns.countplot(data=df, x=xvarname, y=yvarname, hue=groupby, ax=ax, palette=colormap,
                            hue_order=hue_order, order=order, orient=countparamsdictdefault[
                                "orient"],
                            color=countparamsdictdefault["color"], fill=bool(
                                countparamsdictdefault["isfill"]),
                            saturation=countparamsdictdefault["saturation"],
                            stat=countparamsdictdefault["stat"],
                            width=countparamsdictdefault["width"],
                            dodge=countparamsdictdefault["dodge"] if countparamsdictdefault["dodge"] == "auto" else bool(
                                countparamsdictdefault["dodge"]),
                            gap=countparamsdictdefault["gap"],
                            log_scale=bool(countparamsdictdefault["islog"]) if countparamsdictdefault[
                                "islog"] == 0 or countparamsdictdefault["islog"] == 1 else countparamsdictdefault["islog"],
                            legend=countparamsdictdefault["legend"]
                            )
    # 标题参数
    if xlabel is not None:
        ax.set_xlabel(xlabel, fontproperties=fontobj,
                        fontsize=xlabelsize)
    if ylabel is not None:
        ax.set_ylabel(ylabel, fontproperties=fontobj,
                        fontsize=ylabelsize)
    if title is not None:
        ax.set_title(title, fontproperties=fontobj, fontsize=titlesize)
    # 刻度参数，刻度标签参数
    ax.tick_params('x', labelsize=xticklabelsize,
                    rotation=xticklabelrotation)
    ax.tick_params('y', labelsize=yticklabelsize,
                    rotation=yticklabelrotation)
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(),
                    fontproperties=fontobj)
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                    fontproperties=fontobj)
    # 移除spines
    sns.despine(
        left=removeleftspine,
        right=removerightspine,
        top=removetopspine,
        bottom=removebottomspine,
        offset=offset,
        trim=trim)
    if savefilename is not None:
        fig.savefig(savefilename)
    else:
        pass
    if bool(isshowplot):
        plt.show(**kwargs)
    else:
        pass
    return ax
    