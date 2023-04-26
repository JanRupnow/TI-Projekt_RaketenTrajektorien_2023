import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard
import time
fig, ax = plt.subplots()

#line, = ax.plot(x, y)
ExtraKraft= 0
Startwinkel = 45                # Winkel des Starts auf der Erde [°C]
Abwurfhoehe = 0                 # Höhe über dem Meeresspiegel nur in z-Richtung [m]
AbwurfWinkel = 0                # Winkel [°]
KoerperMasse = 100000           # Masse des Objekts [kg]
AbwurfGeschwindigkeit = 11000   # Abwurfsgeschwindigkeit [m/s]
Luftwiederstand = 0.0162        # Luftwiderstandsbeiwert
Startzeit = 0                   # [s]
Endzeit = 200000                # [s]
Rechenschritte = 100000
z_schub = 0                     # aktuell nicht genutzt     
x_schub = 0                     #  - Verwendung zur Einstellung des Schubs
Stop = False                    # Wenn eine Kollision mit der Erde festgestellt wurde, dann deaktiviert diese Variable weitere Berechnungen
FallBeschleunigung = 9.81       # [m/s^2]
c = Luftwiederstand/KoerperMasse
ZeitArray = []
KraftArray = []

p_0 = 1.225 # Luftdichte auf Meereshöhe [kg/m^3]
h_s = 8400  # Skalenhöhe [m]

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

### Funktionen ###
x_last_update_time = 0
z_last_update_time = 0
WAIT_TIME = 1  # 2 Sekunden

# Funktion zur Verarbeitung der Schubes
def on_key_press(event):
    global x_schub, z_schub, x_last_update_time, z_last_update_time
    current_time = time.time()
    if event.name == "w":
        if current_time - z_last_update_time >= WAIT_TIME:
            z_schub += 1
            z_last_update_time = current_time
    elif event.name == "s":
        if current_time - z_last_update_time >= WAIT_TIME:
            z_schub -= 1
            z_last_update_time = current_time
    elif event.name == "d":
        if current_time - x_last_update_time >= WAIT_TIME:
            x_schub += 1
            x_last_update_time = current_time
    elif event.name == "a":
        if current_time - x_last_update_time >= WAIT_TIME:
            x_schub -= 1
            x_last_update_time = current_time

    # Überprüfen, ob die Position innerhalb des erlaubten Bereichs liegt
    x_schub = max(-10, min(x_schub, 10))
    z_schub = max(-5, min(z_schub, 5))
def check_key_press():
    global x_schub, z_schub, x_last_update_time, z_last_update_time
    current_time = time.time()
    if ((current_time - z_last_update_time >= WAIT_TIME) and (current_time - x_last_update_time >= WAIT_TIME)):
        return True
    elif (((current_time - z_last_update_time >= WAIT_TIME) or (current_time - x_last_update_time >= WAIT_TIME))): 
        return True
    else: 
        return False
    

# Key-Listener registrieren
# Berechnung nach Runge-Kutta Verfahren
def berechneNaechstenSchritt(i: int):
    global r_x, r_z, v_x, v_z, F
    # z-Komponente
    k1 = f1(r_x[i], r_z[i], v_z[i], t[i])
    k2 = f1(r_x[i], r_z[i], v_z[i] + k1*dt/2, t[i])
    k3 = f1(r_x[i], r_z[i], v_z[i] + k2*dt/2, t[i])
    k4 = f1(r_x[i], r_z[i], v_z[i] + k3*dt/2, t[i])
    k = (k1 + 2*k2 + 2*k3 + k4)/6
    v_z[i+1] = v_z[i] + k*dt
    r_z[i+1] = r_z[i] + v_z[i]*dt
    F = k * KoerperMasse

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
    r0 = np.sqrt(r_x**2 + r_z**2)
    y=( -(G*m_E/r0**2) - (Luftwiederstand*x**2*np.sign(x) * p_0 * np.exp(-abs((r0-r_E)) / h_s))/(2 * KoerperMasse) ) * (r_z/r0) #Extrakraft z einbauen
    #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_z - c*x**2*np.sign(x)
    if AktuellerSchritt == AktuellerRechenschritt:
        if z_schub!=0:
            y += 10*z_schub
    # Beschleunigung soll nur zum aktuellen Zeitpunkt hinzugefügt werden
    return y

# Methode für die x-Komponente
def f2(r_x, r_z, x, t):
    r0 = np.sqrt(r_x**2 + r_z**2)
    y=( -(G*m_E/r0**2) - (Luftwiederstand*x**2*np.sign(x) * p_0 * np.exp(-abs((r0-r_E)) / h_s))/(2 * KoerperMasse) ) * (r_x/r0) #Extrakraft x einbauen
    #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
    if AktuellerSchritt == AktuellerRechenschritt:
        if x_schub!=0:
            y += 10*x_schub
    # Beschleunigung soll nur zum aktuellen Zeitpunkt hinzugefügt werden

    return y

# Anfangsbedingungen
r_x[0] = (r_E + Abwurfhoehe) * np.sin(Startwinkel * np.pi / 180)
r_z[0] = (r_E + Abwurfhoehe) * np.cos(Startwinkel * np.pi / 180)
v_x[0] = AbwurfGeschwindigkeit * np.cos(AbwurfWinkel * np.pi / 180)
v_z[0] = AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi / 180)

# Die ersten 1000 Schritte berechnen
for i in range(1000):
    berechneNaechstenSchritt(AktuellerRechenschritt)
    AktuellerRechenschritt += 1

def animate(i):
    global AktuellerRechenschritt, AktuellerSchritt, Stop, KraftArray, ZeitArray,ExtraKraft
    # Wenn WASD gedrückt werden müssen die Vorhersagen angepasst werden
    if not Stop:
        if (check_key_press):
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

        keyboard.on_press(on_key_press)


        # Wenn die Rakete in die Erde fliegt, dann stoppt die Berechnung
        if np.sqrt(r_x[AktuellerSchritt+1]**2 + r_z[AktuellerSchritt+1]**2) <= r_E:
            Stop = True

        # Anzeige mit neuen Daten aktualisieren
        line.set_ydata(r_z[AktuellerSchritt:AktuellerRechenschritt])
        line.set_xdata(r_x[AktuellerSchritt:AktuellerRechenschritt])
        lineBisJetzt.set_xdata(r_x[:AktuellerSchritt+1])
        lineBisJetzt.set_ydata(r_z[:AktuellerSchritt+1])
        aktuellerPunkt.set_xdata(r_x[AktuellerSchritt:AktuellerSchritt+1])
        aktuellerPunkt.set_ydata(r_z[AktuellerSchritt:AktuellerSchritt+1])

        AktuellerSchritt += 1
        # Skalierung der Animation relativ zu Erde
        ax.set_ylim(r_z[AktuellerSchritt]-r_E*5,r_z[AktuellerSchritt]+r_E*5)
        ax.set_xlim(left=r_x[AktuellerSchritt]-r_E*5, right=r_x[AktuellerSchritt]+r_E*5)
        # Skalierung des Graphen 

        # Anzeigen von Daten (rechts oben) (Position, Geschwindigkeit, Zeit)
        text.set_text("r_x: {0}km\nr_z: {1}km\nv_x: {2}m/s\nv_z: {3}m/s\nt: {4}s\nF: {5}X-Schub\n {6} Z-Schub".format(
                            round(r_x[AktuellerSchritt]/1000, 2),
                            round(r_z[AktuellerSchritt]/1000, 2),
                            round(v_x[AktuellerSchritt], 2),
                            round(v_z[AktuellerSchritt], 2), 
                            AktuellerSchritt * dt,
                            x_schub,
                            z_schub))
        # Array mit momentaner Zeit füllen
        ZeitArray.append(AktuellerSchritt*dt)
        # Array mit momentaner Kraft füllen
        KraftArray.append(F)
    else:
        line.set_ydata(r_z[:0])
        line.set_xdata(r_x[:0])

    return line, lineBisJetzt, aktuellerPunkt, ZeitArray, KraftArray

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

text = ax.text(0.65, 0.75, '', transform=ax.transAxes)

plt.gca().set_aspect('equal')
# Normalerweise würde beim Plotten, wenn 's' gedrückt wird, sich ein Fenster zum Speichern öffnen. Dies wird hiermit deaktiviert
plt.rcParams['keymap.save'].remove('s')
plt.show()
plt.close()
plt.plot(ZeitArray, KraftArray)
# Add labels and title
plt.xlabel('Zeit in Sekunden')
plt.ylabel('Kraft')
plt.title('Kraftgraph des Raketenstarts')
# Show the plot
plt.show()