# -*- coding: utf-8 -*-
#
# This file created with KivyCreatorProject
# <https://github.com/HeaTTheatR/KivyCreatorProgect
#
# Copyright آ© 2017 Easy
#
# For suggestions and questions:
# <kivydevelopment@gmail.com>
# 
# LICENSE: MIT

import os
import sys
from ast import literal_eval

from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.logger import PY2
from kivy.clock import Clock
from kivy.utils import get_color_from_hex, get_hex_from_color
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty

from main import __version__
from libs.translation import Translation
from libs.uix.baseclass.startscreen import StartScreen
from libs.uix.lists import Lists

from kivymd.theming import ThemeManager
from kivymd.label import MDLabel
from kivymd.toast import toast

from dialogs import card


class name_project(App):
    title = 'name_project'
    icon = 'icon.png'
    nav_drawer = ObjectProperty()
    theme_cls = ThemeManager()
    theme_cls.primary_palette = 'Blue'
    lang = StringProperty('en')

    def __init__(self, **kvargs):
        super(name_project, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.events_program)
        Window.soft_input_mode = 'below_target'

        self.list_previous_screens = ['base']
        self.window = Window
        self.config = ConfigParser()
        self.manager = None
        self.window_language = None
        self.exit_interval = False
        self.dict_language = literal_eval(
            open(
                os.path.join(self.directory, 'data', 'locales', 'locales.txt')).read()
        )
        self.translation = Translation(
            self.lang, 'Ttest', os.path.join(self.directory, 'data', 'locales')
        )

    def get_application_config(self):
        return super(name_project, self).get_application_config(
                        '{}/%(appname)s.ini'.format(self.directory))

    def build_config(self, config):
        '''ذ،ذ¾ذ·ذ´ذ°ر‘ر‚ ر„ذ°ذ¹ذ» ذ½ذ°رپر‚ر€ذ¾ذµذ؛ ذ؟ر€ذ¸ذ»ذ¾ذ¶ذµذ½ذ¸رڈ name_project.ini.'''

        config.adddefaultsection('General')
        config.setdefault('General', 'language', 'en')

    def set_value_from_config(self):
        '''ذ£رپر‚ذ°ذ½ذ°ذ²ذ»ذ¸ذ²ذ°ذµر‚ ذ·ذ½ذ°ر‡ذµذ½ذ¸رڈ ذ؟ذµر€ذµذ¼ذµذ½ذ½ر‹ر… ذ¸ذ· ر„ذ°ذ¹ذ»ذ° ذ½ذ°رپر‚ر€ذ¾ذµذ؛ name_project.ini.'''

        self.config.read(os.path.join(self.directory, 'name_project.ini'))
        self.lang = self.config.get('General', 'language')

    def build(self):
        self.set_value_from_config()
        self.load_all_kv_files(os.path.join(self.directory, 'libs', 'uix', 'kv'))
        self.screen = StartScreen()  # ذ³ذ»ذ°ذ²ذ½ر‹ذ¹ رچذ؛ر€ذ°ذ½ ذ؟ر€ذ¾ذ³ر€ذ°ذ¼ذ¼ر‹
        self.manager = self.screen.ids.manager
        self.nav_drawer = self.screen.ids.nav_drawer

        return self.screen

    def load_all_kv_files(self, directory_kv_files):
        for kv_file in os.listdir(directory_kv_files):
            kv_file = os.path.join(directory_kv_files, kv_file)
            if os.path.isfile(kv_file):
                if not PY2:
                    with open(kv_file, encoding='utf-8') as kv:
                        Builder.load_string(kv.read())
                else:
                    Builder.load_file(kv_file)

    def events_program(self, instance, keyboard, keycode, text, modifiers):
        '''ذ’ر‹ذ·ر‹ذ²ذ°ذµر‚رپرڈ ذ؟ر€ذ¸ ذ½ذ°ذ¶ذ°ر‚ذ¸ذ¸ ذ؛ذ½ذ¾ذ؟ذ؛ذ¸ ذœذµذ½رژ ذ¸ذ»ذ¸ Back Key
        ذ½ذ° ذ¼ذ¾ذ±ذ¸ذ»رŒذ½ذ¾ذ¼ رƒرپر‚ر€ذ¾ذ¹رپر‚ذ²ذµ.'''

        if keyboard in (1001, 27):
            if self.nav_drawer.state == 'open':
                self.nav_drawer.toggle_nav_drawer()
            self.back_screen(event=keyboard)
        elif keyboard in (282, 319):
            pass

        return True

    def back_screen(self, event=None):
        '''ذœذµذ½ذµذ´ذ¶ذµر€ رچذ؛ر€ذ°ذ½ذ¾ذ². ذ’ر‹ذ·ر‹ذ²ذ°ذµر‚رپرڈ ذ؟ر€ذ¸ ذ½ذ°ذ¶ذ°ر‚ذ¸ذ¸ Back Key
        ذ¸ رˆذµذ²ر€ذ¾ذ½ذ° "ذ‌ذ°ذ·ذ°ذ´" ذ² ToolBar.'''

        # ذ‌ذ°ذ¶ذ°ر‚ذ° BackKey.
        if event in (1001, 27):
            if self.manager.current == 'base':
                self.dialog_exit()
                return
            try:
                self.manager.current = self.list_previous_screens.pop()
            except:
                self.manager.current = 'base'
            self.screen.ids.action_bar.title = self.title
            self.screen.ids.action_bar.left_action_items = \
                [['menu', lambda x: self.nav_drawer._toggle()]]

    def show_about(self, *args):
        self.nav_drawer.toggle_nav_drawer()
        self.screen.ids.about.ids.label.text = \
            self.translation._(
                u'[size=20][b]name_project[/b][/size]\n\n'
                u'[b]Version:[/b] {version}\n'
                u'[b]License:[/b] MIT\n\n'
                u'[size=20][b]Developer[/b][/size]\n\n'
                u'[ref=SITE_PROJECT]'
                u'[color={link_color}]name_author[/color][/ref]\n\n'
                u'[b]Source code:[/b] '
                u'[ref=repo_project_on_github]'
                u'[color={link_color}]GitHub[/color][/ref]').format(
                version=__version__,
                link_color=get_hex_from_color(self.theme_cls.primary_color)
            )
        self.manager.current = 'about'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]

    def show_license(self, *args):
        if not PY2:
            self.screen.ids.license.ids.text_license.text = \
                self.translation._('%s') % open(
                    os.path.join(self.directory, 'LICENSE'), encoding='utf-8').read()
        else:
            self.screen.ids.license.ids.text_license.text = \
                self.translation._('%s') % open(
                    os.path.join(self.directory, 'LICENSE')).read()
        self.nav_drawer._toggle()
        self.manager.current = 'license'
        self.screen.ids.action_bar.left_action_items = \
            [['chevron-left', lambda x: self.back_screen(27)]]
        self.screen.ids.action_bar.title = \
            self.translation._('MIT LICENSE')

    def select_locale(self, *args):
        '''ذ’ر‹ذ²ذ¾ذ´ذ¸ر‚ ذ¾ذ؛ذ½ذ¾ رپذ¾ رپذ؟ذ¸رپذ؛ذ¾ذ¼ ذ¸ذ¼ذµرژر‰ذ¸ر…رپرڈ رڈذ·ر‹ذ؛ذ¾ذ²ر‹ر… ذ»ذ¾ذ؛ذ°ذ»ذ¸ذ·ذ°ر†ذ¸ذ¹ ذ´ذ»رڈ
        رƒرپر‚ذ°ذ½ذ¾ذ²ذ؛ذ¸ رڈذ·ر‹ذ؛ذ° ذ؟ر€ذ¸ذ»ذ¾ذ¶ذµذ½ذ¸رڈ.'''

        def select_locale(name_locale):
            '''ذ£رپر‚ذ°ذ½ذ°ذ²ذ»ذ¸ذ²ذ°ذµر‚ ذ²ر‹ذ±ر€ذ°ذ½ذ½رƒرژ ذ»ذ¾ذ؛ذ°ذ»ذ¸ذ·ذ°ر†ذ¸رژ.'''

            for locale in self.dict_language.keys():
                if name_locale == self.dict_language[locale]:
                    self.lang = locale
                    self.config.set('General', 'language', self.lang)
                    self.config.write()

        dict_info_locales = {}
        for locale in self.dict_language.keys():
            dict_info_locales[self.dict_language[locale]] = \
                ['locale', locale == self.lang]

        if not self.window_language:
            self.window_language = card(
                Lists(
                    dict_items=dict_info_locales,
                    events_callback=select_locale, flag='one_select_check'
                ),
                size=(.85, .55)
            )
        self.window_language.open()

    def dialog_exit(self):
        def check_interval_press(interval):
            self.exit_interval += interval
            if self.exit_interval > 5:
                self.exit_interval = False
                Clock.unschedule(check_interval_press)

        if self.exit_interval:
            sys.exit(0)
            
        Clock.schedule_interval(check_interval_press, 1)
        toast(self.translation._('Press Back to Exit'))
    def on_lang(self, instance, lang):
        self.translation.switch_lang(lang)
