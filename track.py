from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

TRACK_NB_STEPS = 16

class TrackStepButton(ToggleButton):
    pass

class TrackSoundButton(Button):
    pass

class TrackWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(TrackWidget, self).__init__(**kwargs)
        self.add_widget(TrackSoundButton())
        for i in range(0,TRACK_NB_STEPS):
            self.add_widget(TrackStepButton())