from tkinter import *
import random
import time
import pygame
pygame.init()

afficherIMAGE=afficher=0
EcranTitre=1 # 0 : pas d'écran titre, 1 : rien de selectionné, 2 : JOUER, 3 : Tuto, 4 : Credits, 5 : Quitter, 6 : ECRAN TUTO ou CREDITS
PeutJouer = False
commencerLeJeu = False
def input(event) : #variable input
    global canvas,Berangere,BerangereX,BerangereY,Edmond,EdmondX,EdmondY,commencerLeJeu, PeutJouer,EcranTitre,afficherIMAGE,afficher
    global fondtitre,titre,titre_jouer,titre_regles,titre_quitter,titre_soustitre1,titre_soustitre2,titre_credits
    touche = event.keysym
    #touches du menu
    if touche=="j" and EcranTitre>0 :
        EcranTitre=2
        for i in (titre_regles,titre_credits) : canvas.itemconfig(i,fill="#ffec9e")
        canvas.itemconfig(titre_quitter,fill="#014c58")
        canvas.itemconfig(titre_jouer,fill="yellow")
    if touche=="t" and EcranTitre>0 :
        EcranTitre=3
        for i in (titre_jouer,titre_credits,titre_quitter) : canvas.itemconfig(i,fill="#ffec9e")
        canvas.itemconfig(titre_quitter,fill="#014c58")
        canvas.itemconfig(titre_regles,fill="yellow")
    if touche=="c" and EcranTitre>0 :
        EcranTitre=4
        for i in (titre_jouer,titre_regles,titre_quitter) : canvas.itemconfig(i,fill="#ffec9e")
        canvas.itemconfig(titre_quitter,fill="#014c58")
        canvas.itemconfig(titre_credits,fill="yellow")
    if touche=="q" and EcranTitre>0 :
        EcranTitre=5
        for i in (titre_jouer,titre_regles,titre_quitter,titre_credits) : canvas.itemconfig(i,fill="#ffec9e")
        canvas.itemconfig(titre_quitter,fill="yellow")
    if touche=="Return" :

        if EcranTitre==6 :
            canvas.delete(afficherIMAGE)
            EcranTitre=1

        if EcranTitre==2 :
            for i in (fondtitre,titre,titre_jouer,titre_regles,titre_quitter,titre_soustitre1,titre_soustitre2,titre_credits) :
                canvas.delete(i)
            EcranTitre=0
            PeutJouer=True
        if EcranTitre==3 :
            EcranTitre=6
            afficher =PhotoImage(file="tutoriel.png")
            afficherIMAGE=canvas.create_image(0,0,anchor="nw",image=afficher)
        if EcranTitre==4 :
            EcranTitre=6
            afficher =PhotoImage(file="credits.png")
            afficherIMAGE=canvas.create_image(0,0,anchor="nw",image=afficher)
        if EcranTitre==5 :
            canvas.create_rectangle(0,0,700,700,fill="white")
            canvas.create_text(350,350,text="AU REVOIR",font=("Arial",90,"bold"))


    V = 30
    #déplacement berangere
    if touche == "z" and BerangereY-V > 0 : BerangereY -= V
    if touche == "s" and BerangereY+V < 700 : BerangereY += V
    if touche == "d" and BerangereX+V < 350 : BerangereX += V
    if touche == "q" and BerangereX-V > 0 : BerangereX -= V
    canvas.coords(Berangere,BerangereX-5,BerangereY-50,BerangereX+5,BerangereY+50)
    #déplacement edmond
    if touche == "Up" and EdmondY-V > 0 : EdmondY -= V
    if touche == "Down" and EdmondY+V < 700 : EdmondY += V
    if touche == "Right" and EdmondX+V < 700 : EdmondX += V
    if touche == "Left" and EdmondX-V > 350 : EdmondX -= V
    #lancement du jeu
    if touche == "space" and commencerLeJeu==False and PeutJouer==True :
        commencerLeJeu = True
        deplacement_balle()
        RandomBonus()
    canvas.coords(Edmond,EdmondX-5,EdmondY-50,EdmondX+5,EdmondY+50)
    canvas.coords(Edmond,EdmondX-5,EdmondY-50,EdmondX+5,EdmondY+50)

class Timer :
    def __init__(self,limite,joueur) : #fonction constructeur
        self.cpt = limite #la limite de temps, 5 secondes, 10s...
        self.joueur = joueur #1 : bérangère, 2 : edmond
        self.timer = canvas.create_text(20,30,text=self.cpt,fill="black",font=("Arial",20,"bold"))
        self.compteur() #appel de la fonction de comptage

    def compteur(self) :
        #dans cette boucle, on réduit le timer d'1 à chaque seconde. Quand le timer est à 0, on supprime le timer
        if commencerLeJeu==True :
            canvas.delete(self.timer)
            if self.joueur=="berangere" : self.timer = canvas.create_text(20,30,text=self.cpt,fill="yellow",font=("Arial",20,"bold"))
            if self.joueur=="edmond" : self.timer = canvas.create_text(680,30,text=self.cpt,fill="yellow",font=("Arial",20,"bold"))
            self.cpt-=1
            if self.cpt+1==0 :
                if "Bloqueur" in globals() : Bloqueur.autodestruction()
                self.autodestruction()
            else : fen.after(1000,self.compteur)
        else : self.autodestruction()

    def autodestruction(self) :
        #on détruit alors l'objet timer sur tkinter, et l'instance de la classe
        canvas.delete(self.timer)
        del self

couleur_stade=1
couleurR = 255
couleurG = 0
couleurB = 0
class couleur :
    def __init__(self,item) :
        self.objet= item
        self.couleur()

    def couleur(self) :
        global couleur_stade, couleurB, couleurG, couleurR, commencerLeJeu
        if commencerLeJeu==True :
            #tout les stades et leurs détection
            if couleurR==255 and couleurG==0 and couleurB==0 : couleur_stade=1
            if couleurR==255 and couleurG==255 and couleurB==0 : couleur_stade=2
            if couleurR==0 and couleurG==255 and couleurB==0 : couleur_stade=3
            if couleurR==0 and couleurG==255 and couleurB==255 : couleur_stade=4
            if couleurR==0 and couleurG==0 and couleurB==255 : couleur_stade=5
            if couleurR==255 and couleurG==0 and couleurB==255 : couleur_stade=6
            #changement de la couleur, attention la valeure peut être : 1,3,5,15,17,51,85,255 (penser à changer aussi la valeure dans "after")
            if couleur_stade==1 : couleurG +=5
            if couleur_stade==2 : couleurR -=5
            if couleur_stade==3 : couleurB +=5
            if couleur_stade==4 : couleurG -=5
            if couleur_stade==5 : couleurR +=5
            if couleur_stade==6 : couleurB -=5
            #création de la couleur sous la forme #rrrgggbbb en ajoutant des 0 si nécéssaire
            couleurDEF='#%02x%02x%02x' % (couleurR,couleurG,couleurB)
            #définition de la couleur
            canvas.itemconfig(self.objet,fill =couleurDEF, outline=couleurDEF)

        fen.after(10,self.couleur)

"""fonction bonus, faisant, à un interval de temps défini, apparaitre un bonus
il y a 3 types de bonus : Commun, Super, Légendaire.
Le Bonus Commun apparait sur le coté du joueur, et donne un bonus mineur
Le Bonus Super apparait en plus gros, sur le même coté du joueur, et lui donne un bonus majeur.
Le Bonus Légendaire apparait en très gros, sur la limite, et procure un bonus majeur utilisable en temps voulu.
BonusVALUE vaut 1 pour Commun, 2 pour Super, 3 pour légendaire.
"""
class Bonus :

    def __init__(self,posX,posY,bonustype) : #fonction constructeur
        if bonustype=="commun" : self.objet = canvas.create_rectangle(posX-10,posY-10,posX+10,posY+10,fill="blue",outline="red",width=3)
        if bonustype=="super" : self.objet = canvas.create_rectangle(posX-30,posY-30,posX+30,posY+30,fill="yellow",outline="brown",width=5)
        if bonustype=="legendaire" :
            self.objet = canvas.create_rectangle(posX-50,posY-50,posX+50,posY+50,fill="white",outline="#1F1F1F",width=10)
            self.objetTEXTE = canvas.create_text(posX,posY,text="?",fill="white",font=("Arial",50))
            self.couleur = couleur(self.objet)
        self.x = posX
        self.y = posY
        self.type = bonustype

    def collision(self) :
        global BerangereX,BerangereY,EdmondX,EdmondY
        if self.type=="commun" : dim = 20
        if self.type=="super" : dim = 40
        if self.type=="legendaire" : dim = 60
        #test Bérangere dans le Bonus, on test avec les 4 points
        if self.x-dim<=BerangereX-5<=self.x+dim and self.y-dim<=BerangereY-50<=self.y+dim : self.get(1)
        elif self.x-dim<=BerangereX+5<=self.x+dim and self.y-dim<=BerangereY+50<=self.y+dim : self.get(1)
        elif self.x-dim<=BerangereX-5<=self.x+dim and self.y-dim<=BerangereY+50<=self.y-dim : self.get(1)
        elif self.x-dim<=BerangereX+5<=self.x+dim and self.y-dim<=BerangereY-50<=self.y-dim : self.get(1)
        #test Edmond
        elif self.x-dim<=EdmondX-5<=self.x+dim and self.y-dim<=EdmondY-50<=self.y+dim : self.get(2)
        elif self.x-dim<=EdmondX+5<=self.x+dim and self.y-dim<=EdmondY+50<=self.y+dim : self.get(2)
        elif self.x-dim<=EdmondX-5<=self.x+dim and self.y-dim<=EdmondY+50<=self.y-dim : self.get(2)
        elif self.x-dim<=EdmondX+5<=self.x+dim and self.y-dim<=EdmondY-50<=self.y-dim : self.get(2)
        else : fen.after(40,self.collision)

    def get(self,joueur) : #fonction se déclenchant si un des deux joueurs entre en collision avec un bonus
       global Bloqueur
       canvas.delete(self.objet)
       if self.type=="commun" :
        if joueur==1 : Bloqueur = communBONUS(1)
        if joueur==2 : Bloqueur = communBONUS(2)
       if self.type=="legendaire" :
        canvas.delete(self.objetTEXTE)
        if joueur==1 : Bloqueur = legendaireBONUS(1)
        if joueur==2 : Bloqueur = legendaireBONUS(2)
       if self.type=="super" :
        #on appelle un Bloqueur
        if joueur==1 : Bloqueur = superBONUS(1)
        if joueur==2 : Bloqueur = superBONUS(2)


class legendaireBONUS :
    def __init__(self,joueur) :
        self.joueur = joueur
        if self.joueur==1 :
            self.objet = canvas.create_rectangle(351,0,700,700,fill="red",outline="red") #création du bloqueur
            self.timer = Timer(10,"berangere") #on appelle un timer de 5 secondes, du coté de bérangère, qui va détruire le bloqueur à sa fin.
        if self.joueur==2 :
            self.objet = canvas.create_rectangle(0,0,349,700,fill="blue",outline="blue")
            self.timer = Timer(10,"edmond")
        self.isblack = False
        self.clignotement()
        canvas.tag_lower(self.objet)

    def clignotement(self) :
        if self.joueur==1 and self.isblack==False : canvas.itemconfig(self.objet,fill ="red", outline="red")
        if self.joueur==2 and self.isblack==False : canvas.itemconfig(self.objet,fill ="blue", outline="blue")
        if self.isblack==True : canvas.itemconfig(self.objet,fill="black",outline="black")
        if self.isblack==False :
            self.isblack = True
            fen.after(1950,self.clignotement)
        else :
            self.isblack = False
            fen.after(50,self.clignotement)

    def autodestruction(self) :
        global commencerLeJeu, Legendaire
        #on supprime l'objet tkinter, puis l'instance de classe
        canvas.delete(self.objet)
        del self
        #si le jeu n'est pas perdu, on relance l'opération de bonus.
        if commencerLeJeu==True : fen.after(8000,RandomBonus)

class superBONUS :
    """Le superBONUS est un bonus qui prend la même couleur multicolore de la balle,
    ainsi il est difficile pour le joueur contraint de retrouver la trajectoire de la balle"""
    def __init__(self,joueur) : #fonction appellée à l'appel de la classe
        self.joueur = joueur
        if self.joueur==1 :
            self.objet = canvas.create_rectangle(351,0,700,700,fill="red",outline="red") #création du bloqueur
            self.timer = Timer(5,"berangere") #on appelle un timer de 5 secondes, du coté de bérangère, qui va détruire le bloqueur à sa fin.
        if self.joueur==2 :
            self.objet = canvas.create_rectangle(0,0,349,700,fill="red",outline="red")
            self.timer = Timer(5,"edmond")
        self.couleur = couleur(self.objet) #on met de la même couleur le bloqueur de la balle
        canvas.tag_lower(self.objet) #evidemment le bloqueur doit se trouver en arriere plan.

    def autodestruction(self) :
        global commencerLeJeu, Legendaire
        #on supprime l'objet tkinter, puis l'instance de classe
        canvas.delete(self.objet)
        del self
        #si le jeu n'est pas perdu, on relance l'opération de bonus.
        if commencerLeJeu==True : fen.after(8000,RandomBonus)

class communBONUS :
    def __init__(self,joueur) :
        self.joueur = joueur
        self.on = True
        self.listeobjets = [FausseBalle(100),FausseBalle(200),FausseBalle(300),FausseBalle(400),FausseBalle(500),FausseBalle(600),FausseBalle(150),FausseBalle(250),FausseBalle(350),FausseBalle(450),FausseBalle(550),FausseBalle(650),FausseBalle(50)]
        if self.joueur==2 :
            for i in self.listeobjets : i.switchVx()
            self.timer = Timer(20,"edmond")
        else : self.timer = Timer(20,"berangere")
        for i in self.listeobjets : i.deplacement()
        fen.after(3000,self.encore)

    def encore(self):
        global commencerLeJeu
        if commencerLeJeu==True :
            for i in self.listeobjets : i.autodestruction()
            self.listeobjets = [FausseBalle(100),FausseBalle(200),FausseBalle(300),FausseBalle(400),FausseBalle(500),FausseBalle(600),FausseBalle(150),FausseBalle(250),FausseBalle(350),FausseBalle(450),FausseBalle(550),FausseBalle(650),FausseBalle(50)]
            if self.joueur==2 :
                for i in self.listeobjets :
                    i.switchVx()
            for i in self.listeobjets :
                i.deplacement()
            if self.on==True : fen.after(3000,self.encore)

    def autodestruction(self) :
        self.on = False
        del self
        if commencerLeJeu==True : fen.after(8000,RandomBonus)

class FausseBalle :
    def __init__(self,y) :
        self.x = 350
        self.y = y
        self.Vx = random.randint(3,9)
        self.Vy = random.randint(3,9)
        self.objet = canvas.create_oval(self.x-10,y-10,self.x+10,y+10,fill="gray",outline="gray")
        self.couleur = couleur(self.objet)

    def switchVx(self) :
        self.Vx = -self.Vx

    def deplacement(self) :
        futurX,futurY = self.x + self.Vx, self.y + self.Vy
        if futurY > 690 or futurY < 0 :
            self.Vy = -self.Vy
            futurY = self.y + self.Vy
        if futurX > 700 or futurX < 0 : self.autodestruction()
        self.x,self.y = futurX,futurY
        canvas.coords(self.objet,self.x-10,self.y-10,self.x+10,self.y+10)
        fen.after(40,self.deplacement)

    def autodestruction(self) :
        canvas.delete(self.objet)
        del self







def bonus(bonusVALUE) :
    global Bcommun,Bsuper,Ecommun,Esuper,Legendaire
    JoueurQuiBeneficieDuBonus = random.randint(0,1) #0 : Bérangère, 1 : Edmond
    if bonusVALUE==1 :
        #code d'apparition d'un bonus commun
        if JoueurQuiBeneficieDuBonus==0 :
            Bcommun = Bonus(random.randint(10,340),random.randint(10,690),"commun")
            Bcommun.collision()
        if JoueurQuiBeneficieDuBonus==1 :
            Ecommun = Bonus(random.randint(360,690),random.randint(10,690),"commun")
            Ecommun.collision()
    if bonusVALUE==2 :
        #code d'apparition d'un bonus Super
        if JoueurQuiBeneficieDuBonus==0 :
            Bsuper = Bonus(random.randint(30,320), random.randint(30,670),"super")
            Bsuper.collision()
        if JoueurQuiBeneficieDuBonus==1 :
            Esuper = Bonus(random.randint(390,670), random.randint(30,670),"super")
            Esuper.collision()
    if bonusVALUE==3 :
        #code d'apparition d'un bonus Légendaire
        Legendaire = Bonus(350,random.randint(50,650),"legendaire")
        Legendaire.collision()











#Initialisation de la position des deux joueurs
BerangereX = 100
BerangereY = 350
EdmondX = 600
EdmondY = 350

#mise en place fenetre
fen = Tk()
fen.geometry("700x700")
fen.resizable(height=False,width=False)
canvas = Canvas(fen, width=700, height=700, bg="black")
canvas.place(x=0,y=0)

a = 0
b = 0
#Canvas du score
can1 = canvas.create_text(370,15, text="{}".format(a), fill="white", font=('Arial',14, 'bold'))
can2 = canvas.create_text(328,15, text="{}".format(b), fill="white", font=('Arial',14, 'bold'))
#mise en place limite
Limite = canvas.create_line(350,0,350,700,width=3,fill="white")
#Vitesse de la balle
vitesseBalle = 7
V1X, V1Y = vitesseBalle, 4
#Position en x et y de la balle + sa création
Balle1X, Balle1Y = 350,350
Balle1 = canvas.create_oval(340, 340, 360, 360, fill = 'white')
Balle_multi = couleur(Balle1)
#mise en place joueurs
Berangere = canvas.create_rectangle(BerangereX-5,BerangereY-50,BerangereX+5,BerangereY+50,width=0,fill='blue')
Edmond = canvas.create_rectangle(EdmondX-5,EdmondY-50,EdmondX+5,EdmondY+50,width=0,fill='red')
fen.bind_all("<Key>",input)

def deplacement_balle():
    global V1X, V1Y, Balle1X, Balle1Y, canvas ,Berangere ,BerangereX ,BerangereY ,Edmond ,EdmondX ,EdmondY,x,y,commencerLeJeu,x,y,a,b,can1,can2
    if commencerLeJeu==True :
        if V1X<=0 : V1X = -vitesseBalle
        if V1X>=0 : V1X = vitesseBalle
        futurX, futurY = Balle1X + V1X, Balle1Y + V1Y
        #collision avec les bords
        if futurY > 690 or futurY < 0 :
            V1Y = - V1Y
            futurY = Balle1Y + V1Y
        Balle1X, Balle1Y = futurX, futurY
        canvas.coords(Balle1, Balle1X - 10, Balle1Y -10, Balle1X + 10, Balle1Y + 10)
        #gestion de la distance
        dist = (Balle1X)**2 + (Balle1Y)**2
        if dist > 400 :
            fen.after(40,deplacement_balle)
        #gestion de la collision avec Berangere et Edmond.
        if  BerangereX-19 <= futurX <= BerangereX + 19 and BerangereY -60 < futurY < BerangereY + 60:
            V1X = - V1X
            futurY = Balle1Y + V1Y
            futurX = Balle1X + V1X
        if  EdmondX-19<= futurX <= EdmondX + 19 and EdmondY -60 < futurY < EdmondY + 60:
            V1X = - V1X
            futurY = Balle1Y + V1Y
            futurX = Balle1X + V1X
             #Définition du score
    if Balle1X <= 2:
        canvas.delete(can1)
        a = a+1
        can1 = canvas.create_text(370,15, text="{}".format(a), fill="white", font=('Arial',14, 'bold'))
        reset_balle()
    if Balle1X >= 686:
        canvas.delete(can2)
        b = b+1
        can2 = canvas.create_text(328,15, text="{}".format(b), fill="white", font=('Arial', 14, 'bold'))
        reset_balle()

def augmentationVitesseBalle() :
    global vitesseBalle, commencerLeJeu
    if commencerLeJeu==True : vitesseBalle+=1
    fen.after(5000,augmentationVitesseBalle)


def reset_balle() :
    #fonction qui se déclenche quand un joueur perd.
    global commencerLeJeu,canvas,Balle1,Balle1X,Balle1Y,Bcommun,Ecommun,Bsuper,Esuper,Legendaire,BerangereX,BerangereY,EdmondX,EdmondY,vitesseBalle
    commencerLeJeu=False
    vitesseBalle=7
    canvas.coords(Balle1,340, 340, 360, 360) #replacement balle
    canvas.itemconfig(Balle1,fill ="white", outline="white") #colorisation blanche de la balle
    Balle1X, Balle1Y = 350, 350
    EdmondX = 600
    EdmondY = 350
    BerangereX,BerangereY,EdmondX,EdmondY=100,350,600,350
    #replacement des joueurs
    canvas.coords(Berangere,100-5,350-50,100+5,350+50)
    canvas.coords(Edmond,600-5,350-50,600+5,350+50)
    #élimination de tout bonus, si il y en a
    if "Bloqueur" in globals() : Bloqueur.autodestruction()
    if "Bcommun" in globals() : canvas.delete(Bcommun.objet)
    if "Ecommun" in globals() : canvas.delete(Ecommun.objet)
    if "Bsuper" in globals() : canvas.delete(Bsuper.objet)
    if "Esuper" in globals() : canvas.delete(Esuper.objet)
    if "Legendaire" in globals() :
        canvas.delete(Legendaire.objet)
        canvas.delete(Legendaire.objetTEXTE)
    if a==10 : finduJEU("edmond")
    if b==10 : finduJEU("berangere")

def RandomBonus() :
    """fonction qui sélectionne, au hasard, un bonus.
    - Un bonus commun a 40% de chances d'apparaitre
    - Un bonus super a 30% de chances d'apparaitre
    - Un bonus légendaire a 20% de chances d'apparaitre"""
    global commencerLeJeu
    if commencerLeJeu==True :
        n = random.randint(0,100)
        if 0<=n<=40 : bonus(1)
        if 41<=n<=70 : bonus(2)
        if 71<=n<=100 : bonus(3)

def finduJEU(joueur) :
    global Berangere,Edmond,Limite,Balle1,PeutJouer,canvas,can1,can2,a,b
    PeutJouer=False
    trucsasupprimer = [Berangere,Edmond,Limite,Balle1,can1,can2]
    for i in trucsasupprimer : canvas.delete(i)
    fond = canvas.create_rectangle(0,0,700,700,fill="white")
    canvas.tag_lower(fond)
    if joueur=="berangere" : canvas.create_text(350,250,text="B R A V O", fill="blue", font=('Arial', 100, 'bold'))
    if joueur=="edmond" : canvas.create_text(350,250,text="B R A V O", fill="red", font=('Arial', 100, 'bold'))
    berangereSCORE = canvas.create_text(200,500,text=str(b),fill="black",font=('Arial', 100, 'bold'))
    edmondSCORE = canvas.create_text(500,500,text=str(a),fill="black",font=('Arial', 100, 'bold'))
    tiret = canvas.create_text(350,500,text="-",fill="black",font=('Arial', 100, 'bold'))


logo=PhotoImage(file="logo.png")
titre_fond=PhotoImage(file="titre_fond.png")
fondtitre= canvas.create_image(0,0,anchor="nw",image=titre_fond)
titre= canvas.create_image(0,10,anchor="nw",image=logo)
titre_jouer = canvas.create_text(350,300,text="JOUER",fill="#ffec9e",font=("Arial",50,"bold"))
titre_regles = canvas.create_text(350,400,text="TUTORIEL",fill="#ffec9e",font=("Arial",50,"bold"))
titre_credits = canvas.create_text(350,500,text="CREDITS",fill="#ffec9e",font=("Arial",50,"bold"))
titre_quitter = canvas.create_text(90,670,text="QUITTER",fill="#014c58",font=("Arial",25,"bold"))
titre_soustitre1 = canvas.create_text(350,20,text="Bienvenue dans PONG-SENSEI, appuyez sur l'initial de la section pour la selectionner.",fill="#012243",font=("Arial",10))
titre_soustitre2 = canvas.create_text(350,40,text="Puis appuyez sur ENTRÉE pour choisir cette section.",fill="#012243",font=("Arial",10))




def musique() :
    if pygame.mixer.music.get_busy()==False :
        a = random.randint(1,7)
        if a==1 : pygame.mixer.music.load("1.mp3")
        if a==2 : pygame.mixer.music.load("2.mp3")
        if a==3 : pygame.mixer.music.load("3.mp3")
        if a==4 : pygame.mixer.music.load("4.mp3")
        if a==5 : pygame.mixer.music.load("5.mp3")
        if a==6 : pygame.mixer.music.load("6.mp3")
        if a==7 : pygame.mixer.music.load("7.mp3")
        pygame.mixer.music.play()
    fen.after(1000,musique)



image=[PhotoImage(file="stock/1.png"),PhotoImage(file="stock/2.png"),PhotoImage(file="stock/3.png"),PhotoImage(file="stock/4.png"),PhotoImage(file="stock/5.png"),PhotoImage(file="stock/6.png"),PhotoImage(file="stock/7.png"),PhotoImage(file="stock/8.png"),PhotoImage(file="stock/9.png"),PhotoImage(file="stock/10.png")]
fond = canvas.create_image(350,350,image=image[0])
def creerimages() :
    global fond,image
    a = random.randint(0,len(image)-1)
    canvas.itemconfig(fond,image=image[a])
    fen.after(5000,creerimages)


pygame.mixer.music.load("1.mp3")
pygame.mixer.music.play()

def fondtoujoursaufond() :
    global fond,canvas
    canvas.tag_lower(fond)
    fen.after(10,fondtoujoursaufond)


musique()
creerimages()
fondtoujoursaufond()
augmentationVitesseBalle()
fen.mainloop()
