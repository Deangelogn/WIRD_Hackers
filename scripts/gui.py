import sys
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import re
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QComboBox, QDesktopWidget
from PyQt5.QtGui import QIcon

import mysql.connector

class PlotCanvas(FigureCanvas):
    #Define propriedades do canvas matplotlib, atualiza o gráfico, etc
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.PlotInicial()


    def PlotInicial(self):
        data = [random.random() for i in range(25)]
        self.axes.plot(data, 'r-')
        self.axes.set_title('Titulo')
        self.axes.set_ylabel('Eixo Y')
        self.axes.set_xlabel('Eixo X')
        self.draw()

    def UpdatePlot(self, x, y):
        self.axes.clear()
        self.axes.scatter(x,y)
        self.axes.set_title('Titulo')
        self.axes.set_ylabel('Eixo Y')
        self.axes.set_xlabel('Eixo X')
        self.draw()

class App(QMainWindow):

    def __init__(self):
        self.getDataBase()
        #Define propriedades da janela
        super().__init__()
        self.setWindowIcon(QIcon('imgs/logo_tu.png'))
        self.title = 'WIRD'
        self.initUI()
        print('1')

    def initUI(self):
        #Define estrutura da janela, botoes, etc
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)

        screen = QDesktopWidget().screenGeometry()
        self.width = screen.width()
        self.height = screen.height()
        self.setGeometry(self.width*0.1, self.height*0.1, self.width*0.7, self.height*0.7)

        #Cria a janela onde vai ser plotado
        self.canvas = PlotCanvas(self, width=6.5, height=4.5)
        self.canvas.move(self.width*0.1,self.height*0.03)

        #Cria botões x
        EixoX = QPushButton('Eixo X', self)
        EixoX.clicked.connect(self.DefineEixo)
        EixoX.setObjectName('X')
        EixoX.setToolTip('Definir como eixo X')
        EixoX.move(self.width*0.4/2,self.height*0.62)
        EixoX.resize(self.width*0.3,self.height*0.05)

        #Cria botões y
        EixoY = QPushButton('Eixo Y', self)
        EixoY.clicked.connect(self.DefineEixo)
        EixoY.setObjectName('Y')
        EixoY.setToolTip('Definir como eixo Y')
        EixoY.move(self.width*0.02,self.height*0.4/2)
        EixoY.resize(self.width*0.03,self.height*0.6/2)

        self.ListaDataBase = QComboBox(self)

        self.groupList = QComboBox(self)
        self.groupList.move(self.width*0.59,self.height*0.48)
        self.groupList.resize(self.width*0.1,self.height*0.05)

        self.target = QComboBox(self)
        self.target.move(self.width*0.59,self.height*0.56)
        self.target.resize(self.width*0.1,self.height*0.05)

        self.ListaDataBase.hide()
        self.ListaDataBase.move(self.width*0.59,self.height*0.1)
        self.ListaDataBase.resize(self.width*0.1,self.height*0.05)

        self.AdicionaItensLista()

        self.show()

        self.PendenteParaPlot = None


    def getDataBase(self):

        conn = mysql.connector.connect(host='143.106.73.88', database='information_schema', user='htc', password='htc_123456')
        self.tables=pd.read_sql("SELECT * FROM tables where TABLE_TYPE='BASE TABLE'", con=conn)
        self.DataBases=[]
        limit = 2
        count = 0
        for l in self.tables.TABLE_NAME:
            self.DataBases.append(l)
            if count < limit:
                count += 1
            else:
                break

        self.df = []
        for l in self.DataBases:
            print(l)
            conn = mysql.connector.connect(host='143.106.73.88', database='hackthecampus', user='htc', password='htc_123456')
            dataFrame = pd.read_sql("SELECT * FROM " + l, con=conn)
            self.df.append(dataFrame)
        conn.close()

        #Cria o menu dropdown

#    def LoadButtonClicked(self):
#        sender = self.sender()
#        self.ListaDataBase.show()
#        self.Conexao = mysql.connector.connect(host='143.106.73.88', database='hackthecampus', user='htc', password='htc_123456')
#        self.DataBases = ["htc_alunos_doutorado_naturalidade", "htc_alunos_especiais_inter_posgrad_naturalidade", "htc_alunos_especiais_inter_grad_naturalidade", "htc_alunos_graduacao_naturalidade", "htc_alunos_mestrado_naturalidade", "htc_concluintes", "htc_cv_cr", "htc_fapesp", "htc_folha_unicamp", "htc_lotacao_unicamp", "htc_origem_alunos", "htc_sexo_alunos", "htc_siafem_despesas"]
#        self.AdicionaItensLista()

    def AdicionaItensLista(self):
        #Preenche a lista de itens
        for NomeDaBase in self.DataBases:
            self.ListaDataBase.addItem(NomeDaBase)
        #Quando cada item da lista for selecionado, manda a string para a função DataFrameSelecionado
        self.ListaDataBase.activated[str].connect(self.DataFrameSelecionado)
        self.ListaDataBase.show()

    def loadGroupComboBox(self):
        for cn in self.ColunasAtivas:
            self.groupList.addItem(cn)

    def loadTargetComboBox(self):
        for cn in self.ColunasAtivas:
            self.target.addItem(cn)

    def checkComboBox(self):
            if self.groupList.currentText() == self.target.currentText():
                self.target.setCurrentText(self.target.itemText(self.groupList.currentIndex()+1))


    def DataFrameSelecionado(self, text):
        self.DataFrameAtivo = self.df[self.DataBases.index(text)]
        self.ColunasAtivas = self.DataFrameAtivo.columns.values
        self.loadGroupComboBox()
        self.loadTargetComboBox()
        self.checkComboBox()
        #self.ListaDeBotoes = []
        #PoePraBaixo = 0


        #for Coluna in range(0,len(self.ColunasAtivas)):
        #    PoePraBaixo = PoePraBaixo + 40
        #    self.ListaDeBotoes.append(QPushButton(self.ColunasAtivas[Coluna], self))
        #    self.ListaDeBotoes[Coluna].clicked.connect(self.ColunaSelecionada)
        #    self.ListaDeBotoes[Coluna].setObjectName(self.ColunasAtivas[Coluna])
        #    self.ListaDeBotoes[Coluna].setToolTip('Coluna %s do conjunto %s' % (self.ColunasAtivas[Coluna], self.DataFrameSelecionado))
        #    self.ListaDeBotoes[Coluna].move(self.width*0.65-80,60+PoePraBaixo)
        #    self.ListaDeBotoes[Coluna].resize(self.width*0.1,self.height*0.05)
        #    self.ListaDeBotoes[Coluna].show()
        #self.FlagParaPlotar = 0
        #self.UpdatePlot(self, self.DataFrameAtivo[0], self.DataFrameAtivo[1])
        #x = self.DataFrameAtivo[self.ColunasAtivas[0]].values
        #y = self.DataFrameAtivo[self.ColunasAtivas[2]].values
        #self.UpdatePlot(x,y)

    def DefineEixo(self, QualEixo):
        sender = self.sender()
        if (sender.objectName()=='X'):
            self.x = list(map(int,self.DataFrameAtivo[self.PendenteParaPlot].values))
            self.FlagParaPlotar+=1
        elif (sender.objectName()=='Y'):
            self.y = list(map(int,self.DataFrameAtivo[self.PendenteParaPlot].values))
            self.FlagParaPlotar+=1
        if (self.FlagParaPlotar==2):
            self.canvas.UpdatePlot(self.x, self.y)
            self.FlagParaPlotar = 0
            self.ListaDataBase.setEnabled(True)
            self.LoadButton.setEnabled(True)

        for Coluna in range(0,len(self.ColunasAtivas)):
            self.ListaDeBotoes[Coluna].setEnabled(True)
        self.PendenteParaPlot = None

    def ColunaSelecionada(self):
        sender = self.sender()
        self.PendenteParaPlot = sender.objectName()
        for Coluna in range(0,len(self.ColunasAtivas)):
            self.ListaDeBotoes[Coluna].setEnabled(False)
        self.ListaDataBase.setEnabled(False)
        self.LoadButton.setEnabled(False)



if __name__ == '__main__':
    #Inicia a aplicação (janela), executa e sai
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
