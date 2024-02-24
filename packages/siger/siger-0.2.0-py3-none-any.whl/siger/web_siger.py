""" WEB SIGER"""
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from .import_siger import ImportSIGER

class WebSIGER(ImportSIGER):
    r"""Classe destinada a automatizar a extração de dados diretamente do SIGER.

    ...

    Parameters
    ----------
    ...

    Examples
    --------
    Para inicializar a classe, basta chamar ela para o objeto de interesse.

    >>> ...
    >>> ...
    >>> ...
    >>> ...
    """
    ###================================================================================================================
    ###
    ### CÓDIGOS DE INICIALIZAÇÃO
    ###
    ###================================================================================================================
    def __init__(self, url_siger, usuario, senha):
        # Pegando todas as funções da Import_SIGER para uso nesse módulo
        super().__init__(url_siger, usuario, senha)

    ###================================================================================================================
    ###
    ### FUNÇÕES AUXILIARES
    ###
    ###================================================================================================================
    def __inic_navegador(self, cd):
        # Inicializa o navegador
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        navegador = webdriver.Chrome(executable_path=cd, options=chrome_options)

        # service = Service(executable_path=cd)
        # navegador = webdriver.Chrome(service=service, options=chrome_options)

        navegador.maximize_window()
        navegador.get(self.url)

        return navegador

    def __login_siger(self, navegador, user, key):
        # LOGIN
        username = navegador.find_element(By.ID, "Username")
        password = navegador.find_element(By.ID,"Password")
        username.send_keys(user)
        password.send_keys(key)
        xpath = '/html/body/div[3]/main/section/div/div/div/div[2]/div/div/section/form/div[4]/button'
        navegador.find_element(By.XPATH,xpath).click()

    def __imp_arquivo_siger(self, navegador, file, commentary):
        ## Acessando a Importação
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Carimbos
        xpath = '//*[@id="PossuiCarimboData"]'
        navegador.find_element(By.XPATH,xpath).click()
        xpath = '//*[@id="PossuiCarimboEstado"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="ComentarioArquivo"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
            else:
                # print(f"Mensagem desconhecida ao passar o arquivo: {file}")
                return False
        else:
            return False

    def __del_arquivo_siger(self, navegador, file, commentary):
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="ComentarioArquivo"]'
        navegador.find_element(By.XPATH,xpath).clear()
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file)
        ### Marcando carimbo remoção fisica
        time.sleep(self.delay_prop)
        xpath = '//*[@id="Carga"]/div/div[1]/div[3]/div/div/div/div/div/label[2]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Clicando em Submeter
        xpath = '//*[@id="submeterbtn"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Confirmando
        time.sleep(1)
        xpath = '//*[@id="FormModalConfirmacao"]/div/div[2]/input'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
            else:
                # print(f"Mensagem desconhecida ao passar o arquivo: {file}")
                return False
        else:
            return False

    def __esc_arquivo_siger(self, navegador, file, commentary):
        ## Acessando a Tela de Escorregamento
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe ESCORREGAMENTO DE OBRAS
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[2]/a'
        navegador.find_element(By.XPATH,xpath).click()
        #
        ## Selecionado opções na Tela de Escorregamento
        ### Marca Opção Possui carimbo de data e obra
        xpath = '//*[@id="PossuiCarimboDataEObra"]'
        navegador.find_element(By.XPATH,xpath).click()
        ### Inserindo Comentário
        xpath = '//*[@id="Comentario"]'
        navegador.find_element(By.XPATH,xpath).send_keys(commentary)
        ### Escolhendo Arquivo
        xpath = '//*[@id="Arquivos"]'
        file_choosen = navegador.find_element(By.XPATH,xpath)
        file_choosen.send_keys(file.replace("\\","/"))
        ### Clicando em Submeter
        xpath = '/html/body/div[3]/main/div/div/form/div/div[2]/button'
        navegador.find_element(By.XPATH,xpath).click()
        time.sleep(self.delay_prop)
        ### Checando se deu erro!
        xpath = '/html/body/div[3]/div'
        err_msg = navegador.find_element(By.XPATH,xpath).is_displayed()
        if err_msg:
            text_msg = navegador.find_element(By.XPATH,xpath).text
            if text_msg == "×\nNão é possível realizar essa operação, verifique os erros abaixo.\nClique para ver mais" or text_msg =='×\nAlgo inesperado aconteceu!':
                return True
            else:
                # print(f"Mensagem desconhecida ao passar o arquivo: {file}")
                return False
        else:
            return False

    def __zer_arquivo_siger(self, navegador):
        ## Acessando a Importação
        ### Escolhe ADMINISTRAÇÃO
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Importação
        xpath = '//*[@id="bs-navbar-collapse"]/ul/li[1]/ul/li[1]/a'
        navegador.find_element(By.XPATH,xpath).click()
        ### Escolhe Apagar Equipamentos
        xpath = '//*[@id="Carga"]/div/form/button'
        navegador.find_element(By.XPATH,xpath).click()

    ###================================================================================================================
    ###
    ### CARREGAMENTO DOS ARQUIVOS
    ###
    ###================================================================================================================
    def carrega_siger(self, df_arquivos, cd):
        # Parte 1 - Inicializa o navegador
        navegador = self.__inic_navegador(cd)

        # Parte 2 - Faz o login no sistema
        self.__login_siger(navegador, self.user, self.password)

        # Parte 3 - Realiza os carregamentos previstos no df
        for _, row in df_arquivos.iterrows():
            if str(row["ignorar"]) == "0":
                flag_error = True
                nome_arquivo = os.path.basename(row["diretorio"])

                if row["operacao"] == "imp":
                    flag_error = self.__imp_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "esc":
                    flag_error = self.__esc_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "del":
                    flag_error = self.__del_arquivo_siger(navegador, row["diretorio"], nome_arquivo)

                elif row["operacao"] == "zer":
                    self.__zer_arquivo_siger(navegador)
                    flag_error = False

                # Verifica erros
                if flag_error:
                    print(f"Erro ao carregar o arquivo {row['diretorio']}! Favor checar")
                    return False

        return True

    ###================================================================================================================
    ###
    ### CÓDIGOS PARA CARREGAR OS 7 ARQUIVOS E WEB ACESSO
    ###
    ###================================================================================================================
    # def carrega_7_arquivos(self, path_decks, chromedriver_path, report_path = "relatorio.txt", start_deck=1, final_deck=7):
    #     """ Realiza o carregamento automático dos 7 arquivos"""
    #     # Fotografia do estado atual da base
    #     df_robras_original = self.get_robras()

    #     # Coleta lista de decks presentes na pasta
    #     decks_siger = []
    #     for filename in os.listdir(path_decks):
    #         if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
    #             decks_siger.append(os.path.join(path_decks, filename))

    #     # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
    #     if len(decks_siger) == 7:

    #         # Inicializa variáveis de conferência de dados
    #         flag_error = False
    #         details_error = ""

    #         # Inicializa o navegador
    #         service = Service(executable_path=chromedriver_path)
    #         navegador = webdriver.Chrome(service=service)
    #         navegador.maximize_window()
    #         navegador.get(self.url)
    #         delay = 1

    #         # Login SIGER
    #         self.web_login_siger(navegador, self.user, self.password)

    #         # Arquivo 01 - Escorregamento
    #         flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[0], "Arquivo 1 - Escorregamento", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 1!"
    #             return details_error

    #         # Arquivo 02 - Importação
    #         flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[1], "Arquivo 2 - Importação PWF", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 2!"
    #             return details_error

    #         # Arquivo 03 - Importação
    #         flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[2], "Arquivo 3 - Importação ALT", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 3!"
    #             return details_error

    #         # Arquivo 04 - Importação
    #         flag_error = self.web_carrega_file_importacao_remocao(navegador, decks_siger[3], "Arquivo 4 - Remoção Base", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 4!"
    #             return details_error

    #         # Arquivo 05 - Importação
    #         flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[4], "Arquivo 5 - Importação PWF", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 5!"
    #             return details_error

    #         # Arquivo 06 - Importação
    #         flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[5], "Arquivo 6 - Importação ALT", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 6!"
    #             return details_error

    #         # Arquivo 07 - Escorregamento
    #         flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[6], "Arquivo 7 - Escorregamento", delay)
    #         if flag_error:
    #             details_error = "Houve um erro no carregamento do arquivo 7!"
    #             return details_error

    #         # Voltando ao menu
    #         xpath = '/html/body/header/nav/div/a/img'
    #         navegador.find_element(By.XPATH,xpath).click()
    #     else:
    #         print("Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!")
    #         details_error = "Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!"
    #         return details_error

    #     # Finalizada a execução do carregamento, verificar o resultado obtido
    #     print("Carregamento concluído com sucesso! Gerando relatório de carregamento...")
    #     df_robras_mod, dic_dfs = self.__get_all_siger_dfs()
    #     df_siger = self.__make_siger_base(dic_dfs)
    #     df_agg = df_siger.groupby(['Código de Obra de Entrada', "Data de Entrada"], as_index=False).agg({'Estado': lambda x: ' '.join(set(x))})
    #     #
    #     # PARTE 1 - CHECAR CONJUNTO EXCLUSIVO
    #     str_exclusivo = self.__aux_check_exclusives(dic_dfs)
    #     #
    #     # PARTE 2 - CHECAR ESTADOS MÚLTIPLOS
    #     df_estado_mult = self.__aux_check_estados_multiplos(df_agg, df_siger)
    #     #
    #     # PARTE 3 - CHECAR DATAS MÚLTIPLAS
    #     df_data_mult = self.__aux_check_datas_multiplas(df_agg)
    #     #
    #     # PARTE 4 - CHECAR ESTADOS DEFASADOS
    #     df_estado_def = self.__aux_check_estados_defasados(df_agg)
    #     #
    #     # PARTE 5 - VERIFICAR ESCORREGAMENTOS EM CASCATA
    #     df_obras_escorregadas_cascata = self.check_escorreg_cascata(df_robras_original, df_robras_mod, decks_siger[6])
    #     #
    #     # PARTE 6 - VERIFICAR EXCLUSÕES EM CASCATA
    #     lista_obras_removidas_cascata = self.check_apagamento_cascata(df_robras_original, df_robras_mod, decks_siger[0], decks_siger[3])

    #     # Crie um arquivo de texto para escrever o relatório
    #     with open(report_path, 'w') as arquivo:
    #         data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         arquivo.write(f"# RELATÓRIO DE CARREGAMENTO SIGER - {data_hora}\n\n")

    #         # Escreva a variável string no arquivo
    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 01 - CONJUNTOS EXCLUSIVOS\n")
    #         arquivo.write(f"{str_exclusivo}\n\n")

    #         # Escreva os DataFrames no arquivo
    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 02 - ESTADOS MÚLTIPLOS\n")
    #         arquivo.write(df_estado_mult.to_string(index=False) + '\n\n')

    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 03 - DATAS MÚLTIPLAS\n")
    #         arquivo.write(df_data_mult.to_string(index=False) + '\n\n')

    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 04 - ESTADOS DEFASADOS\n")
    #         arquivo.write(df_estado_def.to_string(index=False) + '\n\n')

    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 05 - OBRAS ESCORREGADAS EM CASCATA\n")
    #         arquivo.write(df_obras_escorregadas_cascata.to_string(index=False) + '\n\n')

    #         arquivo.write("#"*125 + "\n")
    #         arquivo.write("# CHECAGEM 06 - OBRAS APAGADAS EM CASCATA\n")
    #         arquivo.write("\n".join(lista_obras_removidas_cascata) + '\n\n')

    #     return

    # def carrega_7_arquivos_gui_pt1(self, path_decks, chromedriver_path, carrega_arquivo):
    #     """ Realiza o carregamento automático dos 7 arquivos"""
    #     # Fotografia do estado atual da base
    #     df_robras_original = self.get_robras()

    #     # Coleta lista de decks presentes na pasta
    #     decks_siger = []
    #     for filename in os.listdir(path_decks):
    #         if filename.endswith(('.pwf', '.alt')) or filename.startswith(('1_', '2_', '3_', '4_', '5_', '6_', '7_')):
    #             decks_siger.append(os.path.join(path_decks, filename))

    #     # Verifica se estamos com os 7 arquivos para conseguir prosseguir:
    #     if len(decks_siger) == 7:

    #         # Inicializa variáveis de conferência de dados
    #         flag_error = False
    #         details_error = ""

    #         # Inicializa o navegador
    #         chrome_options = webdriver.ChromeOptions()
    #         chrome_options.add_experimental_option("prefs", {"detach": True})

    #         # Inicializa o navegador
    #         service = Service(executable_path=chromedriver_path)
    #         navegador = webdriver.Chrome(service=service, options=chrome_options)
    #         # navegador = webdriver.Chrome(service=service)
    #         navegador.maximize_window()
    #         navegador.get(self.url)
    #         delay = 1

    #         # Login SIGER
    #         self.web_login_siger(navegador, self.user, self.password)

    #         # Arquivo 01 - Escorregamento
    #         if carrega_arquivo[0]:
    #             flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[0], "Arquivo 1 - Escorregamento", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 1!"
    #                 return details_error, df_robras_original

    #         # Arquivo 02 - Importação
    #         if carrega_arquivo[1]:
    #             flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[1], "Arquivo 2 - Importação PWF", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 2!"
    #                 return details_error, df_robras_original

    #         # Arquivo 03 - Importação
    #         if carrega_arquivo[2]:
    #             flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[2], "Arquivo 3 - Importação ALT", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 3!"
    #                 return details_error, df_robras_original

    #         # Arquivo 04 - Importação
    #         if carrega_arquivo[3]:
    #             flag_error = self.web_carrega_file_importacao_remocao(navegador, decks_siger[3], "Arquivo 4 - Remoção Base", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 4!"
    #                 return details_error, df_robras_original

    #         # Arquivo 05 - Importação
    #         if carrega_arquivo[4]:
    #             flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[4], "Arquivo 5 - Importação PWF", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 5!"
    #                 return details_error, df_robras_original

    #         # Arquivo 06 - Importação
    #         if carrega_arquivo[5]:
    #             flag_error = self.web_carrega_file_importacao_entrada(navegador, decks_siger[5], "Arquivo 6 - Importação ALT", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 6!"
    #                 return details_error, df_robras_original

    #         # Arquivo 07 - Escorregamento
    #         if carrega_arquivo[6]:
    #             flag_error = self.web_carrega_file_escorregamento(navegador, decks_siger[6], "Arquivo 7 - Escorregamento", delay)
    #             if flag_error:
    #                 details_error = "Houve um erro no carregamento do arquivo 7!"
    #                 return details_error, df_robras_original

    #         # Voltando ao menu
    #         xpath = '/html/body/header/nav/div/a/img'
    #         navegador.find_element(By.XPATH,xpath).click()
    #     else:
    #         print("Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!")
    #         details_error = "Não foram encontrados os 7 arquivos na pasta informada. Verificar se há arquivos faltantes ou em excesso!"
    #         return details_error, df_robras_original

    #     return details_error, df_robras_original
