# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 17:26:39 2016

@author: AOsipenko
"""

import pandas as pd


def getFromNIST_isoTherm(fluid_id='', Temp='', Plow='', Phigh='', deltaP = '1',
                TypeOfData = 'IsoTherm' , TempUnits = 'C', PresUnits = 'psia',
                DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
                Surface_tension = 'N%2Fm',Digits = '5'):
    request  = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                + fluid_id + '&Type='+ TypeOfData +'&Digits='+Digits+'&PLow=' + Plow
                + '&PHigh=' + Phigh +'&PInc=' + deltaP + '&T=' + Temp
                + '&RefState=DEF&TUnit=' + TempUnits +'&PUnit=' + PresUnits
                + '&DUnit='+ DensityUnits + '&HUnit='+ EnergyUnits +'&WUnit='+ VelocityUnits
                + '&VisUnit='+ ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')
    return data

def getFromNIST_isoBar(fluid_id='', Pres='', Tlow='', Thigh='', deltaT='1',
                TypeOfData = 'IsoBar' , TempUnits = 'C', PresUnits = 'psia',
                DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
                Surface_tension = 'N%2Fm', Digits = '5'):
    request  = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                + fluid_id + '&Type='+ TypeOfData + '&Digits='+Digits+'&P='+ Pres
                +'&THigh='+Thigh+'&TLow=' + Tlow + '&TInc='+deltaT
                +'&RefState=DEF&TUnit='+ TempUnits +'&PUnit=' + PresUnits
                + '&DUnit='+ DensityUnits + '&HUnit='+ EnergyUnits +'&WUnit='+ VelocityUnits
                + '&VisUnit='+ ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')
    return data

def getFromNIST_IsoChor(fluid_id='',Density = '', Tlow='', Thigh='', deltaT='1',
                TypeOfData = 'IsoChor' , TempUnits = 'C', PresUnits = 'psia',
                DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
                Surface_tension = 'N%2Fm', Digits = '5'):
    request  = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
    + fluid_id+ '&Type='+ TypeOfData +'&Digits='+Digits+'&THigh='+Thigh+'&TLow=' + Tlow
    + '&TInc='+deltaT+'&D='+Density+'&RefState=DEF&TUnit='+ TempUnits +'&PUnit=' + PresUnits
    + '&DUnit='+ DensityUnits + '&HUnit='+ EnergyUnits +'&WUnit='+ VelocityUnits
    + '&VisUnit='+ ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')
    return data


def getFromNIST_SatP(fluid_id='', Tlow='', Thigh='', deltaT='1',
                TypeOfData = 'SatP' , TempUnits = 'C', PresUnits = 'psia',
                DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
                Surface_tension = 'N%2Fm', Digits = '5'):
    request = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                + fluid_id + '&Type='+TypeOfData+'&Digits='+Digits+'&THigh='+Thigh+'&TLow=' + Tlow
                +'TInc=' + deltaT +'&RefState=DEF&TUnit='+ TempUnits +'&PUnit=' + PresUnits
                + '&DUnit='+ DensityUnits + '&HUnit='+ EnergyUnits +'&WUnit='+ VelocityUnits
                + '&VisUnit='+ ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')
    return data

def getFromNIST_SatT(fluid_id='', Plow='', Phigh='', deltaP = '1',
                TypeOfData = 'SatT' , TempUnits = 'C', PresUnits = 'psia',
                DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
                Surface_tension = 'N%2Fm', Digits = '5'):
    request  = ('http://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID='
                +fluid_id +'&Type='+TypeOfData+'&Digits='+Digits+'&PLow=' + Plow
                + '&PHigh=' + Phigh +'&PInc=' + deltaP + '&RefState=DEF&TUnit=' + TempUnits +'&PUnit=' + PresUnits
                + '&DUnit='+ DensityUnits + '&HUnit='+ EnergyUnits +'&WUnit='+ VelocityUnits
                + '&VisUnit='+ ViscosityUnits + '&STUnit=' + Surface_tension)
    data = pd.read_csv(request, delimiter='\t')
    return data

def getNIST(fluid_id='', Temp='', Plow='', Phigh='', deltaP = '1',
        Pres='',Density = '', Tlow='', Thigh='', deltaT='1',
        TypeOfData = '' , TempUnits = 'C', PresUnits = 'psia',
        DensityUnits = 'g%2Fml' , EnergyUnits = 'kJ%2Fmol' , VelocityUnits = 'm%2Fs', ViscosityUnits = 'cP',
        Surface_tension = 'N%2Fm', Digits = '5'):
    Pres = str(Pres)
    Tlow = str(Tlow)
    Thigh = str(Thigh)
    deltaT = str(deltaT)
    Temp = str(Temp)
    Plow = str(Plow)
    Phigh = str(Phigh)
    deltaP = str(deltaP)
    TypeOfData = str(TypeOfData)
    try:
        if TypeOfData == 'IsoTherm':
            return getFromNIST_isoTherm(fluid_id,Temp,Plow, Phigh, deltaP)
        elif TypeOfData == 'IsoBar':
            return getFromNIST_isoBar(fluid_id, Pres, Tlow, Thigh, deltaT)
        elif TypeOfData == 'IsoChor':
            return getFromNIST_IsoChor(fluid_id,Density, Tlow, Thigh, deltaT)
        elif TypeOfData == 'SatP':
            return getFromNIST_SatP(fluid_id, Tlow, Thigh, deltaT)
        elif TypeOfData == 'SatT':
            return getFromNIST_SatT(fluid_id, Plow, Phigh, deltaP)
        else:
            print("Please, specify Type of Data correctly: IsoTherm, IsoBar, IsoChor, SatP or SatT")
    except:
        print("Please, specify parameters correctly")

