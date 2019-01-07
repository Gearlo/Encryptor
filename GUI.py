# -*- coding: utf-8 -*-
# created by: Gerardo Rivera López
# released under the GNU GPL v2 license
# 
# github.com/gearlo


from PyQt4.QtGui import QWidget, QLabel, QPixmap, QDialog, QCheckBox
from PyQt4.QtCore import Qt, QSize, QRect,  SIGNAL, QString

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class cryoGUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Crypto App")
        self.resize(500, 260)
        self.setMinimumSize(QSize(500, 260))
        self.setMaximumSize(QSize(500, 260))
        self.label = QLabel(self)
        self.label.setGeometry(QRect(66, 55, 150, 150))
        self.label.setPixmap(QPixmap("images/padlock.png"))
        self.label.setScaledContents(True)
        self.label.setToolTip('Encrypt files and folders')

        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QRect(282, 55, 150, 150))
        self.label_2.setPixmap(QPixmap("images/unlock.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setToolTip('Decrypt files and folders')
        self.label_2.mousePressEvent = self.__initDecrypter

        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QRect(66, 180, 150, 16))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setText('<b style="color: white">ENCRYPT</b>')

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(282, 180, 150, 16))
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setText('<b style="color: white">DECRYPT</b>')

        self.label_3.mousePressEvent = self.label.mousePressEvent = self.__initEncrypter
        self.label_4.mousePressEvent = self.label_2.mousePressEvent = self.__initDecrypter


    def __initEncrypter(self,e):
        E = EncryptDialog()
        E.exec_()

    def __initDecrypter(self,e):
        E = DecryptDialog()
        E.exec_()




from techniques import caesarCipher, monoAlphabeticCipher, vigenereCipher, vernanCipher, oneTimePad, AESCipher as AES, checksum, reduceMd5

from binascii import unhexlify

from PyQt4.QtGui import QTreeView, QFileSystemModel, QFormLayout, QGroupBox, QScrollArea, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,QComboBox, QProgressBar, QMessageBox
from PyQt4.QtCore import QDir

class EncryptDialog(QDialog):

    def __init__(self):
        self.techniquesClass = {'caesar cipher':caesarCipher, 'mono alphabetic cipher':monoAlphabeticCipher, 'vigenere cipher':vigenereCipher, 'vernan cipher':vernanCipher, 'one time pad':oneTimePad}

        self.rowsview = []
        self.filesview = []
        self.techniques = []

        QDialog.__init__(self)
        self.setWindowTitle("CryptoSystems")
        self.resize(1024,600)
        self.setMinimumSize(QSize(1024, 600))
        self.setMaximumSize(QSize(1024, 600))

        self.checkBox_2 = QCheckBox(self)
        self.checkBox_2.setGeometry(QRect(620, 10, 130, 20))
        self.checkBox_2.setText('Select All')
        self.checkBox_2.clicked.connect(self.__selectAllFiles)

        self.treeView = QTreeView(self)
        self.treeView.setGeometry(QRect(10, 10, 230, 580))
        self.treeView.setObjectName("treeView")

        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)

        self.fileSystemModel.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot )
        root = self.fileSystemModel.setRootPath("/")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        self.treeView.hideColumn(1); self.treeView.hideColumn(2); self.treeView.hideColumn(3)
        self.treeView.clicked.connect(self.__eventDirectoryChanged)

        self.mygroupbox = QGroupBox(self)
        self.mygroupbox.setGeometry(QRect(0, 0, 1000, 1000))
        self.myform = QFormLayout()
        for j in list(range(100)):
            horizontalLayout = QHBoxLayout()
            self.myform.addRow(horizontalLayout)
            self.rowsview.append(horizontalLayout)

        self.mygroupbox.setLayout(self.myform)
        scroll = QScrollArea(self)
        scroll.setWidget(self.mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setGeometry(QRect(250, 30, 500, 580))
        scroll.setWidgetResizable(True)

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(780, 30, 31, 16))
        self.label_4.setPixmap(QPixmap("images/key.png"))
        self.label_4.setScaledContents(True)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(820, 30, 180, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText (_fromUtf8('write your password'))
        self.lineEdit.setEchoMode(QLineEdit.Password)

        self.techniquesGroup = QGroupBox(self)
        self.tecniquesform = QFormLayout()
        self.techniquesGroup.setLayout(self.tecniquesform)

        self.techniquesScroll = QScrollArea(self)
        self.techniquesScroll.setGeometry(QRect(770, 100, 230, 300))
        self.techniquesScroll.setWidget(self.techniquesGroup)
        self.techniquesScroll.setWidgetResizable(True)

        self.rowsTechiques = []
        for i in list(range(8)):
            horizontalLayout = QHBoxLayout()
            self.tecniquesform.addRow(horizontalLayout)
            self.rowsTechiques.append(horizontalLayout)

        techniquesCombo = QComboBox()
        techniquesCombo.setGeometry(QRect(10, 50, 171, 22))
        techniquesCombo.addItems(self.techniquesClass.keys())
        self.techniques.append(techniquesCombo)
        self.rowsTechiques[0].addWidget(techniquesCombo)
        self.techniquesNumber = 1

        self.addTechnique = QPushButton()
        self.addTechnique.setGeometry(QRect(90, 90, 31, 21))
        self.addTechnique.setFixedSize(31,21)
        self.addTechnique.setText('+')
        self.connect(self.addTechnique, SIGNAL("clicked()"), self.__eventAddTechnique)
        self.rowsTechiques[len(self.rowsTechiques) - 1].addWidget(self.addTechnique)


        self.okButton = QPushButton(self)
        self.okButton.setGeometry(QRect(920, 560, 80, 20))
        self.okButton.setText('Start...')
        self.connect(self.okButton, SIGNAL("clicked()"), self.__eventInitEncryption)


    def __eventAddTechnique(self):
        techniquesCombo = QComboBox()
        techniquesCombo.setGeometry(QRect(10, 50, 171, 22))
        techniquesCombo.addItems(self.techniquesClass.keys())
        self.techniques.append(techniquesCombo)
        self.rowsTechiques[self.techniquesNumber].addWidget(techniquesCombo)
        self.techniquesNumber = self.techniquesNumber + 1
        if ((len(self.rowsTechiques) - 1) == self.techniquesNumber):
            self.addTechnique.setEnabled(False)


    def __eventDirectoryChanged(self):
        index = self.treeView.currentIndex()
        self.__changeDirectory( self.fileSystemModel.filePath(index))

    def __changeDirectory(self, path):
        for c in self.filesview:
            c.setParent(None)
            c.deleteLater()
        self.filesview = []
        self.checkBox_2.setChecked(False)

        self.progressBars = {}
        for f in self.__getFiles(path):
            try:
                group = QGroupBox(f,self)
                group.setGeometry(QRect(20, 20, 100, 150))
                group.setCheckable(True)
                group.setChecked(False)
                group.setFixedSize(100,150)
                group.setFlat(True)
                group.setToolTip(f)


                label = QLabel(group)
                label.setScaledContents(True)
                label.setGeometry(QRect(5, 25, 90, 90))
                label.setToolTip(f)

                progressBar = QProgressBar(group)
                progressBar.setGeometry(QRect(0, 70, 111, 10))
                progressBar.setProperty("value", 0)
                progressBar.setTextVisible(False)
                progressBar.setToolTip('0%')
                progressBar.setVisible(False)
                self.progressBars[f] = progressBar


                self.filesview.append( group )
                from os.path import isfile
                if isfile(path + '/' + f):
                    ext = f.split('.')[-1]
                    if isfile('icons/'+ ext.lower() +'.png') :
                        label.setPixmap(QPixmap('icons/'+ ext.lower() +'.png'))
                    else:
                        label.setPixmap(QPixmap('icons/default.png'))
                else:
                    label.setPixmap(QPixmap('icons/folder.png'))
                self.connect(group, SIGNAL("clicked()"), self.__deselectFile)
            except ValueError:
                pass


        i = 0
        for x in list(range(len(self.filesview))):
            if (x%4) == 0:
                i = i + 1
            self.rowsview[i].addWidget(self.filesview[x])

    def __selectAllFiles(self):
        for o in self.filesview:
            o.setChecked(self.checkBox_2.isChecked())

    def __deselectFile(self):
        #print 'deselect'
        self.checkBox_2.setChecked(False)

    def __arrozconpollo(self):
        self.__obtainSelectedFIles()

    def __obtainSelectedFIles(self):
        files = []
        for o in self.filesview:
            if o.isChecked():
                files.append(str(o.title()))
                self.progressBars[str(o.title())].setVisible(True)
        return files

    def __getFiles(self, path):
        from os import listdir
        from os.path import isfile

        f = []

        for base in listdir(path):
            try:
                if isfile(path + '/' + base):
                    f.append(base)
            except ValueError:
                pass
        f.sort()
        return f


    def __eventInitEncryption(self):
        if len(self.__obtainSelectedFIles()) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You must specify the files you want to encrypt")
                msg.setWindowTitle("CryptoSystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        if str(self.lineEdit.text()).strip() == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("You must specify a key")
                msg.setWindowTitle("CryptoSystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        self.okButton.setEnabled(False)
        self.techniquesGroup.setEnabled(False)
        self.lineEdit.setEnabled(False)

        index = self.treeView.currentIndex()

        path = self.fileSystemModel.filePath(index)
        selectedFiles = self.__obtainSelectedFIles()

        from os.path import getsize
        blockSize = 4096

        from hashlib import md5
        Hash = md5()
        Hash.update(str(self.lineEdit.text()))
        key = Hash.hexdigest()

        for f in selectedFiles:

            f_in = open(path + '/' + f,'rb')
            f_out = open(path + '/' + reduceMd5( checksum(path + '/' + f) ) + '.cry', 'wb')



            f_out.write('CRYOGENESIS' + unhexlify('00') + 'ARCHIVE' + unhexlify('01'))

            header_list = ''; techniquesObjects =[]
            for t in self.techniques:
                header_list = header_list + t.currentText() + ':'
                techniquesObjects.append( self.techniquesClass[str(t.currentText())](key) )

            file_header =  str('header|' + str(f_in.name.split('/')[-1]) + '|'+ str(header_list) +'|' + str(checksum(path + '/' + f)))



            aes = AES(key)
            f_out.write( aes.encrypt(file_header) )
            f_out.write( unhexlify('02') )

            in_size = getsize(path + '/' + f)
            in_progress = 0.0


            block = f_in.read(blockSize)
            while(block):
                block_c = block
                for t in techniquesObjects:
                    block_c = t.encrypt(block_c)
                f_out.write(block_c)
                in_progress = in_progress + blockSize

                progress = (in_progress/in_size) * 100
                #print progress
                self.progressBars[str(f)].setProperty("value", int(progress))
                self.progressBars[str(f)].setToolTip(str(progress) +'%')
                block = f_in.read(blockSize)


            f_in.close()
            f_out.close()

        msg = QMessageBox()

        msg.setIcon(QMessageBox.Information)

        msg.setText("Encryption has successfully concluded")
        msg.setWindowTitle("CryptoSystems")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        self.hide()




























class DecryptDialog(QDialog):

    def __init__(self):
        self.techniquesClass = {'caesar cipher':caesarCipher, 'mono alphabetic cipher':monoAlphabeticCipher, 'vigenere cipher':vigenereCipher, 'vernan cipher':vernanCipher, 'one time pad':oneTimePad}

        self.rowsview = []
        self.filesview = []
        #self.techniques = []

        QDialog.__init__(self)
        self.setWindowTitle("Desencriptador de Cryogenesis Systems.")
        self.resize(1024,600)
        self.setMinimumSize(QSize(1024, 600))
        self.setMaximumSize(QSize(1024, 600))

        self.checkBox_2 = QCheckBox(self)
        self.checkBox_2.setGeometry(QRect(620, 10, 130, 20))
        self.checkBox_2.setText('seleccionar todos')
        self.checkBox_2.clicked.connect(self.__selectAllFiles)

        self.treeView = QTreeView(self)
        self.treeView.setGeometry(QRect(10, 10, 230, 580))
        self.treeView.setObjectName("treeView")

        self.fileSystemModel = QFileSystemModel(self.treeView)
        self.fileSystemModel.setReadOnly(False)

        self.fileSystemModel.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot )
        root = self.fileSystemModel.setRootPath("/")
        self.treeView.setModel(self.fileSystemModel)
        self.treeView.setRootIndex(root)
        self.treeView.hideColumn(1); self.treeView.hideColumn(2); self.treeView.hideColumn(3)
        self.treeView.clicked.connect(self.__eventDirectoryChanged)

        self.mygroupbox = QGroupBox(self)
        self.mygroupbox.setGeometry(QRect(0, 0, 1000, 1000))
        self.myform = QFormLayout()
        for j in list(range(100)):
            horizontalLayout = QHBoxLayout()
            self.myform.addRow(horizontalLayout)
            self.rowsview.append(horizontalLayout)

        self.mygroupbox.setLayout(self.myform)
        scroll = QScrollArea(self)
        scroll.setWidget(self.mygroupbox)
        scroll.setWidgetResizable(True)
        scroll.setGeometry(QRect(250, 30, 500, 580))
        scroll.setWidgetResizable(True)

        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QRect(780, 30, 31, 16))
        self.label_4.setPixmap(QPixmap("images/key.png"))
        self.label_4.setScaledContents(True)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(820, 30, 180, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText (_fromUtf8('escriba su contraseña'))
        self.lineEdit.setEchoMode(QLineEdit.Password)

        self.okButton = QPushButton(self)
        self.okButton.setGeometry(QRect(920, 560, 80, 20))
        self.okButton.setText('Iniciar...')
        self.connect(self.okButton, SIGNAL("clicked()"), self.__eventInitDecryption)

    def __eventDirectoryChanged(self):
        index = self.treeView.currentIndex()
        self.__changeDirectory( self.fileSystemModel.filePath(index))

    def __changeDirectory(self, path):
        for c in self.filesview:
            c.setParent(None)
            c.deleteLater()
        self.filesview = []
        self.checkBox_2.setChecked(False)

        self.progressBars = {}
        for f in self.__getFiles(path):
            try:
                group = QGroupBox(f,self)
                group.setGeometry(QRect(20, 20, 100, 150))
                group.setCheckable(True)
                group.setChecked(False)
                group.setFixedSize(100,150)
                group.setFlat(True)
                group.setToolTip(f)

                label = QLabel(group)
                label.setScaledContents(True)
                label.setGeometry(QRect(5, 25, 90, 90))
                label.setToolTip(f)

                progressBar = QProgressBar(group)
                progressBar.setGeometry(QRect(0, 70, 111, 10))
                progressBar.setProperty("value", 0)
                progressBar.setTextVisible(False)
                progressBar.setToolTip('0%')
                progressBar.setVisible(False)
                self.progressBars[f] = progressBar

                self.filesview.append( group )
                from os.path import isfile
                if isfile(path + '/' + f):
                    ext = f.split('.')[-1]
                    if isfile('icons/'+ ext.lower() +'.png') :
                        label.setPixmap(QPixmap('icons/'+ ext.lower() +'.png'))
                    else:
                        label.setPixmap(QPixmap('icons/default.png'))
                else:
                    label.setPixmap(QPixmap('icons/folder.png'))
                self.connect(group, SIGNAL("clicked()"), self.__deselectFile)
            except ValueError:
                pass


        i = 0
        for x in list(range(len(self.filesview))):
            if (x%4) == 0:
                i = i + 1
            self.rowsview[i].addWidget(self.filesview[x])

    def __selectAllFiles(self):
        for o in self.filesview:
            o.setChecked(self.checkBox_2.isChecked())

    def __deselectFile(self):
        #print 'deselect'
        self.checkBox_2.setChecked(False)

    def __arrozconpollo(self):
        self.__obtainSelectedFIles()

    def __obtainSelectedFIles(self):
        files = []
        for o in self.filesview:
            if o.isChecked():
                files.append(str(o.title()))
                self.progressBars[str(o.title())].setVisible(True)
        return files

    def __getFiles(self, path):
        from os import listdir
        from os.path import isfile

        f = []

        for base in listdir(path):
            try:
                if isfile(path + '/' + base) and base.split('.')[-1] == 'cry':
                    f.append(base)
            except ValueError:
                pass
        f.sort()
        return f

    def __eventInitDecryption(self):
        if len(self.__obtainSelectedFIles()) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Debes especificar los archivos que quieres desencriptar")
                msg.setWindowTitle("Cryosystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        if str(self.lineEdit.text()).strip() == '':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Debes especificar una clave")
                msg.setWindowTitle("Cryosystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

        self.okButton.setEnabled(False)
        self.lineEdit.setEnabled(False)

        index = self.treeView.currentIndex()

        path = self.fileSystemModel.filePath(index)
        selectedFiles = self.__obtainSelectedFIles()

        from hashlib import md5
        Hash = md5()
        Hash.update(str(self.lineEdit.text()))
        key = Hash.hexdigest()

        errors = 0

        from os.path import getsize
        blockSize = 4096
        for f in selectedFiles:

            f_in = open(path + '/' + f,'rb')
            print path + '/' + f

            header = ''
            if(f_in.read(20) == ('CRYOGENESIS' + unhexlify('00') + 'ARCHIVE' + unhexlify('01'))):
                while(True):
                    c = f_in.read(1)
                    if c == unhexlify('02'):
                        break
                    else:
                        header = header + c
            else:
                print 'esto no es un archivo cifradodo de Cryogenesis Systems'

            #print key
            aes = AES(key)
            #print aes.decrypt(header)
            header_sections = aes.decrypt(header).split('|')

            if header_sections[0] != 'header':
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("La clave no es correcta para el archivo:" + f)
                msg.setWindowTitle("Cryosystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                errors = errors + 1
                continue

            f_out = open(path + '/' + header_sections[1],'wb');

            techniques = header_sections[2].split(':')[:-1]

            techniquesObjects = []

            for t in techniques:
                techniquesObjects.append(self.techniquesClass[t](key))
            techniquesObjects.reverse()


            in_size = getsize(path + '/' + f)
            in_progress = 0.0

            block = f_in.read(blockSize)
            while(block):
                block_p = block
                for t in techniquesObjects:
                    block_p = t.decrypt(block_p)
                f_out.write(block_p)
                in_progress = in_progress + blockSize
                progress = (in_progress/in_size) * 100
                self.progressBars[str(f)].setProperty("value", int(progress))
                self.progressBars[str(f)].setToolTip(str(progress) +'%')
                block = f_in.read(blockSize)

            f_in.close()
            f_out.close()

            if(checksum(path + '/' + header_sections[1]) != header_sections[3]):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("El archivo" + f + 'se ha corrompido')
                msg.setWindowTitle("Cryosystems")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                errors = errors + 1
                from os import remove ; remove(header_sections[1])


        msg = QMessageBox()
        msg.setWindowTitle("Cryosystems")
        msg.setStandardButtons(QMessageBox.Ok)

        if(errors == 0):
            msg.setIcon(QMessageBox.Information)
            msg.setText("La desencriptacion ha concluido exitosamente")
        else:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("La desencriptacion ha concluido con " + str(errors)+ ' error(es)'  )



        msg.exec_()
        self.hide()



