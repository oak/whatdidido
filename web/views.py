# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login as lin, logout as lout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from web.forms import LoginForm
from django.forms.util import ErrorList
from web.models import Action
from web.actions.forms import ActionForm
from django.utils.translation import ugettext_lazy as _
from web.services.action_service import ActionService


@login_required
def home(request):
    form = ActionForm()
    action_service = ActionService()

    latest_actions = action_service.get_latest_actions(request.user, 4)

    return render_to_response('index.html', { 'form': form, 'latest_actions': latest_actions, },
                          context_instance=RequestContext(request))


@login_required
def create_new_action(request):
    if request.method == 'GET':
        form = ActionForm()
        return render_to_response('actions/create.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ActionForm(request.POST)
        if form.is_valid():
            action = Action()
            action.user = request.user
            action.thing = form.thing
            action.save()
            return redirect('home')
        else:
            return render_to_response('actions/create.html', {'form': form},
                                      context_instance=RequestContext(request))


@login_required
def create_new_action_with_new_thing(request):
    if request.method == 'GET':
        form = ActionForm()
        return render_to_response('actions/create.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ActionForm(request.POST)
        if form.is_valid():
            action = Action()
            action.user = request.user
            action.thing = form.thing
            action.save()
            return redirect('home')
        else:
            return render_to_response('actions/create.html', {'form': form},
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
