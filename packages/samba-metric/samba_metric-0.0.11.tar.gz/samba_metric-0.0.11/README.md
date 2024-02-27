# SAMBA (Smoothed imAge MicroBiome distAnce)

 This code is attached to the paper "SAMBA: A Novel Smoothed Image-Based Metric for Microbial Sequencing Data Analysis".
 SAMBA is a novel microbial metric. SAMBA utilizes the iMic method to transform microbial data into images, incorporating phylogenetic structure and abundance similarity. 
This image-based representation enhances data visualization and analysis. Moreover, SAMBA employs a fast Fourier transform (FFT) with adjustable thresholding to smooth the images,
reducing noise and accentuating meaningful information. Various distance metrics, such as SAM and MSE, can be applied to the processed images.

## How to apply SAMBA
SAMBA's code is available at this [GitHub](https://github.com/oshritshtossel/SAMBA/new/master?readme=1) as well as [PyPi](https://pypi.org/project/samba-metric/).

### SAMBA's GitHub
There is an example in example_use.py.
You should follow the following steps:
1. Load the raw ASVs table in the following format: the first column is named "ID",
   each row represents a sample and each column represents an ASV. The last row 
   contains the taxonomy information, named "taxonomy".
   
    ```
    df = pd.read_csv("example_data/for_preprocess.csv")
    ```

   
2. Apply the MIPMLP with the defaulting parameters (see [MIPMLP](https://pypi.org/project/MIPMLP/) for more explanations).

    ```
    processed = MIPMLP.preprocess(df)
    ```
    
3. micro2matrix (translate microbiome into matrix according to [iMic](https://doi.org/10.1080/19490976.2023.2224474), and save the images in a prepared folder
   
   ```
    folder = "example_data/2D_images"
    micro2matrix(processed, folder, save=True)
    ```
    
4. Calculate the distance matrix according to SAMBA
   One can choose the FFT cutoff (in the range of [0,1]), and the final metric (one of "sam","mse","d1","d2","d3").
   
   ```
    DM = build_SAMBA_distance_matrix(folder,cutoff=CUTOFF,metric=METRIC)
    ```
5. If a tag table is available. One can load the tag file and visualize the data according to the SAMBA metric by the plot_umap function.
   "example_data" is the folder path for saving.
      ```
     tag = pd.read_csv("example_data/tag.csv",index_col=0)
     plot_umap(DM,tag,"example_data")
    ```


### SAMBA's PyPi
1. Install the SAMBA package

```
pip install samba-metric
```
2. Apply the MIPMLP with the default parameters
   
```
processed = MIPMLP.preprocess(df)
```
or -  load a MIPMLP processed data directly.

```
processed = pd.read_csv("example_data.csv",index_col=0)

```

4. Apply SAMBA on a MIPMLP processed data:
```
from samba import *
# If the tag is available
tag = pd.read_csv("example_data/tag.csv",index_col=0)

folder = "FOLDER_NAME"
array_of_imgs,bact_names, ordered_df = micro2matrix(processed, folder, save=False)

# Calculate the distance matrix according to SAMBA
DM = build_SAMBA_distance_matrix(folder,imgs=array_of_imgs,ordered_df=ordered_df)
DM.to_csv(f"{folder}/samba_dists.csv")
```
5. If a tag table is available. One can load the tag file and visualize the data according to the SAMBA metric by the plot_umap function.
   "example_data" is the folder path for saving.
```
tag = pd.read_csv("example_data/tag.csv",index_col=0)
plot_umap(DM,tag,"example_data")
```
    
    
