import math

from PIL import Image
from matplotlib import pyplot as plt, cm
from matplotlib.colors import ListedColormap
from matplotlib.patches import FancyArrowPatch
from mplsoccer import Pitch, VerticalPitch
import numpy as np
import matplotlib as mpl
import settings
from visuals.match_visuals import PitchDefaultMap


class TwelvePitchVisual:

    def __init__(self, title, subtitle):
        self.arrow_width = 3
        self.arrow_headwidth = 4
        self.arrow_headlength = 4
        self.arrow_headaxislength = 2.5

        self.bg_color = '#59B877'
        self.line_color = 'w'
        self.title = title
        self.subtitle = subtitle
        self.axes_loc_logo = [0.78, 0.905, 0.18, 0.1]
        self.logo_name_url = 'twelve_logo_dark.png'
        self.cmap = 'Greens'
        self.info_text = None

    def crete_logo(self, fig):

        # Twelve Logo
        ax2 = fig.add_axes(self.axes_loc_logo)  # badge
        ax2.axis("off")
        img = Image.open(f'{settings.ROOT_DIR}/data/img/{self.logo_name_url}')
        ax2.imshow(img)

        return ax2

    def crete_info_text_center(self, fig, axes_loc=[0, 0.05, 1, 0.05]):

        # Twelve Info page
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")
        ax2.text(0.5, 0, self.info_text, color=self.bg_color, alpha=0.8, fontsize=10, va='center',ha='center')

        return ax2

    def create_shot_visual(self,start_x, start_y, values, outcomes, pitch_type='opta'):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 7))

        # Transparent color
        fig.set_facecolor(self.bg_color + "1a")
        ax.set_facecolor(self.bg_color + "03")  # 03

        # Shot viz
        pitch = VerticalPitch(pitch_type=pitch_type, goal_type='box',

                              half=True,
                              pitch_color=self.bg_color + "01", pad_bottom=0,
                              pad_top=20,
                              line_zorder=2,
                              linewidth=1.5,
                              line_color='black',
                              spot_scale=0.0
                              )

        pitch.draw(ax)
        # For xG sizes
        xg_size = 3.5
        for x,y,xg, outcome in zip(start_x, start_y, values, outcomes) :
            ms = math.sqrt(xg * xg_size) + 3
            alpha = 1
            if outcome == 'blocked':
                alpha = 0.6
            elif outcome == 'miss':
                alpha = 0.4
            elif outcome=='saved' or outcome == 'post':
                alpha = 0.8

            ax.plot([y], [x], 'o',
                    markersize=ms, color=self.bg_color,
                    alpha=alpha,
                    markeredgecolor=self.bg_color, zorder=5)
            if outcome == 'goal':
                ax.plot([y], [x], '*',
                        markersize=ms, color='w',
                        alpha=1,
                        markeredgecolor=self.bg_color, zorder=5)

        txt = ax.text(x=50, y=116, s=self.subtitle,
                      color=self.bg_color,
                      fontproperties=PitchDefaultMap.TEXT_FONT.get_font_sub_title(),
                      va='center',
                      ha='center')

        #  Title
        txt = ax.text(x=50, y=112, s=self.title,
                      color=self.bg_color,
                      fontproperties=PitchDefaultMap.TEXT_FONT.get_font_title(),
                      va='center',
                      ha='center')
        legend_x = 52
        # Legend
        ax.text(100-3, legend_x, "Missed/blocked", fontsize=8, va='center', ha='left')
        ax.plot([100-1.5], [legend_x],
                marker='o',  # if points[5]>0 else None,
                markersize=8, color=self.bg_color, alpha=0.5,
                markeredgecolor=self.bg_color,
                zorder=7)

        ax.text(100-22.5, legend_x, "On target/post", fontsize=8, va='center', ha='left')
        ax.plot([100-21], [legend_x],
                marker='o',  # if points[5]>0 else None,
                markersize=8, color=self.bg_color, alpha=0.75,
                markeredgecolor=self.bg_color,
                zorder=7)

        ax.text(100-41.5, legend_x, "Goal", fontsize=8, va='center', ha='left')
        ax.plot([100-40], [legend_x],
                marker='o',  # if points[5]>0 else None,
                markersize=8, color=self.bg_color, alpha=1,
                markeredgecolor=self.bg_color,
                zorder=7)

        ax.plot([100-40], [legend_x],
                marker='*',  # if points[5]>0 else None,
                markersize=8, color='w', alpha=1,
                markeredgecolor=self.bg_color,
                zorder=7)

        ax.text(100-75.5, legend_x, "Low xG", fontsize=8, va='center', ha='right', color="k")

        ax.plot([100-77], [legend_x],
                       marker='o',  # if points[5]>0 else None,
                       markersize=math.sqrt(5 * xg_size)+2, color=self.bg_color, alpha=0.55,
                       markeredgecolor=self.bg_color,
                       zorder=7)

        ax.plot([100-81], [legend_x],
                       marker='o',  # if points[5]>0 else None,
                       markersize=math.sqrt(15 * xg_size)+2, color=self.bg_color, alpha=0.55,
                       markeredgecolor=self.bg_color,
                       zorder=7)

        ax.plot([100-86], [legend_x],
                       marker='o',  # if points[5]>0 else None,
                       markersize=math.sqrt(30 * xg_size)+2, color=self.bg_color, alpha=0.55,
                       markeredgecolor=self.bg_color,
                       zorder=7)

        ax.text(100-88.5, legend_x, "High xG", fontsize=8, va='center', ha='left', color="k")


        # Twelve Logo
        self.crete_logo(fig)
        return fig, ax

    def create_pass_visual(self, start_x, start_y, end_x,end_y, values, pitch_type='opta'):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 7))
        fig.set_facecolor(self.bg_color)

        fig.set_facecolor(self.bg_color + "1a")
        ax.set_facecolor(self.bg_color + "03")  # 03

        # Pitch

        pitch = Pitch(pitch_type=pitch_type,
                      pitch_color=self.bg_color + "03",
                      pad_bottom=12,
                      # pad_top = 30,
                      line_color=self.line_color,
                      line_zorder=2)

        # # subt Title

        txt = ax.text(x=50, y=125.5, s=self.subtitle,
                      color=self.bg_color,
                      fontproperties=PitchDefaultMap.TEXT_FONT.get_font_sub_title(),
                      va='center',
                      ha='center')

        #  Title
        txt = ax.text(x=50, y=115.5, s=self.title,
                      color=self.bg_color,
                      fontproperties=PitchDefaultMap.TEXT_FONT.get_font_title(),
                      va='center',
                      ha='center')

        fig.subplots_adjust(left=0.06, right=0.94, top=0.79)
        pitch.draw(ax)

        norm = cm.colors.Normalize(vmin=0.0, vmax=0.3)
        custom_cmap = ListedColormap(cm.get_cmap(self.cmap)(np.linspace(0.25, 1, 10)))
        cmap = mpl.colors.ListedColormap([custom_cmap(x/100) for x in range(50, 100, 1)])

        m = cm.ScalarMappable(norm=norm, cmap=cmap)

        # Arrows
        pitch.arrows(start_x, start_y,
                        end_x,end_y,
                     values,
                     zorder=3,
                     width=self.arrow_width,
                     headwidth=self.arrow_headwidth,
                     headlength=self.arrow_headlength ,
                     headaxislength=self.arrow_headaxislength,
                     # color=[m.get_cmap()(norm(x / 100)) for x in self.values],
                     # settings['pass']["arrow"]["color"], "get_cmap('Greens')
                     alpha=0.9,
                     cmap=m.get_cmap(),
                     # norm=norm,
                     edgecolor='black',
                     ax=ax)

        # Twelve Logo
        self.crete_logo(fig)

        if self.info_text is not None:
            self.crete_info_text_center(fig)

        ax.text(50, -6, 'Attacking',  ha='center',va='center', color=self.bg_color, fontsize=10, zorder=20)
        arrow1 = FancyArrowPatch((40, -10), (60, -10),
                                          mutation_scale=10,
                                          color=self.bg_color,
                                          alpha=0.5, zorder=10,
                                          )

        ax.add_patch(arrow1)

        return fig, ax

