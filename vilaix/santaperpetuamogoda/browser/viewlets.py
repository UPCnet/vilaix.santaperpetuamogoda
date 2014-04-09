# -*- coding: utf-8 -*-
import re
from five import grok
from cgi import escape
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from plone.memoize.view import memoize_contextless

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import PersonalBarViewlet, GlobalSectionsViewlet, PathBarViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet, TitleViewlet, ManagePortletsFallbackViewlet
from plone.app.layout.viewlets.interfaces import IHtmlHead, IPortalTop, IPortalHeader, IBelowContent
from plone.app.layout.viewlets.interfaces import IPortalFooter, IAboveContentTitle, IAboveContentBody
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.ATContentTypes.interface.news import IATNewsItem
from genweb.core.adapters import IImportant

from genweb.core.interfaces import IHomePage
from genweb.core.utils import genweb_config, havePermissionAtRoot, pref_lang

from genweb.theme.browser.interfaces import IGenwebTheme
from genweb.theme.browser.viewlets import gwManagePortletsFallbackViewlet
from vilaix.santaperpetuamogoda.browser.interfaces import ISantaPerpetuaTheme

from plone.app.collection.interfaces import ICollection
from genweb.core import HAS_CAS
from zope.security import checkPermission

import random
from genweb.core import GenwebMessageFactory as _


grok.context(Interface)


class viewletBase(grok.Viewlet):
    grok.baseclass()

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def genweb_config(self):
        return genweb_config()

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.portal(), 'portal_languages')
        return lt.getPreferredLanguage()


class gwHeader(viewletBase):
    grok.name('genweb.header')
    grok.template('header')
    grok.viewletmanager(IPortalHeader)
    grok.layer(ISantaPerpetuaTheme)

    def get_image_class(self):
        if self.genweb_config().treu_menu_horitzontal:
            # Is a L2 type
            return 'l2-image'
        else:
            return 'l3-image'

    def show_login(self):
        isAnon = getMultiAdapter((self.context, self.request), name='plone_portal_state').anonymous()
        return not self.genweb_config().amaga_identificacio and isAnon

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.portal(), 'portal_languages')
        lang = lt.getDefaultLanguage()

        if lang == 'ca':
            pref_lang = 'Català'
        elif lang == 'es':
            pref_lang = 'Español'
        elif lang == 'en':
            pref_lang = 'English'

        return pref_lang

    def languages(self):
        portal = getSite()
        pl = getToolByName(portal, 'portal_languages')     
        return pl.supported_langs
    
    def getDadesLanguages(self):
        portal = getSite()
        urltool = portal.absolute_url()
        pl = getToolByName(portal, 'portal_languages')     
        langs_supported = pl.getSupportedLanguages()
        pref_lang = pl.getPreferredLanguage()
        default_lang = pl.getDefaultLanguage()
        dades = []
        languages = [{'lang': 'ca', 'valor': 'Català'},{'lang': 'es', 'valor': 'Español'},{'lang': 'en', 'valor': 'English'}]

        for i in langs_supported:
            if i in default_lang:
                for x in languages:
                    if x['lang'] in i:
                        literal=x['valor']
                dades.append(dict(url="%s?set_language=%s" % (urltool, default_lang),
                                  lang=default_lang,
                                  literal=literal,
                                  google_translated=False
                                  )
                            )
            else:
                for x in languages:
                    if x['lang'] in i:
                        literal=x['valor']
                dades.append(dict(url="http://translate.google.com/translate?hl=%s&sl=%s&tl=%s&u=%s" % (default_lang, default_lang, i, urltool),
                                  lang = i,
                                  literal=literal,
                                  google_translated=True
                                  )
                            )

        return dades

    # def show_directory(self):
    #     return self.genweb_config().directori_upc

    # def get_image_capsalera(self):
    #     #Obté totes les imatges de la carpeta imatges-capcalera i fa un random retornant una cada cop
    #     urltool = getToolByName(self.context, 'portal_url')
    #     portal_catalog = getToolByName(self.context, 'portal_catalog')
    #     path = urltool.getPortalPath() + '/imatges-capcalera'        
    #     resultats = []
    #     #Imatge capcalera per defecte
    #     style = 'background-image: url("/++vilaix++static/images/capcalera.jpg")'
       
    #     imatges = self.context.portal_catalog.searchResults(portal_type='Image',
    #                                                         path=path)
    #     if imatges.actual_result_count != 0:
    #         imatge = random.choice(imatges)
    #         style = 'background-image: url(' + imatge.getPath() +')'       
        
    #     return style



