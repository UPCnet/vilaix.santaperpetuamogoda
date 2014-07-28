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
