import sqlite3
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton, MDFlatButton, MDFloatingActionButton, MDRaisedButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldRect, MDTextFieldRound
from db_controller import DBController
from ws_controller import WSConstroller

try:
    import thread
except ImportError:
    import _thread as thread

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
        text: root.get_text_username()
        
Screen: 
    MDToolbar:
        id: toolbar
        title: "Chat!"
        right_action_items: [['account', lambda x: app.dialog_nickname()]]
        mg_bg_color: app.theme_cls.primary_color
        elevation: 10
        pos_hint: {"top": 1}
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
            size_hint_x: 1
            height: self.minimum_height
            spacing: "5dp"
    MDIconButton:
        icon: 'arrow-right'
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
    def get_text_username(self):
        return db.get_username()


# sm = ScreenManager()
# sm.add_widget(MenuScreen(name='menu'))
# sm.add_widget(SpinnerScreen(name='spinner'))

db = DBController()

ws = WSConstroller(db)
theme_cls = ThemeManager()

class Chat(MDApp):
    dialog_1 = None
    dialog_2 = None
    chats = dict()
    nickname = 'Guest'
    press = 0
    active_dialog = ''
    chat_id = 1

    def build(self):
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.primary_palette = "LightBlue"
        return self.screen

    def on_start(self):
        ws.set_object_chats(self)
        thread.start_new_thread(lambda: ws.synch_all(self, self.pressed_btn), ())
        for chat in db.get_chats():
            self.chats[chat[0]] = chat[1]
        self.nickname = db.get_username()
        self.get_chats()
        if not db.get_username():
            self.dialog_nickname()

    def check_and_start(self):
        if self.nickname != '':
            self.get_chats()

    def get_message(self, chat_name):
        for key, value in self.chats.items():
            if chat_name == value:
                self.chat_id = key
                ws.set_id_button([key])
                break
        self.root.ids.coc.clear_widgets()
        messages = db.get_messages(self.chat_id)
        for name in messages:
            self.root.ids.coc.add_widget(ThreeLineListItem(text=name[0], secondary_text=name[2], tertiary_text=name[1]))
        ws.set_id_button(self.chat_id)
        ws.synch_messages()


    def get_chats(self):    # update_chats
        chat_name = db.get_chats()
        for chat in chat_name:
            self.root.ids.box.add_widget(
                MDRectangleFlatButton(
                    text=chat[1],
                    size_hint=(.1, None),
                    on_release=self.pressed_btn,
                )
            )


    def pressed_btn(self, instance_toggle_button):
        self.active_dialog = instance_toggle_button.text
        self.get_message(self.active_dialog)

    def set_message(self):
        text_message = self.root.ids.message.text
        if text_message != '':
            today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            db.set_message(text_message,today, self.chat_id, self.nickname)
            self.root.ids.coc.add_widget(ThreeLineListItem(text=text_message, secondary_text=self.nickname, tertiary_text=today))
            self.root.ids.message.text = ""
            ws.send_message(text_message,today ,self.nickname , self.chat_id)

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
                    MDRaisedButton(
                        text="Сохранить", text_color=self.theme_cls.primary_color, on_release=lambda x: self.grabText(inst=x)
                    ),
                ],
            )
        self.dialog_2.set_normal_height()
        self.dialog_2.open()

    def grabText(self, inst):
        for obj in self.dialog_2.content_cls.children:
            if isinstance(obj, MDTextField):
                if obj.text != '':
                    print(obj.text)
                    db.set_username(obj.text)

    def closeDialog(self, inst):
        if self.dialog_2:
            self.dialog_2.dismiss()
            self.check_and_start()
        if self.dialog_1:
            self.dialog_1.dismiss()


Chat().run()
