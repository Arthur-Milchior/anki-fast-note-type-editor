from anki.models import ModelManager
from anki.utils import intTime, splitFields
from anki.consts import *
from anki.hooks import runHook
from .debug import debugFun

@debugFun
def save(self, m=None, templates=False, oldModel=None, newIdxToOld = None):
        """
        * Mark m modified if provided.
        * Schedule registry flush.
        * Calls hook newModel

        Keyword arguments:
        m -- A Model
        templates -- whether to check for cards not generated in this model
        oldModel -- a previous version of the model, to which to compare
        newIdxToOld -- a list whose i-th element state which is the
        new position of the i-th template of the old model.
        """
        # print(f"""oldModel is: «
# {oldModel}
# », newIdxToOld is «
# {newIdxToOld}
# »""")
        if newIdxToOld is None:
            newIdxToOld = {i:None for i in range(len(m['tmpls']))}
        else:
                assert isinstance(newIdxToOld,list)
        posToRecompute = {idx
                          for idx, tmpl in enumerate(m['tmpls'])
                          if (newIdxToOld[idx] is None or
                              tmpl['qfmt']!=oldModel['tmpls'][newIdxToOld[idx]]['qfmt'])
        }
        if m and m['id']:
            m['mod'] = intTime()
            m['usn'] = self.col.usn()
            self._updateRequired(m, oldModel, posToRecompute, newIdxToOld)
            if templates:
                self._syncTemplates(m, posToRecompute)
        self.changed = True
        runHook("newModel")

ModelManager.save = save
@debugFun
def _updateRequired(self, m, oldModel = None, posToRecompute = None, newIdxToOld = None):
        """Entirely recompute the model's req value"""
        if m['type'] == MODEL_CLOZE:
            # nothing to do
            return
        req = []
        flds = [f['name'] for f in m['flds']]
        for idx,t in enumerate(m['tmpls']):
            if oldModel and idx not in posToRecompute :
                oldIdx = newIdxToOld[idx]#Assumed not None,
                # otherwise idx would be in posToRecompute
                req.append(oldModel['req'][oldIdx])
                continue
            else:
                ret = self._reqForTemplate(m, flds, t)
                req.append((t['ord'], ret[0], ret[1]))
        m['req'] = req
ModelManager._updateRequired = _updateRequired

@debugFun
def _syncTemplates(self, m, posToRecompute = None):
    """Generate all cards not yet generated from, whose note's model is m"""
    rem = self.col.genCards(self.nids(m), posToRecompute)
ModelManager._syncTemplates = _syncTemplates

@debugFun
def availOrds(self, m, flds, posToRecompute = None):
        """Given a joined field string, return template ordinals which should be
        seen. See ../documentation/templates_generation_rules.md for
        the detail

        """
        if m['type'] == MODEL_CLOZE:
            return self._availClozeOrds(m, flds)
        fields = {}
        for c, f in enumerate(splitFields(flds)):
            fields[c] = f.strip()
        avail = []#List of ord cards which would be generated
        for ord, type, req in m['req']:
            if posToRecompute and ord not in posToRecompute:
                continue
            # unsatisfiable template
            if type == "none":
                continue
            # AND requirement?
            elif type == "all":
                ok = True
                for idx in req:
                    if not fields[idx]:
                        # missing and was required
                        ok = False
                        break
                if not ok:
                    continue
            # OR requirement?
            elif type == "any":
                ok = False
                for idx in req:
                    if fields[idx]:
                        ok = True
                        break
                if not ok:
                    continue
            avail.append(ord)
        return avail

ModelManager.availOrds = availOrds
