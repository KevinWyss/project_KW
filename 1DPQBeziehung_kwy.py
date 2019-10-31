### numerisch, hydraulische 1D Abflussmodellierung, Kevin Wyss, 2019 ###
# Abflussmodellierung mit der Fliessformel nach Manning Strickler (Q = vm * A)

import numpy as np                        # Liste erstellen / txt laden
import pandas as pd                       # Profil laden / listen zusammenfuegen
import matplotlib.pyplot as plt           # Packet um zu plotten
from prettytable import PrettyTable       # Darstellung der Daten in Tabelle

########################################################################
# ----------------------- Parameter definieren ----------------------- #
########################################################################
pn = 'Querprofil Hasliaare'         # Profilname definieren
fn = 'qp_hasliaare_151019.txt'      # file name (fn) definieren. = Name des files in dem das Profil gespeichert ist
h = 50  # [cm]                      # Wasserhoehe definieren, meist abgelesen von eiener Pegelstation
kst = 25                            # Rauhigkeitsbeiwert nach Strickler definieren (u.a. kalibriert mit Q-Messung)
J = float(0.01086445)   # [m/m]     # Fliesssgefaelle definieren (aufgenommen mit DGPS oder aus Drohnen-DEM)
# Wendenwasser: J = 0.0687312 // kst = 20
# Hasliaare: J = 0.01086445 // kst = 25

########################################################################
# ---------------------------- Loopstart ----------------------------- #
########################################################################
# In diesem for Loop wird der Abfluss (Q) fuer jede Hoehe(H) bis zu h eingetragen
H = [x / 100.0 for x in range(10, h+1)]   # Zu berechnede Hoehen
A_list = []   # Diese Liste enthaelt die Flaechen fuer jede Hoehe H
P_list = []   # Diese Liste enthaelt die benetzten Umfaenge fuer jede Hoehe H
Rhy_list = []   # Diese Liste enthaelt die hydraulischen Radien fuer jede Hoehe H
Q_H = []   # Diese Liste enthaelt die Abfluesse fuer jede Hoehe H

for ele in H:
    h = ele
    kst = kst
    J = J

    ########################################################################
    # --------------------------- Profil laden --------------------------- #
    ########################################################################
    profil_ganz = pd.read_csv(str(fn), sep=',', squeeze=True)  # mit pandas wird das ganze Profil (fn) geladen x und h
    profil_hoehe_ganz = pd.read_csv(str(fn), sep=',', usecols=['h'],
                                    squeeze=True)  # Hoehe aus ganzem Profil extrahieren
    profil_hoehe = profil_hoehe_ganz - min(profil_hoehe_ganz)  # Hoehen vom kleinsten Hoehenwert subtrahieren, nullsetzen

    profil_dist = pd.read_csv(str(fn), sep=',', usecols=['x'], squeeze=True)  # Distanz (x) aus Profil laden

    profile = pd.concat([profil_dist, profil_hoehe], axis=1)  # Distanz und bearbeitete Hoehe zusammenfuegen

    x_h_tuple = np.array(zip(profil_dist, profil_hoehe))  # Distanz und Hoehe in tuples setzen
    x_h_tuple[0].item(
        1)  # Element im Element ansteuern -> x_h_tuple[0] ist das erste tublet und item(1) die rechte Zahl

    ########################################################################
    # --------------------------- Schnittpunkte -------------------------- #
    ########################################################################
    # Die Schnittpunktberechnung erfolgt mit linearer Interpolation. Formel: xa = x1 + (ya - y1) * ((x1 - x2) / (y1 - y2))
    # Die x- und y-Koordinaten sind hier jeweils in Tuples aufgelistet ("x_h_tuple")
    # Im folgenden while-loop sind 21 Bedingungen beschrieben, welche bei der Schnittpunktberechnung eintreffen koennen.
    profile_list = []  # Leere Liste um die neuen Schnittpunkte und die bestehenden Pkt. hinzuzufuegen
    i = 0
    while i <= ((len(x_h_tuple)) - 1):  # Wenn der index (i) kleiner oder gleich der Tuple-Listenlaenge ist mach:
        if i == 0:  # Wenn der Index == 0, also die erste Zahl in Liste, fueg ihn
            profile_list.append(x_h_tuple[i])  # zur neuen Liste hinzu
        # Bei Sonderfall: Wenn i im Wasser, i-1 auch im Wasser aber i+1 GLEICH = h
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) == h:
            profile_list.append(x_h_tuple[i])  # Dann ist kein Schnittpunkt erforderlich, da der Punkt = h
            profile_list.append(x_h_tuple[i + 1])
        # Pkt. (i) im Wasser, i-1 == h, i+1 im Wasser:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) == h and (x_h_tuple[i + 1].item(1)) < h:
            profile_list.append(x_h_tuple[i])  # Ebenfalls kein Schnittpunkt noetig
        # Pkt. (i) < h, i-1 == h, i+1 == h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) == h and (x_h_tuple[i + 1].item(1)) == h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) == h und i-1 == h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) == h and (x_h_tuple[i - 1].item(1)) == h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) == h und i-1 < h und i+1 > h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) == h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) > h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) == h und i-1 > h und i+1 > h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) == h and (x_h_tuple[i - 1].item(1)) > h and (x_h_tuple[i + 1].item(1)) > h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) == h und i-1 < h und i+1 < h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) == h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) < h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) == h und i-1 > h und i+1 < h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) == h and (x_h_tuple[i - 1].item(1)) > h and (x_h_tuple[i + 1].item(1)) < h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) > h und i-1 == h und i+1 < h:
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i - 1].item(1)) == h and (x_h_tuple[i + 1].item(1)) < h:
            x00 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * (((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1)))))
            profile_list.append(x_h_tuple[i])
            profile_list.append(np.array([x00, h]))
        # Pkt. (i) < h, i-1 == h und i+1 > h
        elif i > 0 and ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) == h and (x_h_tuple[i + 1].item(1)) > h:
            x0 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * (((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1)))))
            profile_list.append(x_h_tuple[i])
            profile_list.append(np.array([x0, h]))
        # Pkt. (i) im Wasser, i-1 auch im Wasser und i + 1 auch im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) < h:
            profile_list.append(x_h_tuple[i])  # Ebenfalls kein Schnittpunkt noetig
        # Pkt. (i) im Wasser, i-1 NICHT im Wasser, i+1 NICHT im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) > h and (x_h_tuple[i + 1].item(1)) > h:
            x1 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * ((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1))))
            profile_list.append(x_h_tuple[i])
            profile_list.append(np.array([x1, h]))
        # Pkt. (i) im Wasser, i-1 NICHT im Wasser, i+1 im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) > h:
            profile_list.append(x_h_tuple[i])  # Hier muss kein Schnittpunkt berechnet werden, da dies beim Punkt i-1 erfolgte. Deshalb einfach hinzufuegen
        # Pkt. (i) im Wasser, i-1 auch im Wasser und nun i+1 NICHT im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) < h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) > h:
            x2 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * ((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1))))
            profile_list.append(x_h_tuple[i])  # Pkt. zur liste hinzufuegen
            profile_list.append(np.array([x2, h]))  # Schnittpunkt x1 mit der Wasserhoehe h (das ist die y-Koordinate) hinzufuegen
        # Pkt. (i) NICHT im Wasser, i-1 im Wasser, i+1 im Wasser (Einpunktefall):
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i + 1].item(1)) < h and (x_h_tuple[i - 1].item(1)) < h:
            x3 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * ((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1))))
            profile_list.append(x_h_tuple[i])
            profile_list.append(np.array([x3, h]))
        # Pkt. (i) NICHT im Wasser, i-1 NICHT im Wasser, i+1 im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i + 1].item(1)) < h and (x_h_tuple[i - 1].item(1)) > h:
            x4 = (x_h_tuple[i].item(0)) + ((h - (x_h_tuple[i].item(1))) * ((x_h_tuple[i].item(0)) - (x_h_tuple[i + 1].item(0))) / ((x_h_tuple[i].item(1)) - (x_h_tuple[i + 1].item(1))))
            profile_list.append(x_h_tuple[i])
            profile_list.append(np.array([x4, h]))
        # Pkt. (i) NICHT im Wasser, i-1 im Wasser, i+1 NICHT im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i - 1].item(1)) < h and (x_h_tuple[i + 1].item(1)) > h:
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) NICHT im Wasser und i-1 auch NICHT im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i - 1].item(1)) > h:  # hier ist der aktuelle Punkt ausserhalb von h und der zuvor ist ausserhalb h -> Hier koennte ich diese Punte in die remove list schmeissen
            profile_list.append(x_h_tuple[i])
        # Pkt. (i) NICHT im Wasser und i+1 auch NICHT im Wasser:
        elif i > 0 and i < ((len(x_h_tuple)) - 1) and (x_h_tuple[i].item(1)) > h and (x_h_tuple[i + 1].item(1)) > h:  # hier ist der aktuelle Punkt ausserhalb von h und der naechste ist ausserhalb h -> Hier koennte ich diese Punte in die remove list schmeissen
            profile_list.append(x_h_tuple[i])
        # Letzer Punkt in der Liste:
        elif i == ((len(x_h_tuple)) - 1):
            profile_list.append(x_h_tuple[i])  # Das ist dann die letzte Position in der Liste
        i = i + 1

    profile_liste = np.array(profile_list)
    profile_listen = profile_liste.tolist()

    ########################################################################
    # ------------------ Vorbedingungen zur Berechnung ------------------- #
    ########################################################################
    x_koord = (profile_liste[:, 0]).tolist()  # Die neuen x-Koordinaten mit den Schnittpunktenwerten in Liste
    x_koord_len = len(x_koord)  # Wird fuer die Berechnung von P benoetigt
    y_koord = (profile_liste[:, 1]).tolist()  # Die neuen y-Koordinaten mit den Schnittpunktenwerte in Liste

    y_koord_v = []  # neue verduennte (v) Liste, bei welcher alle y-Koordinaten an die Wasserhoehe h angepasst

    for element in y_koord:  # alle y-Koord. > h werden auf h gesetzt
        if element >= h:
            y_koord_v.append(h)
        elif element < h:
            y_koord_v.append(element)

    x_y = zip(x_koord, y_koord_v)  # heruntergesetztes Profil auf h --> Koennte man plotten zur veranschaulichung
    x_y_np = np.array(x_y)

    ########################################################################
    # --------------------------- Flaeche (A) ---------------------------- #
    ########################################################################
    # Wasserhoehen fuer jeden gemessenen Profilpunkt (zur Integration), da nicht y-Koordinaten, sonst A unter Profil
    wh = (h - (np.array(y_koord_v))).tolist()

    # Berechnung der durchflossenen Flaeche (A):
    # Formel: A = 0.5 * (x2 - x1) * (wassertiefe1 + wassertiefe2)
    laenge = (len(y_koord_v)) - 2  # Die Looplaenge aller y-Koordinaten
    flaeche = []  # Leere liste, wo die berechneten Flaechen geschrieben werden

    i = 0
    while i <= laenge:
        A = 0.5 * (x_koord[i + 1] - x_koord[i]) * (wh[i] + wh[i + 1])
        flaeche.append(A)
        i = i + 1
    A = sum(flaeche)
    A_round = round(A, 3)  # Gerundet auf 3 Nachkommastellen zur besseren Darstellung
    A_list.append(A)

    ########################################################################
    # ---------------------- Benetzter Umfang (P) ------------------------ #
    ########################################################################
    richtungsvekt = []
    laenge2 = (len(x_koord)) - 2

    # Richtungsvektoren berechnen -> AB = (x2/y2) - (x1/y1) = CD, hier bedeutet / ueber
    j = 0
    while j <= laenge2:
        vektorsub = x_y_np[j + 1] - x_y_np[j]  # Subtraktion (sub) des Vektors j+1 minus j = Richtungsvektor
        richtungsvekt.append(vektorsub)
        richtungsvekt_np = np.array(richtungsvekt)
        j = j + 1

    # Laenge der Richtungsvektoren: Betrag von CD (|CD|) -> Quadratwurzel von C^2 + D^2
    richtungsvekt_np_laenge = np.sqrt(((richtungsvekt_np[:, 0]) ** 2) + ((richtungsvekt_np[:, 1]) ** 2))
    richtungsvekt_np_laenge2 = np.ndarray.tolist(richtungsvekt_np_laenge)  # in ndarray wandeln um im naechsten Schritt 0 hinzuzufuegen
    richtungsvekt_np_laenge2.insert(0, 0.0)  # 0 ist die Listenposition und 0.0 die einzufuegende Zahl
    sum(richtungsvekt_np_laenge2)
    y_koord_v2 = [round(elem, 2) for elem in y_koord_v]  # Verduenntes Profil auf 2 Nachkommastellen runden, zur Weiterberechnung

    # Nun duerfen nur die Laengen beruechsichtigt werden, welche effektiv benetzt sind:
    wetlist = []
    removelist = []

    index2 = 0
    while index2 <= (x_koord_len - 1):
        for hoe in y_koord_v2:
            nume = hoe
            if index2 == 0:  # erste Position in Liste
                if nume == h:  # wenn der Fall eintrit, dass quasi h = h bzw. der erste Pkt = h
                    removelist.append(richtungsvekt_np_laenge2[index2])  # weg in die removelist
                else:
                    wetlist.append(richtungsvekt_np_laenge2[index2])  # wenn der erste Pkt jedoch kleiner ist, nehmen
            elif 0 < index2 <= (x_koord_len - 1):  # wenn index groesser 0 aber kleiner als die Listenlaenge:
                if nume == h and y_koord_v2[(index2 - 1)] < h:  # wenn h = h und wenn der vorangegangene Pkt kleiner ist als h:
                    wetlist.append(richtungsvekt_np_laenge2[index2])  # fuege ihn zur Nassliste
                elif nume < h and y_koord_v2[(index2 - 1)] == h:  # wenn h < h und wenn der vorangegangene Pkt gleich h ist (links im Wasser, rechts auf Wasserhoehe (h):
                    wetlist.append(richtungsvekt_np_laenge2[index2])  # fuege ihn zur Nassliste
                elif nume < h and y_koord_v2[(index2 - 1)] < h:  # wenn die benachbarten Punkte beide im Wasser sind:
                    wetlist.append(richtungsvekt_np_laenge2[index2])
                else:
                    removelist.append(richtungsvekt_np_laenge2[index2])
            else:
                removelist.append(richtungsvekt_np_laenge2[index2])
            index2 = index2 + 1

    P = sum(wetlist)
    P_round = round(P, 3)
    sum(removelist)
    P_list.append(P)

    ########################################################################
    # ------------------- hydraulischer Radius(Rhy) ---------------------- #
    ########################################################################
    Rhy = A / P
    Rhy_round = round(Rhy, 3)
    Rhy_list.append(Rhy)

    #########################################################################
    # ------------------------------ Abfluss (Q) -------------------------- #
    #########################################################################
    # Q = vm * A --> vm = kst * Rhy^(2/3) * J^(1/2)
    Q = kst * Rhy ** (2.0 / 3.0) * J ** (1.0 / 2.0) * A
    Q_round = round(Q, 3)
    Q_H.append(Q)
    print("processing...")


#########################################################################
# --------------------------- PrettyTable ----------------------------- #
#########################################################################
# Darstellung der errechneten Werte in einer Tabelle
t = PrettyTable(['Pegel [m]', 'A [m^2]', 'P [m]', 'Rhy [m]', 'Q [m^3/s]'])
for x in range(0, len(H)):   # Achtung die range bezieht sich auf H (H = h - 9)
    t.add_row([H[x], round(A_list[x], 3), round(P_list[x], 3), round(Rhy_list[x], 3), round(Q_H[x], 3)])
print(t)


#########################################################################
# ------------------------ Plot beider Profile ------------------------ #
#########################################################################
plt.figure(1)   # Damit das Profil und PQ-Beziehung separat geplottet werden
plt.plot(profil_dist, profil_hoehe, label='DGPS Profil', color='black', marker='.')
plt.plot(x_koord, y_koord_v, label='verduenntes Profil', color='red', marker='o')
plt.axhline(y=h, color='b', linestyle='-', label='Wasserhoehe (h)')
# plt.axis('equal')
plt.title('Original und verduenntes QP, bei Pegel ' + str(h) + ' m')
plt.legend(loc='best')
plt.xlabel('Distanz [m]')
plt.ylabel('Hoehe [m]')
plt.grid(True)


#########################################################################
# ------------------------ Plot P/Q-Beziehung ------------------------- #
#########################################################################
# kst kalibriert auf die Abflussmessung vom 14.05.19 P=65.8cm, Q=5052 l/s
x = H
y = Q_H

Hoehe_Abfluss = zip(H, Q_H)
plt.figure(2)
plt.plot(x, y, marker='o', color='b', label='modelliert')
plt.legend()
plt.title("P/Q-Beziehung - " + str(pn) + ' \n kst = ' + str(kst))
plt.xlabel ("Pegel (P) [m]")
plt.ylabel("Abfluss (Q)" + " [$m^3$/s]")
plt.grid(True)
plt.show()
