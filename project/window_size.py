"""
Programa simples apenas para otimizar o tamanho da tela para programas
que utilizam selenium, os valores seram mostrados no terminal. 
Variáveis de entrada:
    - time (float): o tempo para você ajeitar a tela do navegador
      ao tamanho desejado.
"""
from web import SeleniumBrowser

time = 20

chrome = SeleniumBrowser()
width, height = chrome.get_window_size(time)

print(f'WIDTH: {width}')
print(f'HEIGHT: {height}')
