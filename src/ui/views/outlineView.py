#!/usr/bin/env python
#--!-- coding: utf8 --!--
 



from qt import *
from enums import *
from functions import *
from ui.views.outlineDelegates import *
from ui.views.dndView import *
from ui.views.outlineBasics import *

class outlineView(QTreeView, dndView, outlineBasics):
    
    def __init__(self, parent=None, modelPersos=None, modelLabels=None, modelStatus=None):
        QTreeView.__init__(self, parent)
        dndView.__init__(self)
        outlineBasics.__init__(self, parent)
        
        self.modelPersos = modelPersos
        self.modelLabels = modelLabels
        self.modelStatus = modelStatus
        
        self.header().setStretchLastSection(False)
        
    def setModelPersos(self, model):
        # This is used by outlinePersoDelegate to select character
        self.modelPersos = model
        
    def setModelLabels(self, model):
        # This is used by outlineLabelDelegate to display labels
        self.modelLabels = model
        
    def setModelStatus(self, model):
        # This is used by outlineStatusDelegate to display statuses
        self.modelStatus = model
        
    def setModel(self, model):
        QTreeView.setModel(self, model)
        
        # Setting delegates
        self.outlineTitleDelegate = outlineTitleDelegate()
        self.outlineTitleDelegate.setView(self)
        self.setItemDelegateForColumn(Outline.title.value, self.outlineTitleDelegate)
        self.outlinePersoDelegate = outlinePersoDelegate(self.modelPersos)
        self.setItemDelegateForColumn(Outline.POV.value, self.outlinePersoDelegate)
        self.outlineCompileDelegate = outlineCompileDelegate()
        self.setItemDelegateForColumn(Outline.compile.value, self.outlineCompileDelegate)
        self.outlineStatusDelegate = outlineStatusDelegate(self.modelStatus)
        self.setItemDelegateForColumn(Outline.status.value, self.outlineStatusDelegate)
        self.outlineGoalPercentageDelegate = outlineGoalPercentageDelegate()
        self.setItemDelegateForColumn(Outline.goalPercentage.value, self.outlineGoalPercentageDelegate)
        self.outlineLabelDelegate = outlineLabelDelegate(self.modelLabels)
        self.setItemDelegateForColumn(Outline.label.value, self.outlineLabelDelegate)
        
        # Hiding columns
        for c in range(1, self.model().columnCount()):
            self.hideColumn(c)
        for c in [Outline.POV.value, Outline.status.value, Outline.compile.value, 
                  Outline.wordCount.value, Outline.goal.value, Outline.goalPercentage.value,
                  Outline.label.value]:
            self.showColumn(c)
        
        self.header().setSectionResizeMode(Outline.title.value, QHeaderView.Stretch)
        self.header().setSectionResizeMode(Outline.POV.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.status.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.label.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.compile.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.wordCount.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.goal.value, QHeaderView.ResizeToContents)
        self.header().setSectionResizeMode(Outline.goalPercentage.value, QHeaderView.ResizeToContents)
        
    def setRootIndex(self, index):
        QTreeView.setRootIndex(self, index)
        self.outlineGoalPercentageDelegate = outlineGoalPercentageDelegate(index)
        self.setItemDelegateForColumn(Outline.goalPercentage.value, self.outlineGoalPercentageDelegate)
        
    def dragMoveEvent(self, event):
        dndView.dragMoveEvent(self, event)
        QTreeView.dragMoveEvent(self, event)
        
    def mouseReleaseEvent(self, event):
        QTreeView.mouseReleaseEvent(self, event)
        outlineBasics.mouseReleaseEvent(self, event)
        