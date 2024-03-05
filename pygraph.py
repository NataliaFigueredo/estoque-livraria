from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QPieSeries, QStackedBarSeries, QBarSet
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import sys

# Supondo que você já possui uma lista de valores obtidos da consulta no banco de dados
valores = [('o urso e o rouxinol', 14), ('joao e maria', 7), ('a arte da guerra', 45)]
print(type(valores), valores)
app = QApplication(sys.argv)

widget = QWidget()
layout = QVBoxLayout(widget)

# Cria um QChartView para exibir o gráfico
chart_view = QChartView(widget)

# Cria um QChart
chart = QChart()

# Cria uma série de dados para o gráfico
series = QPieSeries()

# Adiciona os valores e rótulos à série de dados
index = 0
for rotulo, valor in valores:
    if index == 0:
        slice = series.append(f'({valor})'+rotulo, float(valor))
        slice.setExploded(True)
        slice.setLabelVisible(True)
        index +=1
    series.append(rotulo, float(valor))
    #slice = series.append(rotulo, valor)
    # # slice.setLabel("{:.1f}%".format(slice.percentage() * 100))
    # series.append(slice)

# Adiciona a série de dados ao gráfico
chart.addSeries(series)

# Define o eixo X como índice da lista de valores
chart.createDefaultAxes()

# Define o título do gráfico
chart.setTitle("Gráfico de Valores")

# Habilita a antialiasing (suavização) do gráfico
chart.setTheme(QChart.ChartThemeLight)
chart.setAnimationOptions(QChart.AllAnimations)
chart_view.setRenderHint(QPainter.Antialiasing)

# Adiciona o QChart ao QChartView
chart_view.setChart(chart)

# Adiciona o QChartView ao layout do widget
layout.addWidget(chart_view)

widget.show()
sys.exit(app.exec_())
