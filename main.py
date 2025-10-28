from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from track import TrackWidget
from sound_kit_service import *
from audio_engine import AudioEngine

Builder.load_file("track.kv")

TRACK_NB_STEPS = 16


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()

    def __init__(self, **kw):
        super(MainWidget, self).__init__(**kw)
        self.sound_kit_service = SoundKitService()

        kick_sound = self.sound_kit_service.get_sound_at(0)

        self.audio_engine = AudioEngine()
        #self.audio_engine.play_sound(kick_sound.samples)

        #self.audio_engine.create_track(kick_sound.samples, 120)
        self.audio_engine.create_mixer(self.sound_kit_service.soundkit.get_all_samples(), 120, TRACK_NB_STEPS)

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound, self.audio_engine, TRACK_NB_STEPS))


class BeatBoxApp(App):
    pass

BeatBoxApp().run()