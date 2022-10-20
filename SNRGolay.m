%Z score tells us how many std abover or below the mean a particular data
%point i

% Data
y = x;

% Settings
lag = 100;
threshold = 3;

% Get results`                                                          
[signals] = Signal2NoiseRatio(y,lag,threshold);

%Plottigng stuff
figure; subplot(2,1,1); hold on;
plot(1:length(y),y,'b');
subplot(2,1,2);
stairs(signals,'r','LineWidth',1.5); ylim([-1.5 1.5]);



function [signals] = Signal2NoiseRatio(y,lag,threshold)
% Initialise signal results
signals = zeros(length(y),1);
% Initialise filtered series
filteredY = y(1:lag+1);
% Initialise filters
avgFilter(lag+1,1) = mean(y(1:lag+1));
stdFilter(lag+1,1) = std(y(1:lag+1));
% Loop over all datapoints y(lag+2),...,y(t)
Peaks = [];
PeakVec = {};
PeakMax = [];
Noise = [];
changeCon = [0,0];
counter = 1;
temp = [];
for i=lag+2:length(y)
    
    if changeCon(1,1) ~= changeCon(1,2)
        counter = counter +1;
        PeakVec = [PeakVec,temp];
        temp = [];
    end
    
    if (mod(counter, 2) == 0 | counter ==1)
   
    else
        temp = [temp,y(i)];
      
    end
     % If new value is a specified number of deviations away
    if abs(y(i)-avgFilter(i-1)) > threshold*stdFilter(i-1)
        
        peakAsign = 1;
        if y(i) > 0
            
            % Positive signal
            signals(i) = 1;
            Peaks = [Peaks, y(i)];
          
        else
            % Negative signal
            signals(i) = -1;
            Peaks = [Peaks, y(i)];
            
        end
        % Make influence lower
        filteredY(i) = filteredY(i-1);
        Peaks = [Peaks, y(i)];
        
        
    else
        % No signal
        signals(i) = 0;
        filteredY(i) = y(i);
        Noise = [Noise,y(i)];
        peakAsign = 2;

   
    
    end
    % Adjust the filters
   
    changeCon(1,1)=changeCon(1,2);
    changeCon(1,2)=peakAsign;
    PeakABS = [];
    for c=(PeakVec)
        cMat = cell2mat(c);
        
        PeakABS =  abs(cMat);
        
    end
    
   
    MeanPeak = mean(PeakABS);
    avgFilter(i) = mean(filteredY(i-lag:i));
    stdFilter(i) = std(filteredY(i-lag:i));
    MeanSideLobes = sum((abs(Noise))/length(Noise));
    SNR = MeanPeak/MeanSideLobes;
 
    
end
cMat
end

% Done, now return results