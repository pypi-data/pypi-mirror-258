#%% Imports
import pandas as pd
import os


#%% Input/Output directories
default_jgtpy_data_full= 'full/data'
default_jgtpy_data_full= '/var/lib/jgt/full/data'
data_dir_full = os.getenv('JGTPY_DATA_FULL', default_jgtpy_data_full)
indir_cds = os.path.join(data_dir_full, 'cds')
outdir_tmx = os.path.join(data_dir_full, 'targets', 'mx') #@STCIssue Hardcoded path future JGTPY_DATA_FULL/.../mx

# Create directory if it does not exist
if not os.path.exists(outdir_tmx):
    os.makedirs(outdir_tmx)


import tlid
tlid_tag = tlid.get_minutes()

#%% Read Data
crop_start_dt = "2010-01-01"
crop_end_dt = "2023-10-12"

crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

instruments = I_raw.split(',')
timeframes = T_raw.split(',')


def pov_target_calculation_n_output240222(indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t,pipsize=-1):
    ifn = i.replace('/','-')
        #read instrument prop
    iprop=pds.get_instrument_properties(i)
    pipsize = iprop['pipsize']
    nb_decimal = len(str(pipsize).split('.')[1]) if '.' in str(pipsize) else len(str(pipsize))
    rounder = nb_decimal

        # Possible crop of the dataframe to a specific date range

        # Read the source data of already calculated CDS
    df_cds_source = pd.read_csv(f'{indir_cds}/{ifn}_{t}.csv', index_col=0, parse_dates=True)

    df_result_tmx = calculate_target_variable_min_max(df_cds_source, crop_end_dt, crop_start_dt, rounder=rounder, pipsize=pipsize)

        # Save the result to a csv file
    output_all_cols_fn = f'{outdir_tmx}/{ifn}_{t}.csv'
    try:
        df_result_tmx.to_csv(output_all_cols_fn, index=True)
        print(f"Saved to {output_all_cols_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_all_cols_fn}: {str(e)}")

    keeping_columns = ['Low', 'fdbs', 'fdbb', 'tmax', 'tmin', 'p', 'l', 'target']
    sel = df_result_tmx[keeping_columns].copy()
    sel = sel[(sel['p'] != 0) | (sel['l'] != 0)]
    
    output_sel_cols_fn = f'{outdir_tmx}/{ifn}_{t}_sel.csv'
    try:
        sel.to_csv(output_sel_cols_fn, index=True)
        print(f"Saved to {output_sel_cols_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_sel_cols_fn}: {str(e)}")

    keeping_columns_sel2 = ['Open', 'High', 'Low', 'Close', 'fdbs', 'fdbb', 'target']
    df_selection2 = df_result_tmx[keeping_columns_sel2].copy()
    df_selection2['target'] = df_selection2['target'].round(rounder)
    df_selection2 = df_selection2[(df_selection2['target'] != 0)]
    
    output_tnd_targetNdata_fn = f'{outdir_tmx}/{ifn}_{t}_tnd.csv'
    try:
        df_selection2.to_csv(output_tnd_targetNdata_fn, index=True)
        print(f"Saved to {output_tnd_targetNdata_fn}")
    except Exception as e:
        print(f"Error occurred while saving to {output_tnd_targetNdata_fn}: {str(e)}")
    
    reporting(df_selection2, ifn, t, pipsize,tlid_tag)


def reporting(df_selection2, ifn, t, pipsize,tlid_tag):

    report_file = f"{default_jgtpy_data_full}/report-calc-{tlid_tag}.txt"
    
    with open(report_file, "a") as f:
        f.write(f"--- {ifn}_{t} ---\n")
        f.write(f"Sum of target: {df_selection2['target'].sum()}\n\n")
        #f.write(f" (rounded): {(df_selection2['target'].sum()).round(2)}\n\n")
    



print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        pov_target_calculation_n_output240222(calculate_target_variable_min_max, indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)



