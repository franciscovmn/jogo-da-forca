import random
import os

# Declaração das variáveis globais
palavra_forca = ""
dica = ""
acertos = set()
max_tentativas = 6
saida = ""
pontuacao_atual = 0
indice = 0  # Adiciona a declaração de 'indice' como variável global
usuarios = {}  # Adiciona um dicionário global para armazenar os dados dos jogadores

# Função para escolher uma palavra em ordem do banco de palavras
def escolher_palavra(lista, palavras_adivinhadas, usuario_atual):
    global palavra_forca
    global dica
    global indice  # Adiciona 'indice' ao escopo global

    for indice in range(len(lista)):
        # Verifica se a palavra já foi adivinhada
        if indice not in palavras_adivinhadas:
            palavra_forca = lista[indice]
            partes = palavra_forca.split(';')
            dica = partes[1]
            palavra_forca = partes[0]

            # Verifica se o usuário já acertou a palavra
            if indice not in usuario_atual['palavras_adivinhadas']:
                return indice, palavra_forca, dica

def carregar_usuarios():
    try:
        with open("projeto-python/dados_jogadores.txt", 'r') as arquivo:
            usuarios = [linha.strip().split(';') for linha in arquivo.readlines()]
        return {apelido: {'pontuacao': int(pontuacao) if pontuacao else 0,
                          'palavras_adivinhadas': set(map(int, palavras.split(','))) if palavras else set()}
                for apelido, pontuacao, palavras in usuarios}
    except FileNotFoundError:
        return {}

# Função para salvar os dados dos jogadores em um arquivo
def salvar_usuarios(usuarios):
    with open("projeto-python/dados_jogadores.txt", 'w') as arquivo:
        for apelido, dados in usuarios.items():
            pontuacao = str(dados['pontuacao'])
            palavras = ','.join(map(str, dados['palavras_adivinhadas']))
            arquivo.write(f"{apelido};{pontuacao};{palavras}\n")

# Função para excluir um jogador do arquivo de dados
def excluir_jogador(arquivo, apelido):
    try:
        with open(arquivo, 'r') as f:
            linhas = f.readlines()
        with open(arquivo, 'w') as f:
            for linha in linhas:
                if not linha.startswith(f"{apelido};"):
                    f.write(linha)
    except FileNotFoundError:
        print(f"Arquivo {arquivo} não encontrado. Criando um novo arquivo.")

# Função principal para conduzir as tentativas do jogo da forca
def tentativas(palavras_adivinhadas, usuario_atual):
    global palavra_forca
    global acertos
    global max_tentativas
    global saida
    global pontuacao_atual
    global indice  # Adiciona 'indice' ao escopo global

    erros = 0
    saida = '*' * len(palavra_forca)
    acertos = set()
    pontuacao_atual = 0

    while '*' in saida and erros < max_tentativas:
        print(f"\nPalavra Atual: {saida}\nDica: {dica}")
        desenhar_forca(erros)

        tentativa_letra = input('Digite uma letra: ').lower()

        if len(tentativa_letra) == 1 and tentativa_letra.isalpha():
            if tentativa_letra in palavra_forca:
                acertos.add(tentativa_letra)
                atualizar_saida()
                pontuacao_atual += 10
                print("Letra correta!")
            else:
                print("Letra incorreta. Tente novamente.")
                erros += 1
        else:
            print("Por favor, digite uma única letra. Tente novamente.")

    if '*' not in saida:
        print("Parabéns! Você adivinhou a palavra:", palavra_forca)
        palavras_adivinhadas.add(indice)  # Adiciona a palavra acertada à lista
    else:
        print("Suas tentativas acabaram. A palavra era:", palavra_forca)
        desenhar_forca(erros)

# Função para desenhar a forca conforme os erros do jogador
def desenhar_forca(erros):
    if erros == 0:
        print('┌───┐')
        print('|')
    elif erros == 1:
        print('┌───┐')
        print('│   😐')
    elif erros == 2:
        print('┌───┐')
        print('│   😐')
        print('│   |')
    elif erros == 3:
        print('┌───┐')
        print('│   😐')
        print('│  /|')
    elif erros == 4:
        print('┌───┐')
        print('│   😐')
        print('│  /|\\')
    elif erros == 5:
        print('┌───┐')
        print('│   😐')
        print('│  /|\\')
        print('│  / ')
    elif erros == 6:
        print('┌───┐')
        print('│   😐')
        print('│  /|\\')
        print('│  / \\')

# Função para imprimir a palavra atual ocultando as letras não reveladas
def atualizar_saida():
    global palavra_forca
    global saida
    global acertos
    saida = ''
    for letra in palavra_forca:
        if letra in acertos or letra == '-':
            saida += letra
        else:
            saida += '*'

# Função principal para encerrar o programa
def encerrar_programa(usuarios):
    print("Encerrando o programa. Até mais!")
    salvar_usuarios(usuarios)

# Função principal para iniciar o jogo
def iniciar_jogo(lista):
    global palavra_forca
    global dica
    global usuarios

    usuarios = carregar_usuarios()

    # Menu principal
    while True:
        print("\nMenu Principal:")
        print("1. Jogar")
        print("2. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            apelido = input("Informe seu apelido (nickname): ")

            # Verifica se o apelido já existe
            if apelido in usuarios:
                print(f"\nBem-vindo de volta, {apelido}!")
                usuario_atual = usuarios[apelido]
            else:
                print(f"\nOlá, {apelido}! Um novo jogador foi criado para você.")
                usuario_atual = {'pontuacao': 0, 'palavras_adivinhadas': set()}

            continuar_jogando = True
            while continuar_jogando:
                indice, palavra_forca, dica = escolher_palavra(lista, usuario_atual['palavras_adivinhadas'], usuario_atual)
                tentativas(usuario_atual['palavras_adivinhadas'], usuario_atual)
                # Se acertou todas as palavras, imprime mensagem e apaga histórico do jogador
                if len(usuario_atual['palavras_adivinhadas']) == len(lista):
                    print('____________________________________________________________*')
                    print("Parabéns! Você acertou todas as palavras do jogo da forca!")
                    print('PONTUACAO:', usuario_atual.get('pontuacao', 0))
                    print('____________________________________________________________*')

                    usuario_atual['palavras_adivinhadas'] = set()
                    continuar_jogando = False

                    # Excluir o jogador vencedor do arquivo
                    excluir_jogador(apelido)

                else:
                    opcao_jogo = input("\nDeseja continuar jogando? (1 - Sim, 2 - Não): ")
                    if opcao_jogo != '1':
                        continuar_jogando = False

            # Atualiza ou insere o usuário no dicionário de usuários
            usuarios[apelido] = usuario_atual

            # Salva os dados dos jogadores no arquivo
            salvar_usuarios()

        elif opcao == '2':
            encerrar_programa(usuarios)
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    try:
        # Código para ler o arquivo e escolher a palavra
        arq_palavras = open("projeto-python/banco_de_palavras.txt", 'r')
        texto_palavras = arq_palavras.read()
        lista = texto_palavras.strip().split('\n')
        arq_palavras.close()

        # Iniciar o jogo
        iniciar_jogo(lista)

    except FileNotFoundError:
        print("Erro: O arquivo de palavras não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
