import sqlite3

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

KV = '''
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        hint_text: "Название"
    MDSlider:
        min: 0
        max: 120
        value: 60
        
<Box>
    size_hint_y: 0.5
    height: self.minimum_height
    pos_hint: {"top": 0.5}
    

Screen: 
    MDToolbar:
        id: toolbar
        title: "Welcome to Chat!"
        mg_bg_color: app.theme_cls.primary_color
        elevation: 10
        right_action_items: [["settings", lambda x: x]]
        pos_hint: {"top": 1}
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        elevation_normal: 10
        pos_hint: {"right": 0.98, "top": 0.12}
        on_release: app.show_alert_dialog()
    MDGridLayout:
        size_hint_x: 0.25
        pos_hint: {"top": 0.89, "left":1}
        id: box
        spacing: "5dp"
        cols: 1
    MDGridLayout:
        size_hint_x: 0.75
        pos_hint: {"top": 0.89, "right":1}
        id: coc
        spacing: "5dp"
        cols: 1
'''


class Content(BoxLayout):
    pass


class Box(BoxLayout):
    pass


# class MenuScreen(Screen):
#   pass


# class SpinnerScreen(Screen):
#   pass


# sm = ScreenManager()
# sm.add_widget(MenuScreen(name='menu'))
# sm.add_widget(SpinnerScreen(name='spinner'))


class Chat(MDApp):
    conn = sqlite3.connect('test.db3')
    cursor = conn.cursor()
    sql = {'getChat_name': "SELECT chat_name FROM chat",
           'getMessage_text_message': "SELECT text_message FROM message where chat_id ="}
    dialog = None
    press = 0

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_start(self):
        self.root.ids.coc.add_widget(
            MDRectangleFlatButton(
                text=str('Привет'),
                size_hint=(.1, None),
                # on_press=root.manager.current = 'menu',
            )
        )
        self.cursor.execute(self.sql['getChat_name'])
        chat_name = self.cursor.fetchall()
        for i in range(0, len(chat_name)):
            self.root.ids.box.add_widget(
                MDRectangleFlatButton(
                    text=str(*chat_name[i]),
                    size_hint=(.1, None),
                    on_press=lambda x: self.message(i),
                )
            )

    def message(self, k=0):
        self.cursor.execute(self.sql['getMessage_text_message'] + str(k))
        text_message = self.cursor.fetchall()
        length = 0
        if length != len(text_message):
            for i in range(0, len(text_message) - length):
                self.root.ids.coc.add_widget(
                    MDLabel(
                        text="text_message[i]",
                        orientation="vertical",
                    )
                )
        length = len(text_message)

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Новый чат",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="Cansel", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="Create", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
            self.dialog.open()
            self.dialog = None


Chat().run()
