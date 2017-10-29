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
        
    def lineChart(self, df, X, Y, t):
        self.axes.clear()
        df.plot(ax = self.axes, kind="line", legend=False)
        self.axes.set_title(t)
        self.axes.set_ylabel(Y)
        self.axes.set_xlabel(X)
        self.draw()     
            
    def barChart(self, df, X, Y, t):
        self.axes.clear()
        df.plot(ax = self.axes, kind="bar", legend=False)
        self.axes.set_title(t)
        self.axes.set_ylabel(Y)
        self.axes.set_xlabel(X)
        self.draw() 
        
    def pieChart(self, df, X, Y, t):
        self.axes.clear()
        df['count'].plot(ax = self.axes, kind='pie', autopct='%.2f', legend=False)
        self.axes.set_title(t)
        self.axes.set_ylabel(Y)
        self.axes.set_xlabel(X)
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

        #Botão plot
        plotButton =  QPushButton('Plot', self)
        plotButton.clicked.connect(self.plot)
        plotButton.setObjectName('plotButton')
        plotButton.setToolTip('Plot')
        plotButton.move(self.width*0.59,self.height*0.64)
        plotButton.resize(self.width*0.1,self.height*0.05)
            
        self.groupList = QComboBox(self)
        self.groupList.move(self.width*0.59,self.height*0.48)
        self.groupList.resize(self.width*0.1,self.height*0.05)

        self.target = QComboBox(self)
        self.target.move(self.width*0.59,self.height*0.56)
        self.target.resize(self.width*0.1,self.height*0.05)

        
        self.ListaDataBase = QComboBox(self)
        self.ListaDataBase.hide()
        self.ListaDataBase.move(self.width*0.59,self.height*0.1)
        self.ListaDataBase.resize(self.width*0.1,self.height*0.05)
        
        self.plotOptions = QComboBox(self)
        self.plotOptions.move(self.width*0.01,self.height*0.1)
        self.plotOptions.resize(self.width*0.08,self.height*0.05)
        self.plotOptions.addItem("Bar")
        self.plotOptions.addItem("Pie")
        self.plotOptions.addItem("Line")
        
        self.AdicionaItensLista()

        self.show()

        self.PendenteParaPlot = None


    def plot(self):
        xLabel = self.groupList.currentText()
        yLabel = self.target.currentText()
        self.out = self.df[self.currentIndex].groupby(xLabel)[yLabel].agg(['count'])
        
        self.chartType = self.plotOptions.currentText()
        
        if self.chartType == "Bar":
            self.canvas.barChart(self.out, xLabel, yLabel, xLabel + ' vs ' + yLabel)
        elif self.chartType == "Pie":
            self.canvas.pieChart(self.out, xLabel, yLabel, xLabel + ' vs ' + yLabel)
        elif self.chartType == "Line":
            self.canvas.lineChart(self.out, xLabel, yLabel, xLabel + ' vs ' + yLabel)

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
        self.currentIndex = self.DataBases.index(text)
        self.DataFrameAtivo = self.df[self.currentIndex]
        self.ColunasAtivas = self.DataFrameAtivo.columns.values
        self.loadGroupComboBox()
        self.loadTargetComboBox()
        self.checkComboBox()
  
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
