from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
import pyVoIP

pyVoIP.DEBUG = True


def answer(call):
    print('I am here')
    try:
        f = wave.open('hello_welcome_uz-8bit.wav', 'rb')
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        # call.answer()
        call.write_audio(data)  # This writes the audio data to the transmit buffer, this must be bytes.

        stop = time.time() + (
                frames / 8000)  # frames/8000 is the length of the audio in seconds. 8000 is the hertz of PCMU.
        print('I am here')
        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)
            print('I am waiting')
        call.hangup()
    except InvalidStateError:
        print(InvalidStateError)
    except Exception as e:
        print(e)
        call.hangup()


if __name__ == "__main__":
    phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
                      password='a4RHeHnE', callCallback=answer)

    phone.start()
    # call = phone.call('909773053')
    call = phone.call('900969699')
    # print("Dailing...", end="")
    time.sleep(10)
    # print('\ngo')
    call.state = CallState.ANSWERED
    if call.state == CallState.ANSWERED:
        answer(call)
        print('all is good')
        # call.hangup()
    input('Press enter to disable the phone')
    phone.stop()
"""
/usr/share/freeswitch/sounds/en/us/callie/aziza/hello_welcome_uz.wav
"test2_sip.py" 42L, 1278C                                                                                                           10,2-9        Top
"""
