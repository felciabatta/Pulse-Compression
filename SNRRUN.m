SNRlist = [];
for c=1:length(defects)
    y = x(:,defects(c));
    
   
    [signals,SNR] = Signal2NoiseRatio(y,lag,threshold, influence, UseMaxPeak);
    disp(SNR)
    SNRlist = [SNRlist,SNR]
end
meanSNR = mean(SNRlist)