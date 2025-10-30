from audiostream.sources.thread import ThreadSource
from array import array

class AudioSourceTrack(ThreadSource):
    steps = ()
    step_nb_samples = 0
    buf = None

    def __init__(self, output_stream, wav_samples, sample_rate, bpm, min_bpm, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.current_samples_index = 0
        self.current_step_index = 0
        self.wav_samples = wav_samples
        self.nb_wav_samples = len(wav_samples)
        self.min_bpm = min_bpm
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.last_sound_sample_start_index = 0

        self.step_nb_samples = self.compute_step_nb_samples(bpm)
        self.buffer_nb_samples = self.compute_step_nb_samples(min_bpm)
        self.buf = array('h', b"\x00\x00" * self.buffer_nb_samples)
        self.silence = array('h', b"\x00\x00" * self.buffer_nb_samples)

        if not self.bpm == 0:
            n = int(self.sample_rate * 15 / self.bpm)
            if not n == self.step_nb_samples:
                self.step_nb_samples = n

    def set_steps(self, steps):
        if not len(self.steps) == len(self.steps):
            self.current_step_index = 0
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.step_nb_samples = self.compute_step_nb_samples(bpm)
    
    def compute_step_nb_samples(self, bpm_value):
        if not bpm_value == 0:
            n = int(self.sample_rate * 15 / bpm_value)
            return n
        return 0

    def no_steps_activated(self): # function to prevent sounds when launching the app

        if len(self.steps) == 0:
            return True
        
        for i in range(len(self.steps)):
            if self.steps[i] == 1:
                return False
        
        return True

    
    def get_bytes_array(self):

        result_buf = None
        if self.no_steps_activated():
            result_buf = self.silence[0: self.step_nb_samples]
        elif self.steps[self.current_step_index] == 1:  # if step is active, play song
            #if step activated and sound has more samples than the step
            self.last_sound_sample_start_index = self.current_samples_index  # to remember the last position (in the sample) if next step = 0
            if self.nb_wav_samples >= self.step_nb_samples:
                result_buf = self.wav_samples[0: self.step_nb_samples]
            else: # step activated but sound a-has less samples than the step
                silence_nb_samples = self.step_nb_samples - self.nb_wav_samples
                result_buf = self.wav_samples[0: self.nb_wav_samples]
                result_buf.extend(self.silence[0: silence_nb_samples])
        else: # the step is not activated, but we must play the rest of the sound
            index = self.current_samples_index - self.last_sound_sample_start_index
            # what we have left to play is longer than a step
            if index > self.nb_wav_samples:
                # step not activated and we have finished playing sound -> silence
                result_buf = self.silence[0: self.step_nb_samples]
            elif self.nb_wav_samples - index >= self.step_nb_samples:
                result_buf = self.wav_samples[index: self.step_nb_samples + index]
            else:
                silence_nb_samples = self.step_nb_samples - self.nb_wav_samples + index
                result_buf = self.wav_samples[index: self.nb_wav_samples]
                result_buf.extend(self.silence[0: silence_nb_samples])
            
        self.current_samples_index += self.step_nb_samples


        self.current_step_index += 1
        if self.current_step_index >= len(self.steps): # make a loop
            self.current_step_index = 0

        if result_buf is None:
            print("None")
        elif not len(result_buf) == self.step_nb_samples:
            print("result_buf len is not step_nb_samples")
    
        return result_buf
    
    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()