
def main():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as ani
    fig, ax = plt.subplots()
    def f1(x, t):
        y=-FallBeschleunigung-c*x**2*np.sign(x) 
        if ((t>5)&(t<6)):
            y=y+10*FallBeschleunigung
        return y
    def f2(x, t):
        y=-c*x**2*np.sign(x)
        return y
    ###Eingabe Abwurfhoehe
    while True:
        try:
            Abwurfhoehe = float(input("Bitte geben sie eine Abwurfhoehe die groeßer als 0m ist an:  "))
            if 0 <= Abwurfhoehe:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine Abwurfhoehe die groeßer als 0m ist an.")
        except:
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Koerpermasse
    while True:
        try:
            KoerperMasse = float(input("Bitte geben sie eine positive Masse des Wurfkoerpes in kg an: "))
            if 0 <= KoerperMasse:
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
            if 0 <=AbwurfGeschwindigkeit:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine positive Abwurfgeschwindigkeit in KoerperMasse/s an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Luftwiederstand
    while True:
        try:
            Luftwiederstand = float(input("Bitte geben sie eine positive Luftwiederstand an: "))
            if 0 <=Luftwiederstand:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine positive Luftwiederstand an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Startzeit
    while True:
        try:
            Startzeit = float(input("Bitte geben sie eine Startzeit in Sekunden an: "))
            if 0 <=Startzeit:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine positive Startzeit an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Endzeit
    while True:
        try:
            Endzeit = float(input("Bitte geben sie eine Endzeit an: "))
            if Startzeit <=Endzeit:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine spätere Endzeit als Startzeit an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Eingabe Rechenschritte
    while True:
        try:
            Rechenschritte = int(input("Bitte geben sie eine Anzahl von Rechenschritte an: "))
            if 0 < Rechenschritte:
                break
            else:
                print("Ungültige Eingabe! Bitte geben sie eine postive Anzahl von Rechenschritten an.")
        except: 
            print("Bitte nur Zahlen eingeben!")
    ###Ausgabe der eingegebenen Werte
    print("\nEingebene Werte:\nAbwurfhoehe = " , Abwurfhoehe ,"m")
    print("Masse =" , KoerperMasse , "kg")
    print("Abwurfwinkel = " , AbwurfWinkel , "grad")
    print ("Abwurfgeschwindigkeit = " , AbwurfGeschwindigkeit , "m/s")
    print ("Luftwiederstand = " , Luftwiederstand)
    ###Berechnung Gesamtflugdauer
    FallBeschleunigung = 9.81
    c = Luftwiederstand/KoerperMasse
 
    r_x= np.zeros(Rechenschritte)
    r_z= np.zeros(Rechenschritte)
    v_x=np.zeros(Rechenschritte)
    v_z=np.zeros(Rechenschritte)
    t=np.linspace(Startzeit, Endzeit, Rechenschritte)
    dt=(Endzeit-Startzeit)/Rechenschritte

    # Anfangsbedingungen
    r_x[0] = 0
    r_z[0] = Abwurfhoehe
    v_x[0] = AbwurfGeschwindigkeit * np.cos(AbwurfWinkel * np.pi / 180)
    v_z[0] = AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi / 180)
    
    for i in range(Rechenschritte - 1):
        # z-Komponente
        k1 = f1(v_z[i], t[i])
        k2 = f1(v_z[i] + k1*dt/2, t[i])
        k3 = f1(v_z[i] + k2*dt/2, t[i])
        k4 = f1(v_z[i] + k3*dt/2, t[i])
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        v_z[i+1] = v_z[i] + k*dt
        r_z[i+1] = r_z[i] + v_z[i]*dt

        # x-Komponente
        k1 = f2(v_x[i], t[i])
        k2 = f2(v_x[i] + k1*dt/2, t[i])
        k3 = f2(v_x[i] + k2*dt/2, t[i])
        k4 = f2(v_x[i] + k3*dt/2, t[i])
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        v_x[i+1] = v_x[i] + k*dt
        r_x[i+1] = r_x[i] + v_x[i]*dt

    ###Darstellung der Funktion
    line = ax.plot(r_x, r_z, 'r--')  ###Wurfbahn
    #ax.plot(r_x, 0, 'ro')  ###Kontakt mit dem Boden

    ###Skalierung der Achsen
    ax.set_ylim(np.min(r_z)*1.1, np.max(r_z)*1.1)
    ax.set_xlim(np.min(r_x)*1.1, np.max(r_x)*1.1)

    ###Achsenbeschriftung
    ax.set_title('Schiefer Wurf')
    ax.set_xlabel('Wurfweite [m]')
    ax.set_ylabel('Wurfhoehe [m]')

    plt.show()
if __name__ == '__main__':
    main()