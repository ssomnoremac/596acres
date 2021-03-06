from django.conf import settings
from django.core.mail import mail_managers
from django.template.loader import render_to_string

from mail import mail_lot_organizers, mail_lot_watchers
from models import Note, Organizer, Picture

url_suffixes = {
    Note: '#notes',
    Picture: '#pictures',
    Organizer: '#organizers',
}

def notify_managers(obj):
    obj_model_name = obj.__class__.__name__.lower()
    subject_template_name = 'organize/notifications/managers_new_%s_subject.txt' % obj_model_name
    text_template_name = 'organize/notifications/managers_new_%s_text.txt' % obj_model_name

    subject = render_to_string(subject_template_name).strip()
    message = render_to_string(text_template_name, {
        'obj': obj,
        'BASE_URL': settings.BASE_URL,
    })
    mail_managers(subject, message)

def notify_organizers_and_watchers(obj):
    """
    Send Organizers and Watchers of a given lot updates.
    """
    lot = obj.lot
    if not lot: return

    # don't notify of new organizers when a group already has access
    if lot.group_has_access and isinstance(obj, Organizer): return

    message = _get_object_message(obj)
    kwargs = {}
    try:
        kwargs['excluded_emails'] = [obj.email]
    except Exception:
        kwargs['excluded_emails'] = []
    kwargs['is_note'] = isinstance(obj, Note)
    kwargs['url_suffix'] = url_suffixes[obj.__class__]

    mail_lot_watchers(lot, 'Watched lot updated!', message, **kwargs)
    mail_lot_organizers(lot, 'Organized lot updated!', message, **kwargs)

def _get_object_message(o):
    """
    Get a message specific to the given object.
    """
    # TODO push to templates?
    if isinstance(o, Note):
        return "A note was added by %s:\n\"%s\" " % (o.noter, o.text)
    elif isinstance(o, Picture):
        return 'A new picture was added with the description "%s".' % o.description
    elif isinstance(o, Organizer):
        return "A new organizer named %s was added. " % o.name
    return ""
