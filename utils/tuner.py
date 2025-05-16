import numpy as np
import pyaudio

NOTE_FREQUENCIES = {
    "E2": 86.13,
    "A2": 107.67,
    "D3": 150.73,
    "G3": 193.80,
    "B3": 215.10,
    "E4": 329.63,
}

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 4096

def get_closest_note_and_status(frequency):
    closest_note = None
    closest_freq = None
    min_difference = float('inf')

    for note, freq in NOTE_FREQUENCIES.items():
        difference = abs(frequency - freq)
        if difference < min_difference:
            closest_note = note
            closest_freq = freq
            min_difference = difference

    if closest_freq:
        if frequency < closest_freq - 2:
            status = "음이 낮습니다."
        elif frequency > closest_freq + 2:
            status = "음이 높습니다."
        else:
            status = "적절합니다."
    else:
        status = "알 수 없는 음입니다."

    return closest_note, status

def measure_background_noise(stream, duration=1):
    total_amplitude = 0
    sample_count = int(RATE / CHUNK * duration)

    for _ in range(sample_count):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        total_amplitude += np.max(np.abs(data))

    background_noise_level = total_amplitude / sample_count
    return background_noise_level

def run_tuner_with_callback(device_id, callback, is_running):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_id,
                        frames_per_buffer=CHUNK)

        background_noise_level = measure_background_noise(stream)
        effective_threshold = background_noise_level * 2.0

        previous_frequencies = []

        while is_running():
            data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
            mono_data = np.mean(data.reshape(-1, 2), axis=1).astype(np.int16)

            amplitude = np.max(np.abs(mono_data))
            if amplitude < effective_threshold:
                previous_frequencies.clear()
                continue

            fft = np.fft.fft(mono_data)
            freqs = np.fft.fftfreq(len(fft), 1 / RATE)
            magnitudes = np.abs(fft)

            positive_freqs = freqs[:len(freqs)//2]
            positive_magnitudes = magnitudes[:len(magnitudes)//2]
            peak_freq = positive_freqs[np.argmax(positive_magnitudes)]

            if not (80 <= peak_freq <= 1000):
                previous_frequencies.clear()
                continue

            previous_frequencies.append(peak_freq)
            if len(previous_frequencies) > 3:
                previous_frequencies.pop(0)

            if len(set(map(lambda x: round(x, 1), previous_frequencies))) == 1:
                note, status = get_closest_note_and_status(peak_freq)
                callback(note, peak_freq, status)
                previous_frequencies.clear()

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()