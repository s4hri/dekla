#!/usr/bin/env python3
"""
    additional widgets for Dekla, mainly for options and config windows

    they do not carry the Cute- prefix, because they are intended
    to be as independent from the Dekla structure as possible
    for later reuse


"""


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DictionaryLineEdit(QWidget):
        """ Simple line edit for all the
        label = DictionaryLineEdit(dict1, 'hello', 'Just a test')

        after pressing 'enter' syncs the values to the dictionary
        """
        def __init__(self,dictionary,fieldname,description):
                super().__init__()
                layout = QHBoxLayout()

                self.dictionary = dictionary
                self.fieldname = fieldname
                self.valuetype = type( self.dictionary[self.fieldname] )

                self.desc1 = QLabel( fieldname + ' (' + str(self.valuetype) + '): ' + description )

                self.lineEdit = QLineEdit( str( self.dictionary[self.fieldname] ) )
                self.lineEdit.returnPressed.connect( self.setValue )
                self.lineEdit.textEdited.connect( self.editedValue )
                self.resetButton = QPushButton("reset")
                self.resetButton.pressed.connect( self.resetValue )

                self.palette1 = QPalette()
                self.palette1.setColor(QPalette.Base,Qt.green)
                #palette.setColor(QPalette::Text,Qt::white);
                self.lineEdit.setPalette(self.palette1)

                layout.addWidget( self.desc1 )
                layout.addWidget( self.resetButton )
                layout.addWidget( self.lineEdit )
                self.setLayout(layout)

        def resetValue(self):
                self.lineEdit.setText( str( self.dictionary[self.fieldname] ) )
                self.changeColor( Qt.green )

        def setValue(self):
                self.dictionary[self.fieldname] = self.valuetype( self.lineEdit.text() )
                self.changeColor( Qt.green )

        def editedValue(self):
                if self.dictionary[self.fieldname] != self.valuetype( self.lineEdit.text() ):
                        self.changeColor( Qt.yellow )

        def changeColor(self,color):
                self.palette1.setColor(QPalette.Base,color)
                self.lineEdit.setPalette(self.palette1)


class FontsLister(QWidget):
        """ FontsLister

        lists all the available fonts
        adds a 24-size preview of a chosen font

        """
        def __init__(self):
                super().__init__()
                self.layout1 = QVBoxLayout()

                # font previews:
                database = QFontDatabase()
                fontTree = QTreeWidget()
                fontTree.setColumnCount(2)
                fontTree.setHeaderLabels([ "Font", "Smooth Sizes" ])
                fontFamilies = database.families()
                for family in fontFamilies:
                        familyItem = QTreeWidgetItem(fontTree)
                        familyItem.setText(0, family)
                        fontStyles = database.styles(family)
                        for style in fontStyles:
                                styleItem = QTreeWidgetItem(familyItem)
                                styleItem.setText(0, style)

                                sizes = list()
                                smoothSizes = database.smoothSizes(family, style)
                                sizes = [ str(points)+' ' for points in smoothSizes ]

                                styleItem.setText(1, str(sizes))

                self.fontTree = fontTree

                self.ledit = QLineEdit()
                self.pbutton = QPushButton("Update")
                self.label = QLabel("Test this is a test")

                self.pbutton.pressed.connect(self.updatelabel)

                self.layout1.addWidget(self.fontTree)
                self.layout1.addWidget(self.ledit)
                self.layout1.addWidget(self.pbutton)
                self.layout1.addWidget(self.label)

                self.setLayout(self.layout1)
        def updatelabel(self):
                self.label.setFont( QFont( self.ledit.text(), 24, QFont.Bold ) )

