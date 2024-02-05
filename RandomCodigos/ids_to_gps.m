% Define the folder containing the original text files
originalFolder = 'C:/Users/Vastingood/Documents/Github/Tese/NNs/Testing/ids/';  % Replace with the actual path

% Define the folder for the new text files
newFolder = fullfile(originalFolder, 'LPs');

% Create the "LPs" folder if it doesn't exist
if ~exist(newFolder, 'dir')
    mkdir(newFolder);
end

% List the original text files
originalFiles = dir(fullfile(originalFolder, '*.txt'));

% Load the GPS data timetable
load('gps_data.mat');  % Load your GPS data timetable

% Iterate through each original file
for fileIdx = 1:numel(originalFiles)
    % Read the contents of the original file
    originalFile = fullfile(originalFiles(fileIdx).folder, originalFiles(fileIdx).name);
    originalContents = textread(originalFile, '%s', 'delimiter', '\n');
    
    % Extract the unique codes from the file
    uniqueCodes = unique(originalContents);
    
    % Create a new file for each unique code
    for codeIdx = 1:numel(uniqueCodes)
        code = uniqueCodes{codeIdx};
        % Find indices of lines with the current code
        indices = find(ismember(originalContents, code));
        
        % Create a new file for the current code
        newFileName = fullfile(newFolder, [code, '.txt'])
        fid = fopen(newFileName, 'w');
        
        % Write latitude and longitude for each timestamp to the new file
        for idx = indices
            line = originalContents{idx};
            timestamp = line(9:end);  % Extract HH:MM:SS:mmm
            % Find the corresponding GPS data from the timetable
            gpsIndex = find(ismember(gpsData.Timestamp, timestamp));
            if ~isempty(gpsIndex)
                latitude = gpsData.Latitude(gpsIndex);
                longitude = gpsData.Longitude(gpsIndex);
                fprintf(fid, '%s %f %f\n', timestamp, latitude, longitude);
            end
        end
        
        fclose(fid);
    end
end
