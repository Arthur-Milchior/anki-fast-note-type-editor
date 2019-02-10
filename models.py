from anki.models import ModelManager
from anki.utils import intTime, splitFields
from anki.consts import *
from anki.hooks import runHook
from .debug import debugFun

@debugFun
def getPosToRecompute(m, forCards, oldModel = None, newIdxMeta=None):
        print(f"Computing getPosToRecompute for "+("cards" if forCards else "req")+ f". newIdxMeta is {newIdxMeta}")
        if newIdxMeta is None:
                posToRecompute = list(range(len(m['tmpls'])))
        posToRecompute = []
        for idx, tmpl in enumerate(m['tmpls']):
                oldIdx = newIdxMeta[idx]["old idx"]
                if oldIdx is None:
                        posToRecompute.append(idx)
                else:
                        oldTmpl =oldModel['tmpls'][oldIdx]
                        if ((newIdxMeta[idx]["is new"] and forCards) or
                            tmpl['qfmt']!=oldTmpl['qfmt']):
                                posToRecompute.append(idx)
        print(f"posToRecompute is {posToRecompute}")
        return posToRecompute

@debugFun
def save(self, m=None, templates=False, oldModel=None, newIdxMeta = None):
        """
        * Mark m modified if provided.
        * Schedule registry flush.
        * Calls hook newModel

        Keyword arguments:
        m -- A Model
        templates -- whether to check for cards not generated in this model
        oldModel -- a previous version of the model, to which to compare
        newIdxMeta -- a list whose i-th element state which is the
        new position of the i-th template of the old model and whether the template is new.
        """
        # print(f"""oldModel is: «
# {oldModel}
# », newIdxMeta is «
# {newIdxMeta}
# »""")
        if m and m['id']:
            if newIdxMeta is None:
                    print("All indexes are new")
                    newIdxMeta = [{"is new": True,
                                   "old idx":None}]*len(m['tmpls'])
            else:
                    assert isinstance(newIdxMeta,list)
            m['mod'] = intTime()
            m['usn'] = self.col.usn()
            self._updateRequired(m, oldModel, newIdxMeta)
            if templates:
                self._syncTemplates(m, getPosToRecompute(m, True, oldModel, newIdxMeta))
        self.changed = True
        runHook("newModel")

ModelManager.save = save
@debugFun
def _updateRequired(self, m, oldModel = None, newIdxMeta = None):
        """Entirely recompute the model's req value"""
        if m['type'] == MODEL_CLOZE:
            # nothing to do
            return
        posToRecompute = getPosToRecompute(m, False, oldModel, newIdxMeta)
        req = []
        flds = [f['name'] for f in m['flds']]
        for idx,t in enumerate(m['tmpls']):
            if oldModel is not None and idx not in posToRecompute :
                #print(f"Old model is not None and idx {idx} not is posToRecompute")
                oldIdx = newIdxMeta[idx]["old idx"]# Assumed not None,
                # otherwise idx would be in posToRecompute
                ord, type, req_ = oldModel['req'][oldIdx]
                tup = (idx, type, req_)
                req.append(tup)
                #print(f"Appending to req «{tup}»")
                continue
            else:
                # if oldModel is  None:
                #         #print("oldModel is None")
                # else:
                #         #print(f"idx {idx} is posToRecompute")
                ret = self._reqForTemplate(m, flds, t)
                tup = (idx, ret[0], ret[1])
                req.append(tup)
                #print(f"Appending to req «{tup}»")
        m['req'] = req
ModelManager._updateRequired = _updateRequired

@debugFun
def _syncTemplates(self, m, posToRecompute = None):
    """Generate all cards not yet generated from, whose note's model is m"""
    rem = self.col.genCards(self.nids(m), posToRecompute)
ModelManager._syncTemplates = _syncTemplates

@debugFun
def availOrds(self, m, flds, posToRecompute = None):
        #oldModel = None, newIdxMeta = None
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
        for tup in m['req']:
            # print(f"""tup is {tup}.
            # m['req'] is {m['req']}
            # m is {m}""")
            ord, type, req = tup
            if posToRecompute is not None and ord not in posToRecompute:
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
