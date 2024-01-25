#Projeto elaborado por:
    # Andre Borili
    # Caio Alves
    # Carlos Augustin
    # Leonildo Linck
    # Rafael Vaz

import random  # Importando gerador randômico para horas.
import difflib  # Importando aproximação de strings, importante para tornar o chat mais amigável e evitar erros.
from tabulate import tabulate

resumo_pedido = list()  # Lista que irá guardar as pizzas selecionadas pelo cliente.
dados_cliente = list()  # Lista que irá guardar os dados do cliente, para ser printada na hora de fechar o pedido.
respostas_positivas = ['sim', 's', 'yes', 'ok', 'por favor', 'claro', 'blz', 'confirma',
                       'confirmar']  # Criação de uma lista com palavras genéricas para obter um SIM.
respostas_negativas = ['nao', 'não', 'n',
                       'no']  # Criação de uma lista com palavras genéricas relevantes para obter um NÃO.
atendimento_cardapio = ['menu', 'visualizar', 'cardapio', 'precos',
                        'sabores',
                        '1']  # Criação de uma lista com palavras  relevantes para a decisão de abrir o cardápio.
atendimento_pedido = ['pedido', 'pedir', 'realizar',
                      'comprar', '2']  # Criação de uma lista com palabras geréricas relevantes para o contexto.
atendimento_sair = ['sair', 'fechar', 'tchau', 'sai',
                    'adeus', '3']  # Criação de uma lista com palabras geréricas relevantes para o contexto.
cardapio = [
    ("Calabresa", 69.99),
    ("Mussarela", 49.99),
    ("Peperoni", 79.99),
    ("Margherita", 79.99),
    ("Vegetariana", 79.99),
    ("Frango com Catupiry", 69.99),
    ("Quatro Queijos", 69.99)
]  # Lista com os itens a serem vendidos.


def horario(hora): #Função que recebe a hora gerada pelo randInt e condiciona conforme o padrão de funcionamento do restaurante.
    if 17 <= hora < 18: #Das 17 às 18 será um boa tarde.
        saudacao = 'Boa tarde'
        return saudacao
    elif 18 <= hora <= 23: #Das 18 às 23 será um Boa noite.
        saudacao = 'Boa noite'
        return saudacao
    else:
        saudacao = 'Bom dia' #Tudo que não for isso, será um bom dia.
        return saudacao


def imprimir_cardapio(arg: object = 0) -> object: # Função para imprimir o cardárpio usando a biblioteca tabulate,
                                                  # economizando linhas e facilitando o trabalho no restante do código.

    #Basta inserir a lista e o tipo de grafico na função.
    print(tabulate(cardapio, headers=["Nome da Pizza", "R$ Preço"], tablefmt="grid"))

def pedido_dados(*args): #Uma função para colher dados do cliente e cupom de desconto.
    for arg in args:
        while True:
            dado = input(f'Por favor informe os seu {arg}: ')
            dados_cliente.append(dado) #lista onde os dados são guardados para posterior print ao final do pedido
            break
    pedido() #ao final ele é redirecionado para começar o pedido


def pedido(*args):  #Função que gerencia o pedido, essa é a maior função do programa, talvez devesse ter sido dividida em mais funções.
    while True:     #laço principal pque imprime o cardapio e controla o input
        imprimir_cardapio() # sempre é mostrado o cardápio antes de perguntar o sabor
        resposta = input('Vamos fazer o pedido? É só me dizer o sabor que deseja pedir: ')
        matches = difflib.get_close_matches(resposta, [item[0] for item in cardapio], n=1, cutoff=0.1) #biblioteca que recebe o input,
                                                                                                       #consulta e lista e retorna o valor corrigido da consulta.
        if not matches: #condição que retorna o laço se o matches não conseguir uma resposta
            print(f'Desculpe, não temos a pizza de "{resposta}". Vou perguntar novamente.')
            continue
        else: #SE o matches funcionar
            item_escolhido = matches[0] #atribuição do resultado a uma variável
            for tupla in cardapio: #um laço para comparar o valor retornado do match com a lista para atribuir o valor correspondente.
                if item_escolhido == tupla[0]:
                    preco = tupla[1]
                    if resposta != item_escolhido: #condição que corrige o sabor digita e o correto e manda para o cliente confirmar.
                        print(f'A pizza {resposta} não está no menu. Você quis dizer {item_escolhido}?')
                    else:
                        print(f'Você escolheu {item_escolhido}, ela está disponivel.') #caso o cliente digite corretamente o sabor da pizza.
            confirmacao = input(f'Posso confirmar {item_escolhido}? ').lower() #confirmação para inserir na lista resumo_pedido
            if confirmacao in respostas_positivas: #input consulta uma lista pré-definida de respostas
                while True: #laço para o opcional de borda recheada
                    pergunta_borda = input(
                        'Deseja o adicional de borda recheada com Catupiry por mais R$ 6,99? ').lower()
                    if pergunta_borda in respostas_negativas: #input consulta uma lista pré-definida de respostas
                        resumo_pedido.append(item_escolhido) #inserindo somente a pizza na lista resumo_pedidos
                        resumo_pedido.append(preco) #inserindo somente o valor da pizza na lista resumo_pedidos
                        print(f'Sem problemas, vamos de {item_escolhido} por R$ {preco}.')
                        break
                    else: #input consulta uma lista pré-definida de respostas
                        borda = 'Adicional de borda recheada'
                        preco_borda = 6.99 #valor da borda
                        resumo_pedido.append(item_escolhido) #inserindo a pizza na lista resumo_pedidos
                        resumo_pedido.append(preco) #inserido o preço da pizza na lista resumo_pedidos
                        resumo_pedido.append(borda) #inserindo o item bordana lista resumo_pedidos
                        resumo_pedido.append(preco_borda) #inserindo o valor do item borda na lista resumo_pedidos

                        print(
                            f'Pronto. Já anotei sua pizza de {item_escolhido} com adicional de borda no valor total de R$ {(preco + preco_borda):.2f}') #retorno do que foi selecionado para o cliente
                        break
        encerrar_pedido = input('Deseja encerrar o pedido? ').lower() #final do menu pedido
        if encerrar_pedido in respostas_negativas:
            continue
        else:
            imprimir_pedido(resumo_pedido) #chama a função de imprimir o pedido
            break


def imprimir_pedido(arg=0): #função que imprime o pedido
    entrega = 3.99 #taxa de entrega arbitrada, mas podendo futuramente ser calculada em uma função de entregadores
    print(f'{"-" * 27}RESUMO DO PEDIDO{"-" * 27}') #titulo
    print(f'{"Produto":<27} {"Quantidade":<14} {"Preço Unitário":<15} {"Preço Total":>1}') #cabeçalho
    for c in range(0, len(arg), 2): #laço que recebe a lista gerada pelo pedido e imprime formatada na tela
        print(f'{arg[c]:<32} {"1":<15} {arg[c + 1]:<15} {arg[c + 1]:.2f}'.rjust(69))
    print('-' * 70)
    subtotal = 0
    for i in range(1, len(arg), 2): #laço que percorre os valores e gera um subtotal
        subtotal += arg[i]
    print(f'Subtotal: {subtotal:.2f}'.rjust(69))
    print(f'Taxa de Entrega: R$ {entrega:.2f}'.rjust(69))
    cupom =0
    if dados_cliente[3].upper() == 'ADA10': #if que verifica se o cupom foi digitado corretamente.
        cupom = 10.00
        print(f'Cupom de desconto: R$ {cupom:.2f}'.rjust(69))
    else:
        print(f'Cupom de desconto: R$ {cupom:.2f}'.rjust(69))

    print('-' * 71)
    pagar = subtotal + entrega - cupom #calculando o valor total do pedido
    print(f'Total a pagar: R$ {pagar:.2f}'.rjust(69))
    print('-' * 71)
    print(f'Nome: {dados_cliente[0]}')
    print(f'Endereço de entrega: {dados_cliente[1]}')
    print(f'Forma de pagamento: {dados_cliente[2]}')
    print('-' * 71)
    sair()


def sair(*args):
    print('Obrigado e volte sempre, a Pizzaria Delicia agradece a sua preferência!') #mensagem de despedida

def main(*args): #Função principal, onde temos as boas vindas, a primeira interação e a primeira chamada pra função é feita.
                 #Não sei se a maneira que foi estrutura é a mais correta, com uma
                 #função chamando a outra, ou se todas deveriam retornar para o main() e partir daí a chamada de funções é feita
    hora = random.randint(00, 23) # horário de funcionamento entre 17 às 03h
    while 3 <= hora < 17: # Forçando o randInt a Não gerar um horário que não seja o de funcionamento.
        hora = random.randint(00, 23)

    nome = 'nome' # inserindo variáveis para reaproveitamento na função pedido_dados()
    endereco = 'endereço' # inserindo variáveis para reaproveitamento na função pedido_dados()
    pagamento = 'tipo de pagamento (Dinheiro, Cartão ou Pix)' # inserindo variáveis para reaproveitamento na função pedido_dados()
    cupom = 'cupom de desconto, se houver (dica: ADA10)' # inserindo variáveis para reaproveitamento na função pedido_dados()

    saudacao = horario(hora) #Chamando a função hora e definindo dentro de uma variável qual saudação é a mais apropriada.

    while True: #Loop para o menu principal do programa
        print(f'{saudacao}, seja bem vindo a Pizzaria Delícia!') #Boas vinda usando a função de horario
        print('Opções de atendimento: ') #menu principal, claro e direto.
        print('1. Visualizar Menu') #Note que se pode usar tanto números como respostas discursivas para seleção.
        print('2. Fazer Pedido') #Note que se pode usar tanto números como respostas discursivas para seleção.
        resposta = input(f'Gostaria de olhar nosso menu, fazer um pedido ou sair?').lower() #Note que se pode usar tanto números como respostas discursivas para seleção.
        if resposta in atendimento_cardapio: #input consulta uma lista pré-definida de respostas
            imprimir_cardapio() #direcionando para a função correspondente
        elif resposta in atendimento_pedido: #input consulta uma lista pré-definida de respostas
            imprimir_cardapio() #direcionando para a função correspondente
            pedido_dados(nome, endereco, pagamento, cupom)
            break
        else:
            print('Desculpe, não entendi sua resposta, vou perguntar novamente.')

main()
