from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label


class EventWidget(GridLayout):

  def __init__(self, event=None, **kwargs):
    super(EventWidget, self).__init__(**kwargs)
    self.cols = 1
    self.rows = 3
    self.lbl_name = Label(color=[0,0.5,1,1])
    self.lbl_date = Label(color=[0,0.5,1,1])
    self.lbl_location = Label(color=[0,0.5,1,1])
    self.add_widget(self.lbl_name)
    self.add_widget(self.lbl_date)
    self.add_widget(self.lbl_location)
    self.event = event
    if self.event:
      self.update()
  
  def update(self):
    self.lbl_name.text = self.event.name
    self.lbl_date.text = self.event.date
    self.lbl_location.text = self.event.location
    
    
class EventListbox(StackLayout):

  def __init__(self, **kwargs):
    super(EventListbox, self).__init__(**kwargs)
    self.is_updating = False
    self.orientation = 'lr-tb'
    self.items = []
    self.bind(pos=self.draw, size=self.draw)
    self.data_bindings = dict()
    self.selected_view = None
    self.selected_item = None
    # content
    self.content = StackLayout(orientation = 'lr-tb')
    self.content.size_hint_y = None #for scrollviewer
    self.content.bind(minimum_height=self.content.setter('height'))
    self.scrollview = ScrollView(size_hint=[1, 1])
    self.scrollview.do_scroll_x = False
    self.scrollview.add_widget(self.content)
    self.add_widget(self.scrollview)
    
  def begin_update(self):
    self.is_updating = True
    
  def end_update(self):
    self.is_updating = False
    self.draw()
    
  def add_item(self, item):
    self.items.append(item)
    if not self.is_updating:
      self.draw()
    
  def clear_items(self):
    del self.items[:]
    self.clear_selection()
    self.draw()
    
  def clear_selection(self):
    self.selected_view = None
    self.selected_item = None
    
  def draw(self, *args):
    self.content.clear_widgets()
    self.data_bindings.clear()
    n = len(self.items)
    i = 0
    while i < n:
      item_wgt = EventWidget(self.items[i])
      item_wgt.height = self.height/4
      item_wgt.size_hint = [1, None] #for scrollviewer parent
      item_wgt.bind(on_touch_down=self.selection_change)
      self.content.add_widget(item_wgt)
      self.data_bindings[item_wgt] = self.items[i]
      i += 1
    # self.draw_background()
      
  def selection_change(self, instance, touch):
    for item_wgt in self.content.children:
      if item_wgt.collide_point(touch.x, touch.y):
        self.selected_view = item_wgt
        self.selected_item = self.data_bindings[item_wgt]