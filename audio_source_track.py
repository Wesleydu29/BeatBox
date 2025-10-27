from audiostream.sources.thread import ThreadSource
from array import array

class AudioSourceTrack(ThreadSource):
    steps = ()
    step_nb_samples = 0
    buf = None

    def __init__(self, output_stream, *args, wav_samples, sample_rate, bpm, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.current_samples_index = 0
        self.current_step_index = 0
        self.wav_samples = wav_samples
        self.nb_wav_samples = len(wav_samples)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.compute_step_nb_samples_and_alloc_buffer()

    def set_steps(self, steps):
        if len(self.steps) == self.steps:
            self.current_step_index = 0
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.compute_step_nb_samples_and_alloc_buffer()
    
    def compute_step_nb_samples_and_alloc_buffer(self):
        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / self.bpm)
            if not n == self.step_nb_samples:
                self.step_nb_samples = n
                self.buf = array('h', b"\x00\x00" * self.step_nb_samples) #to 64 bytes


    
    def get_bytes(self, *args, **kwargs):
        for i in range(0, self.step_nb_samples):
            if len(self.steps) > 0:
                if self.steps[self.current_step_index] == 1:  # if step is active, play song
                    self.buf[i] = self.wav_samples[i]
                else:
                    self.buf[i] = 0
            else:
                self.buf[i] = 0

        self.current_step_index += 1
        if self.current_step_index >= len(self.steps): # make a loop
            self.current_step_index = 0

        #self.current_samples_index += 1
        return self.buf.tobytes()