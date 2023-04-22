import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import keyboard
import time
fig, ax = plt.subplots()

#line, = ax.plot(x, y)


Abwurfhoehe = 0
AbwurfWinkel = 0
KoerperMasse = 100000
AbwurfGeschwindigkeit = 11000
Luftwiederstand = 0.0002
Startzeit = 0
Endzeit = 100000
Rechenschritte = 100000
z_speed = 0
x_speed = 0
Stop = False
FallBeschleunigung = 9.81
c = Luftwiederstand/KoerperMasse

G = 6.674 * 10**(-11)   # Gravitationskonstante [Nm^2/kg^2]
m_E = 5.972 * 10**24    # Erdmasse [kg]
r_E = 6.37 * 10**6      # Erdradius [m]

r_x= np.zeros(Rechenschritte)
r_z= np.zeros(Rechenschritte)
v_x=np.zeros(Rechenschritte)
v_z=np.zeros(Rechenschritte)
t=np.linspace(Startzeit, Endzeit, Rechenschritte)
dt=(Endzeit-Startzeit)/Rechenschritte

AktuellerSchritt = 0
AktuellerRechenschritt = 0

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

def f1(r_x, r_z, x, t):
    y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_z - c*x**2*np.sign(x)
    
    if AktuellerSchritt == AktuellerRechenschritt:
        #y = z_speed
        
        if keyboard.is_pressed("w"):
            #y = z_speed

            y += 10*FallBeschleunigung
        if keyboard.is_pressed("s"):
            y -= 10*FallBeschleunigung
        
    return y

def f2(r_x, r_z, x, t):
    y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
    
    if AktuellerSchritt == AktuellerRechenschritt:
        if keyboard.is_pressed("d"):
            y += 10*FallBeschleunigung
        if keyboard.is_pressed("a"):
            y -= 10*FallBeschleunigung

    return y

#def berechneAktuelleExtraKraft():
""""
def tastenGedrueckt():
    if keyboard.is_pressed("a"):
"""
# Anfangsbedingungen
r_x[0] = 0
r_z[0] = r_E + Abwurfhoehe
v_x[0] = AbwurfGeschwindigkeit * np.cos(AbwurfWinkel * np.pi / 180)
v_z[0] = AbwurfGeschwindigkeit * np.sin(AbwurfWinkel * np.pi / 180)

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

        else:
            berechneNaechstenSchritt(AktuellerRechenschritt)
            AktuellerRechenschritt += 1
        # Wenn die Rakete in die Erde fliegt stoppt die Berechnung
        if np.sqrt(r_x[i+1]**2 + r_z[i+1]**2) <= r_E:
            Stop = True

        # Anzeige mit neuen Daten aktualisieren
        line.set_ydata(r_z[:AktuellerRechenschritt])
        line.set_xdata(r_x[:AktuellerRechenschritt])
        AktuellerSchritt += 1

    return line,

# Plotten der Erde
circle1 = plt.Circle((0,0), r_E)
ax.add_artist(circle1)

# Fluglinie
line, = ax.plot(r_x[:AktuellerRechenschritt], r_z[:AktuellerRechenschritt], 'r--')

# Animationsfunktion
ani = animation.FuncAnimation(
    fig, animate, interval=1, blit=True, save_count=50)

# Normalerweise würde beim Plotten, wenn 's' gedrückt wird, sich ein Fenster zum Speichern öffnen. Dies wird hiermit deaktiviert
plt.rcParams['keymap.save'].remove('s')
plt.show()

###Darstellung der Funktion
""""
    line = ax.plot(x, Abwurfhoehe, 'r--')[0]  ###Wurfbahn
    ax.plot(WurfWeite, 0, 'bo')  ###Kontakt mit dem Boden
"""