# Copyright (C) <2020>  <Michele Viotto>
import botogram
import covid
import json
from datetime import datetime
import os


bot = botogram.create("YOUR_API_KEY")

try:
    os.makedirs('grafici/nazionali')
    os.makedirs('grafici/regionali')
except OSError:
    pass


# COMANDI DEL BOT
@bot.command("start")
def start_command(chat, message, args):
    """Avvia il bot e manda il menù principale"""
    #print("Started by %s" % message.sender.first_name)
    chat.send(get_start_message(), attach=get_start_buttons())


# CALLBACK DEL BOT
@bot.callback("callback_start")
def callback_start(query, chat, message):
    """Menù principale da tastiera"""
    message.edit(get_start_message(), attach=get_start_buttons())


@bot.callback("callback_ultimi_andamenti")
def callback_ultimi_andamenti(query, chat, message):
    """Menù per scegliere quale ultimo aggiornamento si vuole vedere"""
    btns = botogram.Buttons()
    btns[0].callback("Nazionale", "callback_ultimo_nazionale")
    btns[1].callback("Regionale", "callback_ultimo_regionale")
    btns[2].callback("Indietro", "callback_start")
    message.edit(
        "Scegli quale ultimo andamento vuoi vedere tra nazionale"
        " o regionale con i bottoni qui sotto.", attach=btns
        )


@bot.callback("callback_ultimo_nazionale")
def callback_ultimo_nazionale(query, chat, message):
    """Messaggio per vedere l'ultimo andamento nazionale con numero
        nuovi casi rispetto al giorno precedente"""
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_ultimi_andamenti")
    # contiene json con tutti i dati dell'ultimo aggiornamento
    aggiornamento = covid.get_andamento_nazionale(latest=True)
    message.edit(get_andamento_message(aggiornamento, True), attach=btns)


# tre bottoni con divisione in tre zone
@bot.callback("callback_ultimo_regionale")
def callback_ultimo_regionale(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Nord", "callback_ultimo_regionale_zona", "nord")
    btns[1].callback("Centro", "callback_ultimo_regionale_zona", "centro")
    btns[2].callback("Sud", "callback_ultimo_regionale_zona", "sud")
    btns[3].callback("Indietro", "callback_ultimi_andamenti")
    message.edit(
        "Seleziona dai tasti qui sotto la zona di cui vuoi vedere le regioni.",
        attach=btns
        )


# messaggio con i bottoni delle varie regioni in base alla zona scelta
@bot.callback("callback_ultimo_regionale_zona")
def callback_ultimo_regionale_zona(query, data, chat, message):
    regioni = covid.get_andamento_regionale(latest=True)
    btns = botogram.Buttons()
    if data == "nord":
        # "nome regione", "callback", "id regione presente in {regioni}"
        btns[0].callback("Valle d'Aosta", "callback_ultimo_regione", "2")
        btns[0].callback("Piemonte", "callback_ultimo_regione", "1")
        btns[0].callback("Liguria", "callback_ultimo_regione", "7")
        btns[1].callback("Trentino A. A.", "callback_ultimo_regione", "4")
        btns[1].callback("Lombardia", "callback_ultimo_regione", "3")
        btns[1].callback("Veneto", "callback_ultimo_regione", "5")
        btns[2].callback("Friuli Venezia Giulia", "callback_ultimo_regione", "6")
        btns[2].callback("Emilia Romagna", "callback_ultimo_regione", "8")
        btns[3].callback("Indietro", "callback_ultimo_regionale")
    elif data == "centro":
        # "nome regione", "callback", "id regione presente in {regioni}"
        btns[0].callback("Toscana", "callback_ultimo_regione", "9")
        btns[0].callback("Marche", "callback_ultimo_regione", "11")
        btns[0].callback("Umbria", "callback_ultimo_regione", "10")
        btns[1].callback("Lazio", "callback_ultimo_regione", "12")
        btns[1].callback("Abruzzo", "callback_ultimo_regione", "13")
        btns[2].callback("Indietro", "callback_ultimo_regionale")
    elif data == "sud":
        # "nome regione", "callback", "id regione presente in {regioni}"
        btns[0].callback("Molise", "callback_ultimo_regione", "14")
        btns[0].callback("Puglia", "callback_ultimo_regione", "16")
        btns[0].callback("Campania", "callback_ultimo_regione", "15")
        btns[1].callback("Basilicata", "callback_ultimo_regione", "17")
        btns[1].callback("Calabria", "callback_ultimo_regione", "18")
        btns[1].callback("Sicilia", "callback_ultimo_regione", "19")
        btns[2].callback("Sardegna", "callback_ultimo_regione", "20")
        btns[3].callback("Indietro", "callback_ultimo_regionale")

    message.edit(
        "Seleziona dai tasti qui sotto la regione di cui vuoi vedere i dati.",
        attach=btns
    )


# ultimo andamento per singola regione
@bot.callback("callback_ultimo_regione")
def callback_ultimo_regione(query, data, chat, message):
    """Messaggio per vedere l'ultimo andamento regionale con numero
        nuovi casi rispetto al giorno precedente"""
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_ultimo_regionale")
    # contiene json con tutti i dati dell'ultimo aggiornamento
    regioni = covid.get_andamento_regionale(latest=True)
    text = ""
    for regione in regioni:
        if regione["codice_regione"] == int(data):
            text += (get_andamento_message(regione))
            if int(data) is not 4:
                break
    message.edit(text,attach=btns)


# grafici
@bot.callback("callback_grafici")
def callback_grafici(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Grafici nazionali", "callback_grafici_nazionali")
    btns[1].callback("Indietro", "callback_start")
    message.edit(
        "Vuoi vedere o grafici nazionali o regionali? Scegli qui sotto."
        "\n*REGIONALI NON ANCORA DISPONIBILI*",
        attach=btns
        )

# grafici nazionali
@bot.callback("callback_grafici_nazionali")
def callback_grafici_nazionali(query, data, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Positivi attuali", "callback_grafico_nazionale_positivi_attuali")
    btns[0].callback("Nuovi positivi", "callback_grafico_nazionale_positivi_nuovi")
    btns[1].callback("Totale deceduti", "callback_grafico_nazionale_totale_deceduti")
    btns[1].callback("Cumulativo", "callback_grafico_nazionale_cumulativo")
    btns[2].callback("Indietro", "callback_grafici")
    text = "Seleziona il grafico nazionale che vuoi vedere con i tasti qui sotto."
    # perchè non posso modificare un messaggio con la foto quindi devo eliminarlo
    if data == "delete":
        message.delete()
        chat.send(text, attach=btns)
    else:
        message.edit(text, attach=btns)


@bot.callback("callback_grafico_nazionale_positivi_attuali")
def callback_grafico_nazionale_positivi_attuali(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_grafici_nazionali", "delete")
    covid.create_grafico_andamento_nazionale()
    # non posso aggiungere una foto ad un messaggio esistente quindi lo elimino
    message.delete()
    chat.send_photo("grafici/nazionali/totali_positivi.png", attach=btns)


@bot.callback("callback_grafico_nazionale_positivi_nuovi")
def callback_grafico_nazionale_positivi_nuovi(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_grafici_nazionali", "delete")
    covid.create_grafico_nuovi_positivi_nazionale()
    # non posso aggiungere una foto ad un messaggio esistente quindi lo elimino
    message.delete()
    chat.send_photo("grafici/nazionali/nuovi_positivi.png", attach=btns)


@bot.callback("callback_grafico_nazionale_totale_deceduti")
def callback_grafico_nazionale_totale_deceduti(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_grafici_nazionali", "delete")
    covid.create_grafico_totale_deceduti_nazionale()
    # non posso aggiungere una foto ad un messaggio esistente quindi lo elimino
    message.delete()
    chat.send_photo("grafici/nazionali/totale_deceduti.png", attach=btns)


@bot.callback("callback_grafico_nazionale_cumulativo")
def callback_grafico_nazionale_cumulativo(query, chat, message):
    btns = botogram.Buttons()
    btns[0].callback("Indietro", "callback_grafici_nazionali", "delete")
    covid.create_grafico_cumulativo_nazionale()
    # non posso aggiungere una foto ad un messaggio esistente quindi lo elimino
    message.delete()
    chat.send_photo("grafici/nazionali/cumulativo.png", attach=btns)


# Info
@bot.callback("callback_bot_info")
def callback_bot_info(query, chat, message):
    btns = botogram.Buttons()
    btns[0].url("Codice sorgente", "https://github.com/xMicky24GIT/covid19ita-telegram-bot")
    btns[1].callback("Indietro", "callback_start")
    message.edit(
        "Ho iniziato a creare questo bot principalmente per trasformare"
        " questa quarantena in qualcosa di positivo ed imparare qualcosa di"
        " nuovo ma allo stesso tempo creare qualcosa di carino e utile.\n"
        "Puoi trovare il codice sorgente qui sotto. (a breve)",
        attach=btns
        )


# FUNZIONI DI APPOGGIO
def get_start_message():
    return (
        "Ciao!\n"
        "Grazie a me puoi tenere traccia dell'andamento nazionale e"
        " regionale di tutto ciò che riguarda i numeri di"
        " Covid19 in Italia.\n"
        "Clicca uno dei pulsanti qui sotto per iniziare."
    )


def get_start_buttons():
    btns = botogram.Buttons()
    btns[0].callback("Ultimi andamenti", "callback_ultimi_andamenti")
    btns[1].callback("Grafici", "callback_grafici", "asd") # "asd" is not important
    btns[2].callback("Info", "callback_bot_info")

    return btns


def get_andamento_message(dati, nazione = False):
    if nazione:
        di_cosa = "nazione"
    else:
        di_cosa = dati["denominazione_regione"]
    # formatto la data per avere solo giorno-mese-anno
    data = datetime.strptime(dati["data"], "%Y-%m-%dT%H:%M:%S")
    data = data.strftime("%d-%m-%Y")

    return (
        "*Ultimo aggiornamento per %s:*\n"
        "*Data*: %s\n"
        "*Tamponi totali*: %s\n"
        "*Casi totali*: %s\n"
        "*Attualmente positivi*: %s\n"
        "*Totale ospedalizzati*: %s\n"
        "   - *con sintomi*: %s\n"
        "   - *terapia intensiva*: %s\n"
        "*In isolamento domiciliare*: %s\n"
        "*Deceduti*: %s\n"
        "*Dimessi guariti*: %s\n"
        "*Nuovi casi positivi*: %s\n"
        % (
            di_cosa, data, format(dati["tamponi"], ',d'),
            format(dati["totale_casi"], ',d'), format(dati["totale_attualmente_positivi"], ',d'),
            format(dati["totale_ospedalizzati"], ',d'), format(dati["ricoverati_con_sintomi"], ',d'),
            format(dati["terapia_intensiva"], ',d'), format(dati["isolamento_domiciliare"], ',d'),
            format(dati["deceduti"], ',d'), format(dati["dimessi_guariti"], ',d'),
            format(dati["nuovi_attualmente_positivi"], ',d')
            )
        )


if __name__ == "__main__":
    bot.run()
