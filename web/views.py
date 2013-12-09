# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as lin, logout as lout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from web.forms import LoginForm
from django.forms.util import ErrorList
from web.models import Action
from web.actions.forms import QuickActionForm
from django.utils.translation import ugettext_lazy as _
from web.services.action_service import ActionService
from whatdidido.settings import DEFAULT_PAGE_SIZE


@login_required
def home(request):
    form = QuickActionForm()
    action_service = ActionService()

    latest_actions = action_service.get_latest_actions(request.user, DEFAULT_PAGE_SIZE)
    scheduled_actions = action_service.get_scheduled_actions(request.user, DEFAULT_PAGE_SIZE)

    return render_to_response('index.html', { 'form': form, 'latest_actions': latest_actions, 'scheduled_actions': scheduled_actions},
                          context_instance=RequestContext(request))


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('login.html', {'form': form}, RequestContext(request=request))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    lin(request, user)
                    if 'next' in request.GET:
                        return redirect(request.GET['next'])
                    else:
                        return redirect('home')
                else:
                    form._errors["login"] = ErrorList(u'Account disabled')
                    return render_to_response('login.html', {'form': form})
            else:
                form._errors["login"] = ErrorList(u'Invalid login')

        # Return an 'invalid login' error message.
        return render_to_response('login.html', {'form': form}, RequestContext(request=request))


def logout(request):
    lout(request)

    return redirect('home')

@login_required
def reset_schedule(request):
    asvc = ActionService()
    asvc.reset_next_schedules(request.user)

    return redirect('home')