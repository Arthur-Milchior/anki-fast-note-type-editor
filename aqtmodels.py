from aqt.models import Models
from aqt.utils import getText
from aqt.models import AddModel

def onRename(self):
    txt = getText(_("New name:"), default=self.model['name'])
    if txt[1] and txt[0]:
        self.model['name'] = txt[0]
        self.mm.save(self.model, recomputeReq=False)
    self.updateModelsList()

Models.onRename = onRename

def modelChanged(self):
    if self.model:
        self.saveModel(recomputeReq=False)
    idx = self.form.modelsList.currentRow()
    self.model = self.models[idx]
Models.modelChanged = modelChanged

def onAdd(self):
    m = AddModel(self.mw, self).get()
    if m:
        txt = getText(_("Name:"), default=m['name'])[0]
        if txt:
            m['name'] = txt
        self.mm.ensureNameUnique(m)
        self.mm.save(m, recomputeReq=True)
        self.updateModelsList()

Models.onAdd = onAdd

def saveModel(self, recomputeReq=True):
    self.mm.save(self.model, recomputeReq=recomputeReq)
Models.saveModel = saveModel
