import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani

def main():
    fig, ax = plt.subplots()
    ###Eingabe Abwurfhoehe
    while True:
        try:
            Abwurfhoehe = float(input("Bitte geben sie eine Abwurfhoehe die groeßer als 0m ist an:  "))
            if 0 < Abwurfhoehe:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine Abwurfhoehe die groeßer als 0m ist an.")
        except:
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Koerpermasse
    while True:
        try:
            KoerperMasse = float(input("Bitte geben sie eine positive Masse des Wurfkoerpes in kg an: "))
            if 0 < KoerperMasse:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine positive Masse des Wurfkoerpes in kg an.")
        except:
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Abwurfwinkel
    while True:
        try:
            AbwurfWinkel = float(input("Bitte geben sie einen Abwurfwinkel zwischen 0 und 90 Grad an: "))
            if 0 <= AbwurfWinkel <= 90:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie einen Wert zwischen 0 und 90 Grad an.")
        except:
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Abwurfgeschwindigkeit
    while True:
        try:
            AbwurfGeschwindigkeit = float(input("Bitte geben sie eine Abwurfgeschwindigkeit in KoerperMasse/s an: "))
            if 0 <AbwurfGeschwindigkeit:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine positive Abwurfgeschwindigkeit in KoerperMasse/s an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Ausgabe der eingegebenen Werte
    print("\nIhre Werte:\nAbwurfhoehe = " , Abwurfhoehe ,"KoerperMasse")
    print("Masse =" , KoerperMasse , "kg")
    print("Abwurfwinkel = " , AbwurfWinkel , "grad")
    print ("Abwurfgeschwindigkeit = " , AbwurfGeschwindigkeit , "KoerperMasse/s")

    ###Berechnung Gesamtflugdauer
    FallBeschleunigung = 9.81
    FlugDauer = AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi/180) / FallBeschleunigung

    ###Berechnung Maximale Hoehe 
    MaximalHoehe = 0.5 * FallBeschleunigung * FlugDauer ** 2 + Abwurfhoehe

    ###Berechnung Maximale Wurfweite w
    WurfWeite = (AbwurfGeschwindigkeit * np.cos(AbwurfWinkel * np.pi/180) * (AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi/180) + np.sqrt(AbwurfGeschwindigkeit ** 2 * np.sin(AbwurfWinkel * np.pi/180) ** 2 + 2 * FallBeschleunigung * Abwurfhoehe))) / FallBeschleunigung

    ###Wurfbahn Funktion
    def Wurfbahn(x):
        return (-(FallBeschleunigung / (2 * AbwurfGeschwindigkeit ** 2 * np.cos(AbwurfWinkel * np.pi / 180) ** 2)) * x ** 2) + (np.tan(AbwurfWinkel * np.pi / 180) * x + Abwurfhoehe)

    ###Berechnung der Flugbahn mit allen Punkten
    x = np.linspace(0, WurfWeite, 1000)
    Abwurfhoehe = Wurfbahn(x)

    ###Darstellung der Funktion
    line = ax.plot(x, Abwurfhoehe, 'r--')[0]  ###Wurfbahn
    ax.plot(WurfWeite, 0, 'ro')  ###Kontakt mit dem Boden

    ###Animation
    def animate(i):
        line.set_xdata(x[:int(i * len(x) / 150)])
        line.set_ydata(Abwurfhoehe[:int(i * len(Abwurfhoehe) / 150)])
        return line,

    ani = ani.FuncAnimation(fig, animate, frames=150, interval=25, repeat=True)

    ###Skalierung der Achsen
    ax.set_ylim(0, MaximalHoehe + (0.1 * MaximalHoehe))
    ax.set_xlim(0, WurfWeite + (0.1 * WurfWeite))

    ###Achsenbeschriftung
    ax.set_title('Schiefer Wurf')
    ax.set_xlabel('Wurfweite [m]')
    ax.set_ylabel('Wurfhoehe [m]')

    plt.show()
    
if __name__ == '__main__':
    main()