% Z score tells us how many std above or below the mean a particular data point i

%File paths:

%Barker
%"signal_data/barker_1MHz_13/match_result.csv"
%"signal_data/barker_2MHz_13/match_result.csv"

%Chirp
%"signal_data/chirp_0822MHz_2u/match_result.csv"
%"signal_data/chirp_0822MHz_6u/match_result.csv"

%Golay
%"signal_data/golay/match_result.csv"

%Basic input signal with noise
%"signal_data/pulse_1MHznoise/match_result.csv"
%"signal_data/pulse_2MHznoise/match_result.csv"

%Basic input signal no noise
%"signal_data/pulse_2MHznonoise/match_result.csv"

% Data
x = readmatrix("signal_data/golay/match_result.csv");
y = x(:, 10);
% y(y==0)=nan; % using nan often makes it worse - need to sort this issue

% Settings
lag = 300; % window size
threshold = 3; % no. of stds
influence = 0.7; % influence factor for new point in moving window
UseMaxPeak = true; % use max peak rather than mean peaks

% Get results
[signals] = Signal2NoiseRatio(y, lag, threshold, influence, UseMaxPeak);

% Plotting stuff
figure; subplot(2,1,1); hold on;
plot(y,'b');
subplot(2,1,2);
stairs(signals,'r','LineWidth',1.5); ylim([-1.5 1.5]);

function [signals] = Signal2NoiseRatio(y, lag, threshold, influence, UseMaxPeak)

% Initialise signal results
signals = zeros(length(y),1);

% Initialise filtered series (the moving window)
filteredY = y(1:lag);

% Initialise filters ()
avgFilter(lag,1) = mean(y(1:lag)); % means of previous window
stdFilter(lag,1) = std(y(1:lag)); %  stds of previous window

% Loop over all datapoints y(lag+2),...,y(t)
Peaks = []; % vector of all points above threshold
PeakVec = {}; % cell array containing all 'groupings of peaks'
Noise = []; % vector of all points above threshold
changeCon = [0,0]; % determines when classification changes
changeCount = 1;
tempPeaks = []; % vector containing a current selection of peaks

% RMS, STD and Mean over entire signal
y_nozero = y(y~=0);
signalRMS = sqrt(mean(y_nozero.^2));
signalSTD = std(y_nozero);
signalMean = mean(y_nozero);

for i=lag+1:length(y)
    % if classification changes: tally +1, add temp to cell array
    if changeCon(1,1) ~= changeCon(1,2)
        changeCount = changeCount+1;
        PeakVec = [PeakVec,tempPeaks];
        tempPeaks = [];
    end
    
    % if currently on peak ( (tally)mod2 == 0 ): add point to temp
    if (mod(changeCount, 2) == 0)
        tempPeaks = [tempPeaks, y(i)];
    end

    % if new value is above threshold
    % (new val)-(mean of previous window) > (std of prev window)
    if (abs(y(i))-avgFilter(i-1) > threshold*stdFilter(i-1))...
        & (abs(y(i))-signalMean > threshold*signalSTD)
        
        peakAsign = 1; % classify point as a PEAK

        if y(i) > 0 % Positive signal
            signals(i) = 1; % add to list of classified points
        else % Negative signal
            signals(i) = -1; % add to list of classified points
        end

        % Make influence lower
        filteredY(i) = influence*y(i)+(1-influence)*filteredY(i-1);
        Peaks = [Peaks, y(i)];

    else
        % No signal
        signals(i) = 0; % add to list of classified points
        filteredY(i) = y(i);
        if y(i) ~= 0 % to account for 0 values created in data processing
            Noise = [Noise, y(i)]; % add to set of noise points
        end
        peakAsign = 0; % classify point as NOISE
    end

    % Adjust the filters
    changeCon(1,1) = changeCon(1,2); % update change condition
    changeCon(1,2) = peakAsign;

    avgFilter(i) = mean(filteredY(i-lag:i));
    stdFilter(i) = std(filteredY(i-lag:i));
end

PeakABS = [];
for p = PeakVec
    if any(p{:}>0) % only use positive peaks
        Ptemp = max([p{:}]);
        PeakABS = [PeakABS,Ptemp];
    end
end
PeakABS

if isequal(PeakABS,[])
    MeanPeak = 0
else
    MeanPeak = mean(PeakABS)
end

if UseMaxPeak == true
    MAXPeak = max(PeakABS)
end

PeakABS
noiseRMS = sqrt(mean(Noise.^2, 'omitnan'))
SNR = MAXPeak/noiseRMS
end
