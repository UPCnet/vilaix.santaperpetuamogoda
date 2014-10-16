from five import grok
from zope.interface import Interface
from vilaix.santaperpetuamogoda.interfaces import ISantaPerpetuaLayer
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer


class MigrarTramitsView(grok.View):
    """
    """

    grok.name('MigrarTramits')
    grok.context(Interface)
    grok.template('migrartramits')
    grok.layer(ISantaPerpetuaLayer)
    grok.require('cmf.AddPortalContent')

    def MigrarTramits(self):
        """ Migra els tramits creats com a Item a Container
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        workflowTool = getToolByName(self, "portal_workflow")
        tramits = []
        tramits = portal_catalog.searchResults(portal_type='Tramit')

        results = []
        for item in tramits:
            obj = item.getObject()
            pare = obj.aq_parent
            data = {'id': obj.id,
                    'title': obj.title,
                    'description': obj.description,
                    'qui': obj.qui,
                    'documentacio': obj.documentacio,
                    'quan': obj.quan,
                    'quin': obj.quin,
                    'tipus_silenci': obj.tipus_silenci,
                    'preu': obj.preu,
                    'pagament': obj.pagament,
                    'canals': obj.canals,
                    'responsable': obj.responsable,
                    'inici': obj.inici,
                    'fitxer_inici': obj.fitxer_inici}
            status = workflowTool.getInfoFor(obj, "review_state")
            pare.manage_delObjects(obj.id)
            new_tramit = createContentInContainer(
                pare,
                'Tramit',
                title=data['title'],
                description=data['description'],
                qui=data['qui'],
                documentacio=data['documentacio'],
                quan=data['quan'],
                quin=data['quin'],
                tipus_silenci=data['tipus_silenci'],
                preu=data['preu'],
                pagament=data['pagament'],
                canals=data['canals'],
                responsable=data['responsable'],
                inici=data['inici'],
                fitxer_inici=data['fitxer_inici'],
                checkConstraints=False)
            if status != 'esborrany':
                workflowTool.doActionFor(new_tramit, "publish")
            new_tramit.reindexObject()

            results.append(data['title'])

        return results


class MigrarEquipamentsView(grok.View):
    """
    """

    grok.name('MigrarEquipaments')
    grok.context(Interface)
    grok.template('migrarequipaments')
    grok.layer(ISantaPerpetuaLayer)
    grok.require('cmf.AddPortalContent')

    def MigrarEquipaments(self):
        """ Migra els equipaments creats com a factory new item com a Equipament
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        workflowTool = getToolByName(self, "portal_workflow")
        equipaments = []
        equipaments = portal_catalog.searchResults(portal_type='Equipament')

        results = []
        for item in equipaments:
            obj = item.getObject()
            pare = obj.aq_parent

            data = {'id': obj.id,
                    'title': obj.title,
                    'description': obj.description,
                    'image': obj.image,
                    'tipus': obj.tipus,
                    'adreca_contacte': obj.adreca_contacte,
                    'codi_postal': obj.codi_postal,
                    'poblacio': obj.poblacio,
                    'geolocalitzacio': obj.geolocalitzacio,
                    'telefon': obj.telefon,
                    'adreca_correu': obj.adreca_correu,
                    'horari': obj.horari,
                    'mes_informacio': obj.mes_informacio,
                    'ubicacio': obj.ubicacio,
                    'ubicacio_iframe': obj.ubicacio_iframe,
                    'etiquetes': obj.subject}
            status = workflowTool.getInfoFor(obj, "review_state")
            pare.manage_delObjects(obj.id)
            new_equipament = createContentInContainer(
                pare,
                'Equipament',
                title=data['title'],
                description=data['description'],
                image=data['image'],
                tipus=data['tipus'],
                adreca_contacte=data['adreca_contacte'],
                codi_postal=data['codi_postal'],
                poblacio=data['poblacio'],
                geolocalitzacio=data['geolocalitzacio'],
                telefon=data['telefon'],
                adreca_correu=data['adreca_correu'],
                horari=data['horari'],
                mes_informacio=data['mes_informacio'],
                ubicacio=data['ubicacio'],
                ubicacio_iframe=data['ubicacio_iframe'],
                checkConstraints=False)
            if status != 'esborrany':
                workflowTool.doActionFor(new_equipament, "publish")
            new_equipament.setSubject(data['etiquetes'])
            new_equipament.reindexObject()

            results.append(data['title'])

        return results
