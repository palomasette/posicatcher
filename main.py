import logging
import pandas as pd
import shutil
import os
import tkinter as tk
from tkinter import filedialog
import openpyxl
import subprocess
import warnings
import threading
from pathlib import Path
from sinqiaconn import Connect

class PosiCatcher:
    def __init__(self):
        self.arquivo_xlsx = None
        self.janela = tk.Tk()
        self.janela.title("PosiCatcher")
        self.janela.geometry("500x150")
        self.janela.resizable(False, False)
        self.janela.configure(bg='gray20')
        
        self.texto_arquivo = tk.Label(self.janela, text="Nenhum arquivo selecionado", fg='yellow', bg='gray20')
        self.texto_arquivo.pack(pady=10)
        
        estilo_botao = {'bg': 'cyan', 'fg': 'black'}
        
        self.botao_importar = tk.Button(self.janela, text="Importar Arquivo", command=self.importar_arquivo, **estilo_botao)
        self.botao_importar.pack(pady=10)
        
        self.botao_processar = tk.Button(self.janela, text="Processar Arquivo", command=self.executar_processo, **estilo_botao)
        self.botao_processar.pack(pady=10)
        
        # Configurando o logger
        logging.basicConfig(filename='log.txt', level=logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(console_handler)
        warnings.filterwarnings("ignore")
        subprocess.call('cls', shell=True)

    def importar_arquivo(self):
        self.arquivo_xlsx = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
        if self.arquivo_xlsx:
            self.texto_arquivo.config(text=f'Arquivo selecionado: {self.arquivo_xlsx}')

    def file_not_empty(self, arquivo):
        with open(arquivo, 'r') as arquivo:
            linhas = arquivo.readlines()
        numero_de_linhas = len(linhas)
        if numero_de_linhas < 3:
            return False
        return True

    def rename_txt_file_from_downloads(self, old_name, new_name):
        downloads_path = str(Path.home() / "Downloads")
        path_new_name = os.path.join(downloads_path, new_name)
        try:
            os.rename(old_name, path_new_name)
            return path_new_name
        except OSError as e:
            print(f"Erro ao renomear o arquivo: {e}")

    def processar_arquivo(self):
        if self.arquivo_xlsx:
            workbook = openpyxl.load_workbook(self.arquivo_xlsx)
            df = pd.read_excel(self.arquivo_xlsx)
            df['carteira'] = df['carteira'].astype(str)
            df['cliente'] = df['cliente'].astype(str)

            for index, row in df.iterrows():
                cliente = row['cliente']
                fundo = row['carteira']

                # logs
                logging.info(70 * "*")
                logging.info(f"Cliente {cliente} | Fundo {fundo}\n")

                con = Connect()
                folder_cli = "FUNDO_" + fundo
                file_name45 = f"45_cliente{cliente}_fundo{fundo}.txt"
                file_name224 = f"224_cliente{cliente}_fundo{fundo}.txt"

                logging.info(f"Verificando diretório para fundo {fundo}.\n")
                cli_folder = os.path.join('registro_movi_posi_fundos', folder_cli)
                if not os.path.exists(cli_folder):
                    logging.info(f"Criado o diretório para fundo o {fundo}.\n")
                    os.mkdir(cli_folder)

                logging.info(f"Acessando a Sinqia e obtendo o arquivo 224 para cliente {cliente}...\n")
                file224 = con.get_224(cliente, fundo, 'psette', 'Ativa!@#002')
                file224 = self.rename_txt_file_from_downloads(file224, file_name224)
                if self.file_not_empty(file224):
                    logging.info(f"\nARQUIVO CONTÉM INFORMAÇÃO. \n")
                    shutil.copy(file224, os.path.join(cli_folder, file_name224))
                    logging.info(f"\nARQUIVO {file_name224} CRIADO EM {cli_folder}. \n")
                else:
                    logging.info(f"\nARQUIVO (CLIENTE {cliente}/FUNDO {fundo}) VAZIO! \n")

                logging.info(f"Acessando a Sinqia e obtendo o arquivo 45 para cliente {cliente}...\n")
                file45 = con.get_45(cliente, fundo, 'psette', 'Ativa!@#002')
                file45 = self.rename_txt_file_from_downloads(file45, file_name45)
                if self.file_not_empty(file45):
                    logging.info(f"\nARQUIVO CONTÉM INFORMAÇÃO. \n")
                    shutil.copy(file45, os.path.join(cli_folder, file_name45))
                    logging.info(f"\nARQUIVO {file_name45} CRIADO EM {cli_folder}. \n")
                else:
                    logging.info(f"\nARQUIVO (CLIENTE {cliente}/FUNDO {fundo}) VAZIO! \n")

                logging.info(70 * "*")
                logging.info("\n")

    def executar_processo(self):
        thread = threading.Thread(target=self.processar_arquivo)
        thread.start()

    def run(self):
        self.janela.mainloop()

if __name__ == "__main__":
    app = PosiCatcher()
    app.run()
