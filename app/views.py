from django.shortcuts import redirect, HttpResponse, render
from .models import Agent
from logic.gsmobile import phone as phone_mobile
from logic.payment import run as phone_payment
from pyVoIP.SIP import InvalidAccountInfoError
import threading


def home(request):
    return redirect('/admin')


def run(request):
    return HttpResponse('ok')


def agent(request):
    agents = Agent.objects.all()
    return render(request, 'agent.html', {'agents': agents})


def agent_detail(request, pk):
    agent_obj = Agent.objects.get(id=pk)
    if request.method == 'POST':
        if agent_obj.status == 'STOP':
            agent_obj.status = 'RUN'
            if agent_obj.cat == 'INBOUND':
                try:
                    # phone.start()
                    t = threading.Thread(target=phone_mobile.start)
                    t.start()
                except Exception as e:
                    # phone.start()
                    print(e)
                    t = threading.Thread(target=phone_mobile.start)
                    t.start()
            else:
                number = request.POST.get('number')
                try:
                    # phone.start()
                    t = threading.Thread(target=phone_payment, args=[number])
                    t.start()
                    # phone_payment.call('900969699')
                except Exception as e:
                    # phone.start()
                    print(e)
                    t = threading.Thread(target=phone_payment, args=[number])
                    t.start()
                    # phone_payment.call('900969699')

        else:
            agent_obj.status = 'STOP'
            if agent_obj.cat == 'INBOUND':
                phone_mobile.stop()
            else:
                # phone_payment.stop()
                pass

        agent_obj.save()
        return render(request, 'agent_detail.html', {'agent': agent_obj})
    return render(request, 'agent_detail.html', {'agent': agent_obj})
