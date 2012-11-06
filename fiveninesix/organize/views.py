import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.views.generic.edit import DeleteView

from recaptcha_works.decorators import fix_recaptcha_remote_ip

from forms import OrganizerForm, WatcherForm, NoteForm, PictureForm
from lots.models import Lot
from lots.util import get_nearby
from models import Organizer, Watcher

def details(request, bbl=None):
    organizers = Organizer.objects.filter(lot__bbl=bbl)

    details = []
    for organizer in organizers:
        details.append({
            'name': organizer.name,
            'phone': organizer.phone,
            'email': organizer.email,
            'url': organizer.url,
            'type': organizer.type.name,
            'lots': [organizer.lot.bbl],
        })
    return HttpResponse(json.dumps(details), mimetype='application/json')

def details_tab(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)

    return render_to_response('organize/tab.html', {
        'organizers': lot.organizer_set.all()
    }, context_instance=RequestContext(request))


@fix_recaptcha_remote_ip
def add_organizer(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = OrganizerForm(request.POST, user=request.user)
        if form.is_valid():
            organizer = form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_organizer.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_watcher(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = WatcherForm(request.POST, user=request.user)
        if form.is_valid():
            watcher = form.save()
            return redirect('organize.views.add_watcher_success', bbl=bbl,
                            email_hash=watcher.email_hash[:10])
    else:
        form = WatcherForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_watcher.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

def add_watcher_success(request, bbl=None, email_hash=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    try:
        watcher = Watcher.objects.filter(email_hash__istartswith=email_hash)[0]
    except Exception:
        raise Http404

    return render_to_response('organize/add_watcher_success.html', {
        'lot': lot,
        'nearby_lots': get_nearby(lot),
        'watcher': watcher,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_note(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = NoteForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_note.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def add_picture(request, bbl=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    if request.method == 'POST':    
        form = PictureForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = PictureForm(initial={
            'lot': lot,
        }, user=request.user)

    template = 'organize/add_picture.html'

    return render_to_response(template, {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def edit_organizer(request, bbl=None, id=None):
    lot = get_object_or_404(Lot, bbl=bbl)
    organizer = get_object_or_404(Organizer, id=id)

    if request.method == 'POST':    
        form = OrganizerForm(request.POST, instance=organizer)
        if form.is_valid():
            organizer = form.save()
            return redirect('lots.views.details', bbl=bbl)
    else:
        form = OrganizerForm(instance=organizer)

    return render_to_response('organize/edit_organizer.html', {
        'form': form,
        'lot': lot,
    }, context_instance=RequestContext(request))

def delete_organizer(request, bbl=None, id=None):
    organizer = get_object_or_404(Organizer, id=id)
    organizer.delete()

    return redirect('lots.views.details', bbl=bbl)

def edit_participant(request, hash=None):
    organizers = Organizer.objects.filter(email_hash__istartswith=hash).order_by('lot__bbl')
    watchers = Watcher.objects.filter(email_hash__istartswith=hash).order_by('lot__bbl')
    email = None
    if watchers:
        email = watchers[0].email

    return render_to_response('organize/edit_participant.html', {
        'email': email,
        'hash': hash,
        'organizers': organizers,
        'watchers': watchers,
    }, context_instance=RequestContext(request))

def delete_participant_organizer(request, id=None, hash=None):
    organizer = get_object_or_404(Organizer, id=id, email_hash__istartswith=hash)
    organizer.delete()
    return redirect('organize.views.edit_participant', hash=hash)

def delete_participant_watcher(request, id=None, hash=None):
    watcher = get_object_or_404(Watcher, id=id, email_hash__istartswith=hash)
    watcher.delete()
    return redirect('organize.views.edit_participant', hash=hash)

class DeleteParticipantView(DeleteView):

    def get_context_data(self, **kwargs):
        context = super(DeleteParticipantView, self).get_context_data(**kwargs)
        context['lot'] = self.object.lot
        context['next_url'] = self.request.GET.get('next_url')
        return context

    def get_success_url(self):
        return self.request.POST.get('next_url', self.object.lot.get_absolute_url())
