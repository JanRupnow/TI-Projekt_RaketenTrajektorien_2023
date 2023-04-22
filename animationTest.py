import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard
fig, ax = plt.subplots()

#line, = ax.plot(x, y)


Abwurfhoehe = 0                 # Höhe über dem Meeresspiegel nur in z-Richtung [m]
AbwurfWinkel = 0                # Winkel [°]
KoerperMasse = 100000           # Masse des Objekts [kg]
AbwurfGeschwindigkeit = 11000   # Abwurfsgeschwindigkeit [m/s]
Luftwiederstand = 0.0002        # Luftwiderstandsbeiwert
Startzeit = 0                   # [s]
Endzeit = 100000                # [s]
Rechenschritte = 100000
z_speed = 0                     # aktuell nicht genutzt     
x_speed = 0                     #  - Verwendung zur Einstellung des Schubs
Stop = False                    # Wenn eine Kollision mit der Erde festgestellt wurde, dann deaktiviert diese Variable weitere Berechnungen
FallBeschleunigung = 9.81       # [m/s^2]
c = Luftwiederstand/KoerperMasse

G = 6.674 * 10**(-11)           # Gravitationskonstante [Nm^2/kg^2]
m_E = 5.972 * 10**24            # Erdmasse [kg]
r_E = 6.37 * 10**6              # Erdradius [m]

r_x= np.zeros(Rechenschritte)   # x-Position [m]
r_z= np.zeros(Rechenschritte)   # z-Position [m]
v_x=np.zeros(Rechenschritte)    # x-Geschwindigkeit [m/s]
v_z=np.zeros(Rechenschritte)    # z-Geschwindigkeit [m/s]
t=np.linspace(Startzeit, Endzeit, Rechenschritte)
dt=(Endzeit-Startzeit)/Rechenschritte

AktuellerSchritt = 0
AktuellerRechenschritt = 0

# Berechnung nach Runge-Kutta Verfahren
def berechneNaechstenSchritt(i: int):
    global r_x, r_z, v_x, v_z
    # z-Komponente
    k1 = f1(r_x[i], r_z[i], v_z[i], t[i])
    k2 = f1(r_x[i], r_z[i], v_z[i] + k1*dt/2, t[i])
    k3 = f1(r_x[i], r_z[i], v_z[i] + k2*dt/2, t[i])
    k4 = f1(r_x[i], r_z[i], v_z[i] + k3*dt/2, t[i])
    k = (k1 + 2*k2 + 2*k3 + k4)/6
    v_z[i+1] = v_z[i] + k*dt
    r_z[i+1] = r_z[i] + v_z[i]*dt

    # x-Komponente
    k1 = f2(r_x[i], r_z[i], v_x[i], t[i])
    k2 = f2(r_x[i], r_z[i], v_x[i] + k1*dt/2, t[i])
    k3 = f2(r_x[i], r_z[i], v_x[i] + k2*dt/2, t[i])
    k4 = f2(r_x[i], r_z[i], v_x[i] + k3*dt/2, t[i])
    k = (k1 + 2*k2 + 2*k3 + k4)/6
    v_x[i+1] = v_x[i] + k*dt
    r_x[i+1] = r_x[i] + v_x[i]*dt

# Methode für die z-Komponente
def f1(r_x, r_z, x, t):
    y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_z - c*x**2*np.sign(x)
    
    # Beschleunigung soll nur zum aktuellen Zeitpunkt hinzugefügt werden
    #  - 'w' beschleunigt nach oben und 's' nach unten
    if AktuellerSchritt == AktuellerRechenschritt:
        if keyboard.is_pressed("w"):
            y += 10*FallBeschleunigung
        if keyboard.is_pressed("s"):
            y -= 10*FallBeschleunigung
        
    return y

# Methode für die y-Komponente
def f2(r_x, r_z, x, t):
    y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
    
    # Beschleunigung soll nur zum aktuellen Zeitpunkt hinzugefügt werden
    #  - 'd' beschleunigt nach rechts und 'a' nach links
    if AktuellerSchritt == AktuellerRechenschritt:
        if keyboard.is_pressed("d"):
            y += 10*FallBeschleunigung
        if keyboard.is_pressed("a"):
            y -= 10*FallBeschleunigung

    return y

# Anfangsbedingungen
r_x[0] = 0
r_z[0] = r_E + Abwurfhoehe
v_x[0] = AbwurfGeschwindigkeit * np.cos(AbwurfWinkel * np.pi / 180)
v_z[0] = AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi / 180)

# Die ersten 1000 Schritte berechnen
for i in range(1000):
    berechneNaechstenSchritt(AktuellerRechenschritt)
    AktuellerRechenschritt += 1

def animate(i):
    global AktuellerRechenschritt, AktuellerSchritt, Stop
    # Wenn WASD gedrückt werden müssen die Vorhersagen angepasst werden
    if not Stop:
        if keyboard.is_pressed("a") or keyboard.is_pressed("s") or keyboard.is_pressed("d") or keyboard.is_pressed("w"):
            AktuellerRechenschritt = AktuellerSchritt
            # Berechnung der nächsten 1000 Schritte
            for i in range(1000):
                berechneNaechstenSchritt(AktuellerRechenschritt)
                AktuellerRechenschritt += 1

        # Wenn die Funktion animate() aufgerufen wird, dann wird der nächste Schritt angezeigt, 
        # deshalb muss ein weiterer berechnet werden, um immer die nächsten 1000 Schritte anzuzeigen
        else:
            berechneNaechstenSchritt(AktuellerRechenschritt)
            AktuellerRechenschritt += 1

        # Wenn die Rakete in die Erde fliegt, dann stoppt die Berechnung
        if np.sqrt(r_x[i+1]**2 + r_z[i+1]**2) <= r_E:
            Stop = True

        # Anzeige mit neuen Daten aktualisieren
        line.set_ydata(r_z[AktuellerSchritt:AktuellerRechenschritt])
        line.set_xdata(r_x[AktuellerSchritt:AktuellerRechenschritt])
        lineBisJetzt.set_xdata(r_x[:AktuellerSchritt])
        lineBisJetzt.set_ydata(r_z[:AktuellerSchritt])
        aktuellerPunkt.set_xdata(r_x[AktuellerSchritt])
        aktuellerPunkt.set_ydata(r_z[AktuellerSchritt])

        AktuellerSchritt += 1
        # Skalierung der Animation relativ zu Erde
        ax.set_ylim(r_z[AktuellerSchritt]-r_E*5,r_z[AktuellerSchritt]+r_E*5)
        ax.set_xlim(left=r_x[AktuellerSchritt]-r_E*5, right=r_x[AktuellerSchritt]+r_E*5)
        # Skalierung des Graphen 

        # Anzeigen von Daten (rechts oben) (Position, Geschwindigkeit, Zeit)
        text.set_text("r_x: {0}m\nr_z: {1}m\nv_x: {2}m/s\nv_z: {3}m/s\nt: {4}s".format(
                            round(r_x[AktuellerSchritt], 2),
                            round(r_z[AktuellerSchritt], 2),
                            round(v_x[AktuellerSchritt], 2), 
                            round(v_z[AktuellerSchritt], 2), 
                            AktuellerSchritt * dt))
        text.set_position(((r_x[AktuellerSchritt]+r_E*5) * 0.8, (r_z[AktuellerSchritt]+r_E*5) * 0.8))

    return line, lineBisJetzt, aktuellerPunkt

# Plotten der Erde
circle1 = plt.Circle((0,0), r_E)
ax.add_artist(circle1)


# Fluglinie (zukünftige in rot)
line, = ax.plot(r_x[:AktuellerRechenschritt], r_z[:AktuellerRechenschritt], 'r--')
# Fluglinie (vergangene in blau)
lineBisJetzt, = ax.plot(r_x[:0], r_z[:0], 'b--')
# Punkt an der aktuellen Position
aktuellerPunkt, = ax.plot(r_x[0], r_z[0], 'o')

# Animationsfunktion
ani = animation.FuncAnimation(
    fig, animate, interval=1, blit=False)

text = ax.text(0, 0, '')

# Normalerweise würde beim Plotten, wenn 's' gedrückt wird, sich ein Fenster zum Speichern öffnen. Dies wird hiermit deaktiviert
plt.rcParams['keymap.save'].remove('s')
plt.rcParams["figure.autolayout"] = True
plt.show()