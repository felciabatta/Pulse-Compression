% RUN PEAK DETECTION ALGORTIHM - FIND SNR ESTIMATE

%File paths match:

files = ["match_result.csv", "wien_result.csv",...
         "match-wien_result.csv", "wien-match_result.csv"];

dirs = ["signal_data/barker_1MHz_13/",...
        "signal_data/barker_2MHz_13/",...
        "signal_data/chirp_0822MHz_2u/",...
        "signal_data/chirp_0822MHz_6u/",...
        "signal_data/golay/",...
        "signal_data/pulse_1MHznoise/",...
        "signal_data/pulse_2MHznoise/"];

% Basic input signal no noise
% "signal_data/pulse_2MHznonoise/match-wien_result.csv"

defects = [11, 26, 41, 56, 72];

% SETTINGS
lag = 300; % window size
threshold = 3; % no. of stds
influence = 0.7; % influence factor for new point in moving window
UseMaxPeak = true; % use max peak rather than mean peaks

files = files;
dirs = dirs;

PLOTresults = false;
SAMEfigure = false;

SAVEresults = true;

% RUN ALGORITHM FOR EACH SET OF FILTER RESULTS
results = [];
for d = dirs
    for f = files
        % Data
        x = readmatrix(d+f);
        % y(y==0)=nan; % using nan often makes it worse - need to sort this issue
        
        if PLOTresults & SAMEfigure
            figure;
        end
        
        SNRlist = [];
        for c=1:length(defects)
            y = x;

            [signals,SNR] = Signal2NoiseRatio(y, defects(c), lag, threshold, influence, UseMaxPeak);
            if isempty(SNR)
                SNRlist = [SNRlist, 0];
            else
                SNRlist = [SNRlist, SNR];
            end
            % Plotting stuff
            if PLOTresults
                if ~SAMEfigure
                    figure;
                end
                subplot(2,1,1); hold on;
                plot(y(:, defects(c)),'b');
                subplot(2,1,2); hold on;
                stairs(signals,'r','LineWidth',1.5); ylim([-1.5 1.5]);
            end
        end
        meanSNR = mean(SNRlist);
        results = [results, SNRlist, meanSNR];
    end
end
results = reshape(results, [length(files)*6, length(dirs)])'

if SAVEresults
    writematrix(results, "SNR_Results.csv")
end