# Importar as bibliotecas necessárias
from PyQt5.QtChart import QChart, QPieSeries, QChartView
from PyQt5.QtWidgets import QApplication, QMainWindow

# Criar a lista de itens
itens = ['Item 1', 'Item 2', 'Item 3', 'Item 4']

# Criar o QPieSeries
series = QPieSeries()

# Adicionar as fatias ao QPieSeries
for item in itens:
    series.append(item, 0)  # Definir o valor inicial de todas as fatias como 0

# Definir o valor da primeira fatia
series.slices()[0].setValue(50)  # Definir o valor da primeira fatia como 50

# Criar o QChart e adicionar o QPieSeries a ele
chart = QChart()
chart.addSeries(series)

# Criar o QChartView para exibir o gráfico
chart_view = QChartView(chart)

# Criar a janela principal e definir o QChartView como seu widget central
app = QApplication([])
window = QMainWindow()
window.setCentralWidget(chart_view)
window.show()

app.exec_()
