from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave
from app.models import Voice


def say(call, name):
    path = Voice.objects.get(name=name)
    f = wave.open(path, 'rb')
    frames = f.getnframes()
    data = f.readframes(frames)
    f.close()
    call.answer()
    # time.sleep(2)
    call.write_audio(data)
    stop = time.time() + frames // 8000
    print('answering..', end='')
    while time.time() <= stop and call.state == CallState.ANSWERED:
        time.sleep(0.1)


def answer(call):
    try:
        time.sleep(2)
        say(call, 'hello_welcome')
        time.sleep(1)
        say(call, 'how_can_i_help')
        time.sleep(8)
        say(call, 'check_person')
        time.sleep(2)
        say(call, 'check_name')
        time.sleep(2)
        say(call, 'info_packet')
        time.sleep(2)
        say(call, 'packet_turn_off')
        time.sleep(2)
        say(call, 'success_bye')
        time.sleep(1)
        call.hangup()

    except InvalidStateError:
        print('errrroooooooor')
        call.hangup()

    except Exception as e:
        print('new errrroooorr ', e)
        call.hangup()


def run():
    try:
        phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
                          password='a4RHeHnE', callCallback=answer)
        phone.start()
        print('waiting...')
    except:
        phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
                          password='a4RHeHnE', callCallback=answer)
        phone.start()
        print('waiting...')

# if __name__ == "__main__":
#     phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
#                       password='a4RHeHnE', callCallback=answer)
#
#     phone.start()
#     input('Press enter to disable the phone')
#     phone.stop()
