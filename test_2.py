from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton

KV = '''
Screen:
    MDToolbar:
        id: toolbar
        title: "Welcome!"
        mg_bg_color: app.theme_cls.primary_color
        elevation: 10
        right_action_items: [["settings", lambda x: x]]
        pos_hint: {"top": 1}
    MDFloatingActionButton:
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        elevation_normal: 10
        pos_hint: {"right": 0.98, "top": 0.12}
    MDGridLayout:
        pos_hint: {"top": 0.89}
        id: box
        spacing: "5dp"
        cols: 1
'''


class Chat(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = 'Red'
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_string(KV)

    def on_start(self):
        for i in range(3):
            self.root.ids.box.add_widget(
                MDRectangleFlatButton(
                    text="Dialog " + str(i),
                    size_hint=(.1, None),
                )
            )


Chat().run()
