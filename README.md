# Fast not type editor
## Rationale
Assume you have a note type with a lot of card type, or with a lot of
card. Assume you edite the note type. Then, closing the editor and
saving the note type may take several minutes. This is because anki
redoes some useless computation and does not consider the fact that
some template did not change.

This add-on just ensure that this computation is done only when it is
required.

## Usage
Just install this add-on.
## Warning
For some reason unkwon right now, this add-on is not compatible with
the add-on ```Night-Mode```. More precisely, once you turn the night
mode on, you can't edit card's type anymore.

According to (Night mode's author
advice)[https://github.com/krassowski/Anki-Night-Mode/issues/60], you
may solve the problem by changing night's mode configuration,
```View → Night Mode → Choose what to style```
and deactivate night mode for CardLayout. This may solve the problem.

It won't be corrected in the near future (unless someone pay me for
it.) Which means that if you want to use Night-mode, you must disable
the current add-on. If you really need my add-on because it saves a
lot of time, do your change to note type while you are still in day
mode, and goes to night mode only once the changes are done.

## Version 2.0
None
## Internal
This add-on redefine the methods:
* aqt.clayout.CardLayout.__init__
* aqt.clayout.CardLayout.onRemove
* aqt.clayout.CardLayout.onReorder
* aqt.clayout.CardLayout.onAddCard
* aqt.clayout.CardLayout.reject
* aqt.fields.FieldDialog.reject
* aqt.fields.FieldDialog.__init__
* aqt.fields.FieldDialog._uniqueName
* anki.collection._Collection.genCards
* anki.models.ModelManager.save
* anki.models.ModelManager._updateRequired
* anki.models.ModelManager._syncTemplates
* anki.models.ModelManager.availOrds

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-fast-note-type-editor
Addon number| [802285486](https://ankiweb.net/shared/info/802285486)

I believe it should be implemented in anki's core code, but this was
refused. https://anki.tenderapp.com/discussions/ankidesktop/32549-potential-pull-request
