# NIST chemistry webbook wrapper
Easy to use wrapper for NIST chemistry webbook database. Allows to get required physical properties from NIST chemistry database without opening website in browser and in much faster and convenient way than manual searching.  

source: http://webbook.nist.gov/chemistry/fluid/

### Requirements:
Pandas is required:

You can simply install it with
> ` pip unstall pandas `

Or from file *requirements.txt* , with command:
> ` pip install -r requirements.txt `

### Default requests:

**Required variables:**

- fluid_id - id of substanse 
- Temp - temperature for IsoThermic properties
- Plow, Phigh - range of pressure for IsoThermic properties
- deltaP - Increment of pressure in pressure range
- TypeOfData - Isotherm, IsoBar, IsoChor, SatP, SatT

**Optional variables:**

default values are: 
- TempUnits = 'C', 
- PresUnits = 'psia',
- DensityUnits = 'g%2Fml' , 
- EnergyUnits = 'kJ%2Fmol' , 
- VelocityUnits = 'm%2Fs', 
- ViscosityUnits = 'cP',
- Surface_tension = 'N%2Fm', 
- Digits = '5'

Check full descriptions of available units and substances in file [description.md](https://github.com/subpath/NIST_chemistry_webbook_wrapper/blob/master/description.md)


### Example of usage:

>  `data = getNIST(fluid_id = Fluids_ID['argon'], Temp = 30, Plow = 140, Phigh= 200, deltaP = 10, TypeOfData ='IsoTherm')`




Data will be return as pandas [DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html) , and then can easily managed, and exported in [different files type](http://pandas.pydata.org/pandas-docs/stable/io.html).


[See for more examples](https://github.com/subpath/NIST_chemistry_webbook_wrapper/tree/master/examples).


##### Author:                                                                                                                                               
> Alexander Osipenko,     
> e-mail: subpath@ya.ru



