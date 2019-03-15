# Raman-Noodles
![raman noodles logo](https://user-images.githubusercontent.com/46499087/53783952-7c38f680-3ec8-11e9-8549-6bda4ba7743c.PNG)

## This is the UW DIRECT Winter 2019 Team Project GitHub Repo
**Team members (alphabetical by first name): Brandon Kern, Elizabeth Rasmussen, Jon Onorato, Parker Steichen**


### Overall Project Objective
This project identifies components in a Raman spectra. Advantages to using this method are:
1. FULLY Open source, no part of the project is dependent on a paid service
2. AUTOMATED process, analysis is automated leading to fast results
3. VERIFIABLE, user is made aware of how confident they can be in the results via a statistical software stack

- **More detailed background and motivation for the project can be found in the [Project Background and Motivation Wiki Page](https://github.com/raman-noodles/Raman-noodles/wiki/Project-Background-and-Motivation)**

### Assumptions and Project Scope
1. Storing data library that is beyond the decomposition products of formic acid (hydrogen, water, carbon dioxide, carbon monoxide) are not included as other components are beyond the scope of the project at this time.
- Assumed that the user is trying to analyze the decomposition products of formic acid, or a mixture that consists only of: Formic Acid, Hydrogen, Water, Carbon dioxide, Carbon monoxide.
2. This project will not be predictive - that is, it will require the user to specifically input what potential compounds will be 
present in the spectra to be analyzed. This list does not have to be exhaustive; however, the more inclusive the list, the better
the fitting and predicting results will be. 

### Project Breakdown
The project can be thought of as broken down into 3 steps:
1. Data Wrangling
2. Peak fitting and identification
3. Statistical analysis for peak fits

These three sections have their own wiki documents and filled juypter notebooks with more detail included throught, see those for more detail on the individual steps.

### User Flow and Example of Using Raman Noodles
A user will be able to follow the steps to apply Raman-Noodles to YOUR *Formic Acid* data set. An example of using the software can be seen in the [Example Use Case Wiki Page](https://github.com/raman-noodles/Raman-noodles/wiki/Example-of-Raman-Noodle-Use)


### Future Work
The team will continue working on this project in Spring of 2019 as apart of DIRECT program. Future tasks include:
1. Increasing fuctionality of code for different substances beyond Formic Acid
    a. Increasing the size of the library of component Raman Spectra
    b. Creating and using an open internal database stored and accessable via a Google Drive Team folder. 
2. Applying kinetic analysis to data sets to view the change in decomposition and formation of species given different boundary conditions (temperature, resonance time, and strech goal of pressure)

### Conclusion
This software has passed tests to sucessfully identify and analyze the identification of components in a formic acid mixture Raman data set.
