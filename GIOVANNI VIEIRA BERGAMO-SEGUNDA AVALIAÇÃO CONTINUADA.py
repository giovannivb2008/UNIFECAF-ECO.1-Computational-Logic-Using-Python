saldo = 0.0
extrato = []



def depositar(valor):
    global saldo
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: + R$ {valor:.2f}")
        print(f"Sucesso! R$ {valor:.2f} adicionados.")
    else:
        print("Erro: O valor do depósito deve ser positivo.")

def sacar(valor):
    global saldo
    
    if valor > saldo:
        print(f"Operação negada! Saldo insuficiente (Saldo atual: R$ {saldo:.2f})")
    elif valor <= 0:
        print("Erro: O valor do saque deve ser positivo.")
    else:
        saldo -= valor
        extrato.append(f"Saque: - R$ {valor:.2f}")
        print(f"Sucesso! Retire seu dinheiro: R$ {valor:.2f}")

def mostrar_extrato():
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for movimentacao in extrato:
            print(movimentacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("==============================")

opcao = ""

while opcao != '4':
    print("\n===== MENU =====")
    print('1 - Adicionar Dinheiro')
    print('2 - Sacar dinheiro')
    print('3 - Mostrar Extrato')
    print('4 - Sair')
   
    opcao = input('Escolha uma opção: ')

    if opcao == '1':
        valor_deposito = float(input("Quanto deseja depositar? R$ "))
        depositar(valor_deposito)

    elif opcao == '2':
        valor_saque = float(input("Quanto deseja sacar? R$ "))
        sacar(valor_saque)

    elif opcao == '3':
        mostrar_extrato()

    elif opcao == '4':
        print("Obrigado por usar nosso banco! Até logo.")

    else:
        print("Opção inválida! Tente novamente.")