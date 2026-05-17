import mysql.connector
from mysql.connector import Error

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



def total_vendas_periodo():
   
    print("\n--- Filtro de Período ---")
    data_inicio = input("Digite a data inicial (AAAA-MM-DD): ").strip()
    data_fim = input("Digite a data final (AAAA-MM-DD): ").strip()
    
    conexao = conectar()
    if not conexao: return "Falha na conexão"
    
    cursor = conexao.cursor()
    try:
        query = "SELECT SUM(valor_final), COUNT(id) FROM vendas WHERE DATE(data_e_hora) BETWEEN %s AND %s"
        cursor.execute(query, (data_inicio, data_fim))
        total, qtd = cursor.fetchone()
        
        if total is None:
            return f"Nenhuma venda encontrada entre {data_inicio} e {data_fim}."
        return f"Período: {data_inicio} até {data_fim}\nQtd de Vendas: {qtd}\nFaturamento Total: R$ {total:.2f}"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def qtd_vendas_por_vendedor():
    
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT v.nome, COUNT(vd.id) 
            FROM vendas vd
            INNER JOIN vendedores v ON vd.id_vendedor = v.id
            GROUP BY vd.id_vendedor
            ORDER BY COUNT(vd.id) DESC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        retorno = "Vendedor ------------ Qtd Vendas\n"
        for nome, qtd in resultados:
            retorno += f"{nome:<20} {qtd} vendas\n"
        return retorno
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def ticket_medio_geral():
    
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = "SELECT AVG(valor_final) FROM vendas"
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        if resultado is None: return "Sem vendas registradas."
        return f"O Ticket Médio Geral das vendas é: R$ {resultado:.2f}"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def ticket_medio_por_vendedor():
    
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT v.nome, AVG(vd.valor_final) 
            FROM vendas vd
            INNER JOIN vendedores v ON vd.id_vendedor = v.id
            GROUP BY vd.id_vendedor
            ORDER BY AVG(vd.valor_final) DESC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        retorno = "Vendedor ------------ Ticket Médio\n"
        for nome, media in resultados:
            retorno += f"{nome:<20} R$ {media:.2f}\n"
        return retorno
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def produto_mais_vendido_qtd():

    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT p.descricao, SUM(vp.quantidade) 
            FROM vendas_produtos vp
            INNER JOIN produtos p ON vp.id_produto = p.id
            GROUP BY vp.id_produto
            ORDER BY SUM(vp.quantidade) DESC
            LIMIT 1
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        if not resultado: return "Nenhum produto vendido."
        return f"Campeão em Quantidade: {resultado[0]} ({resultado[1]} unidades vendidas)"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def produto_mais_rentavel_valor():
    
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT p.descricao, SUM(vp.valor_total) 
            FROM vendas_produtos vp
            INNER JOIN produtos p ON vp.id_produto = p.id
            GROUP BY vp.id_produto
            ORDER BY SUM(vp.valor_total) DESC
            LIMIT 1
        """
        cursor.execute(query)
        resultado = cursor.fetchone()
        if not resultado: return "Nenhum faturamento registrado."
        return f"Campeão em Faturamento: {resultado[0]} (Arrecadou: R$ {resultado[1]:.2f})"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def total_descontos_aplicados():
   
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = "SELECT SUM(desconto) FROM vendas"
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        if resultado is None: return "Nenhum desconto aplicado até o momento."
        return f"O valor total de descontos cedidos aos clientes foi: R$ {resultado:.2f}"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def percentual_desconto_medio():

    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = "SELECT AVG(desconto / (valor_final + desconto) * 100) FROM vendas WHERE (valor_final + desconto) > 0"
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        if resultado is None: return "Sem dados suficientes para calcular."
        return f"A média percentual de desconto aplicada nas vendas foi de: {resultado:.2f}%"
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def faturamento_por_dia():
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT DATE(data_e_hora), SUM(valor_final) 
            FROM vendas 
            GROUP BY DATE(data_e_hora)
            ORDER BY DATE(data_e_hora) ASC
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        retorno = "Data ---------- Faturamento Diário\n"
        for data, total in resultados:
            retorno += f"{str(data)} ---- R$ {total:.2f}\n"
        return retorno
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()


def top_3_vendedores_faturamento():
    conexao = conectar()
    if not conexao: return "Falha na conexão."
    
    cursor = conexao.cursor()
    try:
        query = """
            SELECT v.nome, SUM(vd.valor_final) 
            FROM vendas vd
            INNER JOIN vendedores v ON vd.id_vendedor = v.id
            GROUP BY vd.id_vendedor
            ORDER BY SUM(vd.valor_final) DESC
            LIMIT 3
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        retorno = "=== PÓDIO TOP 3 VENDEDORES ===\n"
        posicao = 1
        for nome, total in resultados:
            retorno += f"{posicao}º Lugar: {nome:<20} - Faturou: R$ {total:.2f}\n"
            posicao += 1
        return retorno
    except Error as e:
        return f"Erro SQL: {e}"
    finally:
        cursor.close()
        conexao.close()

def menu_relatorios():
    opcoes = {
        "1": ("Total de vendas por periodo", total_vendas_periodo),
        "2": ("Quantidade de vendas por vendedor", qtd_vendas_por_vendedor),
        "3": ("Ticket medio geral", ticket_medio_geral),
        "4": ("Ticket medio por vendedor", ticket_medio_por_vendedor),
        "5": ("Produto mais vendido por quantidade", produto_mais_vendido_qtd),
        "6": ("Produto mais rentavel por faturamento", produto_mais_rentavel_valor),
        "7": ("Total de descontos aplicados", total_descontos_aplicados),
        "8": ("Percentual medio de desconto", percentual_desconto_medio),
        "9": ("Faturamento por dia", faturamento_por_dia),
        "10": ("Top 3 vendedores por faturamento", top_3_vendedores_faturamento),
    }

    while True:
        print("\n=== MENU AC3 - RELATORIOS ===")
        for codigo, (descricao, _) in opcoes.items():
            print(f"{codigo} - {descricao}")
        print("0 - Voltar")

        escolha = input("Escolha uma opcao: ").strip()

        if escolha == "0":
            print("Obrigado por sua presença.")
            break

        if escolha in opcoes:
            descricao, funcao = opcoes[escolha]
            print(f"\nGerando relatorio: {descricao}")
            resultado = funcao()

            if resultado is None:
                print("Relatorio em estrutura base (return vazio).")
            else:
                print("\n-----------------------------------------")
                print(resultado)
                print("-----------------------------------------")
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    menu_relatorios()