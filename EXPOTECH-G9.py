import mysql.connector
from datetime import datetime

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2814',
            database='expotech_g9'
        )
        if conexao.is_connected():
            return conexao
    except mysql.connector.Error as e:
        print(f"\n[!] Erro ao conectar ao MySQL: {e}")
        return None


def cadastrar_cliente():
    print("\n=== CADASTRO DE NOVO CLIENTE (GAMER) ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    nome = input("Digite o nome completo do cliente: ")
    email = input("Digite o e-mail: ")
    telefone = input("Digite o telefone: ")
    nickname = input("Digite o Nickname do Gamer: ")
    
    comando_sql = """
        INSERT INTO tbl_clientes (nome_cliente, email_cliente, telefone_cliente, nickname_cliente) 
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(comando_sql, (nome, email, telefone, nickname))
    conexao.commit()
    print(f"\n{nickname} cadastrado com sucesso! 🎮")
    cursor.close()
    conexao.close()

def listar_clientes():
    print("\n" + "="*73)
    print("===              LISTA DE GAMERS CADASTRADOS NA LAN                   === ")
    print("="*73 + "\n")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id_cliente, nome_cliente, nickname_cliente, email_cliente, telefone_cliente FROM tbl_clientes")
    for cliente in cursor.fetchall():
        print(f"ID: {cliente[0]} | Nick: {cliente[2]} | Nome: {cliente[1]}")
        print(f"E-mail: {cliente[3]} | Telefone: {cliente[4]}")
        print("-" * 73)
    cursor.close()
    conexao.close()

def atualizar_cliente():
    print("\n=== ATUALIZAÇÃO INTELIGENTE DE CADASTRO ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    id_cliente = input("Digite o ID do cliente que deseja atualizar: ")
    
    cursor.execute("SELECT nome_cliente, nickname_cliente, email_cliente, telefone_cliente FROM tbl_clientes WHERE id_cliente = %s", (id_cliente,))
    cliente_atual = cursor.fetchone()
    if not cliente_atual:
        print("❌ Cliente não encontrado!")
        cursor.close()
        conexao.close()
        return
        
    nome_antigo, nickname_antigo, email_antigo, telefone_antigo = cliente_atual
    print("\n--- Pressione ENTER para manter o dado atual ---")
    novo_nome = input(f"Nome atual [{nome_antigo}]: ")
    novo_nick = input(f"Nickname atual [{nickname_antigo}]: ")
    novo_email = input(f"E-mail atual [{email_antigo}]: ")
    novo_tel = input(f"Telefone atual [{telefone_antigo}]: ")
    
    nome_final = novo_nome if novo_nome != "" else nome_antigo
    nickname_final = novo_nick if novo_nick != "" else nickname_antigo
    email_final = novo_email if novo_email != "" else email_antigo
    telefone_final = novo_tel if novo_tel != "" else telefone_antigo
    
    comando_sql = """
        UPDATE tbl_clientes 
        SET nome_cliente = %s, nickname_cliente = %s, email_cliente = %s, telefone_cliente = %s 
        WHERE id_cliente = %s
    """
    cursor.execute(comando_sql, (nome_final, nickname_final, email_final, telefone_final, id_cliente))
    conexao.commit()
    print(f"\nCadastro do cliente ID {id_cliente} foi updated! 🔄")
    cursor.close()
    conexao.close()

def deletar_cliente():
    print("\n=== EXCLUSÃO DE CLIENTE ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    id_cliente = input("Digite o ID do cliente que deseja DELETAR: ")
    
    cursor.execute("DELETE FROM tbl_sessoes WHERE id_cliente = %s", (id_cliente,))
    cursor.execute("DELETE FROM tbl_clientes WHERE id_cliente = %s", (id_cliente,))
    conexao.commit()
    print(f"\nCliente ID {id_cliente} e históricos foram removidos! ❌")
    cursor.close()
    conexao.close()


def cadastrar_maquina():
    print("\n=== CADASTRO DE NOVA MÁQUINA ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    nome = input("Nome da máquina (ex: PC-06): ")
    tipo = input("Tipo (PC ou Console): ")
    status = input("Status inicial (Livre, Ocupada, Manutencao): ")
    valor = input("Valor por hora: ")
    
    comando_sql = """
        INSERT INTO tbl_maquinas (nome_maquina, tipo_maquina, status_maquina, valor_hora_maquina) 
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(comando_sql, (nome, tipo, status, valor))
    conexao.commit()
    print(f"\nMáquina {nome} cadastrada! 🖥️")
    cursor.close()
    conexao.close()

def listar_maquinas():
    print("\n" + "="*60)
    print("===                MÁQUINAS DA LAN HOUSE                ===")
    print("="*60 + "\n")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id_maquina, nome_maquina, tipo_maquina, status_maquina, valor_hora_maquina FROM tbl_maquinas")
    for maq in cursor.fetchall():
        print(f"ID: {maq[0]} | Nome: {maq[1]} | Tipo: {maq[2]}")
        print(f"Status: {maq[3]} | Valor/Hora: R$ {maq[4]}")
        print("-" * 60)
    cursor.close()
    conexao.close()

def atualizar_maquina():
    print("\n=== ALTERAR STATUS / DADOS DA MÁQUINA ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    id_maquina = input("Digite o ID da máquina que deseja alterar: ")
    
    cursor.execute("SELECT nome_maquina, tipo_maquina, status_maquina, valor_hora_maquina FROM tbl_maquinas WHERE id_maquina = %s", (id_maquina,))
    maquina_atual = cursor.fetchone()
    if not maquina_atual:
        print("❌ Máquina não encontrada!")
        cursor.close()
        conexao.close()
        return
        
    nome_antigo, tipo_antigo, status_antigo, valor_antigo = maquina_atual
    print("\n--- Pressione ENTER para manter o dado atual ---")
    novo_nome = input(f"Nome [{nome_antigo}]: ")
    novo_tipo = input(f"Tipo [{tipo_antigo}]: ")
    novo_status = input(f"Status [{status_antigo}]: ")
    novo_valor = input(f"Valor/Hora [{valor_antigo}]: ")
    
    nome_final = novo_nome if novo_nome != "" else nome_antigo
    tipo_final = novo_tipo if novo_tipo != "" else tipo_antigo
    status_final = novo_status if novo_status != "" else status_antigo
    valor_final = novo_valor if novo_valor != "" else valor_antigo
    
    comando_sql = """
        UPDATE tbl_maquinas 
        SET nome_maquina = %s, tipo_maquina = %s, status_maquina = %s, valor_hora_maquina = %s 
        WHERE id_maquina = %s
    """
    cursor.execute(comando_sql, (nome_final, tipo_final, status_final, valor_final, id_maquina))
    conexao.commit()
    print(f"\nMáquina ID {id_maquina} atualizada! 🔄")
    cursor.close()
    conexao.close()

def deletar_maquina():
    print("\n=== REMOVER MÁQUINA DO SISTEMA ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    id_maquina = input("Digite o ID da máquina que deseja REMOVER: ")
    
    cursor.execute("DELETE FROM tbl_sessoes WHERE id_maquina = %s", (id_maquina,))
    comando_sql = "DELETE FROM tbl_maquinas WHERE id_maquina = %s"
    cursor.execute(comando_sql, (id_maquina,))
    conexao.commit()
    print(f"\nMáquina ID {id_maquina} foi removida! ❌")
    cursor.close()
    conexao.close()


def cadastrar_sessao():
    print("\n=== REGISTRAR NOVA SESSÃO INTELIGENTE ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    id_cli = input("ID do Cliente (Gamer): ")
    id_maq = input("ID da Máquina: ")
    
    print("Use o formato igual ao do banco (Exemplo: 2026-05-20 14:00:00)")
    inicio_str = input("Início (AAAA-MM-DD HH:MM:SS): ")
    fim_str = input("Fim (AAAA-MM-DD HH:MM:SS): ")
    
    try:
        formato = "%Y-%m-%d %H:%M:%S"
        data_inicio = datetime.strptime(inicio_str, formato)
        data_fim = datetime.strptime(fim_str, formato)
        
        diferenca = data_fim - data_inicio
        tempo_total_minutos = int(diferenca.total_seconds() / 60)
        
        if tempo_total_minutos <= 0:
            print("❌ Erro: O horário de fim deve ser maior que o horário de início!")
            cursor.close()
            conexao.close()
            return

        cursor.execute("SELECT valor_hora_maquina FROM tbl_maquinas WHERE id_maquina = %s", (id_maq,))
        resultado_maquina = cursor.fetchone()
        
        if not resultado_maquina:
            print("❌ Erro: Máquina não encontrada!")
            cursor.close()
            conexao.close()
            return
            
        valor_hora_maquina = float(resultado_maquina[0])
        valor_total_calculado = (tempo_total_minutos / 60) * valor_hora_maquina
        
        print("\n--- 🧮 CÁCULO AUTOMÁTICO REALIZADO ---")
        print(f"Tempo total de jogo: {tempo_total_minutos} minutos")
        print(f"Valor da máquina por hora: R$ {valor_hora_maquina:.2f}")
        print(f"Valor total a cobrar: R$ {valor_total_calculado:.2f}")
        print("--------------------------------------")
        
        comando_sql = """
            INSERT INTO tbl_sessoes (id_cliente, id_maquina, inicio, fim, tempo_total, valor_total) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(comando_sql, (id_cli, id_maq, inicio_str, fim_str, tempo_total_minutos, valor_total_calculado))
        conexao.commit()
        
        print(f"\nSessão registrada e valor cobrado com sucesso! 🕹️💰")
        
    except ValueError:
        print("❌ Erro: Formato de data/hora inválido! Digite exatamente como o exemplo.")
        
    cursor.close()
    conexao.close()

def listar_sessoes():
    print("\n" + "="*70)
    print("===                HISTÓRICO DE SESSÕES / USO                  === ")
    print("="*70 + "\n")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    cursor.execute("SELECT id_sessao, id_cliente, id_maquina, inicio, fim, tempo_total, valor_total FROM tbl_sessoes")
    for ses in cursor.fetchall():
        print(f"Sessão nº: {ses[0]} | Gamer (ID): {ses[1]} | Máquina (ID): {ses[2]}")
        print(f"Período: De {ses[3]} até {ses[4]}")
        print(f"Tempo: {ses[5]} min | Valor Total: R$ {ses[6]}")
        print("-" * 70)
        
    cursor.close()
    conexao.close()

def atualizar_sessao():
    print("\n=== ATUALIZAÇÃO DE SESSÃO (CÁLCULO AUTOMÁTICO) ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    id_sessao = input("Digite o ID da sessão que deseja atualizar: ")
    try:
        cursor.execute("SELECT id_cliente, id_maquina, inicio, fim FROM tbl_sessoes WHERE id_sessao = %s", (id_sessao,))
        sessao_atual = cursor.fetchone()
        if not ...:
            print("❌ Sessão não encontrada!")
            return
            
        id_cli_antigo, id_maq_antigo, inicio_antigo, fim_antigo = sessao_atual
        
        inicio_antigo_str = inicio_antigo.strftime("%Y-%m-%d %H:%M:%S") if inicio_antigo else ""
        fim_antigo_str = fim_antigo.strftime("%Y-%m-%d %H:%M:%S") if fim_antigo else ""
        
        print("\n--- Pressione ENTER para manter o dado atual ---")
        novo_cli = input(f"ID Cliente [{id_cli_antigo}]: ")
        novo_maq = input(f"ID Máquina [{id_maq_antigo}]: ")
        novo_inicio = input(f"Início [{inicio_antigo_str}]: ")
        novo_fim = input(f"Fim [{fim_antigo_str}]: ")
        
        cli_final = novo_cli if novo_cli != "" else id_cli_antigo
        maq_final = novo_maq if novo_maq != "" else id_maq_antigo
        inicio_final_str = novo_inicio if novo_inicio != "" else inicio_antigo_str
        fim_final_str = novo_fim if novo_fim != "" else fim_antigo_str
        
        formato = "%Y-%m-%d %H:%M:%S"
        data_inicio = datetime.strptime(inicio_final_str, formato)
        data_fim = datetime.strptime(fim_final_str, formato)
        
        tempo_total_minutos = int((data_fim - data_inicio).total_seconds() / 60)
        
        if tempo_total_minutos <= 0:
            print("❌ Erro: O horário de fim deve ser maior que o horário de início!")
            return
            
        cursor.execute("SELECT valor_hora_maquina FROM tbl_maquinas WHERE id_maquina = %s", (maq_final,))
        resultado_maquina = cursor.fetchone()
        if not resultado_maquina:
            print("❌ Erro: Máquina não encontrada!")
            return
            
        valor_hora = float(resultado_maquina[0])
        valor_total_calculado = (tempo_total_minutos / 60) * valor_hora
        
        comando_sql = """
            UPDATE tbl_sessoes 
            SET id_cliente = %s, id_maquina = %s, inicio = %s, fim = %s, tempo_total = %s, valor_total = %s 
            WHERE id_sessao = %s
        """
        cursor.execute(comando_sql, (cli_final, maq_final, inicio_final_str, fim_final_str, tempo_total_minutos, valor_total_calculado, id_sessao))
        conexao.commit()
        print(f"\nSessão ID {id_sessao} atualizada e valores recalculados com sucesso! 🔄💰")
        
    except ValueError:
        print("❌ Erro: Formato de data/hora inválido!")
    except mysql.connector.Error as e:
        print(f"[Erro] Falha ao atualizar sessão: {e}")
    finally:
        cursor.close()
        conexao.close()

def deletar_sessao():
    print("\n=== REMOVER REGISTRO DE SESSÃO ===")
    conexao = conectar_banco()
    if not conexao: return
    cursor = conexao.cursor()
    
    id_sessao = input("Digite o ID da sessão que deseja REMOVER: ")
    try:
        cursor.execute("SELECT id_sessao FROM tbl_sessoes WHERE id_sessao = %s", (id_sessao,))
        if not cursor.fetchone():
            print("❌ Sessão não encontrada!")
            return
            
        confirmar = input(f"Tem certeza que deseja apagar a sessão ID {id_sessao}? (S/N): ").strip().upper()
        if confirmar == 'S':
            cursor.execute("DELETE FROM tbl_sessoes WHERE id_sessao = %s", (id_sessao,))
            conexao.commit()
            print(f"\nSessão ID {id_sessao} foi removida do histórico! ❌")
        else:
            print("Operação cancelada.")
            
    except mysql.connector.Error as e:
        print(f"[Erro] Falha ao deletar sessão: {e}")
    finally:
        cursor.close()
        conexao.close()


while True:
    print("\n" + "="*40)
    print("    SISTEMA DE GESTÃO - LAN HOUSE     ")
    print("="*40)
    print("[1] Gerenciar Clientes (Gamers)")
    print("[2] Gerenciar Máquinas (PCs/Consoles)")
    print("[3] Gerenciar Sessões (Tempo/Uso)")
    print("[0] Sair do Sistema")
    print("="*40)
    
    opcao_menu = input("Escolha uma opção: ")

    if opcao_menu == "1":
        while True:
            print("\n--- MENU: GERENCIAR CLIENTES ---")
            print("[1] Cadastrar Novo Gamer")
            print("[2] Listar Gamers")
            print("[3] Atualizar Dados de Gamer")
            print("[4] Deletar Gamer")
            print("[0] Voltar ao Menu Principal")
            op = input("Escolha uma opção: ")
            if op == "1": cadastrar_cliente()
            elif op == "2": listar_clientes()
            elif op == "3": atualizar_cliente()
            elif op == "4": deletar_cliente()
            elif op == "0": break
            else: print("❌ Opção inválida!")
            input("\nPressione ENTER para continuar...")
        continue  

    elif opcao_menu == "2":
        while True:
            print("\n--- MENU: GERENCIAR MÁQUINAS ---")
            print("[1] Cadastrar Nova Máquina")
            print("[2] Listar Máquinas da Lan")
            print("[3] Alterar Dados/Status da Máquina")
            print("[4] Remover Máquina")
            print("[0] Voltar ao Menu Principal")
            op = input("Escolha uma opção: ")
            if op == "1": cadastrar_maquina()
            elif op == "2": listar_maquinas()
            elif op == "3": atualizar_maquina()
            elif op == "4": deletar_maquina()
            elif op == "0": break
            else: print("❌ Opção inválida!")
            input("\nPressione ENTER para continuar...")
        continue  

    elif opcao_menu == "3":
        while True:
            print("\n--- MENU: GERENCIAR SESSÕES ---")
            print("[1] Registrar Nova Sessão")
            print("[2] Listar Histórico de Sessões")
            print("[3] Atualizar Dados de Sessão")
            print("[4] Remover Registro de Sessão")
            print("[0] Voltar ao Menu Principal")
            op = input("Escolha uma opção: ")
            if op == "1": cadastrar_sessao()
            elif op == "2": listar_sessoes()
            elif op == "3": atualizar_sessao()
            elif op == "4": deletar_sessao()
            elif op == "0": break
            else: print("❌ Opção inválida!")
            input("\nPressione ENTER para continuar...")
        continue  

    elif opcao_menu == "0":
        print("\nObrigado por usar o sistema da Lan House! Até mais. 🕹️")
        break
    else:
        print("\n❌ Opção inválida! Tente novamente.")