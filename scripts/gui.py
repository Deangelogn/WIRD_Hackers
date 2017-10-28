import sys
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QComboBox
from PyQt5.QtGui import QIcon

import mysql.connector, pandas

class App(QMainWindow):

    def __init__(self):
        #Define propriedades da janela
        super().__init__()
        self.setWindowIcon(QIcon('imgs/logo_tu.png'))
        self.left = 50
        self.top = 50
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        #Define estrutura da janela, botoes, etc
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Cria a janela onde vai ser plotado
        m = PlotCanvas(self, width=5, height=4)
        m.move(0,0)

        #Cria botão e conecta a função LoadButtonClicked quando clicado
        LoadButton = QPushButton('Coletar Dados', self)
        LoadButton.clicked.connect(self.LoadButtonClicked)
        LoadButton.setToolTip('Coleta do banco de dados')
        LoadButton.move(500,0)
        LoadButton.resize(140,100)

        #Cria o menu dropdown
        self.ListaDataBase = QComboBox(self)
        self.ListaDataBase.hide()
        self.ListaDataBase.move(500,100)
        self.ListaDataBase.resize(140,100)
        self.show()


    def LoadButtonClicked(self):
        sender = self.sender()
        self.ListaDataBase.show()
        self.Conexao = mysql.connector.connect(host='143.106.73.88', database='hackthecampus', user='htc', password='htc_123456')
        self.DataBases = ["htc_alunos_doutorado_naturalidade", "htc_alunos_especiais_inter_posgrad_naturalidade", "htc_alunos_especiais_inter_grad_naturalidade", "htc_alunos_graduacao_naturalidade", "htc_alunos_mestrado_naturalidade", "htc_concluintes", "htc_cv_cr", "htc_fapesp", "htc_folha_unicamp", "htc_lotacao_unicamp", "htc_origem_alunos", "htc_sexo_alunos", "htc_siafem_despesas"]
        self.AdicionaItensLista()

    def AdicionaItensLista(self):
        #Preenche a lista de itens
        for NomeDaBase in self.DataBases:
            self.ListaDataBase.addItem(NomeDaBase)
        #Quando cada item da lista for selecionado, manda a string para a função DataFrameSelecionado
        self.ListaDataBase.activated[str].connect(self.DataFrameSelecionado)


    def DataFrameSelecionado(self, text):
        #Prepara a query
        s = "SELECT * FROM "
        #Puxa o data frame
        self.DataFrameAtivo = pandas.read_sql(s + text, con=self.Conexao)
        self.ColunasAtivas = self.DataFrameAtivo.columns.values
        self.ListaDeBotoes = []
        PoePraBaixo = 0
        for Coluna in range(0,len(self.ColunasAtivas)):
            PoePraBaixo = PoePraBaixo + 20
            self.ListaDeBotoes.append(QPushButton(self.ColunasAtivas[Coluna], self))
            self.ListaDeBotoes[Coluna].clicked.connect(self.LoadButtonClicked)
            self.ListaDeBotoes[Coluna].setToolTip('Coluna %s do conjunto %s' % (self.ColunasAtivas[Coluna], self.DataFrameSelecionado))
            self.ListaDeBotoes[Coluna].move(500,180+PoePraBaixo)
            self.ListaDeBotoes[Coluna].resize(80,20)
            self.ListaDeBotoes[Coluna].show()




class PlotCanvas(FigureCanvas):
    #Define propriedades do canvas matplotlib, atualiza o gráfico, etc
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('Titulo')
        ax.set_ylabel('Eixo Y')
        ax.set_xlabel('Eixo X')
        self.draw()


if __name__ == '__main__':
    #Inicia a aplicação (janela), executa e sai
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
