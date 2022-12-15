import wave
from typing import Tuple

from google.cloud import speech
# from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types

TESTCASES = [
    {
        'filename': 'audio/2830-3980-0043.wav',
        'text': 'experience proves this',
        'encoding': 'LINEAR16',
        'lang': 'en-US'
    },
    {
        'filename': 'audio/4507-16021-0012.wav',
        'text': 'why should one halt on the way',
        'encoding': 'LINEAR16',
        'lang': 'en-US'
    },
    {
        'filename': 'audio/8455-210777-0068.wav',
        'text': 'your power is sufficient i said',
        'encoding': 'LINEAR16',
        'lang': 'en-US'
    }
]


def read_wav_file(filename) -> Tuple[bytes, int]:
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)

    return buffer, rate


def simulate_stream(buffer: bytes, batch_size: int = 4096):
    buffer_len = len(buffer)
    offset = 0
    while offset < buffer_len:
        end_offset = offset + batch_size
        buf = buffer[offset:end_offset]
        yield buf
        offset = end_offset


def response_stream_processor(responses):
    print('interim results: ')

    transcript = ''
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        print('{0}final: {1}'.format(
            '' if result.is_final else 'not ',
            transcript
        ))

    return transcript


def google_streaming_stt(filename: str, lang: str, encoding: str) -> str:
    buffer, rate = read_wav_file(filename)

    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[encoding],
        sample_rate_hertz=rate,
        language_code=lang
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    audio_generator = simulate_stream(buffer)  # chunk generator
    requests = (
        types.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator
    )
    responses = client.streaming_recognize(
        streaming_config, requests
    )
    # Now, put the transcription responses to use.
    return response_stream_processor(responses)


# Run tests
for t in TESTCASES:
    print('\naudio file="{0}"    expected text="{1}"'.format(
        t['filename'], t['text']
    ))
    print('google-cloud-streaming-stt: "{}"'.format(
        google_streaming_stt(
            t['filename'], t['lang'], t['encoding']
        )
    ))
