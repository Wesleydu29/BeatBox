from audiostream.sources.thread import ThreadSource
from array import array
from audio_source_track import AudioSourceTrack

class AudioSourceMixer(ThreadSource):
    buf = None

    def __init__(self, output_stream, *args, all_wav_samples, bpm, sample_rate, nb_steps, on_current_step_changed, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)

        self.tracks = []

        for i in range(0, len(all_wav_samples)):
            track = AudioSourceTrack(output_stream, wav_samples=all_wav_samples[i], bpm=bpm, sample_rate=sample_rate)
            track.set_steps((0,) * nb_steps)
            self.tracks.append(track)

        self.nb_steps = nb_steps
        self.current_samples_index = 0
        self.current_step_index = 0
        self.sample_rate = sample_rate
        self.on_current_step_changed = on_current_step_changed
        self.is_playing = False

    def set_steps(self, index, steps):
        if index >= len(self.tracks):
            return
        if not len(steps) == self.nb_steps:
            self.tracks[index].set_steps(steps)

    def set_bpm(self, bpm):
        for i in range(0, len(self.tracks)):
            self.tracks[i].set_bpm(bpm)


    def get_bytes(self, *args, **kwargs):

        step_nb_samples = self.tracks[0].step_nb_samples
        if self.buf is None or not len(self.buf) == step_nb_samples:
            self.buf = array('h', b"\x00\x00" * step_nb_samples)

        track_buffers = []
        for i in range(0, len(self.tracks)):
            track = self.tracks[i]
            track_buffer = track.get_bytes_array()
            track_buffers.append(track_buffer)
        
        for i in range(0, step_nb_samples):
            self.buf[i] = 0
            for j in range(0, len(track_buffers)): # to mix, to add sample 1 of the first track, with the sample 1 of the second track ...
                self.buf[i] += track_buffers[j][i]

        # to send the current step index to the PlayIndicator
        if self.on_current_step_changed is not None:
            step_index_for_display = self.current_step_index - 2  # to synchronize the index and the sound
            if step_index_for_display < 0:
                step_index_for_display += self.nb_steps
            self.on_current_step_changed(step_index_for_display)


        self.current_step_index += 1
        if self.current_step_index >= self.nb_steps: # make a loop
            self.current_step_index = 0

        #self.current_samples_index += 1
        return self.buf.tobytes()