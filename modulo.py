import random
from contextlib import nullcontext
from operator import index


class Game():
    def __init__(self,domande,plist):
        self.domande = domande
        self.plist = plist
        self.livello = 0
        self.domande = self.carica_domande()
        self.partita=True

    def carica_domande(self):
        domande=[]
        with open(self.domande, "r") as f:
            lines=[]
            line=f.readline()
            while(line!=""):
                if line!="\n":
                    lines.append(line)
                line=f.readline()
            for i in range(0, len(lines)-5, 6):
                testo = lines[i]
                livello = lines[i+1]
                risposta_corretta = lines[i+2]
                altre_risposte= [lines[i+3],lines[i+4],lines[i+5]]
                domande.append(Domanda(testo, livello, risposta_corretta, altre_risposte))
        return domande

    def get_domanda(self):
        domande_possibili=[]
        for i in self.domande:
            if self.livello==int(i.livello):
                domande_possibili.append(i)
        return random.choice(domande_possibili)

    def gioco(self):
        while self.partita and self.livello<=4:
            domanda=self.get_domanda()
            risposte=domanda.get_risposte()
            print(f"{self.livello}. {domanda.testo}")
            for i in range(0,4):
                print(f"{i+1}. {risposte[i]}")
            indice_corretta=0
            cont=0
            for i in risposte:
                if i==domanda.risposta_corretta:
                    indice_corretta=cont+1
                cont+=1
            risposta_utente=int(input("Inserisci la tua risposta: "))
            if(risposte[risposta_utente-1]==domanda.risposta_corretta):
                print("Risposta corretta!")
                if(self.livello==4):
                    self.partita=False
                    nickname=input("Inserisci il tuo nickname: ")
                    ptemp=Player(self.plist, nickname, self.livello)
                    ptemp.aggiorna_punteggio()
                    self.livello=0
                else:
                    self.livello+=1
            else:
                print(f"Risposta sbagliata! La risposta corretta era la {indice_corretta}")
                self.partita=False
                nickname = input("Inserisci il tuo nickname: ")
                ptemp = Player(self.plist, nickname, self.livello)
                ptemp.aggiorna_punteggio()
                self.livello = 0




class Domanda():
    def __init__(self, testo, livello, risposta_corretta, altre_risposte):
        self.testo = testo
        self.livello = livello
        self.risposta_corretta = risposta_corretta
        self.altre_risposte = altre_risposte

    def get_risposte(self):
        risposte=[self.risposta_corretta]+[self.altre_risposte[0],self.altre_risposte[1],self.altre_risposte[2]]
        random.shuffle(risposte)
        return risposte


class Player():
    def __init__(self, plist, nickname, punteggio):
        self.plist = plist
        self.nickname = nickname
        self.punteggio = punteggio
        self.punteggi=self.carica_punteggi()

    def carica_punteggi(self):
        punteggi={}
        with open(self.plist, "r") as f:
            for line in f:
                punteggi[line.split(" ")[0]]=int(line.split(" ")[1])
        return punteggi

    def aggiorna_punteggio(self):
        self.punteggi.update({self.nickname:self.punteggio})
        punteggi_ordinati = dict(sorted(self.punteggi.items(), key=lambda item: item[1], reverse=True))
        with open(self.plist, "w") as f:
            for nome in punteggi_ordinati:
                f.write(f"{nome} {punteggi_ordinati[nome]}\n")