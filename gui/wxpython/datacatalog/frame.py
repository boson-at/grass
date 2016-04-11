"""
@package datacatalog::frame

@brief Data catalog frame class

Classes:
 - datacatalog::DataCatalogFrame

(C) 2014-2016 by Tereza Fiedlerova, and the GRASS Development Team

This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

@author Tereza Fiedlerova (original author)
@author Martin Landa <landa.martin gmail.com> (various improvements)
"""

import os
import sys

import wx

from core.utils import _
from core.globalvar import ICONDIR
from datacatalog.tree import DataCatalogTree
from datacatalog.toolbars import DataCatalogToolbar

class DataCatalogFrame(wx.Frame):
    """Frame for testing purposes only."""
    def __init__(self, parent, giface=None):
        wx.Frame.__init__(self, parent=parent,
                          title=_('GRASS GIS Data Catalog'))
        self.SetName("DataCatalog")
        self.SetIcon(wx.Icon(os.path.join(ICONDIR, 'grass.ico'), wx.BITMAP_TYPE_ICO))

        self._giface = giface
        self.panel = wx.Panel(self)

        self.toolbar = DataCatalogToolbar(parent = self)
        # workaround for http://trac.wxwidgets.org/ticket/13888
        if sys.platform != 'darwin':
            self.SetToolBar(self.toolbar)

        # tree
        self.tree = DataCatalogTree(parent=self.panel, giface=self._giface)
        self.tree.InitTreeItems()
        self.tree.ExpandCurrentMapset()
        
        # buttons
        self.btnClose = wx.Button(parent=self.panel, id=wx.ID_CLOSE)
        self.btnClose.SetToolTipString(_("Close GRASS GIS Data Catalog"))
        self.btnClose.SetDefault()

        # events
        self.btnClose.Bind(wx.EVT_BUTTON, self.OnCloseWindow)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self._layout()

    def _layout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, proportion=1, flag=wx.EXPAND)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.AddStretchSpacer()
        btnSizer.Add(self.btnClose)

        sizer.Add(item=btnSizer, proportion=0,
                  flag=wx.ALL | wx.ALIGN_RIGHT | wx.EXPAND,
                  border=5)

        self.panel.SetSizer(sizer)
        sizer.Fit(self.panel)

        self.SetMinSize((400, 500))

    def OnCloseWindow(self, event):
        """Cancel button pressed"""
        if not isinstance(event, wx.CloseEvent):
            self.Destroy()

        event.Skip()

    def OnReloadTree(self, event):
        """Reload whole tree"""
        self.tree.ReloadTreeItems()
        self.tree.ExpandCurrentMapset()

    def OnReloadCurrentMapset(self, event):
        """Reload current mapset tree only"""
        self.tree.ReloadCurrentMapset()
