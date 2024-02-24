#%% Imports
import pandas as pd
import os
import jgtml as jml
from jgtml import calc as jtc


import tlid
tlid_tag = tlid.get_minutes()


crop_end_dt=None;crop_start_dt=None

I_raw = os.getenv('I')
T_raw = os.getenv('T')

if I_raw is None or T_raw is None:
    raise ValueError("Environment variables 'I' and 'T' must be set.")

instruments = I_raw.split(',')
timeframes = T_raw.split(',')


#def pov_target_calculation_n_output240222(indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t


print("Processing", I_raw, T_raw)
for i in instruments:
    for t in timeframes:
        print("Processing POV:" , i, t)
        #pov_target_calculation_n_output240222(calculate_target_variable_min_max, indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)
        #jml.pov_calc_targets(indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)
        #pov_target_calculation_n_output240222(calculate_target_variable_min_max, indir_cds, outdir_tmx, crop_start_dt, crop_end_dt, i, t)
        jml.calc_target_to_file()



