import mysql.connector
from mysql.connector import Error
from datetime import datetime

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2814',
            database='projeto_vendas_eletronicos_unifecaf'
        )
        if conexao.is_connected():
            return conexao
    except Error as e:
        print(f"\n[!] Erro ao conectar ao MySQL: {e}")
        return None


def criar_produto():
    print("\n--- Cadastrar Novo Produto ---")
    descricao = input("Descrição do produto: ").strip()
    preco = float(input("Preço unitário: R$ "))

    conexao = conectar()
    if not conexao: return

    cursor = conexao.cursor()
    try:
        query = "INSERT INTO produtos (descricao, preco) VALUES (%s, %s)"
        cursor.execute(query, (descricao, preco))
        conexao.commit()
        print(f"[Sucesso] Produto '{descricao}' cadastrado com o ID {cursor.lastrowid}!")
    except Error as e:
        print(f"[Erro] Não foi possível cadastrar o produto: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_produtos():
    conexao = conectar()
    if not conexao: return

    cursor = conexao.cursor()
    try:
        query = "SELECT id, descricao, preco FROM produtos ORDER BY id"
        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            print("\nNenhum produto cadastrado.")
            return

        print("\nID   | Descrição                          | Preço")
        print("-" * 50)
        for idx, desc, preco in resultados:
            print(f"{idx:<4} | {desc:<34} | R$ {preco:.2f}")
    except Error as e:
        print(f"[Erro] Falha ao listar produtos: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_produto():
    print("\n--- Atualizar Produto ---")
    id_produto = int(input("Digite o ID do produto que deseja alterar: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
    
        cursor.execute("SELECT descricao, preco FROM produtos WHERE id = %s", (id_produto,))
        produto = cursor.fetchone()
        if not produto:
            print("[!] Produto não encontrado.")
            return
        
        print(f"Dados atuais -> Descrição: {produto[0]} | Preço: R$ {produto[1]:.2f}")
        nova_desc = input("Nova descrição (Deixe em branco para manter a atual): ").strip()
        novo_preco_str = input("Novo preço (Deixe em branco para manter o atual): ").strip()
        
        desc_final = nova_desc if nova_desc != "" else produto[0]
        preco_final = float(novo_preco_str) if novo_preco_str != "" else produto[1]
        
        query = "UPDATE produtos SET descricao = %s, preco = %s WHERE id = %s"
        cursor.execute(query, (desc_final, preco_final, id_produto))
        conexao.commit()
        print("[Sucesso] Produto atualizado com êxito!")
    except Error as e:
        print(f"[Erro] Falha na atualização: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_produto():
    print("\n--- Excluir Produto ---")
    id_produto = int(input("Digite o ID do produto para exclusão: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
       
        cursor.execute("SELECT COUNT(*) FROM vendas_produtos WHERE id_produto = %s", (id_produto,))
        if cursor.fetchone()[0] > 0:
            print("[Bloqueado] Não é possível excluir. Este produto está vinculado a vendas existentes.")
            return
            
        query = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(query, (id_produto,))
        conexao.commit()
        if cursor.rowcount > 0:
            print("[Sucesso] Produto removido do sistema.")
        else:
            print("[!] Produto não localizado.")
    except Error as e:
        print(f"[Erro] Não foi possível excluir: {e}")
    finally:
        cursor.close()
        conexao.close()


def criar_vendedor():
    print("\n--- Cadastrar Novo Vendedor ---")
    nome = input("Nome completo do vendedor: ").strip()

    conexao = conectar()
    if not conexao: return

    cursor = conexao.cursor()
    try:
        query = "INSERT INTO vendedores (nome) VALUES (%s)"
        cursor.execute(query, (nome,))
        conexao.commit()
        print(f"[Sucesso] Vendedor(a) '{nome}' cadastrado(a) com ID {cursor.lastrowid}!")
    except Error as e:
        print(f"[Erro] Falha ao cadastrar vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_vendedores():
    conexao = conectar()
    if not conexao: return

    cursor = conexao.cursor()
    try:
        query = "SELECT id, nome FROM vendedores ORDER BY id"
        cursor.execute(query)
        resultados = cursor.fetchall()

        if not resultados:
            print("\nNenhum vendedor cadastrado.")
            return

        print("\nID   | Nome Completo")
        print("-" * 40)
        for idx, nome in resultados:
            print(f"{idx:<4} | {nome}")
    except Error as e:
        print(f"[Erro] Falha ao listar vendedores: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_vendedor():
    print("\n--- Atualizar Vendedor ---")
    id_vendedor = int(input("Digite o ID do vendedor que deseja alterar: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT nome FROM vendedores WHERE id = %s", (id_vendedor,))
        vendedor = cursor.fetchone()
        if not vendedor:
            print("[!] Vendedor não encontrado.")
            return
            
        print(f"Nome atual: {vendedor[0]}")
        novo_nome = input("Novo nome: ").strip()
        
        if novo_nome == "":
            print("[Aviso] O nome não pode ser vazio. Operação cancelada.")
            return
            
        query = "UPDATE vendedores SET nome = %s WHERE id = %s"
        cursor.execute(query, (novo_nome, id_vendedor))
        conexao.commit()
        print("[Sucesso] Nome do vendedor atualizado!")
    except Error as e:
        print(f"[Erro] Falha ao atualizar vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_vendedor():
    print("\n--- Excluir Vendedor ---")
    id_vendedor = int(input("Digite o ID do vendedor para remoção: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
       
        cursor.execute("SELECT COUNT(*) FROM vendas WHERE id_vendedor = %s", (id_vendedor,))
        if cursor.fetchone()[0] > 0:
            print("[Bloqueado] Impossível remover. Este vendedor possui registros de vendas vinculados.")
            return
            
        query = "DELETE FROM vendedores WHERE id = %s"
        cursor.execute(query, (id_vendedor,))
        conexao.commit()
        if cursor.rowcount > 0:
            print("[Sucesso] Vendedor removido do banco.")
        else:
            print("[!] Vendedor não localizado.")
    except Error as e:
        print(f"[Erro] Falha ao excluir vendedor: {e}")
    finally:
        cursor.close()
        conexao.close()


def criar_venda_com_itens():  
    print("\n--- Criar Nova Venda com Itens ---")
    id_vendedor = int(input("ID do Vendedor responsável: "))
    desconto = float(input("Valor do Desconto (R$): "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
      
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO vendas (id_vendedor, data_e_hora, desconto, valor_final) VALUES (%s, %s, %s, 0.0)",
            (id_vendedor, data_atual, desconto)
        )
        id_venda = cursor.lastrowid
        
        valor_total_venda = 0.0
        
       
        while True:
            id_prod = int(input("\nID do Produto a comprar (ou 0 para encerrar os itens): "))
            if id_prod == 0: break
            
            
            cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_prod,))
            prod_dados = cursor.fetchone()
            if not prod_dados:
                print("[!] Produto inexistente. Tente outro ID.")
                continue
                
            preco_uni = float(prod_dados[0])
            qtd = int(input(f"Quantidade do produto: "))
            
            valor_total_item = preco_uni * qtd
            valor_total_venda += valor_total_item
            
            cursor.execute(
                "INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)",
                (id_venda, id_prod, qtd, preco_uni, valor_total_item)
            )
        

        valor_final_com_desconto = max(0.0, valor_total_venda - desconto)
        cursor.execute("UPDATE vendas SET valor_final = %s WHERE id = %s", (valor_final_com_desconto, id_venda))
        
        conexao.commit()
        print(f"\n[Sucesso] Venda Nº {id_venda} fechada com valor final de R$ {valor_final_com_desconto:.2f}!")
    except Error as e:
        conexao.rollback()
        print(f"[Erro] Falha completa na transação de venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def listar_vendas_completas():
    conexao = conectar()
    if not conexao: return

    cursor = conexao.cursor()
    try:
        
        query_vendas = """
            SELECT v.id, vd.nome, v.data_e_hora, v.desconto, v.valor_final 
            FROM vendas v
            INNER JOIN vendedores vd ON v.id_vendedor = vd.id
            ORDER BY v.id
        """
        cursor.execute(query_vendas)
        lista_vendas = cursor.fetchall()
        
        if not lista_vendas:
            print("\nNenhuma venda registrada até o momento.")
            return
            
        for id_venda, nome_vend, data, desc, final in lista_vendas:
            print(f"\n=======================================================")
            print(f" VENDA Nº: {id_venda} | Atendente: {nome_vend} | Data: {data}")
            print(f" Desconto aplicado: R$ {desc:.2f} | VALOR FINAL DA NOTA: R$ {final:.2f}")
            print(f"-------------------------------------------------------")
            print(f"   Item Produto              | Qtd | Val. Unitário | Total")
            
           
            cursor.execute("""
                SELECT p.descricao, vp.quantidade, vp.valor_unitario, vp.valor_total 
                FROM vendas_produtos vp
                INNER JOIN produtos p ON vp.id_produto = p.id
                WHERE vp.id_venda = %s
            """, (id_venda,))
            
            for desc_p, qtd, vu, vt in cursor.fetchall():
                print(f"   {desc_p:<25} | {qtd:<3} | R$ {vu:<11.2f} | R$ {vt:.2f}")
        print("=======================================================")
    except Error as e:
        print(f"[Erro] Falha ao ler relatório de vendas: {e}")
    finally:
        cursor.close()
        conexao.close()


def atualizar_venda_e_itens():
    print("\n--- Atualizar Venda e Itens ---")
    id_venda = int(input("Digite o ID da venda que deseja refazer/atualizar: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
      
        cursor.execute("SELECT id FROM vendas WHERE id = %s", (id_venda,))
        if not cursor.fetchone():
            print("[!] Nota de venda não localizada.")
            return
            
        print("[Aviso] Você irá redefinir os itens e o desconto desta venda.")
        novo_desconto = float(input("Digite o novo valor de desconto (R$): "))
        
        
        cursor.execute("DELETE FROM vendas_produtos WHERE id_venda = %s", (id_venda,))
        
      
        valor_total_venda = 0.0
        while True:
            id_prod = int(input("\nID do novo Produto (ou 0 para salvar): "))
            if id_prod == 0: break
            
            cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_prod,))
            prod_dados = cursor.fetchone()
            if not prod_dados:
                print("[!] Produto inválido.")
                continue
                
            preco_uni = float(prod_dados[0])
            qtd = int(input("Quantidade: "))
            
            valor_total_item = preco_uni * qtd
            valor_total_venda += valor_total_item
            
            cursor.execute(
                "INSERT INTO vendas_produtos (id_venda, id_produto, quantidade, valor_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)",
                (id_venda, id_prod, qtd, preco_uni, valor_total_item)
            )
            
        
        valor_final_com_desconto = max(0.0, valor_total_venda - novo_desconto)
        cursor.execute(
            "UPDATE vendas SET desconto = %s, valor_final = %s WHERE id = %s",
            (novo_desconto, valor_final_com_desconto, id_venda)
        )
        
        conexao.commit()
        print(f"[Sucesso] Venda Nº {id_venda} atualizada com sucesso! Novo Total: R$ {valor_final_com_desconto:.2f}")
    except Error as e:
        conexao.rollback()
        print(f"[Erro] Falha ao atualizar venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def excluir_venda():
    print("\n--- Excluir Nota de Venda ---")
    id_venda = int(input("Digite o ID da venda que deseja excluir: "))
    
    conexao = conectar()
    if not conexao: return
    
    cursor = conexao.cursor()
    try:
       
        cursor.execute("DELETE FROM vendas_produtos WHERE id_venda = %s", (id_venda,))
        
       
        cursor.execute("DELETE FROM vendas WHERE id = %s", (id_venda,))
        
        conexao.commit()
        print(f"[Sucesso] Venda {id_venda} e todos os seus itens associados foram removidos!")
    except Error as e:
        conexao.rollback()
        print(f"[Erro] Falha ao excluir venda: {e}")
    finally:
        cursor.close()
        conexao.close()


def menu():
    opcoes = {
        "1": ("Criar produto", criar_produto),
        "2": ("Listar produtos", listar_produtos),
        "3": ("Atualizar produto", atualizar_produto),
        "4": ("Excluir produto", excluir_produto),
        "5": ("Criar vendedor", criar_vendedor),
        "6": ("Listar vendedores", listar_vendedores),
        "7": ("Atualizar vendedor", atualizar_vendedor),
        "8": ("Excluir vendedor", excluir_vendedor),
        "9": ("Criar venda com itens", criar_venda_com_itens),
        "10": ("Listar vendas completas", listar_vendas_completas),
        "11": ("Atualizar venda e itens", atualizar_venda_e_itens),
        "12": ("Excluir venda", excluir_venda),
    }

    while True:
        print("\n=== MENU AC4 - CRUD COMPLETO ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Sair do Sistema")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Desconectando do sistema de gerenciamento. Até logo!")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\n[Executando] {descricao}...")
            funcao()  
        else:
            print("Opcao invalida. Tente novamente.")

if __name__ == "__main__":
    menu()