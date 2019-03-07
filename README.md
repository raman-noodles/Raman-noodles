# Raman-Noodles
![raman noodles logo](https://user-images.githubusercontent.com/46499087/53783952-7c38f680-3ec8-11e9-8549-6bda4ba7743c.PNG)

## This is the UW DIRECT Winter 2019 Team Project GitHub Repo
**Team members (alphabetical by first name): Brandon Kern, Elizabeth Rasmussen, Jon Onorato, Parker Steichen**


### Overall Project Objective
This package allows for the auto analysis of a mixture's Raman spectra. It compares the input mixture spectra against an individual component's spectra contained. 
- Background and motivation for the project can be found in the [Background and Motivation Wiki Page](https://github.com/raman-noodles/Raman-noodles/wiki/Project-Background-and-Motivation)

### Assumptions and Project Scope
1. Baseline subtraction is beyond the scope of this project. 
- Assumed that input mixture data has already been properly baseline subtracted
2. Storing data library that is beyond the components of Formic Acid (Hydrogen, Water, Carbon dioxide, Carbon monoxide) are not included as other components are beyond the scope of the project at this time.
- Assumed that the user is trying to analyze Formic Acid, or a mixture that consists only of: Formic Acid, Hydrogen, Water, Carbon dioxide, Carbon monoxide.

### Project Breakdown
The project can be thought of as broken down into 3 steps:
1. Data Wrangling
2. Peak fitting and identification
3. Statistical analysis for peak fits

These three sections have their own wiki documents and filled juypter notebooks with more detail included throught, see those for more detail on the individual steps.

### User Flow: As a user you should follow these steps to apply Raman-Noodles to YOUR data
#### Note: these are major steps that will walk you through the three major steps. 
1. [need to fill in]


### Example of Using Raman Noodles
An example of using the software can be seen in the wiki page: [Link to Raman-Noodles Example Use Case Wiki Page](https://github.com/raman-noodles/Raman-noodles/wiki/Example-of-Raman-Noodle-Use)


### Future Work
The team will continue working on this project in Spring of 2019 as apart of DIRECT program. Future tasks include:
1. Increasing fuctionality of code for different substances beyond Formic Acid
    a. Increasing the size of the library of component Raman Spectra
    b. Creating and using an open internal database stored and accessable via a Google Drive Team folder. 
2. Applying kinetic analysis to data sets to view the change in decomposition and formation of species given different boundary conditions (temperature, resonance time, and strech goal of pressure)

### Conclusion
This software has passed tests to sucessfully identify and analyze the identification of a Formic Acid mixture Raman data.
