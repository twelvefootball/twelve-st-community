import math

from PIL import ImageColor, Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, cm
from mplsoccer import VerticalPitch, Pitch

import settings

import pandas as pd

from helpers.font_helper import FontHelper
from helpers.helper import result_probabilities


def get_color_distance_fast(hex_1, hex_2):
    try:
        color_1 = ImageColor.getcolor(hex_1, "RGB")
        color_2 = ImageColor.getcolor(hex_2, "RGB")

        dist  = abs(color_1[0] - color_2[0])
        dist += abs(color_1[1] - color_2[1])
        dist += abs(color_1[2] - color_2[2])
        return dist
    except Exception as err:
        print(err)
        return 1000


class DefaultVisual:

    FIG_SIZE = (7, 7)
    # FIG_SIZE = (7.5, 3.2)

    def __init__(self, bg_color='#20CF7B'):
        if bg_color is None:
            bg_color = '#20CF7B'
        self.bg_color = bg_color

    def create_initial_figure(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=DefaultVisual.FIG_SIZE)

        return fig, ax

    def set_bg_color(self,color):
        self.bg_color = color

    def create_match_initial_figure(self, ax=None):

        if ax is None:
            fig, axmain = plt.subplots(nrows=1, ncols=1, figsize=DefaultVisual.FIG_SIZE)
            axmain.axis('off')

            widths = [1]
            heights = [0.5, 0.5, 10, 1]

            specs = fig.add_gridspec(ncols=1, nrows=4, width_ratios=widths, height_ratios=heights)
            ax = fig.add_subplot(specs[2, 0])  # ax = fig.add_subplot(131, polar=True)

            bottom_axes_color = '#3572AF'
            bottom_axes_line_width = 4

            # COLORS
            fig.set_facecolor(self.bg_color)
            ax.patch.set_facecolor(self.bg_color)
            fig.patch.set_alpha(alpha=0.05)
            ax.patch.set_alpha(alpha=0.005)

            # AXIS
            spines = ["top", "right", "bottom", "left"]
            for s in spines:
                if s in ["top", "right", "left", "bottom"]:
                    ax.spines[s].set_visible(False)
                else:
                    ax.spines[s].set_color(bottom_axes_color)
                    ax.spines[s].set_linewidth(bottom_axes_line_width)
                    ax.spines[s].set_bounds((0, 100))

            return fig, ax, specs
        else:

            ax.axis('off')

            bottom_axes_color = '#3572AF'
            bottom_axes_line_width = 4

            # COLORS
            #fig.set_facecolor(self.bg_color)
            ax.patch.set_facecolor(self.bg_color)
            #fig.patch.set_alpha(alpha=0.05)
            ax.patch.set_alpha(alpha=0.005)

            # AXIS
            spines = ["top", "right", "bottom", "left"]
            for s in spines:
                if s in ["top", "right", "left", "bottom"]:
                    ax.spines[s].set_visible(False)
                else:
                    ax.spines[s].set_color(bottom_axes_color)
                    ax.spines[s].set_linewidth(bottom_axes_line_width)
                    ax.spines[s].set_bounds((0, 100))

            return None, ax, None

    def crete_logo(self):

        # Twelve Logo
        ax2 = self.fig.add_axes([0.75, 0.15, 0.12, 0.05])  # badge
        ax2.axis("off")
        img = Image.open(f'{settings.ROOT_DIR}/data/img/twelve_logo_white.png')
        ax2.imshow(img)


class DefaultMatchVisual:

    hr_lines_color = "grey"
    fig_background_color = '#20CF7B'
    plot_background_color = '#20CF7B'
    LABEL_SIZE = 12

    LINE_WIDTH = 1

    @staticmethod
    def create_horizontal_lines(ax, max_y, max_x,  include_negatives=False,num_lines=5, line_color='grey', alpha=0.3):
        # Create Vertical Colors
        hr_lines = np.linspace(0, max_y, num_lines)
        for i in hr_lines[1:num_lines-1]:
            ax.plot([0, max_x], [i, i], color=line_color, lw=1, ls='-', alpha=alpha)
            if include_negatives:
                ax.plot([0, max_x], [-i, -i], color=line_color, lw=1, ls='-', alpha=alpha)

        return hr_lines

    @staticmethod
    def create_x_axis_labels(ax, end_period, color_home, ticks_visible=False):
        # Bottom Line
        # Ticks
        x_ticks = [0, 45, 90]
        # if end_period == 1:
        #     x_ticks = [0, 15, 30, 45]
        if end_period > 2:
            x_ticks = [0, 45, 90, 120]

        x_ticks_labels = [f"{x}'" for x in x_ticks]

        plt.xticks(ticks=x_ticks, color=color_home)
        ax.tick_params(axis="x", color=color_home, length=5, width=0, labelcolor=color_home, labelsize= DefaultMatchVisual.LABEL_SIZE)

        ax.set_xticklabels(x_ticks_labels)

        if not ticks_visible:
            plt.yticks(ticks=[],color=DefaultMatchVisual.plot_background_color)  # Tick to not visible
            ax.tick_params(axis="y", length=0, labelcolor=DefaultMatchVisual.plot_background_color, labelsize=16, labelrotation=45)

    @staticmethod
    def create_labels(ax, home_team_abbr, home_team_y, color_home, away_team_abbr, away_team_y, color_away, end_min=95):

        # Label
        if abs(sum(home_team_y) - sum(away_team_y)) > 0.1:
            t_home = ax.annotate(home_team_abbr, (end_min+1.5, sum(home_team_y)), color=color_home,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='center', fontweight="bold", ha='left')  # fontfamily="Roboto",
            t_away = ax.annotate(away_team_abbr, (end_min+1.5, sum(away_team_y)), color=color_away,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='center', fontweight="bold", ha='left')  # fontfamily="Roboto",

        elif sum(home_team_y) > sum(away_team_y):
            t_home = ax.annotate(home_team_abbr, (end_min+1.5, sum(home_team_y)), color=color_home,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='bottom', fontweight="bold", ha='left')  # fontfamily="Roboto",
            t_away = ax.annotate(away_team_abbr, (end_min+1.5, sum(away_team_y)), color=color_away,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='top', fontweight="bold", ha='left')  # fontfamily="Roboto",
        else:
            t_home = ax.annotate(home_team_abbr, (end_min+1.5, sum(home_team_y)), color=color_home,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='top', fontweight="bold", ha='left')  # fontfamily="Roboto",
            t_away = ax.annotate(away_team_abbr, (end_min+1.5, sum(away_team_y)), color=color_away,
                                 fontsize=DefaultMatchVisual.LABEL_SIZE,
                                 va='bottom', fontweight="bold", ha='left')  # fontfamily="Roboto",

    @staticmethod
    def create_title(fig, title_text, sub_title_text, text_color, subtitle_y=0.88, title_y=0.82):

        fig.text(0.5, subtitle_y, sub_title_text.upper(), ha="center", color=text_color,fontproperties=FontHelper.get_font_sub_title())

        fig.text(0.5, title_y, title_text, ha="center", color=text_color, fontproperties=FontHelper.get_font_title())

    @staticmethod
    def create_title_split(fig, specs, title_text, sub_title_text_left, sub_title_text_right, text_color, secondary_color, subtitle_y=0.88, title_y=0.82):

        ax_t = fig.add_subplot(specs[0, 0])
        ax_t.axis('off')
        from highlight_text import ax_text, fig_text

        # add a fancy box
        # fancybox = mpatches.FancyBboxPatch((0.1, 0.5), 0.05, 0.5,  fc=text_color, ec="b", lw=0, boxstyle=mpatches.BoxStyle("Round", pad=0.02))

        bbox_props = dict(boxstyle="round, pad=0.25", fc=text_color, ec=text_color, lw=3)
        bbox_props2 = dict(boxstyle="round, pad=0.25", fc=secondary_color, ec=secondary_color, lw=3)

        ax_text(s= f"<{sub_title_text_left}>   -   <{sub_title_text_right}>", x=0.5, y=1 , va='bottom',ha='center', color=text_color,
                    fontproperties=FontHelper.get_font_sub_title(),
                    highlight_textprops = [{'color': 'w', 'weight': 'bold', 'bbox': {'facecolor': text_color, **bbox_props}},
                                           {'color': 'w', 'weight': 'bold','bbox': {'facecolor': secondary_color, **bbox_props2}}],

                ax = ax_t
                )


        # fig.text(0.48, subtitle_y, sub_title_text_left.upper(), ha="right", color='w', bbox=bbox_props,
        #          fontproperties=FontHelper.get_font_sub_title())
        #
        # fig.text(0.5, subtitle_y, "-", ha="center", color=text_color,
        #          fontproperties=FontHelper.get_font_sub_title())
        #
        #
        # fig.text(0.52, subtitle_y, sub_title_text_right.upper(), ha="left", color='w',  bbox=bbox_props2,
        #          fontproperties=FontHelper.get_font_sub_title())
        #
        fig.text(0.5, title_y, title_text, ha="center", color=text_color, fontproperties=FontHelper.get_font_title())

    @staticmethod
    def crete_logo(fig, dark_logo=False, axes_loc=[0.75, 0.01, 0.18, 0.1], logo_name_url = None):

        # Twelve Logo
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")
        if logo_name_url is None:
            if dark_logo:
                img = Image.open(f'{settings.ROOT_DIR}/data/img/twelve_logo_dark.png')
            else:
                img = Image.open(f'{settings.ROOT_DIR}/data/img/twelve_logo_white.png')
        else:
            img = Image.open(f'{settings.ROOT_DIR}/data/img/{logo_name_url}')
        ax2.imshow(img)

    @staticmethod
    def crete_logo_top(fig, dark_logo=False, axes_loc=[0.78, 0.905, 0.18, 0.1], logo_name_url=None):

        # Twelve Logo
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")
        if logo_name_url is None:
            if dark_logo:
                img = Image.open(f'{settings.ROOT_DIR}/data/img/twelve_logo_dark.png')
            else:
                img = Image.open(f'{settings.ROOT_DIR}/data/img/twelve_logo_white.png')
        else:
            img = Image.open(f'{settings.ROOT_DIR}/data/img/{logo_name_url}')
        ax2.imshow(img)


    @staticmethod
    def crete_logo_image(fig, path, axes_loc=[0.75, 0.01, 0.18, 0.1]):

        # Twelve Logo
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")

        img = Image.open(path)
        ax2.imshow(img)

    @staticmethod
    def crete_info_text(fig, text, color='white', alpha=0.8,axes_loc=[0.10, 0.12, 0.12, 0.05]):

        # Twelve Logo
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")
        ax2.text(0,0,text, color=color, alpha=alpha, fontsize=10)

    @staticmethod
    def crete_info_text_center(fig, text, color='white', alpha=0.8,axes_loc=[0, 0.05, 1, 0.05]):

        # Twelve Logo
        ax2 = fig.add_axes(axes_loc)  # badge
        ax2.axis("off")
        ax2.text(0.5, 0, text, ha='center', va='center', color=color, alpha=alpha, fontsize=10)

    @staticmethod
    def draw_bottom_axis(ax, color, end_min):
        # AXIS
        spines = ["top", "right", "bottom", "left"]
        for s in spines:
            if s in ["top", "right", "left"]:
                ax.spines[s].set_visible(False)
            else:
                ax.spines[s].set_color(color)
                ax.spines[s].set_linewidth(1)
                ax.spines[s].set_bounds((0, end_min))
                ax.spines[s].set_visible(False)

    @staticmethod
    def create_inital_figure(bg_color):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=DefaultVisual.FIG_SIZE)

        bottom_axes_color = '#3572AF'
        bottom_axes_line_width = 2

        # COLORS
        fig.set_facecolor(bg_color)
        # ax.patch.set_facecolor(self.bg_color)
        fig.patch.set_alpha(0.1)
        ax.patch.set_alpha(0.05)

        # AXIS
        spines = ["top", "right", "bottom", "left"]
        for s in spines:
            if s in ["top", "right", "left", "bottom"]:
                ax.spines[s].set_visible(False)
            else:
                ax.spines[s].set_color(bottom_axes_color)
                ax.spines[s].set_linewidth(bottom_axes_line_width)
                ax.spines[s].set_bounds((0, 100))

        return fig, ax


class XGMatchShots:
    plt.switch_backend('agg')
    MARKER_SIZE = 12

    def __init__(self, viz_name, home_team_abbr, away_team_abbr, home_team_score, away_team_score, bg_color='#20CF7B'):

        super().__init__()
        self.viz_name = viz_name

        self.home_team_abbr = home_team_abbr
        self.away_team_abbr = away_team_abbr
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

        self.default_viz = DefaultVisual(bg_color)

        self.color_home = '#20CF7B'
        self.color_away = '#FF4B4B'

        self.end_period = 2
        self.end_min = 95

        self.sub_title_text = ""#Height is xG & strength and color is outcome"
        self.title_text = "Shots with xG by minute"
        self.match_stories = None

    def set_team_colors(self, home_team_home_color=None, home_team_away_color=None,
                        away_team_home_color=None, away_team_away_color=None):

        self.color_home = self.color_home if home_team_home_color is None else home_team_home_color
        self.color_away = self.color_away if away_team_home_color is None else away_team_home_color

        # Check Colors
        home_color_rgb = get_color_distance_fast(self.color_home, self.color_away)
        if home_color_rgb < 200:
            self.color_away = away_team_away_color

    def set_data(self, twelve_match_stories, home_team_shots, away_team_shots):
        self.match_stories = twelve_match_stories
        self.home_team_shots = home_team_shots
        self.away_team_shots = away_team_shots

        xG_shots_home = [x['xg'] for x in home_team_shots]
        xG_shots_away = [x['xg'] for x in away_team_shots]

        self.sub_title_text_left = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f})"
        self.sub_title_text_right = f"{self.away_team_abbr} ({sum(xG_shots_away):0.2f})"
        self.sub_title_text = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f}) - ({sum(xG_shots_away):0.2f}) {self.away_team_abbr}"

    def create_visual(self, persist=False):

        home_team_id = self.match_stories['homeTeam']['teamId']
        away_team_id = self.match_stories['awayTeam']['teamId']

        match_stories = [x for x in self.match_stories['stories'] if x['type_id'] in [13, 14, 15, 16]]
        match_details_home = [x for x in match_stories if len(x['players']) == 1 and x['players'][0]['teamId'] == home_team_id]
        match_details_away = [x for x in match_stories if len(x['players']) == 1 and x['players'][0]['teamId'] == away_team_id]

        def get_transparency(type, txt):

            if type == 13:
                return 0.4
            if type == 14:
                return 0.8
            if type == 15 and 'blocked' in txt:
                return 0.6
            return 0.8

        shots_home = [(x['minute'], x['xg'] + 0.01, get_transparency(x['type'], x['typeName'])) for x in self.home_team_shots if x['type'] in [13, 14, 15]]
        shots_away = [(x['minute'], x['xg'] + 0.01, get_transparency(x['type'], x['typeName'])) for x in self.away_team_shots if x['type'] in [13, 14, 15]]

        goals_home = {x['minute']: x['xg'] + 0.01 for x in self.home_team_shots if x['typeName'] == 'goal'}
        goals_home_own = {x['minute']: 0.05 for x in match_details_away if x['description'] == 'OWN GOAL!'}
        if len(goals_home_own) > 0:
            goals_home = {**goals_home, **goals_home_own}

        goals_away = {x['minute']: x['xg'] + 0.01 for x in self.away_team_shots if x['typeName'] == 'goal'}
        goals_away_own = {x['minute']: 0.05 for x in match_details_home if x['description'] == 'OWN GOAL!'}
        if len(goals_away_own) > 0:
            goals_away = {**goals_away, **goals_away_own}

        # DATA
        end_min = self.match_stories['stories'][-1]['minute']
        if end_min < 90:
            end_min =90

        end_period = self.match_stories['stories'][-1]['period']
        if end_period>2:
            end_min = 120

        home_shots_max = 0
        if len(self.home_team_shots) > 0:
            home_shots_max = max([x['xg'] for x in self.home_team_shots])
        away_shots_max = 0
        if len(self.away_team_shots) > 0:
            away_shots_max = max([x['xg'] for x in self.away_team_shots])

        ymax = max([home_shots_max,away_shots_max, 0.3]) + 0.15

        # Initial Figure
        fig, ax ,specs= self.default_viz.create_match_initial_figure()

        plt.hlines(0, 0, end_min, linestyles='--', color=self.color_home, lw=1, zorder=5)

        # Create Horizontal Lines
        hr_lines = DefaultMatchVisual.create_horizontal_lines(ax, ymax, end_min,True,line_color=self.color_home)

        # Title
        # DefaultMatchVisual.create_title(fig, self.title_text, self.sub_title_text, self.color_home)

        # Shots

        shots_home.sort(key=lambda x: x[2],reverse=True)
        for minute, xg, alpha in shots_home:

            ax.plot([minute, minute], [0, xg], '-', color=self.color_home, linewidth=2, alpha=alpha)

            # ax.plot([minute], [xg], 'o', markersize=XGMatchShots.MARKER_SIZE+2, color=self.color_home, alpha=1, markeredgecolor=self.color_home, zorder=5)
            ax.plot([minute], [xg+0.018], 'o',  markersize=XGMatchShots.MARKER_SIZE, color=self.color_home, alpha=alpha, markeredgecolor=self.color_home, zorder=5) #fillstyle

        for minute, xg in goals_home.items():
            ax.plot([minute, minute], [0, xg], '-', color=self.color_home, linewidth=2)

            ax.plot([minute], [xg+0.018], 'o', markersize=XGMatchShots.MARKER_SIZE, color=self.color_home, alpha=1, markeredgecolor=self.color_home, zorder=4)
            ax.plot([minute], [xg+0.018], '*', markersize=XGMatchShots.MARKER_SIZE, color='w', alpha=1, markeredgecolor=self.color_home, zorder=5)

        shots_away.sort(key=lambda x: x[2], reverse=True)
        for minute, xg, alpha in shots_away:

            ax.plot([minute, minute], [0, -xg], '-', color=self.color_away, linewidth=2, alpha=alpha)
            # ax.plot([minute], [-xg], 'o', markersize=XGMatchShots.MARKER_SIZE + 2, color=self.color_away, alpha=1,markeredgecolor=self.color_away, zorder=5)
            ax.plot([minute], [-xg-0.018], 'o',  markersize=XGMatchShots.MARKER_SIZE, color=self.color_away, alpha=alpha, markeredgecolor=self.color_away, zorder=5)

        for minute, xg in goals_away.items():
            ax.plot([minute, minute], [0, -xg], '-', color=self.color_away, linewidth=2)

            ax.plot([minute], [-xg-0.018], 'o', markersize=XGMatchShots.MARKER_SIZE, color=self.color_away, alpha=1, markeredgecolor=self.color_away, zorder=4)
            ax.plot([minute], [-xg-0.018], '*', markersize=XGMatchShots.MARKER_SIZE, color='w', alpha=1, markeredgecolor=self.color_away, zorder=5)

        # # Axis Labels
        DefaultMatchVisual.create_x_axis_labels(ax, end_period, self.color_home)

        # Labels
        # t_home = ax.annotate(self.home_team_abbr, (end_min+1, hr_lines[1]/2), color=self.color_home,
        #                      fontsize=DefaultMatchVisual.LABEL_SIZE,
        #                      va='bottom', fontweight="bold", ha='left')  # fontfamily="Roboto",
        # t_away = ax.annotate(self.away_team_abbr, (end_min+1, -(hr_lines[1]/2)), color=self.color_away,
        #                      fontsize=DefaultMatchVisual.LABEL_SIZE,
        #                      va='top', fontweight="bold", ha='left')  # fontfamily="Roboto",

        plt.xlim([-1, end_min+1])
        plt.ylim([-ymax, ymax])

        DefaultMatchVisual.draw_bottom_axis(ax, self.color_home, end_min)

        # Twelve Logo
        DefaultMatchVisual.crete_logo(fig,dark_logo=True)

        DefaultMatchVisual.create_title_split(fig, specs, self.title_text, self.sub_title_text_left, self.sub_title_text_right, self.color_home,self.color_away)

        # Persist Img
        if persist:
            plt.savefig(f'../output/xg_shot_momentum_{self.viz_name}.jpg', dpi=200, facecolor=fig.get_facecolor(),
                        transparent=False, bbox_inches='tight', pad_inches=0.35)
        return fig, ax


class XGMatchTrend:

    XG_PADDING = 0.25
    MARKER_SIZE = 60

    def  __init__(self, viz_name, home_team_abbr, away_team_abbr, home_team_score, away_team_score,
                  bg_color='#20CF7B',

                  ):

        self.viz_name = viz_name

        self.home_team_abbr = home_team_abbr
        self.away_team_abbr = away_team_abbr
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

        self.color_home = '#20CF7B'
        self.color_away = '#FF4B4B'

        self.end_period = 2
        self.end_min = 95

        self.default_viz = DefaultVisual(bg_color)

        self.title_text = "xG for and against by minute"
        # self.line_color = line_color
        # self.title_text = ""

    def set_team_colors(self, home_team_home_color=None, home_team_away_color=None,
                        away_team_home_color=None, away_team_away_color=None):

        self.color_home = self.color_home if home_team_home_color is None else home_team_home_color
        self.color_away = self.color_away if away_team_home_color is None else away_team_home_color

        # Check Colors
        home_color_rgb = get_color_distance_fast(self.color_home, self.color_away)
        if home_color_rgb < 200:
            self.color_away = away_team_away_color

    def set_data(self, home_xg_shots, home_min_shots,
                 away_xg_shots, away_min_shots,
                 end_period=2, end_min=95):

        end_min_actual = end_min

        if end_period <= 2 and end_min > 95:
            end_min = 95

        elif end_period > 2:
            end_min = 120
        else:
            end_min = 90

        self.end_min = end_min
        self.end_period = end_period
        if end_period > 2:
            min_space = np.linspace(0, 120, num=20, endpoint=True)

        else:
            min_space = np.linspace(0, 90, num=15, endpoint=True)
            # min_space[0] = 10
            if max(end_min, 90) > 90:
                min_space = np.append(min_space, max(end_min, 90))


        min_space = sorted(min_space)

        df_home = pd.DataFrame()
        df_home['xg'] = home_xg_shots
        df_home['minute_ajd'] = [min_space[np.digitize(min(x, end_min), min_space, right=True)] for x in home_min_shots]
        df_home = df_home.groupby('minute_ajd').sum()['xg'].reset_index()

        df_away = pd.DataFrame()
        df_away['xg'] = away_xg_shots
        df_away['minute_ajd'] = [min_space[np.digitize(min(x, end_min), min_space, right=True)] for x in away_min_shots]
        df_away = df_away.groupby('minute_ajd').sum()['xg'].reset_index()

        xG_shots_home = [0] + [shot for shot in df_home['xg']]# + [0]
        xG_shots_away = [0] + [shot for shot in df_away['xg']] #+ [0]

        if end_min_actual >= 90:
            self.times_shots_home = np.array([0] + [x for x in df_home['minute_ajd']] + [end_min])
            self.times_shots_away = np.array([0] + [x for x in df_away['minute_ajd']] + [end_min])

            xG_shots_home += [0]
            xG_shots_away += [0]

        else:
            self.times_shots_home = np.array([0] + [x for x in df_home['minute_ajd']])  # + [end_min])
            self.times_shots_away = np.array([0] + [x for x in df_away['minute_ajd']])  # + [end_min])

        MAX_XG = max([sum(home_xg_shots), sum(away_xg_shots)]) + XGMatchTrend.XG_PADDING

        self.MAX_XG = MAX_XG
        self.xG_shots_home = xG_shots_home
        self.xG_shots_away = xG_shots_away

        self.sub_title_text = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f}) - ({sum(xG_shots_away):0.2f}) {self.away_team_abbr}"
        self.sub_title_text_left = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f})"
        self.sub_title_text_right = f"{self.away_team_abbr} ({sum(xG_shots_away):0.2f})"

    def create_visual(self, persist=False):
        # if self.df_passes is None:
        #     raise Exception('Passes not set')

        # Initial Figure
        fig, ax, specs = self.default_viz.create_match_initial_figure()

        # Create Horizontal Lines
        DefaultMatchVisual.create_horizontal_lines(ax, self.MAX_XG, self.end_min, line_color=self.color_home)

        # Create Data Lines

        # Outer Line
        plt.step(self.times_shots_home, np.cumsum(self.xG_shots_home), where='post', c=self.color_home, lw=2.0, zorder=2)
        plt.step(self.times_shots_away, np.cumsum(self.xG_shots_away), where='post', c=self.color_away, lw=2.0, zorder=2)

        # AWAY TEAM
        ax.scatter(self.times_shots_away[1:],
            np.cumsum(self.xG_shots_away)[1:],
            s=XGMatchTrend.MARKER_SIZE,
            color='white',
            edgecolors=self.color_away,
            linewidth=DefaultMatchVisual.LINE_WIDTH,
            zorder=3,
            marker="o",
            alpha=1,
        )

        ax.fill_between(self.times_shots_away,
                        np.cumsum(self.xG_shots_away),
                        linewidth=1,
                        color=self.color_away, zorder=2,
                        alpha=0.2, step='post'
                        )

        # Circles - HOME TEAM
        ax.scatter(self.times_shots_home[1:],
            np.cumsum(self.xG_shots_home)[1:],
            s=XGMatchTrend.MARKER_SIZE,
            color='white',
            edgecolors=self.color_home,
            linewidth=DefaultMatchVisual.LINE_WIDTH,
            zorder=3,
            marker="o",
            alpha=1
        )
        ax.fill_between(self.times_shots_home,
                        np.cumsum(self.xG_shots_home),
                        linewidth=1,
                        color=self.color_home,
                        alpha=0.2, step='post', zorder=2,
                        )

        # # Team Labels
        # DefaultMatchVisual.create_labels(ax,
        #                                  self.home_team_abbr, self.xG_shots_home,  self.color_home,
        #                                  self.away_team_abbr, self.xG_shots_away, self.color_away, self.end_min)

        # Axis Labels
        DefaultMatchVisual.create_x_axis_labels(ax,  self.end_period,self.color_home)

        # Title
        # DefaultMatchVisual.create_title(fig, self.title_text, self.sub_title_text, self.color_home)

        # Twelve Logo
        DefaultMatchVisual.crete_logo(fig, dark_logo=True)

        DefaultMatchVisual.create_title_split(fig, specs, self.title_text, self.sub_title_text_left, self.sub_title_text_right,
                                              self.color_home,self.color_away,)

        # Persist Img
        if persist:
            plt.savefig(f'../output/xg_match_{self.viz_name}.jpg', format='png', dpi=200, facecolor=fig.get_facecolor(), frameon=True, transparent=True, bbox_inches=None)
        ax.set_ylim(-0.03, self.MAX_XG)

        return fig, ax


class XGMatchProb:


    TEXT_FONT_SIZE = 12
    TEXT_FONT_SIZE_LARGE = 20

    def __init__(self, viz_name, home_team_abbr, away_team_abbr, home_team_score, away_team_score, bg_color='#20CF7B'):

        self.viz_name = viz_name
        self.default_viz = DefaultVisual(bg_color)
        self.match_stories = None

        self.color_home = '#20CF7B'
        self.color_away = '#FF4B4B'

        self.sub_title_text = ""
        self.title_text = "Result probability based on xG"
        self.home_team_abbr = home_team_abbr
        self.away_team_abbr = away_team_abbr
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score
        self.perc_home = 0
        self.perc_away = 0
        self.perc_draw = 0
        self.text_font = FontHelper.custom_font(XGMatchProb.TEXT_FONT_SIZE, 'bold', 'Montserrat')
        self.text_font_large = FontHelper.custom_font(XGMatchProb.TEXT_FONT_SIZE_LARGE, 'bold', 'Montserrat')

    def set_team_colors(self, home_team_home_color=None, home_team_away_color=None,
                        away_team_home_color=None, away_team_away_color=None):

        self.color_home = self.color_home if home_team_home_color is None else home_team_home_color
        self.color_away = self.color_away if away_team_home_color is None else away_team_home_color

        # Check Colors
        home_color_rgb = get_color_distance_fast(self.color_home, self.color_away)
        if home_color_rgb < 200:
            self.color_away = away_team_away_color

    def set_data(self, xg_home, xg_away):

        # Simulate results
        self.perc_home, self.perc_away, self.perc_draw = result_probabilities(xg_home,xg_away)

        self.sub_title_text = f"{self.home_team_abbr} ({sum(xg_home):0.2f}) {self.home_team_score}-{self.away_team_score} ({sum(xg_away):0.2f}) {self.away_team_abbr}"
        self.sub_title_text_left = f"{self.home_team_abbr} ({sum(xg_home):0.2f}) {self.home_team_score}"
        self.sub_title_text_right = f"{self.away_team_score} ({sum(xg_away):0.2f}) {self.away_team_abbr}"

    def create_visual(self,persist=False):
        if self.perc_home + self.perc_away + self.perc_draw == 0:
            raise Exception('Data not set')

        # Initial Figure
        fig, ax, specs = self.default_viz.create_match_initial_figure()

        # Sizes
        ax.set_ylim(0, 1)
        ax.set_xlim(0, 1)

        # COLORS PROBABILITY
        from matplotlib import cm
        m = cm.ScalarMappable(norm=plt.Normalize(0.1, 0.8), cmap="Blues")
        m_r = cm.ScalarMappable(norm=plt.Normalize(0.1, 0.8), cmap="Blues_r")

        # HOME
        ax.annotate(self.home_team_abbr, (0.19, 0.68), ha='center', color=self.color_home, fontproperties=self.text_font, fontweight="bold")
        rectangle = patches.Rectangle((0.06, 0.40), 0.25, 0.25, edgecolor=self.color_home, alpha=min([self.perc_home+10,100])/100,
                                      facecolor=self.color_home, linewidth=0)

        ax.add_patch(rectangle)
        ax.annotate(f"{self.perc_home:0.0f}%", (0.19, 0.50), ha='center', color='w' if self.perc_home>50 else 'k', alpha=1,#min([self.perc_home+10,100])/100,
                    fontproperties=self.text_font_large, fontweight="bold")

        # DRAW
        ax.annotate("DRAW", (0.47, 0.68), ha='center', color=self.color_home, fontproperties=self.text_font)
        ax.annotate(f"{self.perc_draw:0.0f}%", (0.485, 0.50), ha='center', color='w' if self.perc_draw>50 else 'k', fontproperties=self.text_font_large, alpha=1)
        rectangle1 = patches.Rectangle((0.355, 0.40), 0.25, 0.25, edgecolor=self.color_home, alpha=min([self.perc_draw+10, 100])/100,
                                      facecolor=self.color_home, linewidth=0)
        ax.add_patch(rectangle1)

        #AWAY
        ax.annotate(self.away_team_abbr, (0.77, 0.68), ha='center', color=self.color_home, fontproperties=self.text_font)
        ax.annotate(f"{self.perc_away:0.0f}%", (0.77, 0.50), ha='center',color='w' if self.perc_away>50 else 'k', alpha=1,#min([self.perc_away+10, 100])/100,
                    fontproperties=self.text_font_large)

        rectangle2 = patches.Rectangle((0.65, 0.40), 0.25, 0.25, edgecolor=self.color_home, alpha=min([self.perc_away+10,100])/100,
                                      facecolor=self.color_home, linewidth=0)

        ax.add_patch(rectangle2)

        # Title
        DefaultMatchVisual.create_title(fig, self.title_text, self.sub_title_text, self.color_home)

        plt.axis('off')

        # Twelve Logo
        DefaultMatchVisual.crete_logo(fig,dark_logo=True)

        # DefaultMatchVisual.create_title_split(fig, specs, self.title_text, self.sub_title_text_left,
        #                                       self.sub_title_text_right, self.color_home, self.color_away)

        # Persist Img
        if persist:
            plt.savefig(f'../output/xg_match_prob_{self.viz_name}.jpg', dpi=200, facecolor=fig.get_facecolor(), transparent=False, bbox_inches='tight', pad_inches=0.35)
        return fig, ax


class PitchDefaultMap:

    TEXT_FONT = FontHelper()
    CMAP_COLOR = 'Greens'

    @staticmethod
    def create_initial_figure(bg_color, sub_title_text, title_text,vertical=False, transparent=False, title=True, check_brightness=False,pitch_type='opta'):

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7, 7))
        fig.set_facecolor(bg_color)
        ax.patch.set_facecolor(bg_color)
        if transparent:
            # if check_brightness:
            #     brightness = get_color_brightnes(bg_color)
            #     print(brightness)
            #     if brightness > 100:
            #         fig.patch.set_alpha(0.2)
            #         ax.patch.set_alpha(0.02)
            #     else:
            #         fig.patch.set_alpha(0.1)
            #         ax.patch.set_alpha(0.01)
            # else:
                fig.patch.set_alpha(0.20)
                ax.patch.set_alpha(0)

        # Pitch
        if vertical:
            pitch = VerticalPitch(pitch_type = pitch_type, tight_layout=False, constrained_layout=True,
                          half=True,
                          pitch_color = bg_color, pad_bottom=-20,
                          line_color=bg_color if transparent else 'w',
                          line_zorder=2)
            # # subt
            if title:
                # if pitch_type == 'opta':
                txt = ax.text(x=50, y=110, s=sub_title_text,
                              color=bg_color if transparent else 'w', fontproperties=PitchDefaultMap.TEXT_FONT.get_font_sub_title(),
                              va='center',
                              ha='center')

                #  Title
                txt = ax.text(x=50, y=105, s=title_text,
                              color=bg_color if transparent else 'w', fontproperties=PitchDefaultMap.TEXT_FONT.get_font_title(),
                              va='center',
                              ha='center')

        else:
            pitch = Pitch(pitch_type = pitch_type,


                          pitch_color = bg_color,
                          pad_bottom = 12,
                          # pad_top = 30,
                          line_color='w',
                          line_zorder=2)

            # # subt Title
            if title:

                if pitch_type == 'wyscout':
                    txt = ax.text(x=50, y=-25.5, s=sub_title_text,
                                  color=bg_color if transparent else 'w', fontproperties=PitchDefaultMap.TEXT_FONT.get_font_sub_title(),
                                  va='center',
                                  ha='center')

                    #  Title
                    txt = ax.text(x=50, y=-15.5, s=title_text,
                                  color=bg_color if transparent else 'w', fontproperties=PitchDefaultMap.TEXT_FONT.get_font_title(),
                                  va='center',
                                  ha='center')
                else:
                    txt = ax.text(x=50, y=125.5, s=sub_title_text,
                                  color=bg_color if transparent else 'w',
                                  fontproperties=PitchDefaultMap.TEXT_FONT.get_font_sub_title(),
                                  va='center',
                                  ha='center')

                    #  Title
                    txt = ax.text(x=50, y=115.5, s=title_text,
                                  color=bg_color if transparent else 'w',
                                  fontproperties=PitchDefaultMap.TEXT_FONT.get_font_title(),
                                  va='center',
                                  ha='center')

        # ax_content = fig.add_axes([0.10, 0.20, 0.80, 0.6],zorder=1)  # [left, bottom, width, height] # [left, bottom, width, height]
        # ax_content.set_yticklabels([])
        #
        # ax_content.patch.set_alpha(0.0)
        # ax_content.axis('off')

        fig.subplots_adjust(left=0.06, right=0.94, top=0.79)
        pitch.draw(ax)
        return fig, ax, pitch

    @staticmethod
    def create_title_split(fig, ax, title_text, sub_title_text_left, sub_title_text_right, text_color, secondary_color, subtitle_y=0.88, title_y=0.82):

        from highlight_text import ax_text, fig_text

        # add a fancy box
        # fancybox = mpatches.FancyBboxPatch((0.1, 0.5), 0.05, 0.5,  fc=text_color, ec="b", lw=0, boxstyle=mpatches.BoxStyle("Round", pad=0.02))

        bbox_props = dict(boxstyle="round, pad=0.25", fc=text_color, ec=text_color, lw=3)
        bbox_props2 = dict(boxstyle="round, pad=0.25", fc=secondary_color, ec=secondary_color, lw=3)

        fig_text(s= f"<{sub_title_text_left}>   -   <{sub_title_text_right}>", x=0.5, y=subtitle_y , va='bottom',ha='center', color=text_color,
                    fontproperties=FontHelper.get_font_sub_title(),
                    highlight_textprops = [{'color': 'w', 'weight': 'bold', 'bbox': {'facecolor': text_color, **bbox_props}},
                                           {'color': 'w', 'weight': 'bold','bbox': {'facecolor': secondary_color, **bbox_props2}}],

                ax = ax
                )

        fig.text(0.5, title_y, title_text, ha="center", color=text_color,
                 fontproperties=FontHelper.get_font_title())


class PitchMatchShotmapViz:

    def __init__(self, viz_name, home_team_abbr, away_team_abbr,
                 home_team_score, away_team_score, bg_color='#59B877'):

        self.home_team_abbr = home_team_abbr
        self.away_team_abbr = away_team_abbr
        self.home_team_score = home_team_score
        self.away_team_score = away_team_score

        self.viz_name = viz_name
        self.title_text = f'xG Shot Map'
        self.sub_title_text = f"{self.home_team_abbr} {self.home_team_score} - {self.away_team_score} {self.away_team_abbr}"
        if bg_color is None:
            bg_color = '#20CF7B'
        self.bg_color = bg_color
        self.color_home = '#20CF7B'
        self.color_away = '#FF4B4B'

    def set_title_text(self,text):
        self.title_text = text

    def set_sub_title_text(self, text):
        self.sub_title_text = text

    def set_data(self, home_team_shots, away_team_shots, stories=None):

        self.stories = stories
        self.home_team_shots = home_team_shots
        self.away_team_shots = away_team_shots

        xG_shots_home = [x['xg'] for x in home_team_shots]
        xG_shots_away = [x['xg'] for x in away_team_shots]

        self.sub_title_text_left = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f})"
        self.sub_title_text_right = f"{self.away_team_abbr} ({sum(xG_shots_away):0.2f})"
        self.sub_title_text = f"{self.home_team_abbr} ({sum(xG_shots_home):0.2f}) - ({sum(xG_shots_away):0.2f}) {self.away_team_abbr}"

    def set_team_colors(self, home_team_home_color=None, home_team_away_color=None,
                        away_team_home_color=None, away_team_away_color=None):

        self.color_home = self.color_home if home_team_home_color is None else home_team_home_color
        self.color_away = self.color_away if away_team_home_color is None else away_team_home_color

        # Check Colors
        home_color_rgb = get_color_distance_fast(self.color_home, self.color_away)
        if home_color_rgb < 200:
            self.color_away = away_team_away_color

    def create_visual(self, persist=False):

        def get_transparency(type, txt):
            if type == 13:
                return 0.4
            if type == 14:
                return 0.8
            if type == 15 and 'blocked' in txt:
                return 0.6
            return 0.8

        shots_home = [(x['startX'], x['startY'], x['xg'] + 0.01, get_transparency(x['type'], x['typeName'])) for x in self.home_team_shots if x['type'] in [13, 14, 15]]
        shots_away = [(x['startX'], x['startY'], x['xg'] + 0.01, get_transparency(x['type'], x['typeName'])) for x in self.away_team_shots if x['type'] in [13, 14, 15]]

        goals_home = [(x['startX'], x['startY'], x['xg'] + 0.01) for x in self.home_team_shots if x['typeName'] == 'goal']
        goals_away = [(x['startX'], x['startY'], x['xg'] + 0.01) for x in self.away_team_shots if x['typeName'] == 'goal']

        if self.stories is not None:
            home_team_id = self.stories['homeTeam']['teamId']
            away_team_id = self.stories['awayTeam']['teamId']

            match_stories = [x for x in self.stories['stories'] if x['type_id'] in [13, 14, 15, 16]]
            match_details_home = [x for x in match_stories if len(x['players']) == 1 and x['players'][0]['teamId'] == home_team_id]
            match_details_away = [x for x in match_stories if len(x['players']) == 1 and x['players'][0]['teamId'] == away_team_id]

            goals_home_own = [(100-x['x'], 100-x['y'], 0.01) for x in match_details_away if x['description'] == 'OWN GOAL!']
            goals_home.extend(goals_home_own)
            goals_away_own = [(100-x['x'], 100-x['y'], 0.01) for x in match_details_home if x['description'] == 'OWN GOAL!']
            goals_away_own.extend(goals_away_own)

        fig, ax, pitch = PitchDefaultMap.create_initial_figure(self.bg_color,
                                                               title_text=self.title_text,
                                                               sub_title_text=self.sub_title_text,transparent=True, title=False)
        PitchDefaultMap.create_title_split(fig, ax, self.title_text, self.sub_title_text_left, self.sub_title_text_right, self.color_home,self.color_away)

        # For xG sizes
        min_space = np.linspace(0, 0.5, num=5, endpoint=True)
        min_space = np.append(min_space, 1)

        markers_size = [ 8, 9, 10, 11, 12, 13]

        for x, y, xg, alpha in shots_home:
            ms = markers_size[np.digitize(xg,min_space)]
            ax.plot([x], [y], 'o', markersize=ms, color=self.color_home,
                    alpha=alpha,
                    markeredgecolor=self.color_home, zorder=5)
        for x, y, xg in goals_home:
            ms = markers_size[np.digitize(xg,min_space)]
            ax.plot([x], [y], 'o', markersize=ms, color=self.color_home,
                    alpha=1,
                    markeredgecolor=self.color_home, zorder=5)
            ax.plot([x], [y], '*', markersize=ms, color='w',
                    alpha=1,
                    markeredgecolor=self.color_home, zorder=5)

        for x, y , xg, alpha in shots_away:
            ms = markers_size[np.digitize(xg,min_space)]
            ax.plot([100-x], [100-y], 'o', markersize=ms, color=self.color_away,
                    alpha=alpha,
                    markeredgecolor=self.color_away, zorder=5)
        for x, y, xg in goals_away:
            ms = markers_size[np.digitize(xg,min_space)]
            ax.plot([100-x], [100-y], 'o', markersize=ms, color=self.color_away,
                    alpha=1,
                    markeredgecolor=self.color_away, zorder=5)
            ax.plot([100-x], [100-y], '*', markersize=ms, color='w',
                    alpha=1,
                    markeredgecolor=self.color_away, zorder=5)

        DefaultMatchVisual.crete_logo(fig, True)
        # Persist Img
        if persist:
            plt.savefig(f'../output/{self.title_text}_{self.viz_name}.jpg', dpi=200, facecolor=fig.get_facecolor(), transparent=False, bbox_inches=None)

        return fig, ax


arrow_width = 4
arrow_headwidth = 4
arrow_headlength = 3
arrow_headaxislength = 2.5


class PitchHorizontalArrows:
    plt.switch_backend('agg')

    def __init__(self, viz_name, title='Title', subtitle ='Subtitle', cmap ='Greens', pitch_dim = (105, 68), provider=None, fig_size=(7,7)):
        self.viz_name = viz_name
        self.title = title
        self.subtitle = subtitle
        self.cmap = cmap
        self.pitch_dim = pitch_dim
        self.provider = provider
        self.fig_size = fig_size
        self.max_value = 1
        self.min_value = 0
        self.info_text = ''
        self.event_data = None

    def set_data(self, start_x: [], start_y: [], end_x: [], end_y: [], values: []):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.values = values


    def create_visual(self, persist=False):

        pitch = Pitch(pitch_type='custom' if self.provider is None else self.provider,
                      linewidth=1,
                      goal_type='box',
                      pitch_length = self.pitch_dim[0],
                      pitch_width= self.pitch_dim[1],
                      line_zorder=2)
        fig, axs = pitch.grid(figheight=10, title_height=0.08, endnote_space=0,
                              # Turn off the endnote/title axis. I usually do this after
                              # I am happy with the chart layout and text placement
                              axis=False,
                              title_space=0.02, grid_height=0.82, endnote_height=0.05)

        plt.gca().invert_yaxis()
        ax = axs['pitch']
        # endnote /title

        axs['title'].text(0.5, 0.7, self.subtitle, color='k', va='center', ha='center', fontsize=18) #fontproperties=robotto_regular.prop, )
        axs['title'].text(0.5, 0.25, self.title, color='k', va='center', ha='center',fontsize=30) #fontproperties=robotto_regular.prop,

        axs['endnote'].text(1, 0.5, self.info_text, color='k', va='center', ha='right', fontsize=15)


        events = pd.DataFrame({'x1': self.start_x,
                                      'y1': self.start_y,
                                      'x2': self.end_x,
                                      'y2': self.end_y,
                                      })


        # # Setup the pitch
        # pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
        # fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        # fig.set_facecolor('#22312b')
        # print(self.values)
        # print(norm(self.values))
        # Plot the completed passes

        pitch.arrows(events.x1, events.y1,
                     events.x2, events.y2,
                     width=arrow_width,
                     headwidth=arrow_headwidth, headlength=arrow_headlength,
                     headaxislength=arrow_headaxislength,
                     color= "green",
                     # edgecolor='black',
                     alpha=1,
                     zorder = 3,
                     ax=ax, )

        if persist:
            plt.savefig(f'../output/{self.title}_{self.subtitle}_{self.viz_name}.jpg', dpi=200, facecolor=fig.get_facecolor(), transparent=False, bbox_inches=None)

        return fig, ax