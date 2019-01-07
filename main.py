# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QStyleFactory
from sys import argv as args, exit
from GUI import cryoGUI

app = QApplication(args)
app.setStyle(QStyleFactory.create("gtk+"))
window = cryoGUI()
window.show()
exit(app.exec_())




