#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.network.urlrequest import UrlRequest
import html_parser
from eventwidget import EventWidget, EventListbox


Builder.load_string("""
<LoginScreen>:
  FloatLayout:
    canvas:
      Rectangle:
        pos: root.pos
        size: root.size
    Label: 
      color: .1,.3,.6,1
      text: 'YesGroup'
      pos_hint: {'center_x': .5, 'center_y':.8}
      size_hint: None, .1
      font_size: 48
    Label: 
      color: .1,.3,.6,1
      text: 'Email :'
      pos_hint: {'center_x': .5, 'center_y':.55}
      size_hint: .2, .1
    TextInput: 
      id: ti_email
      color: .1,.3,.6,1
      pos_hint: {'center_x': .5, 'center_y':.5}
      size_hint: .4, .05
      valign: 'middle'
    Label: 
      color: .1,.3,.6,1
      text: 'Mot de passe :'
      pos_hint: {'center_x': .5, 'center_y':.4}
      size_hint: .2, .1
    TextInput: 
      id: ti_pwd
      color: .1,.3,.6,1
      pos_hint: {'center_x': .5, 'center_y':.35}
      size_hint: .4, .05
      password: True
    Button:
      pos_hint: {'center_x': .5, 'center_y':.2}
      size_hint: .4, .1
      text: 'Connexion'
      on_press: root.login()

<MenuScreen>:
  FloatLayout:
    canvas:
      Rectangle:
        pos: root.pos
        size: root.size
      Color:
        rgb: 0,.5,1
      Rectangle: 
        pos: root.x, root.height * .9
        size: root.width, root.height * .1
    Label:
      color: 1,1,1,1
      text: 'Accueil'
      pos_hint: {'center_x': .5, 'center_y':.95}
      size_hint: 1, .1
    Image:
      source: './img/home.png'
      size_hint: None, .1
      pos_hint: {'center_x': .9, 'center_y':.95}
    Label:
      color: 0,.5,1,1
      text: 'Profil'
      pos_hint: {'center_x': .6, 'center_y':.7}
      size_hint: .6, .1
      on_touch_down: root.show_profile(*args)
    Image:
      source: './img/profile.png'
      size_hint: None, .1
      pos_hint: {'center_x': .2, 'center_y':.7}
      on_touch_down: root.show_profile(*args)
    Label:
      color: 0,.5,1,1
      text: 'Evénements'
      pos_hint: {'center_x': .6, 'center_y':.5}
      size_hint: .6, .1
      on_touch_down: root.show_events(*args)
    Image:
      source: './img/events.png'
      size_hint: None, .1
      pos_hint: {'center_x': .2, 'center_y':.5}
      on_touch_down: root.show_events(*args)
      
<ProfileScreen>:
  FloatLayout:
    canvas:
      Rectangle:
        pos: root.pos
        size: root.size
      Color:
        rgb: 0,.5,1
      Rectangle: 
        pos: root.x, root.height * .9
        size: root.width, root.height * .1
      Rectangle: 
        pos: root.x, root.y
        size: root.width, root.height * .1
    Label:
      color: 1,1,1,1
      text: 'Nom Prénom'
      pos_hint: {'center_x': .5, 'center_y':.95}
      size_hint: 1, .1
    Image:
      source: './img/profile.png'
      size_hint: None, .1
      pos_hint: {'center_x': .9, 'center_y':.95}
    Label:
      color: 1,1,1,1
      text: 'Retour'
      pos_hint: {'center_x': .5, 'center_y':.05}
      size_hint: 1, .1
      on_touch_down: root.show_menu(*args)
      
<EventScreen>:
  FloatLayout:
    canvas:
      Rectangle:
        pos: root.pos
        size: root.size
      Color:
        rgb: 0,.5,1
      Rectangle: 
        pos: root.x, root.height * .9
        size: root.width, root.height * .1
        size: root.width, root.height * .1
      Rectangle: 
        pos: root.x, root.y
        size: root.width, root.height * .1
    Label:
      color: 1,1,1,1
      text: 'Evénements'
      pos_hint: {'center_x': .5, 'center_y':.95}
      size_hint: 1, .1
    Image:
      source: './img/events.png'
      size_hint: None, .1
      pos_hint: {'center_x': .9, 'center_y':.95}
    Label:
      color: 1,1,1,1
      text: 'Retour'
      pos_hint: {'center_x': .5, 'center_y':.05}
      size_hint: 1, .1
      on_touch_down: root.show_menu(*args)
""")


class MenuScreen(Screen):

  def show_events(self, *args):
    wgt = args[0]
    touch = args[1]
    if wgt.collide_point(touch.x, touch.y):
      sm.current = 'events'
      sm.current_screen.load_upcoming_events()
      
  def show_profile(self, *args):
    wgt = args[0]
    touch = args[1]
    if wgt.collide_point(touch.x, touch.y):
      sm.current = 'profile'
      
class LoginScreen(Screen):

  def login(self):
    sm.current = 'menu'
    
    
class EventScreen(Screen):

  def __init__(self, **kwargs):
    super(EventScreen, self).__init__(**kwargs)
    self.event_list = EventListbox(size_hint=[1,.8], pos_hint={'center_x':0.5, 'center_y':0.5})
    self.add_widget(self.event_list)

  def parse_upcoming_events(self, req, result):
    events = html_parser.upcoming_events(result)
    self.event_list.clear_items()
    print events
    for event in events:
      self.event_list.add_item(event)

  def load_upcoming_events(self):
    req = UrlRequest('http://yesgroup.fr', on_success=self.parse_upcoming_events)
    
  def show_menu(self, *args):
    wgt = args[0]
    touch = args[1]
    if wgt.collide_point(touch.x, touch.y):
      sm.current = 'menu'
  
  
class ProfileScreen(Screen):

  def show_menu(self, *args):
    wgt = args[0]
    touch = args[1]
    if wgt.collide_point(touch.x, touch.y):
      sm.current = 'menu'

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(EventScreen(name='events'))

class YesGroupApp(App):

  def build(self):
    sm.current = 'login'
    return sm

if __name__ == '__main__':
  YesGroupApp().run()