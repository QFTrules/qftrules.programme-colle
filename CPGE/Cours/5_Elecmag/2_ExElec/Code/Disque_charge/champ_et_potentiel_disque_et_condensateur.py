# -*- coding: utf-8 -*-
"""
Created on 15/01/2023

@author: Jean-Marie Biansan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import bisect
from matplotlib.colors import Normalize
# attention: nécessite version scipy>=1.8.0
from scipy.special import elliprf, elliprj,ellipe,ellipk

#notations: sigma densité de charge
#rayon disques armature: a
#V0=(sigma a)/(2 epsilon0)
#E0=sigma/(2 epsilon0)
#rapport épaisseur sur rayon noté e_a


######################################################################################
#fonction de Heaviside
def ep(x):
    #renvoie 1 si x>0, 0 si x=0, -1 si x<0
    return((np.heaviside(x,0.5)-0.5)*2)
######################################################################################

######################################################################################
#intégrale elliptique complète de 3éme espèce
def ellippi(n, m):
    if m >= 1:
        raise ValueError('m doit être < 1')
    y = 1 - m
    rf = elliprf(0, y, 1)
    rj = elliprj(0, y, 1, 1 - n)
    return(rf + rj * n / 3)
######################################################################################


######################################################################################
#expression rigoureuse du potentiel du disque, utilisant les intégrales elliptiques
#Référence: E. Duran, "Electrostatique, Tome 1, Les distributions"
def potentiel_sur_V0_disque(r_a,z_a):
    #expression en fonction de r/a et z/a
    #normalement r>=0; mais au cas où la fonction serait appelée avec r<0, on remplace r par sa valeur absolue
    r_a_abs=abs(r_a)
    k2=4*r_a_abs/(np.power(1+r_a_abs,2)+np.power(z_a,2))
    m2=4*r_a_abs/np.power(1+r_a_abs,2)
    return(1/np.pi*(-ep(z_a)*(1-ep(r_a_abs-1))*np.pi/2*z_a+np.sqrt(np.power(1+r_a_abs,2)+np.power(z_a,2))*ellipe(k2)+(1-np.power(r_a_abs,2))/np.sqrt(np.power(1+r_a_abs,2)+np.power(z_a,2))*ellipk(k2)+np.power(z_a,2)/np.sqrt(np.power(1+r_a_abs,2)+np.power(z_a,2))*(1-r_a_abs)/(1+r_a_abs)*ellippi(m2,k2)))
######################################################################################
#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
potentiel_sur_V0_disque_vectorialisee=np.vectorize(potentiel_sur_V0_disque)
######################################################################################


######################################################################################
#expression rigoureuse du potentiel du condensateur, utilisant celui du disque
def potentiel_sur_V0_condensateur(r_a,z_a,e_a):
    return(-potentiel_sur_V0_disque(r_a,z_a-e_a/2)+potentiel_sur_V0_disque(r_a,z_a+e_a/2))
######################################################################################
#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
potentiel_sur_V0_condensateur_vectorialisee=np.vectorize(potentiel_sur_V0_condensateur)
######################################################################################





######################################################################################
#expression rigoureuse de la composante radiale du champ du disque, utilisant les intégrales elliptique
def e_r_sur_E0_disque(r_a,z_a):
    #expression en fonction de r/a et z/a
    #normalement r>=0; mais au cas où la fonction serait appelée avec r<0, on remplace r par sa valeur absolue
    r_a_abs=abs(r_a)
    #singularité en r=a et z=0
    if r_a_abs==1 and z_a==0:
        return(np.nan)
    #champ sur l'axe
    if r_a==0:
        return(0.0)

    k2=4*r_a_abs/(np.power(1+r_a_abs,2)+np.power(z_a,2))
    m2=4*r_a_abs/np.power(1+r_a_abs,2)
    res=(1/np.pi*np.sqrt((1+r_a_abs)**2+z_a**2)/r_a_abs*((1-k2/2)*ellipk(k2)-ellipe(k2)))
    #si r<0, changement de signe de la composante radiale
    if r_a>0:
        return(res)
    else:
        return(-res)
######################################################################################

#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
e_r_sur_E0_disque_vectorialisee=np.vectorize(e_r_sur_E0_disque)
######################################################################################




######################################################################################
#expression rigoureuse de la composante radiale du champ du condensateur, utilisant celle du disque
def e_r_sur_E0_condensateur(r_a,z_a,e_a):
        return(-e_r_sur_E0_disque(r_a,z_a-e_a/2)+e_r_sur_E0_disque(r_a,z_a+e_a/2))
######################################################################################

#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
e_r_sur_E0_condensateur_vectorialisee=np.vectorize(e_r_sur_E0_condensateur)
######################################################################################






######################################################################################
#expression rigoureuse de la composante axiale du champ du disque, utilisant les intégrales elliptique
def e_z_sur_E0_disque(r_a,z_a):
    #expression en fonction de r/a et z/a
    #normalement r>=0; mais au cas où la fonction serait appelée avec r<0, on remplace r par sa valeur absolue
    r_a_abs=abs(r_a)
    #champ sur l'axe
    if r_a==0:
        return(ep(z_a)-z_a/np.sqrt(1+z_a**2))
    #singularité sir r=a et z=0
    if r_a_abs==1 and z_a==0:
        return(np.nan)
    k2=4*r_a_abs/(np.power(1+r_a_abs,2)+np.power(z_a,2))
    m2=4*r_a_abs/np.power(1+r_a_abs,2)
    if m2==1:
        return(1/np.pi/2*(ep(z_a)*(1-ep(r_a_abs-1))*np.pi+2*z_a/np.sqrt((1+r_a_abs)**2+z_a**2)*(-ellipk(k2))))
    else:
        return(1/np.pi/2*(ep(z_a)*(1-ep(r_a_abs-1))*np.pi+2*z_a/np.sqrt((1+r_a_abs)**2+z_a**2)*(ep(r_a_abs-1)*np.sqrt(1-m2)*ellippi(m2,k2)-ellipk(k2))))
######################################################################################
#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
e_z_sur_E0_disque_vectorialisee=np.vectorize(e_z_sur_E0_disque)
######################################################################################



######################################################################################
#expression rigoureuse de la composante axiale du champ du condensateur, utilisant celle du disque
def e_z_sur_E0_condensateur(r_a,z_a,e_a):
    return(-e_z_sur_E0_disque(r_a,z_a-e_a/2)+e_z_sur_E0_disque(r_a,z_a+e_a/2))
######################################################################################
#vectorialisation de la fonction précédente,  pour pouvoir l'appliquer à des tableaux numpy
e_z_sur_E0_condensateur_vectorialisee=np.vectorize(e_z_sur_E0_condensateur)
######################################################################################






######################################################################################
#renvoie les 2 composantes du champ du disque
def Champ_Disque(r_a,z_a):
    res1,res2=e_r_sur_E0_disque(r_a,z_a),e_z_sur_E0_disque(r_a,z_a)
    if not(np.isnan(res1)) and not(np.isnan(res2)):
        return([res1,res2])
######################################################################################

######################################################################################
#renvoie les 2 composantes du champ du disque
def Champ_condensateur(r_a,z_a,e_a):
    res1,res2=e_r_sur_E0_condensateur(r_a,z_a,e_a),e_z_sur_E0_condensateur(r_a,z_a,e_a)
    if not(np.isnan(res1)) and not(np.isnan(res2)):
        return([res1,res2])
######################################################################################

######################################################################################
#renvoie les 2 composantes du champ perpendiculaire au champ électrique du disque, dont les lignes sont des équipotentielles
def Champ_Disque_Equipotentielle(r_a,z_a):
    res1,res2=-e_z_sur_E0_disque(r_a,z_a),e_r_sur_E0_disque(r_a,z_a)
    if not(np.isnan(res1)) and not(np.isnan(res2)):
        return([res1,res2])
######################################################################################

######################################################################################
#renvoie les 2 composantes du champ perpendiculaire au champ électrique du disque, dont les lignes sont des équipotentielles
def Champ_condensateur_Equipotentielle(r_a,z_a,e_a):
    res1,res2=-e_z_sur_E0_condensateur(r_a,z_a,e_a),e_r_sur_E0_condensateur(r_a,z_a,e_a)
    if not(np.isnan(res1)) and not(np.isnan(res2)):
        return([res1,res2])
######################################################################################


######################################################################################
#renvoie les 2 composantes du champ perpendiculaire au champ électrique du disque, dont les lignes sont des équipotentielles
def Champ_condensateur_Equipotentielle(r_a,z_a,e_a):
    res1,res2=-e_z_sur_E0_condensateur(r_a,z_a,e_a),e_r_sur_E0_condensateur(r_a,z_a,e_a)
    if not(np.isnan(res1)) and not(np.isnan(res2)):
        return([res1,res2])
######################################################################################



######################################################################################
#détermination de la ligne de champ partant d'un point donné, dans la fenêtre [xmin,xmax], [zmin,zmax], avec un pas "pas"
#la fonction "champ" doit renvoyer les 2 composantes du champ
def Calcule_Ligne_Champ_Runge_Kutta(x0,z0,xmin,xmax,zmin,zmax,Champ,Nombre_Max_Points,pas,*args):
    liste_X,liste_Z=[x0],[z0]
    x,z=x0,z0
#méthode: résolution de dr/ds=Er/E et dz/ds=Ez/E par Runge Kutta
    #vers l'avant
    i=0
    distance_au_point_depart=0
    distance_croissante=True
    revient_trop_pres_du_depart=False
    while((x<=xmax) and (x>=xmin) and (z>=zmin) and (z<=zmax)
    and (i<Nombre_Max_Points) and not(revient_trop_pres_du_depart)):
        i=i+1
        Ch=Champ(x,z,*args)
        if Ch==None:
            break
        Ch_X=Ch[0]
        Ch_Z=Ch[1]
        Norme_Champ=np.sqrt(Ch_X**2+Ch_Z**2)
        if Norme_Champ==0:
            break
        a1,a2=Ch_X/Norme_Champ,Ch_Z/Norme_Champ
        Ch=Champ(x+pas/2*a1,z+pas/2*a2,*args)
        if Ch==None:
            break
        b1,b2=Ch[0],Ch[1]
        Norme_Champ=np.sqrt(b1**2+b2**2)
        if Norme_Champ==0:
            break
        b1,b2=b1/Norme_Champ,b2/Norme_Champ
        Ch=Champ(x+pas/2*b1,z+pas/2*b2,*args)
        if Ch==None:
            break
        c1,c2=Ch[0],Ch[1]
        Norme_Champ=np.sqrt(c1**2+c2**2)
        if Norme_Champ==0:
            break
        c1,c2=c1/Norme_Champ,c2/Norme_Champ
        Ch=Champ(x+pas*c1,z+pas*c2,*args)
        if Ch==None:
            break
        d1,d2=Ch[0],Ch[1]
        Norme_Champ=np.sqrt(d1**2+d2**2)
        if Norme_Champ==0:
            break
        d1,d2=d1/Norme_Champ,d2/Norme_Champ
        x=x+pas/6.*(a1+2*b1+2*c1+d1)
        z=z+pas/6.*(a2+2*b2+2*c2+d2)
        liste_X.append(x)
        liste_Z.append(z)
        nouvelle_distance_au_point_depart=np.sqrt((x-x0)**2+(z-z0)**2)
        distance_croissante=(nouvelle_distance_au_point_depart>distance_au_point_depart)
        revient_trop_pres_du_depart= not(distance_croissante) and (nouvelle_distance_au_point_depart<pas*10)
        distance_au_point_depart=nouvelle_distance_au_point_depart

#vers l'arriere

    distance_au_point_depart=0
    distance_croissante=True
    revient_trop_pres_du_depart=False
    x,z=x0,z0
    while((x<=xmax) and (x>=xmin) and (z>=zmin) and (z<=zmax)
    and (i<Nombre_Max_Points)
    and not(revient_trop_pres_du_depart)):
        i=i+1
        Ch=Champ(x,z,*args)
        if Ch==None:
            break
        Ch_X=-Ch[0]
        Ch_Z=-Ch[1]
        Norme_Champ=np.sqrt(Ch_X**2+Ch_Z**2)
        if Norme_Champ==0:
            break
        a1,a2=Ch_X/Norme_Champ,Ch_Z/Norme_Champ
        Ch=Champ(x+pas/2*a1,z+pas/2*a2,*args)
        if Ch==None:
            break
        b1,b2=Ch[0],Ch[1]
    #attention, on travaille avec l'opposé du champ, il faut changer les signes
        #des composantes après chaque appel à "Champ"
        b1,b2=-b1,-b2
        Norme_Champ=np.sqrt(b1**2+b2**2)
        if Norme_Champ==0:
            break
        b1,b2=b1/Norme_Champ,b2/Norme_Champ
        Ch=Champ(x+pas/2*b1,z+pas/2*b2,*args)
        if Ch==None:
            break
        c1,c2=Ch[0],Ch[1]
        c1,c2=-c1,-c2
        Norme_Champ=np.sqrt(c1**2+c2**2)
        if Norme_Champ==0:
            break
        c1,c2=c1/Norme_Champ,c2/Norme_Champ
        Ch=Champ(x+pas*c1,z+pas*c2,*args)
        if Ch==None:
            break
        d1,d2=Ch[0],Ch[1]
        d1,d2=-d1,-d2
        Norme_Champ=np.sqrt(d1**2+d2**2)
        if Norme_Champ==0:
            break
        d1,d2=d1/Norme_Champ,d2/Norme_Champ
        x=x+pas/6.*(a1+2*b1+2*c1+d1)
        z=z+pas/6.*(a2+2*b2+2*c2+d2)
        liste_X=[x]+liste_X
        liste_Z=[z]+liste_Z
        nouvelle_distance_au_point_depart=np.sqrt((x-x0)**2+(z-z0)**2)
        distance_croissante=(nouvelle_distance_au_point_depart>distance_au_point_depart)
        revient_trop_pres_du_depart= not(distance_croissante) and (nouvelle_distance_au_point_depart<pas*10)
        distance_au_point_depart=nouvelle_distance_au_point_depart
    return(np.array(liste_X),np.array(liste_Z))
######################################################################################




######################################################################################
#tracé du potentiel du disque en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_potentiel_disque_en_fonction_de_z(-1,1,500,[0,0.1,0.2,0.5,0.9,1.1])
def trace_potentiel_disque_en_fonction_de_z(z_a_min,z_a_max,nombre_valeurs_z,liste_r_a):
    plt.figure(0)
    liste_z_a=np.linspace(z_a_min,z_a_max,nombre_valeurs_z)
    liste_pot=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_pot=potentiel_sur_V0_disque_vectorialisee(r_a,liste_z_a)
        plt.plot(liste_z_a,liste_pot,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel('z/a')
    plt.ylabel(r'$V/V_0$  avec $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.title('Potentiel électrostatique crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################

######################################################################################
#tracé du potentiel du disque en fonction de r/a pour diverses valeurs de z/a
#exemple d'utilisation: trace_potentiel_disque_en_fonction_de_r(-1,1,500,[0,0.1,0.2,0.5,0.9,1.1])
def trace_potentiel_disque_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_a):
    plt.figure(10)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_pot=np.zeros(nombre_valeurs_r)
    for z_a in liste_z_a:
        liste_pot=potentiel_sur_V0_disque_vectorialisee(liste_r_a,z_a)
        plt.plot(liste_r_a,liste_pot,label='z/a='+str(z_a))

    plt.grid()
    plt.legend()
    plt.xlabel('r/a')
    plt.ylabel(r'$V/V_0$  avec $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.title('Potentiel électrostatique crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################



######################################################################################
#tracé du potentiel du condensateur en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_potentiel_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,1.1],0.5)
def trace_potentiel_condensateur_en_fonction_de_z(z_e_min,z_e_max,nombre_valeurs_z,liste_r_a,e_a):
    plt.figure(5)
    liste_z_e=np.linspace(z_e_min,z_e_max,nombre_valeurs_z)
    liste_z_a=liste_z_e*e_a
    liste_pot=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_pot=potentiel_sur_V0_condensateur_vectorialisee(r_a,liste_z_a,e_a)
        plt.plot(liste_z_e,liste_pot,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel('z/épaisseur')
    plt.ylabel(r'$V/V_0$  avec $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.title('Potentiel électrostatique crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################


######################################################################################
#tracé du potentiel du condensateur en fonction de r/a pour diverses valeurs de z/e
#exemple d'utilisation: trace_potentiel_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,0.9,1.1],0.5)
def trace_potentiel_condensateur_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_e,e_a):
    plt.figure(15)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_pot=np.zeros(nombre_valeurs_r)
    for z_e in liste_z_e:
        liste_pot=potentiel_sur_V0_condensateur_vectorialisee(liste_r_a,z_e*e_a,e_a)
        plt.plot(liste_r_a,liste_pot,label='z/épaisseur='+str(z_e))

    plt.grid()
    plt.legend()
    plt.xlabel('r/a')
    plt.ylabel(r'$V/V_0$  avec $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.title('Potentiel électrostatique crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################



######################################################################################
#tracé de la composante axiale du champ du disque en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_composante_axiale_disque_en_fonction_de_z(-1,1,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
def trace_composante_axiale_disque_en_fonction_de_z(z_a_min,z_a_max,nombre_valeurs_z,liste_r_a):
    plt.figure(1)
    liste_z_a=np.linspace(z_a_min,z_a_max,nombre_valeurs_z)
    liste_ez=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_ez=e_z_sur_E0_disque_vectorialisee(r_a,liste_z_a)
        plt.plot(liste_z_a,liste_ez,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel("z/a")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante axiale du champ crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################

######################################################################################
#tracé de la composante axiale du champ du disque en fonction de r/a pour diverses valeurs de z/a
#exemple d'utilisation: trace_composante_axiale_disque_en_fonction_de_r(-1,1,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
def trace_composante_axiale_disque_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_a):
    plt.figure(11)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_ez=np.zeros(nombre_valeurs_r)
    for z_a in liste_z_a:
        liste_ez=e_z_sur_E0_disque_vectorialisee(liste_r_a,z_a)
        plt.plot(liste_r_a,liste_ez,label='z/a='+str(z_a))

    plt.grid()
    plt.legend()
    plt.xlabel("r/a")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante axiale du champ crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################





######################################################################################
#tracé de la composante axiale du champ du condensateur en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_composante_axiale_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.02)
def trace_composante_axiale_condensateur_en_fonction_de_z(z_e_min,z_e_max,nombre_valeurs_z,liste_r_a,e_a):
    plt.figure(6)
    liste_z_e=np.linspace(z_e_min,z_e_max,nombre_valeurs_z)
    liste_z_a=liste_z_e*e_a
    liste_ez=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_ez=e_z_sur_E0_condensateur_vectorialisee(r_a,liste_z_a,e_a)
        plt.plot(liste_z_e,liste_ez,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel("z/épaisseur")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante axiale du champ crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################


######################################################################################
#tracé de la composante axiale du champ du condensateur en fonction de r/a pour diverses valeurs de z/e
#exemple d'utilisation: trace_composante_axiale_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.02)
def trace_composante_axiale_condensateur_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_e,e_a):
    plt.figure(16)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_ez=np.zeros(nombre_valeurs_r)
    for z_e in liste_z_e:
        liste_ez=e_z_sur_E0_condensateur_vectorialisee(liste_r_a,z_e*e_a,e_a)
        plt.plot(liste_r_a,liste_ez,label='z/épaisseur='+str(z_e))

    plt.grid()
    plt.legend()
    plt.xlabel("r/a")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante axiale du champ crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################





######################################################################################
#tracé de la composante radiale du champ du disque en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_composante_radiale_disque_en_fonction_de_z(-1,1,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
def trace_composante_radiale_disque_en_fonction_de_z(z_a_min,z_a_max,nombre_valeurs_z,liste_r_a):
    plt.figure(2)
    liste_z_a=np.linspace(z_a_min,z_a_max,nombre_valeurs_z)
    liste_er=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_er=e_r_sur_E0_disque_vectorialisee(r_a,liste_z_a)
        plt.plot(liste_z_a,liste_er,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel("z/a")
    plt.ylabel(r'$E_r /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante radiale du champ crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################


######################################################################################
#tracé de la composante radiale du champ du disque en fonction de r/a pour diverses valeurs de z/a
#exemple d'utilisation: trace_composante_radiale_disque_en_fonction_de_r(-1,1,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
def trace_composante_radiale_disque_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_a):
    plt.figure(12)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_er=np.zeros(nombre_valeurs_r)
    for z_a in liste_z_a:
        liste_er=e_r_sur_E0_disque_vectorialisee(liste_r_a,z_a)
        plt.plot(liste_r_a,liste_er,label='z/a='+str(z_a))

    plt.grid()
    plt.legend()
    plt.xlabel("r/a")
    plt.ylabel(r'$E_r /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante radiale du champ crée par un disque de rayon a uniformément chargé')
    plt.show()
######################################################################################




######################################################################################
#tracé de la composante radiale du champ du condensateur en fonction de z/a pour diverses valeurs de r/a
#exemple d'utilisation: trace_composante_axiale_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.5)
def trace_composante_radiale_condensateur_en_fonction_de_z(z_e_min,z_e_max,nombre_valeurs_z,liste_r_a,e_a):
    plt.figure(7)
    liste_z_e=np.linspace(z_e_min,z_e_max,nombre_valeurs_z)
    liste_z_a=liste_z_e*e_a
    liste_ez=np.zeros(nombre_valeurs_z)
    for r_a in liste_r_a:
        liste_ez=e_r_sur_E0_condensateur_vectorialisee(r_a,liste_z_a,e_a)
        plt.plot(liste_z_e,liste_ez,label='r/a='+str(r_a))

    plt.grid()
    plt.legend()
    plt.xlabel("z/épaisseur")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante radiale du champ crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################



######################################################################################
#tracé de la composante radiale du champ du condensateur en fonction de r/a pour diverses valeurs de z_e
#exemple d'utilisation: trace_composante_axiale_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.5)
def trace_composante_radiale_condensateur_en_fonction_de_r(r_a_min,r_a_max,nombre_valeurs_r,liste_z_e,e_a):
    plt.figure(17)
    liste_r_a=np.linspace(r_a_min,r_a_max,nombre_valeurs_r)
    liste_ez=np.zeros(nombre_valeurs_r)
    for z_e in liste_z_e:
        liste_ez=e_r_sur_E0_condensateur_vectorialisee(liste_r_a,z_e*e_a,e_a)
        plt.plot(liste_r_a,liste_ez,label='z/épaisseur='+str(z_e))

    plt.grid()
    plt.legend()
    plt.xlabel("r/a")
    plt.ylabel(r'$E_z /E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Composante radiale du champ crée par un condensateur de rayon a, épaisseur/rayon='+str(e_a))
    plt.show()
######################################################################################





######################################################################################
#tracé des lignes de champ dans une fenêtre
#exemple d'utilisation: trace_lignes_champ_disque(-2,2,-2,2,[i*0.1 for i in range(-15,16)],[0.01]*31,300,0.01)
#r_a_min,r_a_max,z_a_min,z_a_max sont les limites de la fenêtre de tracé
#les lignes partent des points dont les r/a  et les z/a sont fournis dans les listes liste_r_a_depart,liste_z_a_depart
#pas_integration est la distance entre deux points consécutifs
def trace_lignes_champ_disque(r_a_min,r_a_max,z_a_min,z_a_max,liste_r_a_depart,liste_z_a_depart,nombre_max_points_sur_ligne,pas_integration):
    plt.figure(3)
    plt.xlim(r_a_min,r_a_max)
    plt.ylim(z_a_min,z_a_max)
    normalize = Normalize(vmin=0, vmax=1)
    print('Calculs en cours, veuillez patienter...')
    for i in range(len(liste_r_a_depart)):
        r0 =liste_r_a_depart[i]
        z0=liste_z_a_depart[i]
        R_a,Z_a=Calcule_Ligne_Champ_Runge_Kutta(r0,z0,r_a_min,r_a_max,z_a_min,z_a_max,Champ_Disque,nombre_max_points_sur_ligne,pas_integration)
        norme=np.sqrt(e_r_sur_E0_disque_vectorialisee(R_a,Z_a)**2+e_z_sur_E0_disque_vectorialisee(R_a,Z_a)**2)
        plt.scatter(R_a,Z_a,c=norme,s=[1]*R_a.size,norm=normalize,cmap='rainbow')
        plt.scatter(R_a,-Z_a,c=norme,s=[1]*R_a.size,norm=normalize, cmap='rainbow')
    plt.colorbar(label=r'E/$E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Carte des lignes de champ électrique crée par un disque de rayon a uniformément chargé')
    plt.xlabel('r/a')
    plt.ylabel('z/a')
    #tracé du disque
    plt.plot([-1,1],[0,0],'k',linewidth=2)
    plt.grid()
    plt.show()
######################################################################################



######################################################################################
#tracé des lignes de champ dans une fenêtre
#exemple d'utilisation: trace_lignes_champ_condensateur(-2,2,-2,2,[i*0.1 for i in range(-15,16)],[0.01]*31,300,0.01,0.02)
#r_a_min,r_a_max,z_e_min,z_e_max sont les limites de la fenêtre de tracé
#les lignes partent des points dont les r/a  et les z/e sont fournis dans les listes liste_r_a_depart,liste_z_e_depart
#pas_integration est la distance entre deux points consécutifs
def trace_lignes_champ_condensateur(r_a_min,r_a_max,z_e_min,z_e_max,liste_r_a_depart,liste_z_e_depart,nombre_max_points_sur_ligne,pas_integration,e_a):
    plt.figure(3)
    plt.xlim(r_a_min,r_a_max)
    plt.ylim(z_e_min,z_e_max)
    z_a_min,z_a_max=z_e_min*e_a,z_e_max*e_a
    normalize = Normalize(vmin=0, vmax=2)
    liste_z_a_depart=np.array(liste_z_e_depart)*e_a
    print('Calculs en cours, veuillez patienter...')
    for i in range(len(liste_r_a_depart)):
        r0 =liste_r_a_depart[i]
        z0=liste_z_a_depart[i]
        R_a,Z_a=Calcule_Ligne_Champ_Runge_Kutta(r0,z0,r_a_min,r_a_max,z_a_min,z_a_max,Champ_condensateur,nombre_max_points_sur_ligne,pas_integration,e_a)
        norme=np.sqrt(e_r_sur_E0_condensateur_vectorialisee(R_a,Z_a,e_a)**2+e_z_sur_E0_condensateur_vectorialisee(R_a,Z_a,e_a)**2)
        Z_e=Z_a/e_a
        plt.scatter(R_a,Z_e,c=norme,s=[1]*R_a.size,norm=normalize,cmap='rainbow')
        plt.scatter(R_a,-Z_e,c=norme,s=[1]*R_a.size,norm=normalize, cmap='rainbow')
    plt.colorbar(label=r'E/$E_0$ avec $E_0 =\sigma / (2 \epsilon_0)$')
    plt.title('Carte des lignes de champ électrique du condensateur de rayon a , épaisseur/rayon='+str(e_a))
    plt.xlabel('r/a')
    plt.ylabel('z/épaisseur')
    #tracé des armatures
    plt.plot([-1,1],[0.5,0.5],'k',linewidth=2)
    plt.plot([-1,1],[-0.5,-0.5],'k',linewidth=2)
    plt.grid()
    plt.show()
######################################################################################






######################################################################################
#fonction utilisée pour la dichotomie
def fonction_pour_equipotentielle_disque(z_a,potentiel):
    return(potentiel_sur_V0_disque(0,z_a)-potentiel)
######################################################################################





######################################################################################
#tracé des équipotentielles dans une fenêtre
#exemple d'utilisation: trace_equipotentielles_disque(-2,2,-2,2,[0.3,0.4,0.5,0.6,0.7,0.8,0.9],2000,0.01)
#r_a_min,r_a_max,z_a_min,z_a_max sont les limites de la fenêtre de tracé
#liste_equipotentielles: liste des valeurs de V/V0 pour lesquelles on veut le tracé
#pas_integration est la distance entre deux points consécutifs sur la ligne de champ
#méthode: on détermine d'abord par dichotomie l'ordonnée du point de l'axe ayant le potentiel souhaité
#puis on suit les lignes du champ (-Ez,Er): ces lignes étant orthogonales à celles du champ E, ce sont des équipotentielles
def trace_equipotentielles_disque(r_a_min,r_a_max,z_a_min,z_a_max,liste_equipotentielles,nombre_max_points_sur_ligne,pas_integration):

    plt.figure(4)
    plt.xlim(r_a_min,r_a_max)
    plt.ylim(z_a_min,z_a_max)
    print('Calculs en cours, veuillez patienter...')
    for potentiel in liste_equipotentielles:
    #on cherche l'ordonnée du point sur l'axe (r=0) qui a ce potentiel, par dichotomie
        if fonction_pour_equipotentielle_disque(0,potentiel)*fonction_pour_equipotentielle_disque(z_a_max,potentiel)>0:
            break
        z_a_depart,res=bisect(fonction_pour_equipotentielle_disque,0,z_a_max,args=(potentiel),full_output = True,disp=False)
        if not res.converged:
            break
        R_a,Z_a=Calcule_Ligne_Champ_Runge_Kutta(0,z_a_depart,r_a_min,r_a_max,z_a_min,z_a_max,Champ_Disque_Equipotentielle,nombre_max_points_sur_ligne,pas_integration)
        plt.plot(R_a,Z_a,label='V/$V_0$='+str(potentiel))
    plt.title(r'Carte des équipotentielles créees par un disque de rayon a uniformément chargé'+r'       $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.xlabel('r/a')
    plt.ylabel('z/a')
    #tracé du disque
    plt.plot([-1,1],[0,0],'k',linewidth=2)
    plt.legend()
    plt.grid()
    plt.show()
######################################################################################


######################################################################################
#fonction utilisée pour la dichotomie
def fonction_pour_equipotentielle_condensateur(z_a,e_a,potentiel):
    return(potentiel_sur_V0_condensateur(0,z_a,e_a)-potentiel)
######################################################################################

######################################################################################
#tracé des équipotentielles dans une fenêtre
#exemple d'utilisation: trace_equipotentielles_condensateur(-2,2,-2,2,[0.3,0.4,0.5,0.6,0.7,0.8,0.9],2000,0.01,0.5)
#r_a_min,r_a_max,z_a_min,z_a_max sont les limites de la fenêtre de tracé
#liste_equipotentielles: liste des valeurs de V/V0 pour lesquelles on veut le tracé
#pas_integration est la distance entre deux points consécutifs sur l'équipotentielle
#méthode: on détermine d'abord par dichotomie l'ordonnée du point de l'axe ayant le potentiel souhaité
#puis on suit les lignes du champ (-Ez,Er): ces lignes étant orthogonales à celles du champ E, ce sont des équipotentielles
def trace_equipotentielles_condensateur(r_a_min,r_a_max,z_e_min,z_e_max,liste_equipotentielles,nombre_max_points_sur_ligne,pas_integration,e_a):

    plt.figure(4)
    plt.xlim(r_a_min,r_a_max)
    plt.ylim(z_e_min,z_e_max)
    z_a_max,z_a_min=z_e_max*e_a,z_e_min*e_a
    print('Calculs en cours, veuillez patienter...')
    for potentiel in liste_equipotentielles:
    #on cherche l'ordonnée du point sur l'axe (r=0) qui a ce potentiel, par dichotomie
        if fonction_pour_equipotentielle_condensateur(-e_a/2,e_a,potentiel)*fonction_pour_equipotentielle_condensateur(e_a/2,e_a,potentiel)>0:
            break
        z_a_depart,res=bisect(fonction_pour_equipotentielle_condensateur,-e_a/2,e_a/2,args=(e_a,potentiel),full_output = True,disp=False)
        if not res.converged:
            break
        R_a,Z_a=Calcule_Ligne_Champ_Runge_Kutta(0,z_a_depart,r_a_min,r_a_max,z_a_min,z_a_max,Champ_condensateur_Equipotentielle,nombre_max_points_sur_ligne,pas_integration,e_a)
        Z_e=Z_a/e_a
        plt.plot(R_a,Z_e,label='V/$V_0$='+str(potentiel))
    plt.title('Carte des équipotentielles créees par un condensateur de rayon a , épaisseur/rayon='+str(e_a)+r'    $V_0 =a\sigma / (2 \epsilon_0)$')
    plt.xlabel('r/a')
    plt.ylabel('z/épaisseur')
    #tracé des armatures
    plt.plot([-1,1],[0.5,0.5],'k',linewidth=2)
    plt.plot([-1,1],[-0.5,-0.5],'k',linewidth=2)
    plt.legend()
    plt.grid()
    plt.show()
######################################################################################



######################################################################################
#les exemples:
#trace_potentiel_disque_en_fonction_de_z(-1,1,500,[0,0.1,0.2,0.5,0.9,1.1])
#trace_potentiel_disque_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,1])
#trace_composante_axiale_disque_en_fonction_de_z(-1,1,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
#trace_composante_axiale_disque_en_fonction_de_r(-2,2,500,[0.001,0.1,0.2,0.5,1])
#trace_composante_radiale_disque_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
#trace_composante_radiale_disque_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1])
#trace_lignes_champ_disque(-2,2,-2,2,[i*0.1 for i in range(-15,16)],[0.01]*31,300,0.01)
#trace_equipotentielles_disque(-2,2,-2,2,[0.3,0.4,0.5,0.6,0.7,0.8,0.9],2000,0.01)
#trace_potentiel_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.99,1.01],0.5)
#trace_potentiel_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],1)
#trace_potentiel_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0],0.1)
#trace_composante_axiale_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.1)
#trace_composante_axiale_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.1)
#trace_composante_radiale_condensateur_en_fonction_de_z(-2,2,500,[0,0.1,0.2,0.5,0.9,0.99,1.01,1.1],0.1)
#trace_composante_radiale_condensateur_en_fonction_de_r(-2,2,500,[0,0.1,0.2,0.3,0.4,0.5,0.6,1],0.1)
#trace_lignes_champ_condensateur(-2,2,-2,2,[i*0.1 for i in range(-15,16)]+[i*0.1 for i in range(-9,10)],[0]*31+[0.5001]*19,300,0.02*0.1,0.1)
#trace_equipotentielles_condensateur(-2,2,-2,2,[0.01*i for i in range(-9,10)],4000,0.02,0.1)
#trace_lignes_champ_condensateur(-2,2,-2,2,[i*0.1 for i in range(-15,16)]+[i*0.1 for i in range(-9,10)],[0]*31+[0.5001]*19,300,0.02,1)
trace_equipotentielles_condensateur(-2,2,-2,2,[0,-0.05,-0.1,-0.15,-0.2,-0.25,-0.3,-0.35,0.05,0.1,0.15,0.2,0.25,0.3,0.35],2000,0.02,1)
