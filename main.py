# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:11:47 2022

@author: denilson aguiar
"""

from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, Screen
import asyncio
from bs4 import BeautifulSoup
# agora -> webdriver manager
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from kivymd.toast.kivytoast.kivytoast import toast
from firebase import firebase
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.label import Label
import datetime
from kivy.clock import Clock



Window.size = (400, 550)
click_branco = '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[2]/div'
click_add_valor = '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input'
click_valor = '//*[@id="roulette-controller"]/div[1]/div[2]/div[1]/div/div[1]/input'
click_confirmar_aposta = '//*[@id="roulette-controller"]/div[1]/div[3]/button'

Link_blaze = 'https://blaze.com/pt/games/double'
click_vermelho = '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[1]/div'
click_preto = '//*[@id="roulette-controller"]/div[1]/div[2]/div[2]/div/div[3]/div'

click_entrar_blaze = '//*[@id="header"]/div/div[2]/div/div/div[1]/a'
click_email = '//*[@id="auth-modal"]/div/form/div[1]/div/input'
click_senha = '//*[@id="auth-modal"]/div/form/div[2]/div/input'
click_entrar = '//*[@id="auth-modal"]/div/form/div[4]/button'
api_key = '5692708316:AAHRwyOuDr_wGmdP8ygbe5T_uoZ1mdIxYLo'
############################################################3
automatico = 1
sequencia_automatica = 0
jogue_vermelho_automatico = 0
jogue_preto_automatico = 0
##############################################################

br = 'vazio'
g0 = 'vazio'
g1 = 'vazio'
g2 = 'vazio'

wins = 0
loss = 0
branco = 0
vitoriag1 = 0
vitoriag2 = 0
vitoriag0 = 0
brancog0 = 0
brancog1 = 0
brancog2 = 0
bancareal = 200
########################################################
analisar = 0
gale_atual = 0
analisar_open = 0
resultsDouble = []
######################################################3
margemacerto = 50
margemPRETO = 0
margemVERNELHO = 0
margemBRANCO = 0
margemaerror = 0

global logged_in_user
logged_in_user = ""

global ativar_sequencia
ativar_sequencia = 0
ultimo_numero = 1998
count = 0
sw_started = False
sw_seconds = 0
global finalcor
finalcor = "vazio"
global valornumcor
valornumcor = "vazio"
global progresso
progresso = 0
global nav
global entrada_confirmada_agora
entrada_confirmada_agora = "AGUARDANDO ENTRADA"

ultimo_numero = 5


class LoginScreen(Screen):

    def validate_user(self):
        global ativar_sequencia
        global logged_in_user
        from firebase import firebase
        firebase = firebase.FirebaseApplication("https://blazege-9e853-default-rtdb.firebaseio.com/")
        resultados = firebase.get("blazege-9e853-default-rtdb/Usuarios_blaze", '')
        uname = self.ids.uname_input.text
        pword = self.ids.pword_input.text
        is_found = (1, 2)
        self.ids.uname_input.text = "email@email"
        self.ids.pword_input.text = "1234"
        if is_found:
            logged_in_user = uname + pword
            for i in resultados.keys():
                if resultados[i]['email:'] == uname:
                    if resultados[i]['senha'] == pword:
                        print(resultados[i]['senha'])
                        print(resultados[i]['email:'])
                        ativar_sequencia += 1
                        print("Usuario:" + uname + " e " + "Senha:" + pword + " Correto")
                        self.parent.current = "Tela_PrincipalScreen"
                        print("Seja Bem vindo a tela Principal com a class Tela_PrincipalScreen")
                        print(ativar_sequencia)
                        toast(f"Bem vindo {uname}")

                if resultados[i]['email:'] != uname:
                    if resultados[i]['senha'] != pword:
                        print("Usuario:" + uname + " e " + "Senha:" + pword + " incorreto")
                        toast("usuario ou senha incorreto!")

    def chamando_tela_4(self):
        global ativar_sequencia
        ativar_sequencia = 2
        self.parent.current = 'relogio_tela'
        print(ativar_sequencia)
        toast("configuração Padrão Ativa, padrão de 4 sequencias, clique em iniciar aposta.")


class Tela_PrincipalScreen(Screen):

    def chamando_tela_3(self, text):
        global ativar_sequencia
        ativar_sequencia = 2
        self.parent.current = 'tela_4_digitos'
        print(ativar_sequencia)
        toast("configuração Padrão Ativa, padrão de 4 sequencias, clique em iniciar aposta.")

    def jogada_padrao_sete(self):
        global ativar_sequencia
        ativar_sequencia = 2
        self.parent.current = 'tela_7_digitos'
        # print("chamando tela submenu de class  tela_submenuScreen")
        print(ativar_sequencia)
        toast("em breve sera adicionado o padrao de 7 sequencias...")

    def jogada_padrao_nove(self):
        toast("em breve...")
        # toast("em breve sera adicionado o padrao de 7 sequencias...")

    def jogada_personalizada(self):
        global logged_in_user
        self.ids.nome_usuario.text = logged_in_user
        toast("em breve...")


class ButtonFocus(MDRaisedButton):
    ...


class tela_4_digitos(Screen):
    sw_started = False
    sw_seconds = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = Label()
        self.add_widget(self.label)
        self.task = Clock.schedule_interval(self.update_label, 0.1)

        self.resultado = Label()
        self.add_widget(self.resultado)
        self.task = Clock.schedule_interval(self.resultado_final, 0.1)

        self.resultado_cor = Label()
        self.add_widget(self.resultado_cor)
        self.task = Clock.schedule_interval(self.resultado_cor_sequencia, 0.1)

        self.entradas_disponiveis = Label()
        self.add_widget(self.entradas_disponiveis)
        self.task = Clock.schedule_interval(self.entradas_confirmadas, 0.1)

    def entradas_confirmadas(self, dt):
        global entrada_confirmada_agora
        self.ids.entradas_disponiveis.text = entrada_confirmada_agora

    def resultado_final(self, dt):
        global ultimo_numero
        global valor_de_saida
        global finalcor
        global progresso
        try:
            if valor_de_saida == 1:
                progresso = 100
                self.ids.resultado.text = ultimo_numero
                valor_de_saida = 0
                toast("Novo Resultado")
                if progresso == 100:
                    progresso = 0
                else:
                    "calma"

            elif valor_de_saida != 1:
                self.resultado.text = ultimo_numero
                self.ids.progress_bar.value = progresso
                progresso += 0.45
            else:
                'faço nada'
        except:
            self.ids.resultado.text = "Aguardando"

    def resultado_cor_sequencia(self, dt):
        global ultimo_numero
        global valor_de_saida
        global finalcor
        global valornumcor

        def qualnum(ultimo_numero):
            return int(ultimo_numero)

        def qualcor(ultimo_numero):
            try:
                if qualnum(ultimo_numero) <= 7:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Vermelho"
                    return 'V'
                elif qualnum(ultimo_numero) > 7:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Preto"
                    return 'P'
                elif qualnum(ultimo_numero) == 0:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                elif qualnum(ultimo_numero) <= 1:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                elif qualnum(ultimo_numero) == "B":
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                else:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    "branco"
            except:
                "ERROR"

        qualcor(ultimo_numero)

    def update_label(self, nap):
        now = datetime.datetime.now()
        if self.sw_started:
            self.sw_seconds += nap

        m, s = divmod(self.sw_seconds, 60)
        self.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' % (int(m), int(s), int(s * 100 % 100)))

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def start_stop(self):
        global ativar_sequencia
        self.ids.start_stop.text = 'Iniciar' if self.sw_started else 'Parar'
        self.sw_started = not self.sw_started
        ativar_sequencia = 7
        print(ativar_sequencia)

    def reset(self):

        if self.sw_started:
            self.root.ids.start_stop.text = 'Iniciar'
            self.sw_started = False

        self.sw_seconds = 0

    def barra_de_progresso(self, progresso):
        if progresso == 100:
            progresso = 0
        else:
            progresso += 10
        self.ids.progress_bar.value = progresso

    def desativar_jogo_4_digitos(self):
        global entry
        global ativar_sequencia
        ativar_sequencia = 4
        print(ativar_sequencia)
        toast("Desativando Aposta")

    def abrir_card(self):
        self.add_widget(tela_aposta_g_4())

    def desativar_sequencia_4(self):
        global entry
        global ativar_sequencia
        ativar_sequencia = 5
        toast("Desativando Aposta")

    def historico(self):
        toast("em breve")

class tela_aposta_g_4(MDCard):
    sw_started = False
    sw_seconds = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fechar(self):
        self.parent.remove_widget(self)

    def fechar_btn(self):
        self.parent.remove_widget(self)

    def jogar_sequencia_4(self):
        global ativar_sequencia
        global entry
        global g0
        global g1
        global g2
        global branco
        global br
        global nav
        # g0 = '5'
        # g1 = '12'
        # g2 = '24'
        ativar_sequencia = 6

        print(ativar_sequencia)

        g0 = self.ids.G0_input.text
        g1 = self.ids.G1_input.text
        g2 = self.ids.G2_input.text
        br = self.ids.BRANCO_input.text

        self.ids.G0_input.text = ""
        self.ids.G1_input.text = ""
        self.ids.G2_input.text = ""
        self.ids.BRANCO_input.text = ""
        # self.parent.current = popuop()

        if ativar_sequencia == 6:
            self.ids.jogar_sequencia_7.text = 'Iniciar' if self.sw_started else 'Apostado'
            # print(f"Começando o jogo com apostas G0: {g0},00 G1:{g1},00 G2: {g2},00 branco: {br},00")
            toast(f"Começando o jogo com apostas G0: {g0},00 G1:{g1},00 G2: {g2},00 branco: {br},00")
            # self.parent.current = 'notifica'
            self.parent.remove_widget(self)

            # open the popup

    def desativar_jogo_4_digitos(self):
        self.parent.remove_widget(self)
        global entry
        global ativar_sequencia
        ativar_sequencia = 70
        print(ativar_sequencia)
        toast("fique na tela de analise!")


###############PARA 7 DIGITOS#################################
class tela_7_digitos(Screen):
    sw_started = False
    sw_seconds = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.label = Label()
        self.add_widget(self.label)
        self.task = Clock.schedule_interval(self.update_label, 0.1)

        self.resultado = Label()
        self.add_widget(self.resultado)
        self.task = Clock.schedule_interval(self.resultado_final, 0.1)

        self.resultado_cor = Label()
        self.add_widget(self.resultado_cor)
        self.task = Clock.schedule_interval(self.resultado_cor_sequencia, 0.1)

        self.entradas_disponiveis = Label()
        self.add_widget(self.entradas_disponiveis)
        self.task = Clock.schedule_interval(self.entradas_confirmadas, 0.1)

    def entradas_confirmadas(self, dt):
        global entrada_confirmada_agora
        self.ids.entradas_disponiveis.text = entrada_confirmada_agora

    def resultado_final(self, dt):
        global ultimo_numero
        global valor_de_saida
        global finalcor
        global progresso
        try:
            if valor_de_saida == 1:
                progresso = 100
                self.ids.resultado.text = ultimo_numero
                valor_de_saida = 0
                toast("Novo Resultado")
                if progresso == 100:
                    progresso = 0
                else:
                    "calma"

            elif valor_de_saida != 1:
                self.resultado.text = ultimo_numero
                self.ids.progress_bar.value = progresso
                progresso += 0.45
            else:
                'faço nada'
        except:
            self.ids.resultado.text = "Aguardando"

    def resultado_cor_sequencia(self, dt):
        global ultimo_numero
        global valor_de_saida
        global finalcor
        global valornumcor

        def qualnum(ultimo_numero):
            return int(ultimo_numero)

        def qualcor(ultimo_numero):
            try:
                if qualnum(ultimo_numero) <= 7:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Vermelho"
                    return 'V'
                elif qualnum(ultimo_numero) > 7:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Preto"
                    return 'P'
                elif qualnum(ultimo_numero) == 0:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                elif qualnum(ultimo_numero) <= 1:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                elif qualnum(ultimo_numero) == "B":
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    return 'B'
                else:
                    self.ids.resultado.text = ultimo_numero
                    self.ids.resultado_cor.text = "Branco"
                    "branco"
            except:
                "ERROR"

        qualcor(ultimo_numero)

    def update_label(self, nap):
        now = datetime.datetime.now()
        if self.sw_started:
            self.sw_seconds += nap

        m, s = divmod(self.sw_seconds, 60)
        self.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' % (int(m), int(s), int(s * 100 % 100)))

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def start_stop(self):
        global ativar_sequencia
        self.ids.start_stop.text = 'Iniciar' if self.sw_started else 'Parar'
        self.sw_started = not self.sw_started
        ativar_sequencia = 7
        print(ativar_sequencia)

    def reset(self):

        if self.sw_started:
            self.root.ids.start_stop.text = 'Iniciar'
            self.sw_started = False

        self.sw_seconds = 0

    def barra_de_progresso(self, progresso):
        if progresso == 100:
            progresso = 0
        else:
            progresso += 10
        self.ids.progress_bar.value = progresso

    def desativar_jogo_7_digitos(self):
        global entry
        global ativar_sequencia
        ativar_sequencia = 7
        print(ativar_sequencia)
        toast("Desativando Aposta")

    def abrir_card(self):
        self.add_widget(tela_aposta_g())

    def historico(self):
        toast("em breve")


############### PARA 7 DIGITOS ##############################
class tela_aposta_g(MDCard):
    sw_started = False
    sw_seconds = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fechar(self):
        self.parent.remove_widget(self)

    def fechar_btn(self):
        self.parent.remove_widget(self)

    def jogar_sequencia_7(self):
        global ativar_sequencia
        global entry
        global g0
        global g1
        global g2
        global branco
        global br
        global nav
        # g0 = '5'
        # g1 = '12'
        # g2 = '24'
        ativar_sequencia = 6

        print(ativar_sequencia)

        g0 = self.ids.G0_input.text
        g1 = self.ids.G1_input.text
        g2 = self.ids.G2_input.text
        br = self.ids.BRANCO_input.text

        self.ids.G0_input.text = ""
        self.ids.G1_input.text = ""
        self.ids.G2_input.text = ""
        self.ids.BRANCO_input.text = ""
        # self.parent.current = popuop()

        if ativar_sequencia == 6:
            self.ids.jogar_sequencia_7.text = 'Iniciar' if self.sw_started else 'Apostado'
            # print(f"Começando o jogo com apostas G0: {g0},00 G1:{g1},00 G2: {g2},00 branco: {br},00")
            toast(f"Começando o jogo com apostas G0: {g0},00 G1:{g1},00 G2: {g2},00 branco: {br},00")
            # self.parent.current = 'notifica'
            self.parent.remove_widget(self)

            # open the popup

    def desativar_jogo_7_digitos(self):
        self.parent.remove_widget(self)
        global entry
        global ativar_sequencia
        ativar_sequencia = 70
        print(ativar_sequencia)
        toast("fique na tela de analise!")


class tela_splas_pop(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MegaBlazer(MDApp):
    sw_started = False
    sw_seconds = 0
    firebase = firebase.FirebaseApplication("https://blazege-9e853-default-rtdb.firebaseio.com/")
    # Pegar uma venda específico ou todas as vendas (GET)
    resultados = firebase.get("blazege-9e853-default-rtdb/Usuarios_blaze", '')

    def build(self):
        global sm
        sm = Builder.load_file("main.kv")
        #sm.add_widget(Builder.load_file("splash.kv"))
        self.theme_cls.theme_style = "Dark"

        return sm

    def on_start(self):

        Clock.schedule_once(self.login, 10)

    def login(*args):
        global nav
        global navegador

        print("inciando web")
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
        nav.get('https://blaze.com/pt/games/double')
        # abri o navegador para apostar automatico
        navegador = Service(ChromeDriverManager().install())
        navegador = webdriver.Chrome(service=navegador)
        navegador.get(Link_blaze)
        print("carregou web")
        sm.current = "login_screen"

    async def kivyCoro(self):  # This is the method that's gonna launch your kivy app
        await self.async_run(async_lib='asyncio')
        print('Kivy async app finished...')

    async def GlobalTask(self):
        resultsDouble = []
        while True:
            global ativar_sequencia
            global resulROOL
            global entry
            global g0
            global g1
            global g2
            global branco
            global br
            global ultimo_numero
            global valor_de_saida
            global analisar_open
            global margemVERNELHO
            global margemPRETO
            global margemBRANCO
            global automatico
            global sequencia_automatica
            global jogue_vermelho_automatico
            global jogue_preto_automatico
            global navegador
            global nav
            global progresso
            global entrada_confirmada_agora
            analisar = 0
            gale_atual = 0
            analisar_open = 0
            resultsDouble = []
            await asyncio.sleep(.1)
            #########################################################################################################3
            while True:

                if ativar_sequencia == 3:
                    print(f'dentro do loop valor:{ativar_sequencia}')
                    toast("iniciando pesquisa.....")
                    while True:
                        ativar_sequencia = 4
                        if ativar_sequencia == 4:
                            try:
                                resulROOL = nav.find_element(
                                    By.XPATH, '//*[@id="roulette-timer"]/div[1]').text
                            except NameError as erro:
                                print('ERRO 403')
                            except Exception as erro:
                                print('ERRO 404')

                            if resulROOL == 'Girando...':
                                print(resulROOL)
                                # toast(resulROOL)
                                c = nav.page_source
                                resultsDouble.clear()
                                soup = BeautifulSoup(c, 'html.parser')
                                go = soup.find('div', class_="entries main")
                                entries_div = soup.find("div", {"class": "entries main"})
                                entrys = entries_div.find_all("div", {"class": "roulette-tile"})
                                entrys = entrys[0:1]
                                box_list = []
                                for entry in entrys:
                                    if 'red' in entry.__str__():
                                        box_list.append(('VERMELHO', entry.text))

                                    elif 'black' in entry.__str__():
                                        box_list.append(('PRETO', entry.text))

                                    else:
                                        box_list.append(('BRANCO', '0'))
                                        print(*box_list, sep=' ')

                                print('numero:', entry.text)
                                # toast(entry.text)

                            await asyncio.sleep(.1)

                        if ativar_sequencia == 5:
                            print('Sistema de apostas desativado')
                            break

                #############################################################################################################3
                elif ativar_sequencia == 6:
                    while True:
                        global progresso

                        def qualnum(valornumcor):
                            if valornumcor == '0':
                                return 0

                            if valornumcor == '1':
                                return 1

                            if valornumcor == '2':
                                return 2

                            if valornumcor == '3':
                                return 3

                            if valornumcor == '4':
                                return 4

                            if valornumcor == '5':
                                return 5

                            if valornumcor == '6':
                                return 6

                            if valornumcor == '7':
                                return 7

                            if valornumcor == '8':
                                return 8

                            if valornumcor == '9':
                                return 9

                            if valornumcor == '10':
                                return 10

                            if valornumcor == '11':
                                return 11

                            if valornumcor == '12':
                                return 12

                            if valornumcor == '13':
                                return 13

                            if valornumcor == '14':
                                return 14

                        def qualcor(valornumcor):
                            if valornumcor == '0':
                                return 'B'

                            if valornumcor == '1':
                                return 'V'

                            if valornumcor == '2':
                                return 'V'

                            if valornumcor == '3':
                                return 'V'

                            if valornumcor == '4':
                                return 'V'

                            if valornumcor == '5':
                                return 'V'

                            if valornumcor == '6':
                                return 'V'

                            if valornumcor == '7':
                                return 'V'

                            if valornumcor == '8':
                                return 'P'

                            if valornumcor == '9':
                                return 'P'

                            if valornumcor == '10':
                                return 'P'

                            if valornumcor == '11':
                                return 'P'

                            if valornumcor == '12':
                                return 'P'

                            if valornumcor == '13':
                                return 'P'

                            if valornumcor == '14':
                                return 'P'

                        try:
                            resulROOL = nav.find_element(
                                By.XPATH, '//*[@id="roulette-timer"]/div[1]').text
                        except Exception:
                            print('ERRO 404')

                        analisar_open = 0
                        if resulROOL == 'Girando...':
                            analisar_open = 1
                            print('Analisando')
                            entrada_confirmada_agora = "AGUARDANDO ANALISE.."
                            await asyncio.sleep(10)
                            c = nav.page_source
                            resultsDouble.clear()
                            soup = BeautifulSoup(c, 'html.parser')
                            go = soup.find('div', class_="entries main")
                            entries_div = soup.find("div", {"class": "entries main"})
                            entrys = entries_div.find_all("div", {"class": "roulette-tile"})
                            entrys = entrys[0:1]
                            box_list = []
                            for entry in entrys:
                                if 'red' in entry.__str__():
                                    box_list.append(('VERMELHO', entry.text))
                                    margemVERNELHO += 1
                                    valor_de_saida = 1
                                    progresso = 100
                                elif 'black' in entry.__str__():
                                    box_list.append(('PRETO', entry.text))
                                    margemPRETO += 1
                                    valor_de_saida = 1
                                    progresso = 100
                                else:
                                    box_list.append(('BRANCO', '0'))
                                    print(*box_list, sep=' ')
                                    margemBRANCO += 1
                                    valor_de_saida = 1
                                    progresso = 100

                            if valor_de_saida == 1:
                                try:
                                    ultimo_numero = entry.text
                                    print(f"Ultimo numero:{ultimo_numero}")
                                except:
                                    print('sem valor de saida')

                            else:
                                'continua'
                            for i in go:
                                if i.getText():
                                    resultsDouble.append(i.getText())
                                else:
                                    resultsDouble.append('0')

                            resultsDouble = resultsDouble[:-1]

                            if analisar_open == 1:
                                default = resultsDouble[0:2]
                                mapeando = map(qualnum, default)
                                mapeando2 = map(qualcor, default)
                                finalnum = list(mapeando)
                                finalcor = list(mapeando2)
                                try:
                                    async def CHECK_VERSION(num):
                                        global analisar
                                        global gale_atual
                                        global automatico
                                        global sequencia_automatica
                                        global jogue_vermelho_automatico
                                        global jogue_preto_automatico
                                        global navegador
                                        global entrada_confirmada_agora
                                        ####################################################################################################
                                        # CHAMADA DE SEQUENCIA JOGUE NO:
                                        if analisar == 0:
                                            # 01. SEQUENCIA JOGUE PRETO['X', 'V',V 'V, 'V']:
                                            if num == ['V', 'V']:
                                                print("jogue preto")
                                                # APOSTAR NO VERMELHO elemento para clicar no preto
                                                await asyncio.sleep(1)
                                                navegador.find_element(By.XPATH, click_preto).click()
                                                await asyncio.sleep(1)
                                                # elemento para clicar na caixa de add valor
                                                navegador.find_element(By.XPATH, click_valor).click()
                                                await asyncio.sleep(1)
                                                # clique adicionando money para apostar
                                                navegador.find_element(By.XPATH, click_add_valor).send_keys(g0)
                                                await asyncio.sleep(2)
                                                # elemento para confirmar entrada na cor
                                                navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                await asyncio.sleep(1)
                                                # confirmando branco
                                                navegador.find_element(By.XPATH, click_branco).click()
                                                await asyncio.sleep(1)
                                                # clicando no imput valor
                                                navegador.find_element(By.XPATH, click_valor).click()
                                                await asyncio.sleep(1)
                                                # adicionando valor no branco reais
                                                navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                await asyncio.sleep(1)
                                                # clique para apostar
                                                navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                print("joguei preto auto")
                                                entrada_confirmada_agora = "SEQUENCIA ENCONTRADA NO PRETO COD:01"
                                                analisar = 1
                                                return
                                            # 02. SEQUENCIA JOGUE VERMELHO['X', 'p', 'p, 'P, 'p']:
                                            if num == ['P', 'P']:
                                                print("jogue vermelho")
                                                # APOSTAR NO VERMELHO elemento para clicar no vermelho
                                                navegador.find_element(By.XPATH, click_vermelho).click()
                                                await asyncio.sleep(1)
                                                # elemento para clicar na caixa de add valor
                                                navegador.find_element(By.XPATH, click_valor).click()
                                                await asyncio.sleep(1)
                                                # clique adicionando money para apostar
                                                navegador.find_element(By.XPATH, click_add_valor).send_keys(g0)
                                                await asyncio.sleep(2)
                                                # elemento para confirmar entrada na cor
                                                navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                await asyncio.sleep(1)
                                                # confirmando branco
                                                navegador.find_element(By.XPATH, click_branco).click()
                                                await asyncio.sleep(1)
                                                # clicando no imput valor
                                                navegador.find_element(By.XPATH, click_valor).click()
                                                await asyncio.sleep(1)
                                                # adicionando valor no branco reais
                                                navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                await asyncio.sleep(1)
                                                # clique para apostar
                                                navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                entrada_confirmada_agora = "SEQUENCIA ENCONTRADA NO VERMELHO COD:02"
                                                print("joguei vermelho auto")
                                                analisar = 1
                                                return

                                        ###################################################################################################

                                        elif analisar == 1:
                                            if gale_atual == 0:
                                                # 03. VITORIA COM GALE 1['X', 'P', 'P'  V P V:
                                                if num == ['P', 'V']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO SEM GALE! COD:01"
                                                    print("ganhou sem gale")
                                                    return
                                                if num == ['B', 'V']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO BRANCO SEM GALE! COD:01"
                                                    print("ganhou sem gale BRANCO")
                                                    return

                                                if num == ['V', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO SEM GALE! COD:02"
                                                    print("ganhou sem gale")

                                                    return
                                                if num == ['B', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO SEM GALE! COD:02"
                                                    print("ganhou sem gale BRANCO")
                                                    return

                                                # 02. DERROTA['X', 'P', 'P']:INDO PARA GALE2
                                                if num == ['V', 'V']:
                                                    gale_atual = 1
                                                    navegador.find_element(By.XPATH, click_preto).click()
                                                    await asyncio.sleep(1)
                                                    # elemento para clicar na caixa de add valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # clique adicionando money para apostar
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(g1)
                                                    await asyncio.sleep(2)
                                                    # elemento para confirmar entrada na cor
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    # confirmando branco
                                                    navegador.find_element(By.XPATH, click_branco).click()
                                                    await asyncio.sleep(1)
                                                    # clicando no imput valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # adicionando valor no branco reais
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                    await asyncio.sleep(1)
                                                    # clique para apostar
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    print("joguei preto auto g1")
                                                    entrada_confirmada_agora = "INDO PARA O GALE 01 COD:01"
                                                    print("indo para g1 continue no preto")

                                                    return
                                                if num == ['P', 'P']:
                                                    gale_atual = 1
                                                    print("indo para g1 continue no vermelho")
                                                    # APOSTAR NO VERMELHO elemento para clicar
                                                    navegador.find_element(By.XPATH, click_vermelho).click()
                                                    await asyncio.sleep(1)
                                                    # elemento para clicar na caixa de add valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # clique adicionando money para apostar
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(g1)
                                                    await asyncio.sleep(2)
                                                    # elemento para confirmar entrada na cor
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    # confirmando branco
                                                    navegador.find_element(By.XPATH, click_branco).click()
                                                    await asyncio.sleep(1)
                                                    # clicando no imput valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # adicionando valor no branco reais
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                    await asyncio.sleep(1)
                                                    # clique para apostar
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    print("joguei vermelho auto g1")
                                                    entrada_confirmada_agora = "INDO PARA O GALE 01 COD:02"

                                                    return

                                            #########################################################################################################

                                            if gale_atual == 1:

                                                # 02 E 05.VITORIA COM GALE 2['X', 'P', 'P', 'P']:
                                                if num == ['P', 'V']:
                                                    analisar = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO GALE 1! COD:01"
                                                    print("VITORIA COM GALE 1")

                                                    return
                                                if num == ['B', 'V']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO BRANCO GALE 1! COD:01"
                                                    print("VITORIA COM GALE 1")
                                                    return
                                                if num == ['B', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO BRANCO GALE 1! COD:01"
                                                    print("VITORIA COM GALE 1 BRANCO")
                                                    return
                                                if num == ['V', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO GALE 1! COD:02"
                                                    print("VITORIA COM GALE 1 BRANCO")
                                                    return
                                                ###############################################################################################
                                                # 01. DERROTA['X', 'V', 'V', 'V']: ACEITE KK
                                                if num == ['V', 'V']:
                                                    gale_atual = 2
                                                    print("joguei preto auto g2")
                                                    # APOSTAR NO VERMELHO elemento para clicar
                                                    navegador.find_element(By.XPATH, click_preto).click()
                                                    await asyncio.sleep(1)
                                                    # elemento para clicar na caixa de add valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # clique adicionando money para apostar
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(g2)
                                                    await asyncio.sleep(2)
                                                    # elemento para confirmar entrada na cor
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    # confirmando branco
                                                    navegador.find_element(By.XPATH, click_branco).click()
                                                    await asyncio.sleep(1)
                                                    # clicando no imput valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # adicionando valor no branco reais
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                    await asyncio.sleep(1)
                                                    # clique para apostar
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)

                                                    entrada_confirmada_agora = "INDO PARA O GALE 02 COD:01"
                                                    print("indo para g2 continue no preto")

                                                    return
                                                # 02. indp g2['X', 'P', 'P', 'P']: ACEITE KK
                                                if num == ['P', 'P']:
                                                    gale_atual = 2
                                                    print("indo para g2 continue no vermelho")
                                                    # APOSTAR NO VERMELHO elemento para clicar
                                                    navegador.find_element(By.XPATH, click_vermelho).click()
                                                    await asyncio.sleep(1)
                                                    # elemento para clicar na caixa de add valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # clique adicionando money para apostar
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(g2)
                                                    await asyncio.sleep(2)
                                                    # elemento para confirmar entrada na cor
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    # confirmando branco
                                                    navegador.find_element(By.XPATH, click_branco).click()
                                                    await asyncio.sleep(1)
                                                    # clicando no imput valor
                                                    navegador.find_element(By.XPATH, click_valor).click()
                                                    await asyncio.sleep(1)
                                                    # adicionando valor no branco reais
                                                    navegador.find_element(By.XPATH, click_add_valor).send_keys(br)
                                                    await asyncio.sleep(1)
                                                    # clique para apostar
                                                    navegador.find_element(By.XPATH, click_confirmar_aposta).click()
                                                    await asyncio.sleep(1)
                                                    print("joguei vermelho auto g2")
                                                    entrada_confirmada_agora = "INDO PARA O GALE 02 COD:02"

                                                    return

                                            #########################################################################################################
                                            if gale_atual == 2:

                                                # 02 E 05.VITORIA COM GALE 2['X', 'P', 'P', 'P']:
                                                if num == ['P', 'V']:
                                                    analisar = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO PRETO GALE 2! COD:01"
                                                    print("VITORIA COM GALE 2")

                                                    return
                                                if num == ['B', 'V']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO BRANCO GALE 2! COD:01"
                                                    print("VITORIA COM GALE 2 BRANCO")
                                                    return

                                                if num == ['V', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO VERMELHO GALE 2! COD:02"
                                                    print("VITORIA COM GALE 2")
                                                    return

                                                if num == ['B', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "GANHAMOS NO BRANCO GALE 2! COD:02"
                                                    print("VITORIA COM GALE 2 BRANCO")
                                                    return
                                                ###############################################################################################
                                                # 01. DERROTA['X', 'V', 'V', 'V']: ACEITE KK
                                                if num == ['V', 'V']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "NÃO FOI DESTA VEZ, PERDEMOS..! COD:01"
                                                    print("perdeu totalmente ")
                                                    return
                                                # 02. DERROTA['X', 'P', 'P', 'P']: ACEITE KK
                                                if num == ['P', 'P']:
                                                    analisar = 0
                                                    gale_atual = 0
                                                    entrada_confirmada_agora = "NÃO FOI DESTA VEZ, PERDEMOS..! COD:01"
                                                    print("perdeu totalmente ")
                                                    return
                                                await asyncio.sleep(.1)
                                        await asyncio.sleep(.1)

                                    await CHECK_VERSION(finalcor)
                                    print(finalcor)
                                except:
                                    entrada_confirmada_agora = "CONEXÃO COM A INTERNET TURBULENTA, RECOMENDAMOS REINICIAR O JOGO."
                                    print('sem analise')
                                    analisar = 0

                        await asyncio.sleep(.1)
                        if ativar_sequencia == 7:
                            progresso = 0
                            self.sw_seconds = 0
                            toast("Suas Analises estão em pausa.")
                            print('Sistema de apostas desativado')
                            break
                ####################################################################################################################
                else:
                    "nao rodou "

                await asyncio.sleep(.1)

            await asyncio.sleep(.1)

    async def base(self):
        (done, pending) = await asyncio.wait({self.kivyCoro(), self.GlobalTask()},
                                             return_when='FIRST_COMPLETED')


if __name__ == '__main__':
    async def mainThread():
        instanceApp = MegaBlazer()  # Instanciate your App class
        a = asyncio.create_task(instanceApp.base())  # Run kivyApp as a task
        (done, pending) = await asyncio.wait({a}, return_when='FIRST_COMPLETED')
        # (done, pending) = await asyncio.wait({b}, return_when='FIRST_COMPLETED')


    asyncio.run(mainThread())
