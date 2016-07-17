from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock

from kivy.uix.screenmanager import *
kivy.require('1.9.1')

from functools import partial
import requests

f = open("message.txt", "r+")
g = open("userInfo.txt", "r+")
prev_message = f.read()
user_data = g.read().split("\n")

url_master = requests.get("http://pastebin.com/raw/qdYuAWVV")
url_list = (url_master.text.split('\n'))
for i in range(len(url_list)):
    url_list[i] = str(url_list[i]).translate(None,'\r')

url_links = []
for url in url_list:
    tempArray = url.split('|')
    url_links.append(tempArray[1])


class ScreenWelcome(Screen):
    def __init__(self, **kwargs):
        super(ScreenWelcome, self).__init__(**kwargs)
        Clock.schedule_once(self.callNext, 20)


    def callNext(self,dt):
        self.manager.current = 'Start'


class ScreenStart(Screen):
    def on_enter(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.textInput.text = prev_message
        f.seek(0)
        f.truncate()

    def btn_sub_action(self):
        f.write(self.textInput.text)
        f.close()
        quit()

    def btn_cont_action(self):
        if (user_data[0]!='' and user_data[2]>user_data[1]):
            subscribe_text_raw = requests.get(str(user_data[0]))
            subscribe_text_org = subscribe_text_raw.text.split("|")
            day_messages = str(subscribe_text_org[1]).split("\r\n")
            f.write(day_messages[int(user_data[1])])
            g.seek(0)
            g.truncate()
            g.write(user_data[0]+"\n"+str(int(user_data[1])+1)+"\n"+user_data[2])
            quit()
        else:
            self.textInput.text="Error: No current message series"

class ScreenSelect(Screen):
    layout = GridLayout(cols=2, size_hint_y=None, spacing=33, padding=10)
    layout.bind(minimum_height=layout.setter('height'))

    def generate_list(self):
        for url in url_links:
            raw_data = requests.get(str(url))
            org_data = raw_data.text.split('|')
            next_message = str(org_data[1]).split("\r\n")

            lbl = Label(text=org_data[0], size_hint_y = None, height=100, color=(1,0.5,0.7,1), bold=True, font_size='18sp')
            btn = Button(text="+", font_size='36sp', size_hint= (None,None), height=100, width=100, color=(1,0.5,0.7,1), background_normal='', on_release=partial(self.btn_pressed, next_message[0], url))

            self.layout.add_widget(lbl)
            self.layout.add_widget(btn)

    def __init__(self, **kwargs):
        super(ScreenSelect, self).__init__(**kwargs)
        self.generate_list()
        scroll_list = ScrollView(size_hint=(None, None), size=(800,600))
        scroll_list.add_widget(self.layout)
        self.add_widget(scroll_list)

    def btn_pressed(self, text, link, *args):
        info = text.split(":")
        g.seek(0)
        g.truncate()
        g.write(str(link)+"\n"+"1\n"+str(info[0]))
        f.write(info[1])
        f.close()
        quit()


class ButterflyUI(ScreenManager):
    screen_welcome = ObjectProperty(None)
    screen_start = ObjectProperty(None)
    screen_select = ObjectProperty(None)


class ButterflyApp(App):
    def build(self):
        m = ButterflyUI(transition=NoTransition())
        return m


if __name__ == '__main__':
    ButterflyApp().run()