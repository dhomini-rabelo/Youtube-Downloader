<h1>Youtube Downloader</h1>

<h2>Sobre</h2>
<p>Projeto python usando Selenium para treinar POO. O projeto consiste em um baixador de vídeos do Youtube.</p><br>

<h2>Como usar:</h2>
<li>Verifique a versão do seu Google Chrome, acesse <a href="chrome://settings/help" target="_blank">chrome://settings/help</a></li>
<li>Baixe a versão do chromedriver compatível com a versão do seu Chrome, link para download: <a href="https://chromedriver.chromium.org/downloads" target="_blank">https://chromedriver.chromium.org/downloads</a></li>
<li>Substitua o arquivo chromedrive.exe na pasta project</li>

<li>Crie ambiente virtual e instale as dependências de requirements.txt no seu ambiente virtual</li>

```
python -m venv venv
```

```
venv/Scripts/Activate.ps1 # if PowerShell
```

```
pip install -r requirements.txt
```

<li>Verifique se o botão para baixar do site "<a href="https://pt.savefrom.net/" target="_blank">https://pt.savefrom.net/</a>" tem o texto 'Baixar', se não tiver altere a variável da self.button_name da classe YoutubeVideo no arquivo youtubedownloader.py</li>
<li>Preencha as variáveis de entrada do main.py</li>
<li>Execute arquivo e pronto, seu(s) vídeo(s) estará na pasta download</li>


<h2>Resultado</h2>
<img src="./readme/result.PNG" alt="project-result" style="max-width: 100%; display: block; margin: 10px auto 0 0;">
<img src="./readme/files.PNG" alt="project-result" style="max-width: 100%; display: block; margin: 10px auto 0 0;">
