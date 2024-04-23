import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import sympy as sp





def cykloida(t, r, c):
    x = r * t - c * np.sin(t)
    y = r - c * np.cos(t)
    return x, y

def epicykloida(t, r, R, c):
    x = (R + r) * np.cos(t) - c * np.cos(((R + r) / r) * t)
    y = (R + r) * np.sin(t) - c * np.sin(((R + r) / r) * t)
    return x, y

def hipocykloida(t, r, R, c):
    x = (R - r) * np.cos(t) + c * np.cos(((R - r) / r) * t)
    y = (R - r) * np.sin(t) - c * np.sin(((R - r) / r) * t)
    return x, y

def funkcja_wartosc(wartosc_x, funkcja):
    x = sp.symbols('x')
    return funkcja.subs(x, wartosc_x)

def funkcja_wartosci(t, funkcja):
    y = sp.lambdify(sp.symbols('x'), funkcja, modules='numpy')
    return y(t)

def styczna(wartosc_x): #y=f′(x0)(x−x0)+f(x0)
    x = sp.symbols('x')
    y = funkcja
    pochodna = sp.diff(y, x)
    pochodna_wartosc = pochodna.subs(x, wartosc_x)
    wartosc_y = y.subs(x, wartosc_x)
    return pochodna_wartosc, wartosc_y

def prostopadla_do_stycznej(pochodna_wartosc, wartosc_x, wartosc_y):
    ap = -1/pochodna_wartosc
    bp = - ap * wartosc_x + wartosc_y
    return ap, bp

def wsp_srodek_okregu(wartosc_x, wartosc_y, ap, bp):
    x, y = sp.symbols('x y')
    r1 = sp.Eq(ap * x + bp, y)
    r2 = sp.Eq(sp.sqrt((x-wartosc_x)**2+(y-wartosc_y)**2), r)
    rozwiazania = sp.solve((r1, r2), (x, y))
    return rozwiazania

def odleglosc_miedzy_pkt(wartosc_x, wartosc_y, wartosc_x2, wartosc_y2):
    #print("pierw z: ", (wartosc_x2-wartosc_x)**2+(wartosc_y2-wartosc_y)**2 )
    return np.sqrt(float((wartosc_x2-wartosc_x)**2+(wartosc_y2-wartosc_y)**2))



wybor = input("Wybierz (c, e, h, k): ")
if wybor == "c":
    r = float(input("r: "))
    c = float(input("c: "))
elif wybor == "e":
    R = float(input("R: "))
    r = float(input("r: "))
    c = float(input("c: "))
elif wybor == "h":
    R = float(input("R: "))
    r = float(input("r: "))
    c = float(input("c: "))
elif wybor == "k":
    wyrazenie_uzytkownika = input("Podaj funkcje: ")
    funkcja = sp.sympify(wyrazenie_uzytkownika)
    poczatek_zakresu = float(input("Podaj poczatek zakresu: "))
    koniec_zakresu = float(input("Podaj koniec zakresu: "))
    r = float(input("r: "))
    c = float(input("c: "))



fig, ax = plt.subplots()
ax.set_aspect('equal')


linia, = ax.plot([], [])
wykres, = ax.plot([], [])
male_kolo = plt.Circle((0, 0),r,fill=0)

if wybor == "e" or wybor == "h":
    t = np.linspace(0, 10 * np.pi, 1000)
    kolo = plt.Circle((0,0),R,fill=0)
    ax.set_xlim([-(R+r+c+10), R+r+c])
    ax.set_ylim([-(R+r+c+10), R+r+c])
    ax.add_patch(kolo)
elif wybor == "c":
    t = np.linspace(0, 10 * np.pi, 1000)
    liniapozioma = ax.axhline(y=0)
    ax.set_xlim([-(r + c+10), r*15])
    ax.set_ylim([-(r + c+10), r + c+10])
elif wybor == "k":
    t = np.linspace(poczatek_zakresu, koniec_zakresu, int(koniec_zakresu-poczatek_zakresu)*30)
    y=funkcja_wartosci(t, funkcja)
    ax.set_xlim([poczatek_zakresu-r-10, koniec_zakresu+r+10])
    ax.set_ylim([-10, 50])
    plt.plot(t,y)
        
ax.add_patch(male_kolo)

x4, y4, d = [], [], [0]

def update(frame):
    if wybor == "c":
        x1, y1 = cykloida(t[:frame], r, c)
        male_kolo.set_center([r * t[frame], r])
        linia.set_data([r*(t[frame]-np.sin(t[frame])), r * t[frame]], [r*(1-np.cos(t[frame])), r])
        wykres.set_data(x1, y1)
        


    elif wybor == "e":
        x2, y2 = epicykloida(t[:frame], r, R, c)
        male_kolo.set_center([(R + r) * np.cos(t[frame]), (R + r) * np.sin(t[frame])])
        linia.set_data([(R + r) * np.cos(t[frame]), (R + r) * np.cos(t[frame]) - c * np.cos(((R + r) / r) * t[frame])],
                       [(R + r) * np.sin(t[frame]), (R + r) * np.sin(t[frame]) - c * np.sin(((R + r) / r) * t[frame])])
        wykres.set_data(x2, y2)


    elif wybor == "h":
        male_kolo.set_center([(R - r) * np.cos(t[frame]), (R - r) * np.sin(t[frame])])
        linia.set_data([(R - r) * np.cos(t[frame]), (R - r) * np.cos(t[frame]) + c * np.cos(((R - r) / r) * t[frame])],
                       [(R - r) * np.sin(t[frame]), (R - r) * np.sin(t[frame]) - c * np.sin(((R - r) / r) * t[frame])])
        x3, y3 = hipocykloida(t[:frame], r, R, c)
        wykres.set_data(x3, y3)

    elif wybor == "k":
        
        #print("x4: ", x4)
        #print("y4: ", y4)
        #print("d: ", d)
        wartosc_x = t[frame]
        #print("wartosc x: ", wartosc_x)
        pochodna_wartosc, wartosc_y = styczna(wartosc_x)
        #print("wartosc y: ", wartosc_y)
        #print("pochodna wartosc: ", pochodna_wartosc)
        ap, bp = prostopadla_do_stycznej(pochodna_wartosc, wartosc_x, wartosc_y)
        #print("ap: ", ap)
        #print("bp: ", bp)
        rozwiazania = wsp_srodek_okregu(wartosc_x, wartosc_y, ap, bp)
        pierwsze_rozwiazanie = rozwiazania[0]
        if ap > 0:
            pierwsze_rozwiazanie = rozwiazania[1]
        kolo_x = pierwsze_rozwiazanie[0]
        kolo_y = pierwsze_rozwiazanie[1]
        #print("kolo_x: ", kolo_x)
        #print("kolo_y: ", kolo_y)
        male_kolo.set_center([kolo_x, kolo_y])
        if frame > 1:
            
            d.append(d[-1] + odleglosc_miedzy_pkt(wartosc_x, wartosc_y, t[frame-1], funkcja_wartosc(t[frame-1], funkcja)))
            #print("d: ", d[-1])
            x4.append(kolo_x + c * np.sin(d[-1]/r))
            y4.append(kolo_y + c * np.cos(d[-1]/r))
            #print("x4: ", x4[-1])
            #print("y4: ", y4[-1])

            linia.set_data([kolo_x + c * np.sin(d[-1]/r),kolo_x], [kolo_y + c * np.cos(d[-1]/r),kolo_y])



        wykres.set_data(x4, y4)



    return wykres, linia, male_kolo

ani = FuncAnimation(fig, update, frames=len(t), interval=5, blit=True)
#ani.save('cycloid.gif', writer='pillow')
plt.show()
