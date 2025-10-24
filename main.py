from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from track import TrackWidget
from sound_kit_service import *

Builder.load_file("track.kv")


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kw):
        super(MainWidget, self).__init__(**kw)
        self.sound_kit_service = SoundKitService()

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            self.tracks_layout.add_widget(TrackWidget())


class BeatBoxApp(App):
    pass

BeatBoxApp().run()