#   ---------R Script in Python transformation by kwy Mai 2019---------   #
# Import
import pandas as pd
import numpy as np
# from area import area
# import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression


###########################################################
# ---------------- Profil laden und show ---------------- #
###########################################################
# Die Hoehe (h) auf null setzen = null_hoehe
profile_hoehe_null = pd.read_csv('qp_hasliaare.txt', sep=',', usecols=['h'], squeeze=True)
null_hoehe = profile_hoehe_null - min(profile_hoehe_null)

# Spalte der Distanz extrahieren
profile_distance = pd.read_csv('qp_hasliaare.txt', sep=',', usecols=['x'], squeeze=True)

# Beiden neuen Profile zusammenschweissen
profile = pd.concat([profile_distance, null_hoehe], axis=1)

# NEW aus profile ein array machen
a = np.array(profile)


# *************** Hoehen bei Wasserstand 66cm ***************** #
hoehen = null_hoehe[7:97]
distance = profile_distance[8:97]   # dazugehoerigen Distanzen zu den hoehen, also x und y Koordinaten
hoehdist66 = pd.concat([hoehen, distance], axis=1)


# Profiltitel beschriften
Profil = profile.plot(title='Querprofil Hasliaare', color='black', x='x', y='h', label='Profil', kind='line')
Profil.set_xlabel("Distanz [m]")
Profil.set_ylabel("Hoehe [m]")


###########################################################
# --------------------- Hydraulik ----------------------- #
###########################################################

# ----------- Parameter ----------- #
kst = int(24)   # Stricklerbeiwert von einem Wildbach
J = float(0.01083)   # Fliessgefaelle aus QGIS berechnet
H = np.arange(0.01, 0.67, 0.01)   # Zu untersuchende Hoehe von 0.01 bis 0.66m in Schritten von 0.01
h = 0.66   # zu berechnende Hoehe

# -------- empty vector --------- #
Ah = []
Rh = []


###########################################################
# --------------------- Funktionen ---------------------- #
###########################################################
# -------- Funktion: Flaeche (A) berechnen mit Hilfsfunktion in Abhaengigkeit von h --------- #
# def function (h):
   # return 0.5*np.abs(np.dot(null_hoehe, np.roll(h, 1))-np.dot(h, np.roll(null_hoehe, 1)))
# print sum(PolyArea(hoehen, h))

# Ap = {'type': 'Polygon', 'coordinates': [[[0.56, 6.58], [0.04, 6.82], [0.22, 9.32], [0.5, 18.48], [0.42, 19.27]]]}
# area(Ap)

# -------- Benetzter Umfang berechnen mit der Hilfsfunktion --------- #
# ???


###########################################################
# ---------------- loop durch Vektor -------------------- #
###########################################################
for i in range(1, len(H)):
    h = H[i]

    profile = pd.concat([profile_distance, null_hoehe], axis=1)

    ######### HIER WEITER mit automatisieren!
    # *****Dies muss unbedingt automatisiert werden, dass python selber weis wo das min ist!
    profile_re = profile[0:12]   # Rechtes Profil bis zu h = 0 / min
    profile_li = profile[11:]

    profile_re_u = profile_re[8:12]   # re_u < h(0.66)
    profile_re_o = profile_re[0:8]   # re_o > h(0.66)

    # Punkte zwischen Hoehe h bestimmen, x- und y-Koordinaten
    x1_re = max(Profile_re_u['h'])
    x2_re = max(Profile_re_o['h'])

    y1_re = min(Profile_re_u['x'])
    y2_re = min(Profile_re_o['x'])

    # lineare Interpolation der x_Koord auf der Hoehe h
    x1 = LinearRegression().fit(x1_re, y1_re)  #### Das hier in python schreiben











# ----------- Freibord ----------- #
wasserstand_maximal = Profil.axhline(y=3.83, color='r', label='Maximaler Wasserstand')
wasserstand_hqhundert = plt.hlines(2.95, xmin=0.53, xmax=16.48, colors='b', label='Wasserstand HQ100')
freibord = plt.vlines(10.5, ymin=2.95, ymax=3.83, colors='olive', label='Freibord 90cm', linestyles='--')


# ----------- Zusatzpunkte ----------- #
hilfspkt1 = Profil.plot(0.53, 2.95, "go")   # g = grün und o = Form des Punktes
hilfspkt2 = Profil.plot(16.48, 2.95, "go")


# Plot anzeigen mit Legende
# In der legende wird alles angezeigt, was ein label beinhaltet!
plt.legend(bbox_to_anchor=(0.15, 0.3), loc="upper center")
plt.show()