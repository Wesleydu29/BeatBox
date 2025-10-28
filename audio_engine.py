from audiostream.core import get_output
from audio_source_one_shot import AudioSourceOneShot
from audio_source_track import AudioSourceTrack
from audio_source_mixer import AudioSourceMixer


class AudioEngine:
    NB_CHANNELS = 1 #mono
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 1024
    def __init__(self):
        self.output_stream = get_output(channels= self.NB_CHANNELS, rate= self.SAMPLE_RATE, buffersize=self.BUFFER_SIZE) # to connect to the sound card

        self.audio_source_one_shot = AudioSourceOneShot(self.output_stream)
        self.audio_source_one_shot.start()

    def play_sound(self, wav_samples): 
        self.audio_source_one_shot.set_wav_samples(wav_samples)

    
    def create_track(self, wav_samples, bpm):
        source_track = AudioSourceTrack(self.output_stream, wav_samples= wav_samples, sample_rate= self.SAMPLE_RATE, bpm = bpm,)
        #source_track.set_steps((1, 0, 0, 1))
        source_track.start()
        return source_track

    def create_mixer(self, all_wav_samples, bpm, nb_steps):
        source_mixer = AudioSourceMixer(self.output_stream, all_wav_samples=all_wav_samples, sample_rate =self.SAMPLE_RATE, nb_steps=nb_steps, bpm=bpm)
        source_mixer.start()
        return source_mixer