from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

class FNSAdminMenu(CMSAttachMenu):
    name = _("fns_admin menu")

    def get_nodes(self, request):
        nodes = []

        nodes.append(NavigationNode(_('Backend'), 
                                    reverse('admin:index'), 1))

        nodes.append(NavigationNode(_('Email Organizers and Watchers'),
                                    '/fnsadmin/organizers/mail/', 1))

        nodes.append(NavigationNode(_('Add News'),
                                    '/admin/cmsplugin_blog/entry/add/', 2))

        return nodes

menu_pool.register_menu(FNSAdminMenu)

