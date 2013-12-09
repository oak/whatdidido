# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from web.services.action_service import ActionService
from whatdidido.settings import DEFAULT_PAGE_SIZE
from web.models import Action, Thing
from web.actions.forms import QuickActionForm, EditActionForm


@login_required
def list(request, id=0):
    if int(id) > 0:
        paginator = Paginator(request.user.actions.filter(thing__id=id), DEFAULT_PAGE_SIZE)
    else:
        paginator = Paginator(request.user.actions.order_by('-date'), DEFAULT_PAGE_SIZE)

    page = request.GET.get('actions_page') if request.GET.get('actions_page') is not None else 1
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render_to_response('actions/list.html', {'list': list},
                              context_instance=RequestContext(request))


@login_required
def create(request):
    action_service = ActionService()
    if request.method == 'GET':
        form = QuickActionForm()
        latest_actions = action_service.get_latest_actions(request.user, DEFAULT_PAGE_SIZE)
        return render_to_response('actions/create.html', {'form': form, 'latest_actions': latest_actions, },
                                  context_instance=RequestContext(request))
    else:
        form = QuickActionForm(request.POST)
        if form.is_valid():
            action = Action()
            action.user = request.user
            try:
                thing = Thing.objects.get(name=form.cleaned_data['thing'])
            except Exception:
                thing = Thing()
                thing.name = form.cleaned_data['thing']
                thing.save()

            action.thing = thing
            action.save()
            return redirect('home')
        else:
            latest_actions = action_service.get_latest_actions(request.user, 4)
            return render_to_response('actions/create.html', {'form': form, 'latest_actions': latest_actions, },
                                      context_instance=RequestContext(request))


@login_required
def edit(request, id):
    if request.method == 'GET':
        form = EditActionForm(instance=get_object_or_404(Action, id=id))

        return render_to_response('actions/edit.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = EditActionForm(request.POST, instance=get_object_or_404(Action, id=id))
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render_to_response('actions/edit.html', {'form': form},
                                      context_instance=RequestContext(request))

@login_required
def remove(request, id):
    if request.method == 'GET':
        action = get_object_or_404(Action, id=id)
        action.delete()
        return redirect('home')

@login_required
def list_schedules(request):
    pass
