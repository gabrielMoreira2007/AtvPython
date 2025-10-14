import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os

# --- Lógica de Dados (Pandas) ---
class SistemaAlunos:
    """
    Gerencia a manipulação de dados dos alunos usando Pandas.
    """
    def __init__(self):
        # Inicializa um DataFrame vazio com as colunas necessárias
        self.df = pd.DataFrame(columns=['Nome', 'Idade', 'Curso', 'Nota Final'])

    def adicionar_aluno(self, nome, idade, curso, nota_final):
        """Adiciona um novo aluno ao DataFrame."""
        try:
            # Converte 'Idade' e 'Nota Final' para os tipos corretos
            nova_linha = pd.DataFrame([{
                'Nome': nome,
                'Idade': int(idade),
                'Curso': curso,
                'Nota Final': float(nota_final)
            }])
            self.df = pd.concat([self.df, nova_linha], ignore_index=True)
            return True
        except ValueError:
            return False # Retorna False se a conversão de tipo falhar

    def get_todos_alunos(self):
        """Retorna o DataFrame completo."""
        return self.df

    def filtrar_por_nota(self, media_minima):
        """Filtra alunos com nota acima da média mínima."""
        try:
            media = float(media_minima)
            df_filtrado = self.df[self.df['Nota Final'] >= media]
            return df_filtrado
        except ValueError:
            return pd.DataFrame() # Retorna um DataFrame vazio se a média não for um número

    def salvar_csv(self, filepath):
        """Salva o DataFrame atual em um arquivo CSV."""
        try:
            self.df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar CSV: {e}")
            return False

    def carregar_csv(self, filepath):
        """Carrega dados de um arquivo CSV para o DataFrame."""
        try:
            # Tenta ler o CSV, garantindo que as colunas sejam as esperadas
            df_carregado = pd.read_csv(filepath)
            colunas_esperadas = ['Nome', 'Idade', 'Curso', 'Nota Final']
            if all(coluna in df_carregado.columns for coluna in colunas_esperadas):
                # Converte os tipos de dados para garantir a consistência
                df_carregado['Idade'] = pd.to_numeric(df_carregado['Idade'], errors='coerce').astype('Int64')
                df_carregado['Nota Final'] = pd.to_numeric(df_carregado['Nota Final'], errors='coerce')
                self.df = df_carregado.dropna(subset=['Idade', 'Nota Final']) # Remove linhas com dados inválidos após conversão
                return True
            else:
                return False # Colunas incorretas
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return False

    def exportar_relatorio_csv(self, df_relatorio, filepath):
        """Exporta um DataFrame (relatório filtrado) para um novo CSV."""
        try:
            df_relatorio.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Erro ao exportar relatório CSV: {e}")
            return False

# --- Interface Gráfica (Tkinter) ---
class AplicacaoGUI:
    """
    Cria e gerencia a interface gráfica (GUI) usando Tkinter.
    """
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Gestão de Alunos")
        master.geometry("900x650")

        self.sistema = SistemaAlunos()

        # Configurações de estilo
        style = ttk.Style()
        style.configure("TFrame", padding=10)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        # Container principal
        main_frame = ttk.Frame(master)
        main_frame.pack(fill='both', expand=True)

        # 1. Frame de Cadastro (Topo)
        cadastro_frame = ttk.LabelFrame(main_frame, text="1. Cadastro de Aluno", padding="10 10")
        cadastro_frame.pack(fill='x', padx=10, pady=5)
        self.criar_frame_cadastro(cadastro_frame)

        # 2. Frame de Ações (Meio)
        acoes_frame = ttk.LabelFrame(main_frame, text="2. Ações do Sistema", padding="10 10")
        acoes_frame.pack(fill='x', padx=10, pady=5)
        self.criar_frame_acoes(acoes_frame)

        # 3. Frame da Tabela (Fundo)
        tabela_frame = ttk.LabelFrame(main_frame, text="3. Tabela de Alunos", padding="10 10")
        tabela_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.criar_tabela(tabela_frame)

        # Carrega dados iniciais se o arquivo existir (opcional)
        # self.carregar_dados_iniciais()

    def criar_frame_cadastro(self, parent):
        """Cria os campos de entrada para o cadastro."""
        campos = ['Nome:', 'Idade:', 'Curso:', 'Nota Final:']
        self.entradas = {}

        for i, campo in enumerate(campos):
            ttk.Label(parent, text=campo).grid(row=0, column=i * 2, padx=5, pady=5, sticky='w')
            entrada = ttk.Entry(parent, width=15)
            entrada.grid(row=0, column=i * 2 + 1, padx=5, pady=5, sticky='ew')
            self.entradas[campo.replace(':', '').strip()] = entrada

        # Botão Cadastrar
        ttk.Button(parent, text="Cadastrar Aluno", command=self.cadastrar_aluno).grid(
            row=0, column=len(campos) * 2, padx=10, pady=5, sticky='e')

    def criar_frame_acoes(self, parent):
        """Cria botões de salvar, carregar, filtrar e exportar."""
        # Salvar/Carregar
        ttk.Button(parent, text="Salvar CSV", command=self.salvar_csv).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Button(parent, text="Carregar CSV", command=self.carregar_csv).grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Filtro
        ttk.Label(parent, text="Média Mínima para Filtrar:").grid(row=0, column=2, padx=15, pady=5, sticky='e')
        self.entrada_media = ttk.Entry(parent, width=8)
        self.entrada_media.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.entrada_media.insert(0, "7.0") # Valor padrão

        ttk.Button(parent, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(parent, text="Mostrar Todos", command=self.mostrar_todos).grid(row=0, column=5, padx=5, pady=5)

        # Exportar
        ttk.Button(parent, text="Exportar Relatório Filtrado", command=self.exportar_relatorio).grid(
            row=0, column=6, padx=15, pady=5)
        
        # Variável para armazenar o último DataFrame filtrado para exportação
        self.df_filtrado_atual = self.sistema.get_todos_alunos()

    def criar_tabela(self, parent):
        """Cria o widget Treeview para exibir os dados."""
        colunas = ('Nome', 'Idade', 'Curso', 'Nota Final')

        self.tabela = ttk.Treeview(parent, columns=colunas, show='headings')
        self.tabela.pack(side="left", fill="both", expand=True)

        # Configura cabeçalhos
        for col in colunas:
            self.tabela.heading(col, text=col, anchor='center')
            self.tabela.column(col, anchor='center', width=120)

        # Adiciona barra de rolagem
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tabela.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=scrollbar.set)

        self.atualizar_tabela(self.sistema.get_todos_alunos())

    def atualizar_tabela(self, df):
        """Limpa e preenche a tabela com dados de um DataFrame."""
        # Limpa todos os itens existentes
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        # Adiciona as novas linhas
        for index, row in df.iterrows():
            # Usa tolist() para obter os valores como uma lista
            self.tabela.insert('', tk.END, values=row.tolist())

    # --- Métodos de Funcionalidades ---

    def cadastrar_aluno(self):
        """Pega os dados da GUI e os envia para o SistemaAlunos."""
        try:
            nome = self.entradas['Nome'].get().strip()
            idade = self.entradas['Idade'].get().strip()
            curso = self.entradas['Curso'].get().strip()
            nota_final = self.entradas['Nota Final'].get().strip()

            if not all([nome, idade, curso, nota_final]):
                messagebox.showerror("Erro de Cadastro", "Todos os campos devem ser preenchidos.")
                return

            if self.sistema.adicionar_aluno(nome, idade, curso, nota_final):
                self.atualizar_tabela(self.sistema.get_todos_alunos())
                # Limpa os campos após o cadastro
                for entrada in self.entradas.values():
                    entrada.delete(0, tk.END)
                messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")
                self.df_filtrado_atual = self.sistema.get_todos_alunos() # Atualiza o df de exportação
            else:
                messagebox.showerror("Erro de Cadastro", "Idade e Nota Final devem ser números válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def salvar_csv(self):
        """Abre a caixa de diálogo para salvar o arquivo CSV."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            title="Salvar Dados dos Alunos"
        )
        if filepath:
            if self.sistema.salvar_csv(filepath):
                messagebox.showinfo("Sucesso", f"Dados salvos com sucesso em:\n{filepath}")
            else:
                messagebox.showerror("Erro", "Falha ao salvar o arquivo CSV.")

    def carregar_csv(self):
        """Abre a caixa de diálogo para carregar um arquivo CSV."""
        filepath = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            title="Carregar Dados dos Alunos"
        )
        if filepath:
            if self.sistema.carregar_csv(filepath):
                self.atualizar_tabela(self.sistema.get_todos_alunos())
                messagebox.showinfo("Sucesso", f"Dados carregados com sucesso de:\n{filepath}")
                self.df_filtrado_atual = self.sistema.get_todos_alunos() # Atualiza o df de exportação
            else:
                messagebox.showerror("Erro", "Falha ao carregar o arquivo CSV. Verifique se o arquivo tem as colunas corretas (Nome, Idade, Curso, Nota Final) ou se há dados inválidos.")

    def aplicar_filtro(self):
        """Filtra a tabela com base na média mínima."""
        media_minima = self.entrada_media.get().strip()
        if not media_minima:
            messagebox.showwarning("Aviso", "Informe uma média mínima.")
            return

        df_filtrado = self.sistema.filtrar_por_nota(media_minima)

        if df_filtrado.empty and not self.sistema.get_todos_alunos().empty:
            messagebox.showinfo("Resultado do Filtro", "Nenhum aluno encontrado com nota acima da média mínima informada ou a média não é um número válido.")
            self.atualizar_tabela(df_filtrado)
            self.df_filtrado_atual = df_filtrado
        elif df_filtrado.empty and self.sistema.get_todos_alunos().empty:
             messagebox.showwarning("Aviso", "Não há dados cadastrados para filtrar.")
             self.df_filtrado_atual = df_filtrado
        else:
            self.atualizar_tabela(df_filtrado)
            self.df_filtrado_atual = df_filtrado
            messagebox.showinfo("Filtro Aplicado", f"Exibindo {len(df_filtrado)} aluno(s) com nota >= {media_minima}.")


    def mostrar_todos(self):
        """Limpa o filtro e exibe todos os alunos."""
        self.atualizar_tabela(self.sistema.get_todos_alunos())
        self.df_filtrado_atual = self.sistema.get_todos_alunos()
        messagebox.showinfo("Visualização", "Exibindo todos os alunos cadastrados.")

    def exportar_relatorio(self):
        """Exporta o último DataFrame filtrado (ou o completo) para um novo CSV."""
        if self.df_filtrado_atual.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar no relatório.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            title="Exportar Relatório Filtrado"
        )
        if filepath:
            if self.sistema.exportar_relatorio_csv(self.df_filtrado_atual, filepath):
                messagebox.showinfo("Sucesso", f"Relatório ({len(self.df_filtrado_atual)} registro(s)) exportado com sucesso em:\n{filepath}")
            else:
                messagebox.showerror("Erro", "Falha ao exportar o relatório CSV.")

# --- Execução Principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoGUI(root)
    root.mainloop()