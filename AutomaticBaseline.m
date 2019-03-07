% Automatic Baseline
% Author: David Gorman and Elizabeth Rasmussen
% Date: 4/25/2018
 
%This script will create a consistent automatic baseline after first
%creating a manual baseline and defining anchor points on the Raman
%spectra. This will guarantee that the spectra are processed consistently
%without missing any significant peak information.
 
%This script is designed to be run from within the ConcentrationFinder.m
%Script. Running it alone may cause errors
 
%User inputs
anchor_x = [254.8003;
    276.3905;
    293.8892;
    325.7930;
    395.2405;
    442.0965;
    493.5111;
    550.0000;
    608.0000;
    625.3288;
    642.0000;
    774.6450;
    874.5473;
    899.4382;
    970.0000;
    1113.4852;
    1456.2630;
    1537.5162;
    1795.3263;
    1879.1594;
    1952.0787;
    2019.1565;
    2077.4793;
    2164.3930;
    2274.3366;
    2415.6675;
    2520.9413;
    2629.5319;
    2726.0034;
    2818.3521;
    2880.4902;
    3255.8493];
 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
oldpath = cd;
cd(strcat(cd,folder));
% For baseline subtracted
tic
allFiles = dir('*.txt');
x = cell(length(allFiles),1);
y = x;
params = x;
for i = 1:length(allFiles)
    filename = allFiles(i).name;
    fid = fopen(filename);
    data = textscan(fid,'%f %f %f %f','HeaderLines',24);
    IntTime = dlmread(filename,'\t',[6 1 6 1]);
    NumAvg = dlmread(filename,'\t',[7 1 7 1]);
    LaserPower = dlmread(filename,'\t',[11 1 11 1]);
    x{i} = data{2};
    y{i} = data{4};
    params{i} = [IntTime NumAvg LaserPower];
    fclose(fid);
end
fprintf('Text files processed\n')
 
%Baseline subtraction
baseline = cell(length(allFiles),1);
subtracted = baseline;
anchor_y = baseline;
 
%Scale signals to equivalent laser power and integration time, choosing
%strongest signal as reference. Strength is determined by the product of
%laser power and integration time
strength = zeros(length(allFiles),1);
for i = 1:length(allFiles)
    strength(i) = params{i}(1)*params{i}(3);
end
 
%Correct for laser power and integration time (strength)
[tmp, index] = max(strength);
for i = 1:length(allFiles)
    y{i} = y{i}*strength(index)./strength(i);
end
 
%Subtract Baseline
for i = 1:length(allFiles)
    anchor_y{i} = interp1(x{i},y{i},anchor_x);
    baseline{i} = pchip(anchor_x,anchor_y{i},x{i});
    subtracted{i} = y{i}-baseline{i};
end
 
processed = {x subtracted params};
toc
 
%Plot everything
hold on
for i = 1:length(allFiles)
    plot(x{i},y{i},'k-',x{i},baseline{i},'r--',x{i},subtracted{i},...
        'b-')
end
xlabel('Raman shift, cm^-^1');
ylabel('Intensity, arb. units');
legend('Original Raman Spectra Data', 'Least Squares Fit', 'Subtracted Raman Spectra');
hold off
 
cd(oldpath)