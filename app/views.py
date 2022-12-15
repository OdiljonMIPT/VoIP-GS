from django.shortcuts import redirect, HttpResponse, render
from .models import Agent
from logic.gsmobile import phone
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
            try:
                # phone.start()
                t = threading.Thread(target=phone.start)
                t.start()
            except Exception as e:
                # phone.start()
                print(e)
                t = threading.Thread(target=phone.start)
                t.start()

        else:
            agent_obj.status = 'STOP'
            phone.stop()
        agent_obj.save()
        return render(request, 'agent_detail.html', {'agent': agent_obj})
    return render(request, 'agent_detail.html', {'agent': agent_obj})
