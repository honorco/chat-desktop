import sqlite3
from datetime import datetime

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
        
Screen: 
    MDToolbar:
        id: toolbar
        title: "Chat!"
        right_action_items: [['account', lambda x: app.dialog_nickname()]]
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

    ScrollView:
        size_hint: 0.74, 0.79
        # setting the width of the scrollbar to 50pixels
        bar_width: 10
        # setting the color of the active bar using rgba
        bar_color: 50, 50, 55, .8
        # setting the color of the inactive bar using rgba
        bar_inactive_color: 50, 40, 50, .8
        # setting the content only to scroll via bar, not content
        scroll_type: ['bars']
        pos_hint: {"top": 0.89, "right":0.998}
        GridLayout:
            size_hint_y: None
            id: coc
            cols: 1
            size_hint_x: None
            height: self.minimum_height
            spacing: "5dp"
    MDIconButton:
        icon: "button.png"
        user_font_size: "22sp"
        pos_hint: {"top": 0.1, "right":1}
        on_release: app.set_message()
    MDTextField:
        id: message
        hint_text: "Сообщение"
        md_bg_color: app.theme_cls.accent_color
        pos_hint: {"top": 0.1, "right":0.95}
        size_hint_x: 0.7
        on_text_validate: app.set_message()
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
    chats = {}
    nickname = ''
    press = 0
    count_dialogs = 0
    count_messages = 0
    active_dialog = ''
    chat_id = 1

    def build(self):
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.primary_palette = "LightBlue"
        return self.screen

    def on_start(self):
        self.dialog_nickname()

    def check_and_start(self):
        if self.nickname != '':
            self.get_chats()

    def get_message(self, chat_name, visit):
        self.chat_id = self.chats.get(chat_name)
        if visit == "get_chats":
            self.root.ids.coc.clear_widgets()
            self.count_messages = 0
        self.cursor.execute(self.sql['getMessage_text_message'] + str(self.chat_id))
        text_message = self.cursor.fetchall()
        if self.count_messages != len(text_message):
            for k in range(self.count_messages, len(text_message)):
                self.root.ids.coc.add_widget(
                    MDLabel(
                        text=str(*text_message[k]),
                        size_hint=(.1, None),
                    )
                )
        self.count_messages = len(text_message)

    def get_chats(self):
        self.cursor.execute(self.sql['getChat_name'])
        chat_name = self.cursor.fetchall()
        if self.count_dialogs != len(chat_name):
            for i in range(0, len(chat_name)):
                self.chats[str(*chat_name[i])] = i + 1
                self.root.ids.box.add_widget(
                    MDRectangleFlatButton(
                        text=str(*chat_name[i]),
                        size_hint=(.1, None),
                        on_press=self.pressed_btn,
                    )
                )
        self.count_dialogs = len(chat_name)

    def pressed_btn(self, instance_toggle_button):
        self.active_dialog = instance_toggle_button.text
        self.get_message(self.active_dialog, "get_chats")

    def set_message(self):
        text_message = self.root.ids.message.text
        if text_message != '':
            today = datetime.today()
            self.cursor.execute(
                "INSERT INTO message (text_message, time, chat_id, author) VALUES ('" + text_message + "', '" + today.strftime(
                    "%Y-%m-%d-%H.%M.%S") + "', '" + str(self.chat_id) + "', '" + self.nickname + "');");
            self.conn.commit()
            self.get_message(self.active_dialog, "set_message")
            self.get_chats()
            self.root.ids.message.text = ""

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
                        text="Закрыть", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="Сохранить", text_color=self.theme_cls.primary_color, on_release=self.grabText
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
                        text="Закрыть", text_color=self.theme_cls.primary_color, on_release=self.closeDialog
                    ),
                    MDFlatButton(
                        text="Создать", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog_1.open()

    def grabText(self, inst):
        for obj in self.dialog_2.content_cls.children:
            if isinstance(obj, MDTextField):
                if obj.text != '':
                    self.nickname = obj.text
        self.check_and_start()

    def closeDialog(self, inst):
        if self.dialog_2:
            self.dialog_2.dismiss()
            self.check_and_start()
        if self.dialog_1:
            self.dialog_1.dismiss()

    def on_stop(self):
        self.conn.close()


Chat().run()
