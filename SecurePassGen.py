import random
import string
import time
import os
import sys

# Instala automaticamente os pacotes necessários
try:
    import pyfiglet
except ImportError:
    print("pyfiglet não encontrado. Instalando automaticamente...")
    os.system(f"{sys.executable} -m pip install pyfiglet")
    import pyfiglet

try:
    import colorama
    from colorama import Fore, Style
except ImportError:
    print("colorama não encontrado. Instalando automaticamente...")
    os.system(f"{sys.executable} -m pip install colorama")
    import colorama
    from colorama import Fore, Style

# Inicializa o colorama
colorama.init(autoreset=True)

# Classe para facilitar o uso de cores no terminal
class Cores:
    VERDE = Fore.GREEN
    VERMELHO = Fore.RED
    AMARELO = Fore.YELLOW
    AZUL = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CIANO = Fore.CYAN
    BRANCO = Fore.WHITE
    RESETAR = Style.RESET_ALL

# Gera senha com base na dificuldade escolhida pelo jogador
def gerar_senha_dificuldade(dificuldade):
    if dificuldade == "1":  # Fácil
        return gerar_senha(6, incluir_simbolos=False)
    elif dificuldade == "2":  # Média
        return gerar_senha(10, incluir_simbolos=True)
    elif dificuldade == "3":  # Difícil
        return gerar_senha(16, incluir_simbolos=True)
    return gerar_senha()

# Função principal de geração de senhas
def gerar_senha(tamanho=12, incluir_simbolos=True):
    caracteres = string.ascii_letters + string.digits
    if incluir_simbolos:
        caracteres += string.punctuation
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# Avalia a força da senha com base em critérios simples
def calcular_forca_senha(senha):
    forca = 0
    if len(senha) >= 8: forca += 1
    if any(char.isdigit() for char in senha): forca += 1
    if any(char.islower() for char in senha): forca += 1
    if any(char.isupper() for char in senha): forca += 1
    if any(char in string.punctuation for char in senha): forca += 1
    return forca

# Exibe a força da senha com cores e retorna a pontuação
def exibir_forca(senha):
    forca = calcular_forca_senha(senha)
    if forca < 2:
        print(Cores.VERMELHO + "Senha Fraca!")
    elif forca < 4:
        print(Cores.AMARELO + "Senha Moderada!")
    else:
        print(Cores.VERDE + "Senha Forte!")
    return forca

# Animação de carregamento simples
def animacao(texto, cor=Cores.AZUL):
    print(cor + texto)
    for _ in range(3):
        print(cor + ".", end="", flush=True)
        time.sleep(0.5)
    print()

# Artes visuais para vitória ou derrota em batalhas fictícias

def arte_vitoria_hacker():
    print(Cores.MAGENTA + r"""
     _______                               
    |@_@_@_|     Código Ataca!              
    ( ° ͜ʖ °)   >>   [HACKER] 😱            
   /|     |\    ========>>                 
  /_|_____|_\     ||                       
    |_|_|_|      /  \                      
                /____\                    
    """)

def arte_vitoria_trasher():
    print(Cores.MAGENTA + r"""
     _______                               
    |@_@_@_|     Código Ataca!              
    ( ° ͜ʖ °)   >>   [TRASHER] 😱           
   /|     |\    ========>>                 
  /_|_____|_\     ||                       
    |_|_|_|      /  \                      
                /____\                    
    """)

def arte_derrota():
    print(Cores.VERMELHO + r"""
     _______                               
    |@_@_@_|     Código Ataca!              
    ( ° ͜ʖ °)   >>   [DERROTA] 😱           
   /|     |\    ========>>                 
  /_|_____|_\     ||                       
    |_|_|_|      /  \                      
                /____\                    
    """)

# Exibe o título estilizado do jogo
def arte_titulo():
    os.system('cls' if os.name == 'nt' else 'clear')
    titulo = pyfiglet.figlet_format("Secure Pass")
    print(Cores.CIANO + titulo)
    print(Cores.AZUL + "Desenvolvido por Rafael Oliveira - v1.0\n")
    print(Cores.AMARELO + "Derrote o Trasher e o Hacker usando senhas fortes!\n")

# Simula batalha contra os inimigos com base na força da senha
def batalhar(inimigo, forca):
    animacao(f"\nVocê está enfrentando o {inimigo}!")
    if inimigo == "Trasher" and forca >= 2:
        print(Cores.MAGENTA + f"Você derrotou o {inimigo} com sua senha!")
        arte_vitoria_trasher()
        print("sua senha é: " + Cores.VERDE + f"{forca}")
    elif inimigo == "Hacker" and forca >= 4:
        print(Cores.VERDE + f"Você derrotou o {inimigo} com sua senha!")
        arte_vitoria_hacker()
    else:
        print(Cores.VERMELHO + f"Você foi derrotado pelo {inimigo}!")
        arte_derrota()
        print(Cores.VERMELHO + "Tente novamente com uma senha mais forte!")
        input("\nPressione Enter para voltar ao menu...")
        return False
    return True

# Menu de escolha de dificuldade da senha
def escolher_senha():
    print(Cores.CIANO + "\nEscolha a dificuldade da senha:")
    print("1 - Fácil")
    print("2 - Média")
    print("3 - Difícil")
    escolha = input("Digite o número da opção: ")
    senha = gerar_senha_dificuldade(escolha)
    print(Cores.VERDE + f"\nSenha gerada: {senha}")
    forca = exibir_forca(senha)
    return senha, forca

# Exibe o menu principal do jogo
def menu_principal():
    arte_titulo()
    print("1. Jogar")
    print("2. Sair")
    return input("\nEscolha uma opção: ")

# Função principal que controla o fluxo do jogo
def main():
    while True:
        opcao = menu_principal()
        if opcao == "1":
            arte_titulo()
            senha, forca = escolher_senha()

            if not batalhar("Trasher", forca):
                continue  # volta ao menu principal
            input("\nPressione Enter para enfrentar o Hacker...")

            if not batalhar("Hacker", forca):
                continue
            print(Cores.VERDE + "\nParabéns! Você venceu todos os inimigos!")
            input("\nPressione Enter para voltar ao menu...")

        elif opcao == "2":
            print(Cores.AZUL + "\nSaindo... até logo!")
            break
        else:
            print(Cores.VERMELHO + "Opção inválida!")
            time.sleep(1)

# Executa o jogo se este arquivo for executado diretamente
if __name__ == "__main__":
    main()