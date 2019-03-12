1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
clc; clear all;
 
%Files must be in the working directory, all text files in the working
%directory will be processed
 
tic
allFiles = dir('**/*.txt');
processed = cell(length(allFiles),1);
for i = 1:length(allFiles)
    filename = allFiles(i).name;
    fid = fopen(filename);
    data = textscan(fid,'%f %f %f %f','HeaderLines',24);
    data = {data{1,2} data{1,4}};
    processed{i} = data;
    fclose(fid);
end
fprintf('Text files processed\n')
 
 
%Noise rejection/Signal smoothing (Savitzky-Golay)
order = 3;
framelen = 11;
 
for i = 1:length(processed)
    sgf = sgolayfilt(processed{i}{2},order,framelen);
    processed{i}{2} = sgf;
end
fprintf('Data smoothing complete\n')
toc
%Baseline correction (ModPoly)
%%%
it = 200; %Number of desired iterations
n = 7; %5th order polynomial is standard
i = 1; %Restart while loop
%%%
 
warning('off','all')
while i <= length(processed)
    p = polyfit(processed{i}{1},processed{i}{2},n);
    base = polyval(p,processed{i}{1});
    k = 1;
    while k <= it
        for j = 1:length(base)
            if base(j) > processed{i}{2}(j)
                base(j) = processed{i}{2}(j);
            end
        end
        p_new = polyfit(processed{i}{1},base,n);
        base = polyval(p_new,processed{i}{1});
        k = k+1;
    end
    processed{i}{2} = (processed{i}{2}-base);
    i = i+1;
end
fprintf('Baseline subtracted\n')
toc
 
figure(1)
hold on
for i = 1:length(processed)
%     processed{i}{2} = processed{i}{2}-processed{end}{2};
%     processed{i}{2} = processed{i}{2}/max(processed{end-1}{2});
    plot(processed{i}{1},processed{i}{2})
end
hold off
 
ratio = zeros(length(processed));
for i = 1:length(processed)
    for j = 1:length(processed)
        ratio(i,j) = norm(processed{i}{2})/norm(processed{j}{2});
    end
end
 
ratio = triu(ratio,1);
for i = 1:length(processed)
    for j = 1:length(processed)
        if ratio(i,j) == 0
            ratio(i,j) = NaN;
        end
    end
end
 
fprintf('Water & sapphire signal subtracted\n')