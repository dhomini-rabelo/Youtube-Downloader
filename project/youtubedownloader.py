"""
Arquivo python que possui a classe Youtube Video que é uma classe 
que trata o uso do selenium para efetuar download de vídeos do
youtube pela documentação do selenium, também possui a classe 
process que otimiza o processo. 
"""

from web import SeleniumBrowser
from support import download_checker, new_mp4_downloaded, mp4_videos_count, response, delete_crdownload
from selenium.webdriver.support.expected_conditions import presence_of_element_located as presence
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from time import sleep
import urllib3



class YoutubeVideo(SeleniumBrowser):
    """
    Trata as ações para que seja feito o download 
    """
    def __init__(self, wait_time=15, not_show_browser=False, fullscreen=False, anonymous_mode=False):
        """
        Faz as configurações de inicialização
        Args:
            wait_time (int, optional): Tempo de insistência usado no WebDriverWait, que otimiza a espera por aparição de elementos web. Defaults to 10.
            not_show_browser (bool, optional): Se deve funcionar com a api sendo executada. Defaults to False.
            fullscreen (bool, optional): Tela do browser em modo fullscreen. Defaults to False.
            anonymous_mode (bool, optional): Tela do browser em modo anônimo. Defaults to False.
        Variáveis:
            jump_ocurred (bool): informa se algum vídeo foi pulado pelo excesso
            de tempo de download
            self.video_url (str, None) : salva url do vídeo para ser usada num
            possível bug de não carregamento do site
        """
        super().__init__(wait_time=wait_time, not_show_browser=not_show_browser, fullscreen=fullscreen, anonymous_mode=anonymous_mode)
        self.jump_occurred = False 
        self.video_url = None
        self.button_name = 'Baixar'

    def open_savefrom(self, url):
        """
        Abre o site sevefrom.net com o atalho por link do youtube
        """
        official_url = url[:12] + 'ss' + url[12:]
        self.open(official_url)
        self.video_url = url
    
    def check_filling(self):
        """
        Checa por 15 segundos, por causa do wait_time declarado para o wdw, 
        se o vídeo foi carregado no site
        """
        sleep(5)
        try:
            self.wdw.until(method=presence((By.CSS_SELECTOR, 'div.media-result')), message='')
            return True
        except:
            return False

    def check_url_not_found(self):
        """
        Checa se o site informou que a url não foi encontrada
        """
        sleep(5)
        try:
            self.wdw.until(method=presence((By.CSS_SELECTOR, 'div[class*="result-box"]')), message='')
            return True
        except:
            return False

    def check_popup(self):
        """
        Checa se apareceu uma propaganda de extensão
        """
        try:
            sleep(3)
            popup = self.driver.find_element_by_css_selector('div[class="popup-content"]')
            popup.click()
            return True
        except:
            return False   

    def check_bug_image(self):
        """
        Checa se ocorreu um bug de imagem ao invés do vídeo ser disponibilizado 
        para download
        """
        try:
            sleep(3)
            popup = self.driver.find_element_by_css_selector('div[class="image-box ready"]')
            popup.click()
            return True
        except:
            return False   

    def get_download_archive_name(self):
        """
        Pega o nome vídeo através do botão de baixar
        """
        main_btn = self.driver.find_element_by_link_text(self.button_name)
        name = main_btn.get_attribute('download') 
        return name

    def filling(self):
        """
        Preenche a caixa de input do site com o com link do vÍdeo
        """
        input_box = self.driver.find_element_by_css_selector('input#sf_url')
        input_box.click()
        input_box.send_keys(self.video_url)
        input_box.send_keys(Keys.ENTER)

    def download(self):
        """
        Clica no botão de baixar e fecha todas as guias menos a do 
        download do vídeo
        """
        sleep(0.5)
        id = self.driver.current_window_handle
        id_save = id[:]
        btn = self.driver.find_element_by_link_text(self.button_name)
        response('tentei iniciar o download', entity='program')
        sleep(0.5)
        btn.click()
        response('fechando abas extras', wait=0.5)
        self.close_disposable_windows_for_page_id(id_save)

    def close_possible_alert(self):
        """
        Fecha o alerta se existir 
        """
        sleep(1)
        try: 
            Alert(self.driver).accept()
        except urllib3.exceptions.MaxRetryError:
            response('Alerta aceito e fechando chrome')
            self.jump_occurred = True
        except:
            pass
    
    def end(self, download_path, mp4_quantity):
        """
        Checa se o download encerrou ou tempo de 11,6 estorou assim,
        logo após ele fecha o navegador
        """
        rest_time = 3
        while True:
            sleep(rest_time)
            response('checando...', entity='program')
            if new_mp4_downloaded(download_path, mp4_quantity):
                self.close()
                response('navegador fechado', entity='program')
                break            
            elif rest_time == 113:
                self.close()
                self.close_possible_alert()
                response('navegador fechado', entity='program')
                break
            rest_time += 10


class DownloadProcess:
    """
    Essa classe serve para controlar processo de download do vídeo
    """
    def __init__(self, browserobj, video_url: str, download_path: str):
        """
            Faz as configurações de inicialização
        Args:
            browserobj (SeleniumBrowser): browser do selenium otimizado
            video_url (str): url do vídeo do youtube
            download_path (str): onde o vídeo será baixado
        Variáveis:
            download_url_error (bool): informa se deu erro após a tentative de
            download
            mp4_quantity ([int, None]): quantidade de vídeos .mp4 a pasta de download
            archive_name ([str, None]): Nome do vídeo baixado
        """
        self.browserobj = browserobj
        self.video_url = video_url
        self.download_path = download_path
        self.mp4_quantity = None
        self.archive_name = None
        self.download_url_error = False
    
    def inicializate(self):
        """
        Abre o vídeo de download, salva a quantidade de vídeos mp4 na pasta
        de download no início do processo, checa se existe popup, caso exista fecha o popup
        """
        self.browserobj.open_savefrom(self.video_url)
        self.mp4_quantity = mp4_videos_count(self.download_path)
        response('inicializando processo', entity='program')
        response('Entrei no site de download', wait=0.8,entity='program')
        response('procurando popup', wait=0.5)
        if self.browserobj.check_popup():
            sleep(2)
            response('encontrei um popup')
            popup_btn = self.browserobj.driver.find_element_by_css_selector('div[class*=close-modal]')
            popup_btn.click()
            response('Fechei o popup')
        else:
            response('nenhum popup encontrado')
    
    def filling(self):
        """
        Sua função principal é retornar se o vídeo está disponível ou não. 
        Checa se ocorreu o bug de imagem, se ele persiste durante 2 minutos, 
        também checa se o vídeo está disponível, se url foi encontrada. Caso
        o não tenha ocorrido erros ele preenche o vídeo na caixa de input do
        site.
        """
        response('Checando disponibilidade do vídeo', wait=0.5)
        if  self.browserobj.check_bug_image():
            response('Ocorreu um bug no carregamento do vídeo, aguarde um pouco')
            for c in range(1, 121):
                sleep(1)
                if c % 15 == 0:
                    response('checando se o bug persiste...')
                    if  not self.browserobj.check_bug_image():
                        response('bug finalizado')
                        return True
                if c == 120:
                    response('O bug persistiu, inicializando próximo download')
                    return False
        if self.browserobj.check_filling():
            response('O vídeo está disponível para download')
            return True
        elif self.browserobj.check_url_not_found():
            response('URL NÃO ENCONTRADA')
            return False
        else:
            response('Não está preenchido, irei preencher', wait=0.5)
            self.browserobj.filling()
            self.filling()

    def download(self):
        """
        Deleta se algum tiver algum arquivo de download, pega o nome do 
        arquivo, tenta iniciar o caso não ocorra erros, e termina seu 
        serviço quando o download começa ou termina dependendo do 
        tamanho do arquivo, além de informar caso o bug de url ocorra
        """
        delete_crdownload(self.download_path)
        self.archive_name = self.browserobj.get_download_archive_name()
        while True:
            try:
                self.browserobj.download()  
            except:
                self.download_url_error = True
                break
            sleep(3)
            if download_checker(self.download_path):
                response('Download em andamento')
                break
            elif new_mp4_downloaded(self.download_path, self.mp4_quantity):
                response('Download encerrado')
                break
            else:
                response('o download não foi iniciado')
    
    def closing(self):
        """
        Fecha o navegador e informa resultado da operação
        """
        response('Confirmando se o download foi encerrado', wait=0.3, entity='program')
        self.browserobj.end(self.download_path, self.mp4_quantity)
        if (not self.browserobj.jump_occurred) and (not self.download_url_error):
            response(f'{self.archive_name} baixado com sucesso', wait=0.4, entity='program')
            response('processo finalizado com sucesso', wait=0.3, entity='program')
        elif self.browserobj.jump_occurred:
            response('vídeo demora demais para baixar')
        elif self.download_url_error:
            response('o site não identificou essa url')
