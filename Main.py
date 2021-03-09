from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap
import sqlite3
import sys
from random import randint

class Game(QWidget):
	def __init__(self):
		super().__init__()
		
		self.Layout = QGridLayout(self)
		
		#Botao de inicia e parar
		self.ButtonInit = QPushButton('Start', self)
		self.ButtonInit.clicked.connect(self.InitGame)
		self.ButtonInit.setStyleSheet('QPushButton {font: 28px; border-radius: 20px; padding: 10px; border: 1px solid red; background-color: rgb(190, 190, 255)}')
		self.Layout.addWidget(self.ButtonInit, 0,0,1,2)
		
		#Botao de opcões
		self.Opicoes = QPushButton('Opções', self)
		self.Opicoes.setStyleSheet('QPushButton {font: 28px; border-radius: 20px; padding: 10px; border: 1px solid red; background-color: rgb(190, 190, 255)}')
		self.Opicoes.clicked.connect(self.OptionGame)
		self.Layout.addWidget(self.Opicoes,1, 0, 1, 1)

		#Logo do Criador fodao
		self.Logo = QLabel(self)
		self.Logo.setPixmap(QPixmap('Logo.png'))
		self.Layout.addWidget(self.Logo, 1, 1)
		
		self.Chances = 6
		#Dificuldade
		self.Dificulty = 0
		
		#Configuracoes da tela
		self.setWindowTitle('Forca')
		self.setMinimumSize(800, 600)
		self.show()
	
	def InitGame(self): #Inicia o nova janela no jogo e Minimiza a outra
		self.Init = InitGame()
	
	def OptionGame(self):
		self.Init = Opicoes()

class InitGame(QWidget): #Janela da Forca
	def __init__(self):
		super().__init__()
		
		self.Layout = QGridLayout(self)
		
		#Dados
		self.Chances = Jogo.Chances
		self.LetrasUsadas = ''
		sortir_palavra = self.SortirPalavra()
		self.PalavraSortida = sortir_palavra[0]
		self.PalavraEscondida = ''
		for Letra in self.PalavraSortida:
			self.PalavraEscondida += '_ '
		
		#Labels
		self.ChancesLabel = QLabel(f'Chances: {self.Chances}', self)
		self.ChancesLabel.setStyleSheet('QLabel {font: 28px}')
		self.Layout.addWidget(self.ChancesLabel, 1, 1)
		self.LetrasUsadas_Label = QLabel(f'Letras ja escolhidas: {self.LetrasUsadas}', self)
		self.LetrasUsadas_Label.setStyleSheet('QLabel {font: 28px}')
		self.Layout.addWidget(self.LetrasUsadas_Label, 3, 0)
		self.PalavraEscondida_Label = QLabel(f'Palavra: {self.PalavraEscondida}', self)
		self.PalavraEscondida_Label.setStyleSheet('QLabel {font: 28px}')
		self.Layout.addWidget(self.PalavraEscondida_Label, 1, 0)
		self.Genero = QLabel(self)
		if Jogo.Dificulty == 0 or Jogo.Dificulty == 1:
			self.Genero.setText(f'Genero: {sortir_palavra[1]}')
			self.Genero.setStyleSheet('QLabel {font: 18px}')
			self.Layout.addWidget(self.Genero, 2, 0)
		self.Dica = QLabel(self)
		if Jogo.Dificulty == 0:
			self.Dica.setText(f'Dica: {sortir_palavra[2]}')
			self.Dica.setStyleSheet('QLabel {font: 18px}')
			self.Layout.addWidget(self.Dica, 2, 1)
		
		#Interacao com o usuario
		self.InsertLetra = QLineEdit(self)
		self.InsertLetra.setStyleSheet('QLineEdit {font: 28px}')
		self.InsertLetra.returnPressed.connect(self.ProcurarLetra)
		self.Layout.addWidget(self.InsertLetra, 4, 0)
		self.RespostaButton = QPushButton('Enviar', self)
		self.RespostaButton.setStyleSheet('QPushButton {font: 28px}')
		self.Layout.addWidget(self.RespostaButton, 4, 1)
		self.RespostaButton.clicked.connect(self.ProcurarLetra)
		
		
		#Configuacoes da janela
		self.setWindowTitle('Forca')
		self.setMinimumSize(800, 600)
		self.show()
	
	def SortirPalavra(self):
		try:
			self.update()
			self.LetrasUsadas = ''
			connect = sqlite3.connect('Data.db')
			cursor = connect.cursor()
			cursor.execute('CREATE TABLE IF NOT EXISTS Palavras(Palavra text, Genero text, Dica text)')
			palavra = cursor.execute('SELECT * FROM Palavras')
			palavra = palavra.fetchall()
			palavra1 = [['Futbol', 'Esporte', 'Jogado no campo'], \
			['Maça', 'Comida', 'Vermelha'], \
			['Pistao', 'Parte do carro', 'Perto do motor'], \
			['Ambulancia', 'Automovel', 'Parece uma van'], \
			['Petit Gateou', 'Sobremesa', 'Recheio de chocolate'], \
			['Azul Ciano', 'Cor', 'Como um azul claro']]
			cont = 0
			lista = []
			if randint(0, 2) == 1:
				try:
					for row in palavra:
						lista.append(row)
						cont += 1
					rand = randint(0, cont)
					sortida = lista[rand]
					return sortida
				except:
					rand = randint(0, 3)
					sortida = palavra1[rand]
				return sortida
			else:
				rand = randint(0, 3)
				sortida = palavra1[rand]
				return sortida
		except:
			print('Error')
			
	def ProcurarLetra(self):
		try:
			Letra = str(self.InsertLetra.text()[0]).lower() #Pega a letra em Minusculo
			self.InsertLetra.setText('')
			if Letra.isalpha() == True: #Verifica se ? uma letra
				if not Letra.lower() in self.LetrasUsadas: #Se nao tiver a letra na lista ele adiciona
					self.LetrasUsadas += F'{Letra} '
					self.LetrasUsadas_Label.setText(f'Letras ja escolhidas: {self.LetrasUsadas}')
				
					if Letra in self.PalavraSortida.lower(): #Ve se tem a letra na palavra escolhida
						self.PalavraEscondida = ''
						
						for letra in self.PalavraSortida.lower(): #Transforma '_' na letra
							if letra in self.LetrasUsadas:
								self.PalavraEscondida += letra
							else:
								self.PalavraEscondida += '_ '
					
					else: #Se nao tiver a letra ele diminui a chance
						self.Chances -= 1
						self.ChancesLabel.setText(f'Chances: {str(self.Chances)}')
						if self.Chances == 0:
							self.Msg = QMessageBox()
							self.Msg.setIcon(QMessageBox.Warning)
							self.Msg.setText(f'Voce perdeu! Tente Novamente \nA palavra era: {self.PalavraSortida}')
							self.Msg.setWindowTitle('Alerta')
							self.Msg.exec_()
							self.close()
							Jogo.setMinimumSize(800, 600)
							Jogo.setGeometry(100, 100, 800, 600)
			else:
				self.Msg = QMessageBox()
				self.Msg.setIcon(QMessageBox.Warning)
				self.Msg.setText('So aceitamos Letras!')
				self.Msg.setWindowTitle('Vitoria')
				self.Msg.exec_()
			
			if self.PalavraEscondida.lower() == self.PalavraSortida.lower(): #Verifica se a pala escolhida ja esta completa, se estiver Vitoria
				self.Msg = QMessageBox()
				self.Msg.setIcon(QMessageBox.Warning)
				self.Msg.setText(f'Voce venceu! Parabens \nA palavra era: {self.PalavraSortida}')
				self.Msg.setWindowTitle('Vitoria')
				self.Msg.exec_()
				self.close()
				Jogo.setMinimumSize(800, 600)
				Jogo.setGeometry(100, 100, 800, 600)
			self.PalavraEscondida_Label.setText(f'Palavra: {self.PalavraEscondida}')
			
		except(IndexError):
			self.Msg = QMessageBox()
			self.Msg.setIcon(QMessageBox.Warning)
			self.Msg.setText('Digite uma letra!')
			self.Msg.setWindowTitle('Alerta')
			self.Msg.exec_()

class Opicoes(QWidget):
	def __init__(self):
		super().__init__()
		
		self.Layout = QGridLayout(self)
		
		#Definir quantidades de chances
		self.Chances = QLineEdit(str(Jogo.Chances), self)
		self.Layout.addWidget(QLabel('Chances: ', self), 0, 0)
		self.Layout.addWidget(self.Chances, 0, 1)
		
		#Adicionar nova palavra
		self.NewPalavra = QLineEdit(self)
		self.Layout.addWidget(QLabel('Nova palavra: ', self), 1, 0)
		self.Layout.addWidget(self.NewPalavra, 1, 1)
		self.Genero = QLineEdit(self)
		self.Layout.addWidget(QLabel('Genero: ', self), 1, 2)
		self.Layout.addWidget(self.Genero, 1, 3)
		self.Dica = QLineEdit(self)
		self.Dica.returnPressed.connect(self.AddPalavra)
		self.Layout.addWidget(QLabel('Dica: ', self), 1,4)
		self.Layout.addWidget(self.Dica, 1, 5)
		self.Add = QPushButton('Adicionar palavra', self)
		self.Add.clicked.connect(self.AddPalavra)
		self.Layout.addWidget(self.Add, 2, 0)
		
		self.setStyleSheet('QWidget {font: 18px}')
		
		#Salvar alteracoes
		self.Save = QPushButton('Salvar', self)
		self.Save.clicked.connect(self.SaveDef)
		self.Layout.addWidget(self.Save, 3, 0)
		
		#Dificuldade
		self.Layout.addWidget(QLabel('		Dificuldade: '), 2, 1)
		self.Facil = QPushButton('Facil', self)
		self.Facil.clicked.connect(self.FacilMode)
		self.Layout.addWidget(self.Facil, 2, 2)
		self.Normal = QPushButton('Normar', self)
		self.Normal.clicked.connect(self.NormalMode)
		self.Layout.addWidget(self.Normal, 2, 3)
		self.Dificil = QPushButton('Dificil', self)
		self.Dificil.clicked.connect(self.DificilMode)
		self.Layout.addWidget(self.Dificil, 2, 4)
		
		#Cor padrao das dificuldades
		self.Dificil.setStyleSheet('QPushButton {background-color: gray}')
		self.Normal.setStyleSheet('QPushButton {background-color: gray}')
		self.Facil.setStyleSheet('QPushButton {background-color: gray}')
		
		#Colorindo a dificuldade escolhida
		if Jogo.Dificulty == 0: self.Facil.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
		if Jogo.Dificulty == 1: self.Normal.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
		if Jogo.Dificulty == 2: self.Dificil.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
		
		self.setWindowTitle('Opicoes')
		self.setMinimumSize(600, 400)
		self.show()
	
	def SaveDef(self): #Salvando configuracoes
		if self.Chances.text().isnumeric():
			Jogo.Chances = int(self.Chances.text())
		else:
			pass
		self.close()
		
	def AddPalavra(self): #Adicionando palavras ao bd
		if self.NewPalavra.text() != '' and self.Genero.text() != '' and self.Dica.text() != '' and self.NewPalavra.text().isalpha():
			connect = sqlite3.connect('Data.db')
			cursor = connect.cursor()
			cursor.execute('INSERT INTO Palavras(Palavra, Genero, Dica) VALUES(?, ?, ?)', (self.NewPalavra.text(), self.Genero.text(), self.Dica.text(), ))
			connect.commit()
			connect.close()
			self.NewPalavra.setText('')
			self.Genero.setText('')
			self.Dica.setText('')
			
	def FacilMode(self): #Definindo o modo de jogo para facil
		Jogo.Dificulty = 0
		self.Dificil.setStyleSheet('QPushButton {background-color: gray}')
		self.Normal.setStyleSheet('QPushButton {background-color: gray}')
		if Jogo.Dificulty == 0:
			self.Facil.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
			
	def NormalMode(self): #Deifinindo o modo de jogo para normal
		Jogo.Dificulty = 1
		self.Dificil.setStyleSheet('QPushButton {background-color: gray}')
		self.Facil.setStyleSheet('QPushButton {background-color: gray}')
		if Jogo.Dificulty == 1:
			self.Normal.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
			
	def DificilMode(self): #Definindo o modo de jogo para dificil
		Jogo.Dificulty = 2
		self.Normal.setStyleSheet('QPushButton {background-color: gray}')
		self.Facil.setStyleSheet('QPushButton {background-color: gray}')
		if Jogo.Dificulty == 2:
			self.Dificil.setStyleSheet('QPushButton {background-color: rgb(100, 100, 255)}')
		
		
App = QApplication(sys.argv)
Jogo = Game()
sys.exit(App.exec_())
