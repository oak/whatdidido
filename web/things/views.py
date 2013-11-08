# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from whatdidido.settings import DEFAULT_PAGE_SIZE
from web.models import Thing
from web.things.forms import ThingForm

@login_required
def list(request):
    paginator = Paginator(request.user.things.all(), DEFAULT_PAGE_SIZE)

    page = request.GET.get('things_page') if request.GET.get('things_page') is not None else 1
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        list = paginator.page(paginator.num_pages)

    return render_to_response('things/list.html', {'list': list},
                              context_instance=RequestContext(request))


@login_required
def create(request):
    if request.method == 'GET':
        form = ThingForm()
        return render_to_response('things/create.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ThingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thing-list')
        else:
            return render_to_response('things/create.html', {'form': form},
                                      context_instance=RequestContext(request))


@login_required
def edit(request, id):
    if request.method == 'GET':
        form = ThingForm(instance=get_object_or_404(Thing, id=id))

        return render_to_response('things/edit.html', {'form': form},
                                  context_instance=RequestContext(request))
    else:
        form = ThingForm(request.POST, instance=get_object_or_404(Thing, id=id))
        if form.is_valid():
            form.save()
            return redirect('thing-list')
        else:
            return render_to_response('things/edit.html', {'form': form},
                                      context_instance=RequestContext(request))
