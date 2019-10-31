import os
import numpy as np


import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
from matplotlib.font_manager import FontProperties



#****************************************


#****************************************


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

    # 塗りつぶし 
        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

    # 枠線の描画
        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)
                
    # 各項目のラベル設定
        def set_varlabels(self, labels, font):
            self.set_thetagrids(np.degrees(theta), labels, fontproperties=font, fontsize=18)

    # 中間線を円から直線にする
        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)

    # 最外線を円から直線にする
        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)

                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def make_big_five_graph(param_dic_list: list, filepath: str):

    # 日本語フォントの利用
    if os.name == 'nt':
        font_path = r'c:\Windows\Fonts\meiryo.ttc'
    else:
        font_path = 'fonts/ipam.ttf'

    font = FontProperties(fname=font_path)

    # ラベルとデータ
    labels = ['知的好奇心', '誠実性', '外向性', '協調性', '感情の起伏']
    title = 'Big5 診断結果'
    params = []
    for param_dic in param_dic_list:
        params.append([param_dic['ope'], param_dic['con'], param_dic['ext'], param_dic['agr'], param_dic['emo']])
    print(params)

    # データの色
    colors = ['#7fffd4', '#4F81BD', '#000000', '#ffffff']

    theta = radar_factory(len(labels), frame='polygon')  # polygon：多角形、circle：円

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    # メモリ線を引く
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8])

    # タイトルのセット 「Big5診断結果」
    ax.set_title(title, position=(0.5, 1.1), ha='center', fontproperties=font, fontsize='25')

    # レーダーチャートの色、透明度を設定
    i = 0
    for d in params:
        line = ax.plot(theta, d, color=colors[i])  # 枠線の描画
        ax.fill(theta, d, alpha=0.25, color=colors[i])  # 塗りつぶし
        i = i + 1

    # 角のラベルを設定
    ax.set_varlabels(labels, font)

    # ラベルの表示非表示
    plt.tick_params(labelbottom=True,  # 角ラベル表示
                    labelleft=False)  # メモリラベル非表示

    # 説明の描画
    # legend_info = ('自分', '平均')
    # plt.legend(legend_info, loc=(0.7, .95), labelspacing=0.1, fontsize='medium', prop=font)

    # 図全体の背景透明度
    fig.patch.set_alpha(0.3)
    fig.patch.set_facecolor('blue')
    # subplotの背景色
    ax.patch.set_alpha(0.008)
    ax.patch.set_facecolor('blue')

    # plt.show()  # ウィンドウで確認
    fig.savefig(filepath)  # ファイルに保存


if __name__ == '__main__':
    Ope1 = 0.9970814244982862
    Con1 = 0.986401677449357
    Ext1 = 0.08530058556548387
    Agr1 = 0.18753528603194114
    Emo1 = 0.3898815263207158

    Ope2 = 0.9970814244982862
    Con2 = 0.986401677449357
    Ext2 = 0.08530058556548387
    Agr2 = 0.18753528603194114
    Emo2 = 0.3898815263207158

    # params = [[Ope1, Con1, Ext1, Agr1, Emo1]]
    filepath = "images/sample.png"

    # make_big_five_graph(params, filepath)
