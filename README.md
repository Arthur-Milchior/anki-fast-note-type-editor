# Note type editor and adding card becomes quicker
## Rationale
Assume you have a note type with a lot of card type, or with a lot of
card.
* Assume you edite the note type. Then, closing the editor and
  saving the note type may take several minutes. This is because anki
  recompute some useless data and does not consider the fact that
  some template did not change.
* Assume that you add a card, it sometime takes many seconds. A big
  part is also lost recomputing useless data.

This add-on just ensure that those computations are done only when it
is required.

## Usage
Just install this add-on.
## Version 2.0
None
## Internal
We give methods changed by this add-on.

Both methods require to change:
* anki.models.ModelManager.save


To implement the first change, we change:
* aqt.clayout.CardLayout.__init__
* aqt.clayout.CardLayout.onRemove
* aqt.clayout.CardLayout.onReorder
* aqt.clayout.CardLayout.onAddCard
* aqt.clayout.CardLayout.reject
* aqt.fields.FieldDialog.reject
* aqt.fields.FieldDialog.__init__
* aqt.fields.FieldDialog._uniqueName
* anki.collection._Collection.genCards
* anki.models.ModelManager._updateRequired
* anki.models.ModelManager._syncTemplates
* anki.models.ModelManager.availOrds

To implement the second change, we change:
* aqt.editor.Editor.saveAddModeVars
* aqt.fields.FieldDialog.reject
* aqt.models.Moleds.onRename
* aqt.models.Moleds.modelChanged
* aqt.models.Moleds.onAdd
* aqt.models.Moleds.saveModel




## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-fast-note-type-editor
Addon number| [802285486](https://ankiweb.net/shared/info/802285486)

## Notes

I believe it should be implemented in anki's core code, but this was
refused.
* https://anki.tenderapp.com/discussions/ankidesktop/32549-potential-pull-request
* https://github.com/dae/anki/pull/297#issuecomment-481120247

Some methods calling ```anki.models.ModelManager.save```  are not
modified, because they are long and rarely used; so it's better no to
touch them to avoid incompatibility with :
* anki.collection._Collection.fixIntegrity
* aqt.importing.ImportDialog.accept
* anki.storage._upgradeSchema
* anki.storage._upgradeClozeModel
