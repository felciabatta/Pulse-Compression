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
x = readmatrix("signal_data/pulse_2MHznonoise/match_result.csv");
y = x(:,10);
% y(y==0)=nan; % using nan often makes it worse - need to sort this issue

% Settings
lag = 300; % window size
threshold = 3; % no. of stds
influence = 0.7; % influence factor for new point in moving window
UseMaxPeak = true; % use max peak rather than mean peaks

% Get results
[signals] = Signal2NoiseRatio(y,lag,threshold, influence, UseMaxPeak);

% Plotting stuff
figure; subplot(2,1,1); hold on;
plot(y,'b');
subplot(2,1,2);
stairs(signals,'r','LineWidth',1.5); ylim([-1.5 1.5]);

function [signals] = Signal2NoiseRatio(y, lag, threshold, influence, UseMaxPeak)

% Initialise signal results
signals = zeros(length(y),1);

% Initialise filtered series (the moving window)
filteredY = y(1:lag+1);

% Initialise filters ()
avgFilter(lag+1,1) = mean(abs(y(1:lag+1))); % means of previous window
stdFilter(lag+1,1) = std(abs(y(1:lag+1))); %  stds of previous window

% Loop over all datapoints y(lag+2),...,y(t)
Peaks = []; % vector of all points above threshold
PeakVec = {}; % cell array containing 
Noise = []; % vector of all points above threshold
changeCon = [0,0]; % determines when classification changes
counter = 1;
temp = []; % vector containing a current selction of

for i=lag+2:length(y)
    % if classification changes: tally +1, add temp to cell array
    if changeCon(1,1) ~= changeCon(1,2)
        counter = counter+1;
        PeakVec = [PeakVec,temp];
        temp = [];
    end
    
    % if currently on peak ( (tally)mod2 == 1 ): add point to temp
    if (mod(counter, 2) == 0 | counter ==1)
    else
        temp = [temp,y(i)];
    end

    % if new value is above threshold
    % (new val)-(mean of previous window) > (std of prev window)
    if abs(y(i))-avgFilter(i-1) > threshold*stdFilter(i-1)
        
        peakAsign = 1; % classify point as a PEAK

        if y(i) > 0 % Positive signal
            signals(i) = 1; % add to list of classified points
%             Peaks = [Peaks, y(i)]; % add to set of peak points
        else % Negative signal
            signals(i) = -1; % add to list of classified points
%             Peaks = [Peaks, y(i)]; % add to set of peak points
        % MAYBE have TROUGH points too?
        end

        % Make influence lower
        filteredY(i) = influence*y(i)+(1-influence)*filteredY(i-1);
        Peaks = [Peaks, y(i)]; % add to set of peak points AGAIN???

    else
        % No signal
        signals(i) = 0; % add to list of classified points
        filteredY(i) = y(i);
        Noise = [Noise,y(i)]; % add to set of noise points
        peakAsign = 2; % classify point as NOISE
    end

    % Adjust the filters
    changeCon(1,1) = changeCon(1,2); % update 
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

MeanSideLobes = mean(abs(Noise), 'omitnan')
% MeanSideLobes = sqrt(mean(Noise.^2));
SNR = MAXPeak/MeanSideLobes
end
