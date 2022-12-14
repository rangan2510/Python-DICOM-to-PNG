#%%
import numpy as np
import png, os, pydicom

#%%
source_folder = r"dicom"
output_folder = r"output"

list_of_files = []
for root, dirs, files in os.walk(source_folder):
	for file in files:
		list_of_files.append(os.path.join(root,file))

#%%
for file in list_of_files:
    try:
        print('Converting: ', file)
        ds = pydicom.dcmread(file)
        shape = ds.pixel_array.shape

        # Convert to float to avoid overflow or underflow losses.
        image_2d = ds.pixel_array.astype(float)

        # Rescaling grey scale between 0-255
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0

        # Convert to uint
        image_2d_scaled = np.uint8(image_2d_scaled)

        # Write the PNG file
        dirs_in_path = file.split("\\")
        filename = dirs_in_path[-1] + ".png"
        metaname = dirs_in_path[-1] + ".txt"
        output_path = output_folder + "\\" + str.join("\\", dirs_in_path[1:-1])
        os.makedirs(output_path, exist_ok=True)
        
        output_file = output_path + "\\" + filename
        output_file_meta = output_path + "\\" + metaname
    
        
        with open(output_file, 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)
        print('Written to: ', output_file)

        with open(output_file_meta, 'w+') as meta_file:
            meta_file.write(str(ds))
    except:
        print('Cannot process: ', file)
        
# %%
