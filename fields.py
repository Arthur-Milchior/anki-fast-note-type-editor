from aqt.fields import FieldDialog
import copy

def _uniqueName(self, prompt, ignoreOrd=None, old=""):
    """Ask for a new name using prompt. Return it.

    Unles this name is already used elsewhere, in this case, return None and show a warning.
    If default name is given, return None."""
    txt = getOnlyText(prompt, default=old)
    if not txt:
        return
    for f in self.model['flds']:
        if ignoreOrd is not None and f['ord'] == ignoreOrd:
            if f['name'] == txt:
                return
            continue
        if f['name'] == txt:
            showWarning(_("That field name is already used."))
            return
    return txt
FieldDialog._uniqueName = _uniqueName

oldInit = FieldDialog.__init__
def init(self, *args,**kwargs):
    oldInit(self, *args,**kwargs):
    self.originalModel = copy.deepcopy(self.model)
FieldDialog.__init__ = init

def reject(self):
    print("Calling field's new reject")
    self.saveField()
    if self.oldSortField != self.model['sortf']:
        self.mw.progress.start()
        self.mw.col.updateFieldCache(self.mm.nids(self.model))
        self.mw.progress.finish()
    self.mm.save(self.model, templates = True, oldModel = self.originalModel)
    self.mw.reset()
    QDialog.reject(self)
FieldDialog.reject = reject
