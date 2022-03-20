"""
Programa principal do projeto, para uso otimizado apenas
preenchendo as varáveis de entrada.
Variáveis de entrada
    - download_path: caminho da pasta onde o vídeo será baixado
    -  video_urls: os links dos vídeos do youtube
"""
from youtubedownloader import DownloadProcess, YoutubeVideo
from support import response
from pprint import pprint


#* VARIÁVEIS DE ENTRADA
download_path = r'C:\Users\FAEL\Downloads'.replace('\*','/')
video_urls = ['https://www.youtube.com/watch?v=fYR9L2ZmodM&t=57s']



# Variáveis de auxilio
anonymous_window = False
downloads = 0
problem_videos = []
persistence_of_problem_videos =  []
urls_error = []
urls_content = video_urls[:]


#* BAIXANDO OS VÍDEOS
"""
A estrutura for serve para fazer a operação duas vezes, caso ocorra
erros do site, apenas com os vídeos que deram erros. O outro for
serve para repetir o processo com todos os vídeos.
Dica: existem 2 linhas de comentários de código para otimização 
do tamanho da tela, caso queira personalizar o tamanho da tela use
o programa window_size.py.
"""
for c in range(1, 3, 1):
    if c == 2:
        urls_content = problem_videos[:]
        anonymous_window = not anonymous_window
    for url in urls_content:
        browser = YoutubeVideo(anonymous_mode=anonymous_window)
        process = DownloadProcess(browser, url, download_path)
        # browser.window_maximize()
        # browser.window_size(width=500, height=600)
        try:
            process.inicializate()
        except:
            response('erro na url')
            urls_error.append(url)
            browser.close()
            continue
        if process.filling():
            process.download()
            process.closing()
            if browser.jump_occurred == False and process.download_url_error == False:
                downloads += 1
            else:
                persistence_of_problem_videos.append(url)
            response(f'total de videos baixados: {downloads}',  wait=0.5,entity='program')
        else:
            browser.close()
            if c == 1:
                problem_videos.append(url)
            else:
                persistence_of_problem_videos.append(url)
    if len(problem_videos) == 0:
        break


#* RESPOSTA FINAL AO USUÁRIO - feedback final
if len(urls_error) == 0:
    if downloads == len(video_urls):
        response('Todos os vídeos foram baixados', wait=0.5, entity='program')
    else:
        print('program > Não pude baixar esses links:')
        pprint(persistence_of_problem_videos)
else:
    print('Urls com problema: ')
    pprint(urls_error)
    if len(persistence_of_problem_videos) > 0:
        print('program > Não pude baixar esses links:')
        pprint(persistence_of_problem_videos)
