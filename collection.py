from anki.collection import _Collection
from anki.utils import ids2str, maxID, intTime
from .debug import debugFun

@debugFun
def genCards(self, nids, posToRecompute=None):
        """Ids of cards needed to be removed.

        Generate missing cards of a note with id in nids and with ord in posToRecompute.
        """
        # build map of (nid,ord) so we don't create dupes
        snids = ids2str(nids)
        have = {}#Associated to each nid a dictionnary from card's order to card id.
        dids = {}#Associate to each nid the only deck id containing its cards. Or None if there are multiple decks
        dues = {}#Associate to each nid the due value of the last card seen.
        for id, nid, ord, did, due, odue, odid in self.db.execute(
            "select id, nid, ord, did, due, odue, odid from cards where nid in "+snids):
            # existing cards
            if nid not in have:
                have[nid] = {}
            have[nid][ord] = id
            # if in a filtered deck, add new cards to original deck
            if odid != 0:
                did = odid
            # and their dids
            if nid in dids:
                if dids[nid] and dids[nid] != did:
                    # cards are in two or more different decks; revert to
                    # model default
                    dids[nid] = None
            else:
                # first card or multiple cards in same deck
                dids[nid] = did
            # save due
            if odid != 0:
                due = odue
            if nid not in dues:
                dues[nid] = due
        # build cards for each note
        data = []#Tuples for cards to create. Each tuple is newCid, nid, did, ord, now, usn, due
        ts = maxID(self.db)
        now = intTime()
        rem = []#cards to remove
        usn = self.usn()
        for nid, mid, flds in self.db.execute(
            "select id, mid, flds from notes where id in "+snids):
            model = self.models.get(mid)
            avail = self.models.availOrds(model, flds, posToRecompute)
            did = dids.get(nid) or model['did']
            due = dues.get(nid)
            # add any missing cards
            for t in self._tmplsFromOrds(model, avail):
                doHave = nid in have and t['ord'] in have[nid]
                if not doHave:
                    # check deck is not a cram deck
                    did = t['did'] or did
                    if self.decks.isDyn(did):
                        did = 1
                    # if the deck doesn't exist, use default instead
                    did = self.decks.get(did)['id']
                    # use sibling due# if there is one, else use a new id
                    if due is None:
                        due = self.nextID("pos")
                    data.append((ts, nid, did, t['ord'],
                                 now, usn, due))
                    ts += 1
            # note any cards that need removing
            if nid in have:
                for ord, id in list(have[nid].items()):
                    if ((posToRecompute is None or ord in posToRecompute) and
                        ord not in avail):
                        rem.append(id)
        # bulk update
        self.db.executemany("""
insert into cards values (?,?,?,?,?,?,0,0,?,0,0,0,0,0,0,0,0,"")""",
                            data)
        return rem

_Collection.genCards = genCards
