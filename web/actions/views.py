# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from whatdidido.settings import DEFAULT_PAGE_SIZE
from web.models import Action, Thing
from web.actions.forms import ActionForm

@login_required
def list(request):
    paginator = Paginator(request.user.actions.all(), DEFAULT_PAGE_SIZE)

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
    if request.method == 'GET':
        form = ActionForm()
        return render_to_response('actions/create.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ActionForm(request.POST)
        if form.is_valid():
            action = Action()
            action.user = request.user
            try:
                thing = Thing.objects.get(name=form.cleaned_data['thing'])
            except:
                thing = Thing()
                thing.name = form.cleaned_data['thing']

            thing.usage_count += 1
            thing.save()

            action.thing = thing
            action.save()
            return redirect('home')
        else:
            return render_to_response('actions/create.html', {'form': form},
                                      context_instance=RequestContext(request))


@login_required
def edit(request, id):
    if request.method == 'GET':
        form = ActionForm(instance=get_object_or_404(Action, id=id))

        return render_to_response('actions/edit.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ActionForm(request.POST, instance=get_object_or_404(Action, id=id))
        if form.is_valid():
            form.save()
            return redirect('action-list')
        else:
            return render_to_response('actions/edit.html', {'form': form},
                                      context_instance=RequestContext(request))
