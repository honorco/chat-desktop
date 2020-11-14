import sqlite3

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton, MDFlatButton, MDFloatingActionButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldRect, MDTextFieldRound

KV = '''
<Content>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        hint_text: "Название" 
        
<Dialog>
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    height: "120dp"

    MDTextField:
        hint_text: "Ваш логин"
<MDToolbar>
    MDIconButton:
        id: button
        icon: "dots-vertical"
        pos_hint: {'center_x': .1, "center_y": .5}
        on_release: app.dialog_nickname()
Screen: 
    MDToolbar:
        id: toolbar
        title: "Chat!"
        mg_bg_color: app.theme_cls.primary_color
        elevation: 10
        pos_hint: {"top": 1}
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        elevation_normal: 10
        pos_hint: {"right": 0.1, "top": 0.12}
        on_release: app.new_chat_dialog()
    MDGridLayout:
        size_hint_x: 0.25
        pos_hint: {"top": 0.89, "left":1}
        id: box
        spacing: "5dp"
        cols: 1
    MDGridLayout:
        size_hint_x: 0.75
        pos_hint: {"top": 0.89, "right":1.01}
        id: coc
        spacing: "5dp"
        cols: 1 
    MDTextField:
        id: message
        md_bg_color: app.theme_cls.accent_color
        pos_hint: {"top": 0.1, "right":0.96}
        size_hint_x: 0.7
        on_text_validate:
'''


class Content(BoxLayout):
    pass

class Dialog(BoxLayout):
    pass
# sm = ScreenManager()
# sm.add_widget(MenuScreen(name='menu'))
# sm.add_widget(SpinnerScreen(name='spinner'))


class Chat(MDApp):
    conn = sqlite3.connect('test.db3')
    cursor = conn.cursor()
    sql = {'getChat_name': "SELECT chat_name FROM chat",
           'getMessage_text_message': "SELECT text_message FROM message where chat_id =",
           'getAuthors': "SELECT author FROM message"}
    dialog_1 = None
    dialog_2 = None
    nickname = ''
    press = 0

    def build(self):
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.primary_palette = "LightBlue"
        return self.screen

    def on_start(self):
        self.get_message()
        self.get_chats()

    def get_message(self):
        self.cursor.execute(self.sql['getMessage_text_message'] + '1')
        text_message = self.cursor.fetchall()
        length = 0
        if length != len(text_message):
            for k in range(length, len(text_message)):
                self.root.ids.coc.add_widget(
                    MDLabel(
                        text=str(*text_message[k]),
                        size_hint=(.1, None),
                    )
                )
        length = len(text_message)

    def get_chats(self):
        self.cursor.execute(self.sql['getChat_name'])
        chat_name = self.cursor.fetchall()
        for i in range(0, len(chat_name)):
            self.root.ids.box.add_widget(
                MDRectangleFlatButton(
                    text=str(*chat_name[i]),
                    size_hint=(.1, None),
                )
            )

    def __init__(self, **kwargs):  # создание меню
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def dialog_nickname(self):
        if not self.dialog_2:
            self.dialog_2 = MDDialog(
                title="Никнейм",
                type="custom",
                content_cls=Dialog(),
                buttons=[
                    MDFlatButton(
                        text="Cansel", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="Create", text_color=self.theme_cls.primary_color, on_release=self.grabText
                    ),
                ],
            )
        self.dialog_2.open()

    def new_chat_dialog(self):  # этот метод должен вызваться при нажатии кнопки
        if not self.dialog_1:
            self.dialog_1 = MDDialog(
                title="Новый чат",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="Cansel", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="Create", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog_1.open()

    def grabText(self, inst):
        for obj in self.dialog_2.content_cls.children:
            if isinstance(obj, MDTextField):
                self.nickname = obj.text
                print(self.nickname)

    def closeDialog(self, inst):
        if self.dialog_2:
            self.dialog_2.dismiss()
        if self.dialog_1:
            self.dialog_1.dismiss()


Chat().run()
