"""
Archivo python para dar suporte com funções importantes para main.py e youtubedowloader.py
"""
from time import sleep
from pathlib import Path
from random import randint
import shutil as pc


def fpath(path:str):
    """
    Otimiza a entrada de um caminho para a função Path,
    recomendamos que se use raw strings como entrada,
    nome completo da função é Format Path
    Args:
        path (str): caminho de pastas
    Returns:
        (str): retorna caminho adaptado 
    """
    bar = '\*'
    new_path = path.replace(bar[0], '/')
    return new_path


def download_checker(path: str):
    """
    Checa se download está em andamento
    Args:
        path (str): caminho de pastas

    Returns:
        (Bool): se download está em andamento
    """
    for archive in Path(fpath(path)).iterdir():
        if archive.suffix == '.crdownload':
            return True
    return False


def new_mp4_downloaded(path: str, mp4_videos: int):
    """
    Retorna resposta ao usuário sobre possível novo download de 
    arquivo de extensão .mp4
    Args:
        path (str): caminho de pastas
        mp4_videos (int): parâmetro para saber se novo vídeo foi baixado
    Returns:
        (Bool): Se um novo vídeo .mp4 foi baixado 
    """
    mp4_archives_path = mp4_videos_count(path)
    if mp4_archives_path == mp4_videos:
        return False
    return True




def mp4_videos_count(path: str):
    """
    Conta quantos vídeos .mp4 existe em uma pasta
    Args:
        path (str): caminho onde contará
    Returns:
        (int): quantidade de vídeos .mp4 na pasta
    """
    mp4_archives_path = [archive for archive in Path(fpath(path)).iterdir() if archive.suffix == '.mp4']
    return len(mp4_archives_path)


def response(msg: str, wait=0, entity='browser'):
    """
    Função que mostra um feedback ao usuário 
    Args:
        msg (str): feedback que será mostrado
        wait (int, optional): tempo de espera para vários response não sejam executados juntos. Defaults to 0.
        entity (str, optional): "Entidade" que executa  a ação. Defaults to 'browser'.
    """
    sleep(wait)
    print(f'{entity} > [ {msg.lower()} ]')


def generate_name():
    """
    Gera um nome aleatório
    Returns:
        name (str): nome aleatório
    """
    n = randint(1, 100000)
    return f'name{n}'


def create_dels():
    """
    Cria a pasta dels
    """
    if not Path('dels').exists():
        Path('dels').mkdir()
        sleep(1)


def delete_crdownload(download_path: str):
    """
    Função que esconde todos os arquivos .crdownload de determinada pasta
    Args:
        download_path (str): caminho da pasta onde é feito o download
    """
    for archive in Path(fpath(download_path)).iterdir():
        if archive.suffix == '.crdownload':
            path = archive
            name = path.name
            suffix = path.suffix
            create_dels()
            while Path(f'dels/{name}').exists():
                sleep(0.5)
                new_name = f'{generate_name()}{suffix}'
                Path(path).rename(new_name)
                sleep(0.5)
                path = new_name
                name = new_name
            pc.move(Path(path), Path('dels'))


