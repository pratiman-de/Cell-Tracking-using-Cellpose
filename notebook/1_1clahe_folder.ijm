// Set the input and output folder paths
input_folder_path = "C:/Users/mbiv104/Desktop/29_sep/y/TD/";
output_folder_path = "C:/Users/mbiv104/Desktop/29_sep/y/TD/tdd";
// Check if the output folder exists
if (!File.exists(output_folder_path)) {
	
	// Create the output folder
	File.makeDirectory(output_folder_path);
	print("Folder created at " + output_folder_path);
} else {
	print("Folder already exists at " + output_folder_path);
}

// Define the processing parameters
blocksize = 127;
histogram_bins = 256;
maximum_slope = 3;
mask = "*None*";
fast = true;
process_as_composite = true;

// Loop through input images in the input folder
list = getFileList(input_folder_path);
for (i = 0; i < list.length; i++) {
  input_image_path = input_folder_path + list[i];
  
  // Open the input image
  open(input_image_path);
  
  // Get image dimensions
  getDimensions(width, height, channels, slices, frames);
  isComposite = channels > 1;
  parameters =
    "blocksize=" + blocksize +
    " histogram=" + histogram_bins +
    " maximum=" + maximum_slope +
    " mask=" + mask;
  if (fast)
    parameters += " fast_(less_accurate)";
  if (isComposite && process_as_composite) {
    parameters += " process_as_composite";
    channels = 1;
  }
  
  // Process the image
  for (f = 1; f <= frames; f++) {
    Stack.setFrame(f);
    for (s = 1; s <= slices; s++) {
      Stack.setSlice(s);
      for (c = 1; c <= channels; c++) {
        Stack.setChannel(c);
        run("Enhance Local Contrast (CLAHE)", parameters);
      }
    // Save the processed image to the output folder
  j = i + 1;
  output_image_path = output_folder_path + "/" + j + ".tif";
  saveAs("Tiff", output_image_path);
  close();    
      
    }
  }
  

}
