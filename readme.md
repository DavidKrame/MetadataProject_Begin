## General information
`TS1.csv` and `TS3.csv` are respectively examples of **csv files** containing 1 time series and then 3 series that can be supplied to the code named `code_principal.py` for preprocessing.  
The result of the last treatment will be automatically saved in the `datas_quartiles_npy` folder in [npy format](https://fileinfo.com/extension/npy).  
The **datas_npy** folder contains the data from the original csv file in npy format and the **datas_chunked_npy** folder contains the same data rearranged according to the window considered. These are therefore intermediate folders.  
All these files are generated automatically

## Usage
This code is used by passing as parameters the **name of the CSV** file containing the time series data, the **window size**, the size of the desired prediction **horizon** and the size of the part to be converted into quartiles (**lag**).  
  
**__Example :__**  
We can type in terminal  
```shell
python code_principal.py --dataset-name TS1.csv --window-length 10 --horizon 2 --lag 8
```  
  
If the parameters are not provided, the default is the **TS3.csv** file, a window size of **6**, a lag of **5** (minimum value) and a horizon of **1**.