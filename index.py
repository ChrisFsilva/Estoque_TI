import sqlite3 as sq3 # Banco de dados
import tkinter as tk # Interface basica
from tkinter import messagebox # Caixas de mensagens
from tkinter import ttk # Interface grafica tb

# Função para conectar no banco de dados
def conectar ():
    return sq3.connect ('database.db')

# Função para organizar a tabela
def ordenar_coluna(coluna, reverso):
    dados = [(tree.set(k, coluna), k) for k in tree.get_children('')]
    try:
        dados.sort(key=lambda t: int(t[0]), reverse=reverso)
    except ValueError:
        dados.sort(key=lambda t: t[0].lower(), reverse=reverso)
    for index, (val, k) in enumerate(dados):
        tree.move(k,'', index)

    # Alterar a direção da proxima ordenação
    tree.heading(coluna, command = lambda: ordenar_coluna(coluna, not reverso))

# Função para criar tabela
def criar_tabela():
    conn = conectar()
    # Iniciar alterações do banco de dados
    c = conn.cursor()
    # Alterações que serão executadas
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipamentos(
        id INTEGER NOT NULL,
        hostname TEXT NOT NULL,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        tipo TEXT NOT NULL
        )
    ''')
    # Aplicar alteração no banco de dados
    conn.commit()
    # Encerrar acesso ao banco
    conn.close()

# Criar Item no banco 
def inserir_equipamento():
    serial = entry_serial.get()
    modelo = entry_modelo.get()
    marca = entry_marca.get()
    hostname = entry_hostname.get()
    tipo = combo_tipo.get()
    # Criar regra de inserção 'Se o serial e o modelo não estiver em branco'
    if serial and modelo:
        # Chamar função criar
        conn = conectar ()
        c = conn.cursor()
        c.execute('INSERT INTO equipamentos(id, hostname, marca, modelo, tipo) VALUES(?,?,?,?,?)', (serial, hostname, marca, modelo, tipo))
        conn.commit()
        conn.close()
        # Publicar mensagem
        messagebox.showinfo('AVISO', 'equipamento cadastrado com sucesso!')
        mostrar_equipamento()
    # Se der erro
    else:
        messagebox.showerror('ERRO','NÃO FOI POSSIVEL CADASTRAR O EQUIPAMENTO')

# Ler itens no banco
def mostrar_equipamento():
    # Limpar todas as linhas da árvore antes de adicionar os novos dados
    for row in tree.get_children():
        # Para cada linha na árvore, deleta as existentes
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    # Executa a consulta SQL para selecionar todos os dados da tabela 'equipamentos'
    c.execute('SELECT * FROM equipamentos')
    # Armazena todos os resultados da consulta na variável 'equipamentos'
    equipamentos = c.fetchall()
    # Para cada item na lista 'equipamentos'
    for equipamento in equipamentos:
        # Insere cada equipamento na árvore (Treeview)
        tree.insert("", "end", values=(equipamento[0], equipamento[1], equipamento[2],equipamento[3],equipamento[4]))
    conn.close()  

# Deletar item da lista
def delete_equipamento():
    # Atribuir dado a variavel
    dado_del = tree.selection()
    # Se variavel for invocada
    if dado_del:
        equip_id = tree.item(dado_del)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM equipamentos WHERE id = ?', (equip_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('','EQUIPAMENTO DELETADO')
        mostrar_equipamento()

    else:
        messagebox.showerror('ERRO','EQUIPAMENTO NÃO FOI DELETADO')

# Atualizar itens

def editar():
    selecao = tree.selection()
    if selecao:
        equip_id = tree.item(selecao)['values'][0]
        novo_hostname = entry_hostname.get()
        novo_marca = entry_marca.get()
        novo_modelo = entry_modelo.get()

        if novo_hostname and novo_marca and novo_modelo:
            conn = conectar()
            c = conn.cursor()
            c.execute('UPDATE equipamentos SET hostname = ?, marca = ?, modelo = ? WHERE id = ?', novo_hostname, novo_marca, novo_modelo, equip_id )
            conn.commit()
            conn.close()
            messagebox.showinfo('','EQUIPAMENTO ATUALIZADO COM SUCESSO')
            mostrar_equipamento()

        else:
            messagebox.showwarning('', 'PREENCHA TODOS OS CAMPOS')
    else:
        messagebox.showerror('','ALGO DEU ERRADO!')
    
# COMPLETANDO A INTERFACE GRAFICA

janela = tk.Tk()
janela.title('CRUD')


# Criando variavel e apresentação em tela do hostname

# Criando variavel e apresentação em tela serial Number
label_serial =tk.Label(janela, text = 'Serial Number/Service Tag: ')
label_serial.grid(row = 0, column = 0, padx = 0, pady = 1)
entry_serial = tk.Entry (janela)
entry_serial.grid( row = 0, column = 1, padx = 10, pady = 10)

label_hostname = tk.Label(janela, text = 'Hostname: ')
label_hostname.grid(row = 1, column = 0, padx = 10, pady = 10)
entry_hostname = tk.Entry (janela)
entry_hostname.grid(row = 1, column = 1, padx = 10, pady = 10)

# Criando variavel e apresentação em tela marca
label_marca =tk.Label(janela, text = 'Marca: ')
label_marca.grid(row = 2, column = 0, padx = 0, pady = 1)
entry_marca = tk.Entry (janela)
entry_marca.grid( row = 2, column = 1, padx = 10, pady = 10)

# Criando variavel e apresentação em tela do modelo
label_modelo = tk.Label(janela, text = 'Modelo: ')
label_modelo.grid(row = 3, column = 0, padx = 10, pady = 10)
entry_modelo = tk.Entry(janela)
entry_modelo.grid(row = 3, column = 1, padx = 10, pady = 10)


# Criando variavel e apresentação em tela do modelo
label_tipo = tk.Label(janela, text = 'Tipo de equipamento: ')
label_tipo.grid(row = 4, column = 0, padx = 10, pady = 10)
combo_tipo = ttk.Combobox(janela, values=["Notebook", "Desktop", "Servidor", "Impressora", "Switch", "Roteador","Outros"])
combo_tipo.grid(row = 4, column = 1, padx = 10, pady = 10)

# Criando Botões

# Criar o botão adicionar invocando a função 'inserir_equipamento' 
btn_adc = tk.Button(janela, text = 'Adicionar equipamento', command = inserir_equipamento)
# Localização do botão
btn_adc.grid(row = 1, column = 2, padx = 10, pady = 10)

# Criar botão deletar invocando a função 'delete_equipamento'
btn_deletar = tk.Button(janela, text = 'Excluir', command = delete_equipamento)
btn_deletar.grid(row = 2, column = 2, padx = 10, pady = 10)

# Criar botão atualizar invocando a função 'Editar'
btn_atualizar = tk.Button(janela, text='Atualizar informações', command = editar)
btn_atualizar.grid(row = 3, column = 2, padx = 10, pady = 10)

# Criar arvore
# Colunas da arvore
columns = ('Serial Number', 'Hostname', 'Marca', 'Modelo', 'tipo')

tree = ttk.Treeview(janela, columns = columns, show = 'headings')
tree.grid(row = 6, column = 0, columnspan = 2, padx = 10, pady = 10)

# 
for col in columns:
    tree.heading(col, text = col, command=lambda _col=col: ordenar_coluna(_col, False))

criar_tabela()
mostrar_equipamento()

janela.mainloop()