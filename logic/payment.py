from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave


def answer(call):
    try:
        f = wave.open('../hello_welcome_uz-8bit.wav', 'rb')
        # f = wave.open('/usr/share/freeswitch/sounds/en/us/callie/aziza/hello_welcome_uz.wav', 'rb')
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()
        call.answer()
        # print(call.RTPClients)
        # time.sleep(5)
        call.write_audio(data)
        stop = time.time() + 8
        print('answering..', end='')
        while time.time() <= stop and call.state == CallState.ANSWERED:
            time.sleep(0.1)
            # print('answering.. ', end='')

        # print()
        call.hangup()
    except InvalidStateError:
        print('errrroooooooor')
    except Exception as e:
        print('new errrroooorr ', e)
        call.hangup()


def run(number):
    phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
                      password='a4RHeHnE', callCallback=answer)
    phone.start()
    print('calling...')
    phone.call(number)
    # call.hangup()
    phone.stop()

# if __name__ == "__main__":
#     phone = VoIPPhone(server='217.29.116.216', port=5060, username='781133702',
#                       password='a4RHeHnE', callCallback=answer)
#
#     phone.start()
#     input('Press enter to disable the phone')
#     phone.stop()
