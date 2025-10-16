import tkinter as tk     
from tkinter import ttk, filedialog, messagebox  
import pandas as pd                 
import os                           

# classe lógica pandas 

class SistemaAlunos:
    """
    Classe responsável pela manipulação dos dados dos alunos usando Pandas.
    """

    def __init__(self):
        # Cria um DataFrame vazio com as colunas desejadas
        self.df = pd.DataFrame(columns=['Nome', 'Idade', 'Curso', 'Nota Final'])

    def adicionar_aluno(self, nome, idade, curso, nota_final):
        """Adiciona um novo aluno ao DataFrame."""
        try:
            # Converte idade e nota para número (tratando erros)
            nova_linha = pd.DataFrame([{
                'Nome': nome,
                'Idade': int(idade),
                'Curso': curso,
                'Nota Final': float(nota_final)
            }])
            # Adiciona a nova linha ao DataFrame existente
            self.df = pd.concat([self.df, nova_linha], ignore_index=True)
            return True
        except ValueError:
            # Se a conversão falhar, retorna False
            return False

    def get_todos_alunos(self):
        """Retorna o DataFrame completo com todos os alunos."""
        return self.df

    def filtrar_por_nota(self, media_minima):
        """Retorna apenas alunos com nota >= média mínima."""
        try:
            media = float(media_minima)
            df_filtrado = self.df[self.df['Nota Final'] >= media]
            return df_filtrado
        except ValueError:
            # Retorna DataFrame vazio se a média for inválida
            return pd.DataFrame()

    def salvar_csv(self, filepath):
        """Salva o DataFrame em um arquivo CSV."""
        try:
            self.df.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar CSV: {e}")
            return False

    def carregar_csv(self, filepath):
        """Carrega um arquivo CSV no DataFrame."""
        try:
            df_carregado = pd.read_csv(filepath)
            colunas_esperadas = ['Nome', 'Idade', 'Curso', 'Nota Final']

            # Verifica se o arquivo tem as colunas corretas
            if all(coluna in df_carregado.columns for coluna in colunas_esperadas):
                # Converte os tipos de dados para manter consistência
                df_carregado['Idade'] = pd.to_numeric(df_carregado['Idade'], errors='coerce').astype('Int64')
                df_carregado['Nota Final'] = pd.to_numeric(df_carregado['Nota Final'], errors='coerce')
                # Remove linhas com dados inválidos
                self.df = df_carregado.dropna(subset=['Idade', 'Nota Final'])
                return True
            else:
                return False
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")
            return False

    def exportar_relatorio_csv(self, df_relatorio, filepath):
        """Exporta um DataFrame (filtrado ou completo) para um novo CSV."""
        try:
            df_relatorio.to_csv(filepath, index=False)
            return True
        except Exception as e:
            print(f"Erro ao exportar relatório CSV: {e}")
            return False


# parte de interface grafica tkinter 

class AplicacaoGUI:
    """
    Classe responsável por criar e gerenciar a interface gráfica (GUI).
    """
    def __init__(self, master):
        # Configurações da janela principal
        self.master = master
        master.title("Sistema de Gestão de Alunos")
        master.geometry("900x650")

        # Instancia o sistema de alunos
        self.sistema = SistemaAlunos()

        # --- Estilos visuais ---
        style = ttk.Style()
        style.configure("TFrame", padding=10)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=5)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        # Frame principal
        main_frame = ttk.Frame(master)
        main_frame.pack(fill='both', expand=True)

        # --- 1. Seção de Cadastro ---
        cadastro_frame = ttk.LabelFrame(main_frame, text="1. Cadastro de Aluno", padding="10 10")
        cadastro_frame.pack(fill='x', padx=10, pady=5)
        self.criar_frame_cadastro(cadastro_frame)

        # --- 2. Seção de Ações ---
        acoes_frame = ttk.LabelFrame(main_frame, text="2. Ações do Sistema", padding="10 10")
        acoes_frame.pack(fill='x', padx=10, pady=5)
        self.criar_frame_acoes(acoes_frame)

        # --- 3. Tabela ---
        tabela_frame = ttk.LabelFrame(main_frame, text="3. Tabela de Alunos", padding="10 10")
        tabela_frame.pack(fill='both', expand=True, padx=10, pady=5)
        self.criar_tabela(tabela_frame)

#    criação das sessões (frames) 

    def criar_frame_cadastro(self, parent):
        """Cria os campos e botão do cadastro."""
        campos = ['Nome:', 'Idade:', 'Curso:', 'Nota Final:']
        self.entradas = {}

        # Cria rótulos e campos de entrada
        for i, campo in enumerate(campos):
            ttk.Label(parent, text=campo).grid(row=0, column=i * 2, padx=5, pady=5, sticky='w')
            entrada = ttk.Entry(parent, width=15)
            entrada.grid(row=0, column=i * 2 + 1, padx=5, pady=5, sticky='ew')
            self.entradas[campo.replace(':', '').strip()] = entrada

        # Botão de cadastro
        ttk.Button(parent, text="Cadastrar Aluno", command=self.cadastrar_aluno).grid(
            row=0, column=len(campos) * 2, padx=10, pady=5, sticky='e')

    def criar_frame_acoes(self, parent):
        """Cria botões para salvar, carregar, filtrar e exportar dados."""
        # Botões de salvar/carregar
        ttk.Button(parent, text="Salvar CSV", command=self.salvar_csv).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Button(parent, text="Carregar CSV", command=self.carregar_csv).grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Campo e botão de filtro
        ttk.Label(parent, text="Média Mínima para Filtrar:").grid(row=0, column=2, padx=15, pady=5, sticky='e')
        self.entrada_media = ttk.Entry(parent, width=8)
        self.entrada_media.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.entrada_media.insert(0, "7.0")  # Valor padrão

        ttk.Button(parent, text="Aplicar Filtro", command=self.aplicar_filtro).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(parent, text="Mostrar Todos", command=self.mostrar_todos).grid(row=0, column=5, padx=5, pady=5)

        # Botão para exportar relatório filtrado
        ttk.Button(parent, text="Exportar Relatório Filtrado", command=self.exportar_relatorio).grid(
            row=0, column=6, padx=15, pady=5)

        # Guarda o último DataFrame usado para exportação
        self.df_filtrado_atual = self.sistema.get_todos_alunos()

    def criar_tabela(self, parent):
        """Cria a tabela (Treeview) que mostra os alunos."""
        colunas = ('Nome', 'Idade', 'Curso', 'Nota Final')

        self.tabela = ttk.Treeview(parent, columns=colunas, show='headings')
        self.tabela.pack(side="left", fill="both", expand=True)

        # Define cabeçalhos e largura
        for col in colunas:
            self.tabela.heading(col, text=col, anchor='center')
            self.tabela.column(col, anchor='center', width=120)

        # Adiciona uma barra de rolagem vertical
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.tabela.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabela.configure(yscrollcommand=scrollbar.set)

        # Preenche inicialmente com os dados (vazio)
        self.atualizar_tabela(self.sistema.get_todos_alunos())

    # funções de funcionalidade 

    def atualizar_tabela(self, df):
        """Atualiza os dados da tabela com base em um DataFrame."""
        self.tabela.delete(*self.tabela.get_children())  # Limpa a tabela
        for _, row in df.iterrows():
            self.tabela.insert('', tk.END, values=row.tolist())  # Insere cada linha

    def cadastrar_aluno(self):
        """Lê os dados dos campos e adiciona um aluno."""
        try:
            nome = self.entradas['Nome'].get().strip()
            idade = self.entradas['Idade'].get().strip()
            curso = self.entradas['Curso'].get().strip()
            nota_final = self.entradas['Nota Final'].get().strip()

            # Verifica se todos os campos estão preenchidos
            if not all([nome, idade, curso, nota_final]):
                messagebox.showerror("Erro de Cadastro", "Todos os campos devem ser preenchidos.")
                return

            # Tenta adicionar ao sistema
            if self.sistema.adicionar_aluno(nome, idade, curso, nota_final):
                self.atualizar_tabela(self.sistema.get_todos_alunos())
                # Limpa campos
                for entrada in self.entradas.values():
                    entrada.delete(0, tk.END)
                messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com sucesso!")
                self.df_filtrado_atual = self.sistema.get_todos_alunos()
            else:
                messagebox.showerror("Erro", "Idade e Nota Final devem ser números válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def salvar_csv(self):
        """Permite ao usuário salvar os dados em um arquivo CSV."""
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
        """Permite ao usuário carregar dados de um arquivo CSV."""
        filepath = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            title="Carregar Dados dos Alunos"
        )
        if filepath:
            if self.sistema.carregar_csv(filepath):
                self.atualizar_tabela(self.sistema.get_todos_alunos())
                messagebox.showinfo("Sucesso", f"Dados carregados com sucesso de:\n{filepath}")
                self.df_filtrado_atual = self.sistema.get_todos_alunos()
            else:
                messagebox.showerror("Erro", "Falha ao carregar o CSV. Verifique se o arquivo tem as colunas corretas.")

    def aplicar_filtro(self):
        """Filtra alunos pela nota mínima informada."""
        media_minima = self.entrada_media.get().strip()
        if not media_minima:
            messagebox.showwarning("Aviso", "Informe uma média mínima.")
            return

        df_filtrado = self.sistema.filtrar_por_nota(media_minima)

        if df_filtrado.empty and not self.sistema.get_todos_alunos().empty:
            messagebox.showinfo("Resultado", "Nenhum aluno encontrado com nota acima da média.")
        elif df_filtrado.empty and self.sistema.get_todos_alunos().empty:
            messagebox.showwarning("Aviso", "Não há dados cadastrados.")
        else:
            messagebox.showinfo("Filtro Aplicado", f"Exibindo {len(df_filtrado)} aluno(s) com nota >= {media_minima}.")
        self.atualizar_tabela(df_filtrado)
        self.df_filtrado_atual = df_filtrado

    def mostrar_todos(self):
        """Mostra todos os alunos novamente (remove o filtro)."""
        self.atualizar_tabela(self.sistema.get_todos_alunos())
        self.df_filtrado_atual = self.sistema.get_todos_alunos()
        messagebox.showinfo("Visualização", "Exibindo todos os alunos.")

    def exportar_relatorio(self):
        """Exporta o relatório (dados filtrados ou todos) para CSV."""
        if self.df_filtrado_atual.empty:
            messagebox.showwarning("Aviso", "Não há dados para exportar.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            title="Exportar Relatório Filtrado"
        )
        if filepath:
            if self.sistema.exportar_relatorio_csv(self.df_filtrado_atual, filepath):
                messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso em:\n{filepath}")
            else:
                messagebox.showerror("Erro", "Falha ao exportar o relatório.")

#  para executar o programa 

if __name__ == "__main__":
    root = tk.Tk()              
    app = AplicacaoGUI(root)     
    root.mainloop()              
