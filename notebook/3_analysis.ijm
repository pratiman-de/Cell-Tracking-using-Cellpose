// Install CLIJ library first
// .csv files generated using code_1 and .tif files should be in the same input folder. The output .csv file has same name so the path for output folder must be different.

path = "c:/Users/mbiv104/Desktop/29_sep/y"
scale = 1.0; //change the scaling factor if required
sc = toString(scale*100);


// Function to process an image with translated coordinates
function processImageWithTranslatedCoords(coordsString, translateX, translateY, scaleFactor) {
    // Convert the string of coordinates to arrays
    coordsArray = split(coordsString, " ");
    xCoordinates = newArray();
    yCoordinates = newArray();
    
    // Split the coordinates into separate x and y lists, apply scaling and translation
    for (i = 0; i < coordsArray.length; i += 2) {
        scaledX = parseFloat(coordsArray[i]) * scaleFactor + translateX;
        scaledY = parseFloat(coordsArray[i + 1]) * scaleFactor + translateY;
        
        xCoordinates = Array.concat(xCoordinates, scaledX);
        yCoordinates = Array.concat(yCoordinates, scaledY);
    }

    // Create a PolygonRoi using the translated coordinates
    makeSelection("polygon", xCoordinates, yCoordinates);

    getDimensions(width, height, channels, slices, frames);
    setBatchMode(true); // Enable batch mode to suppress dialogs
    
    // Measure the intensity inside the ROI
    run("Measure");
}

// Define your collection (e.g., an array)
items = newArray("CFP", "YFP");

// Determine the length of the collection
numItems = lengthOf(items);

// Iterate through the collection
for (k = 0; k < numItems; k++) {
    item = items[k];
	csvInputFolderPath = path + "/analysis"; // Specify the folder for CSV files
	tifInputFolderPath = path + "/" + item;
	outputFolderPath = tifInputFolderPath + "/imagej_" + sc;

	// Check if the output folder exists
	if (!File.exists(outputFolderPath)) {
	    // Create the output folder
	    File.makeDirectory(outputFolderPath);
	    print("Folder created at " + outputFolderPath);
	} else {
	    print("Folder already exists at " + outputFolderPath);
	}
	
	listOfCsvFiles = getFileList(csvInputFolderPath);
	listOfTifFiles = getFileList(tifInputFolderPath);
	
	// Loop through the CSV files and their corresponding TIFF files
	for (i = 0; i < listOfCsvFiles.length; i++) {
		print(i);
	    csvFileName = listOfCsvFiles[i];
	    if (endsWith(csvFileName, ".csv")) {
	        csvPath = csvInputFolderPath + '/' + csvFileName;
	        tifFileName = csvFileName.replace(".csv", ".tif");
	        tifPath = tifInputFolderPath + '/' + tifFileName;
	
	        file = File.openAsString(csvPath);
	        lines = split(file, "\n");
	
	        run("CLIJ Macro Extensions", "cl_device=");
	        Ext.CLIJ_clear();
	        // Open the image
	        open(tifPath);
	        Ext.CLIJ_push(tifFileName);
	
	        for (j = 1; j < lines.length; j++) { // Skip header row
	            values = split(lines[j], ",");
	            if (values.length >= 3) {
	                xC = parseFloat(values[0]);
	                yC = parseFloat(values[1]);
	                st = values[2];
		
	                processImageWithTranslatedCoords(st, xC, yC, scale);
	            }
	        }
	
	        selectWindow("Results");
	        saveAs("Results", outputFolderPath + '/' + csvFileName.replace(".csv", "") + ".csv");
	        close("Results"); // Close the Results window
	        close();
	        Ext.CLIJ_clear();
	    }
	}
}
