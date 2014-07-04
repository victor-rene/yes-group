def upcoming_events(page):
  table_start = page.find('<table class="eb_event_list"')
  table_end = page.find('</table>', table_start) + 8
  td_events = []
  i = table_start
  while i < table_end:
    td_event_start = page.find('<td class="eb_event">', i)
    if td_event_start == -1:
      break
    else:
      td_event_end = page.find('</td>', td_event_start) + 5
      td_events.append(page[td_event_start:td_event_end])
      i = td_event_end

  class Event:
    def __init__(self, text):
      self.text = text
      links = []
      i = 0
      n = len(text)
      while i < n:
        link_start = text.find('<a ', i)
        if link_start == -1:
          break
        else:
          link_end = text.find('</a>', link_start) + 4
          links.append(text[link_start:link_end])
          i = link_end
          
      name_start = links[0].find('>') + 1
      name_end = links[0].find('<', name_start)
      self.name = links[0][name_start:name_end]
      
      link_name_start = links[0].find('href="') + 6
      link_name_end = links[0].find('"', link_name_start) + 1
      self.link_name = links[0][link_name_start:link_name_end]
      
      location_start = links[1].find('>') + 1
      location_end = links[1].find('<', location_start)
      self.location = links[1][location_start:location_end]
      
      link_location_start = links[1].find('href="') + 6
      link_location_end = links[1].find('"', link_location_start) + 1
      self.link_location = links[1][link_location_start:link_location_end]
      
      date_start = text.find('<span class="event_date">') + 25
      date_end = text.find('</span>', date_start)
      self.date = text[date_start:date_end]
      
    def __str__(self):
      s = '<Event>:\n'
      vars = vars(self)
      for var in vars:
        s += '  ' + str(var) + '\n'
      return s
     
  events = []
  for td_event in td_events:
    events.append(Event(td_event))

  return events