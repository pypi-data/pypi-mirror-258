import argparse
from pathlib import Path
import pandas as pd
from scipy.stats import spearmanr
import numpy as np
from statsmodels.stats.multitest import multipletests
import logging
import sys
# Create a logger object
logger = logging.getLogger('my_logger')

# Create a formatter object with the desired log format
log_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Create a handler and add the formatter to it
console_handler = logging.StreamHandler()  # Output logs to the console
console_handler.setFormatter(log_format)

# Add the handler to the logger object
logger.addHandler(console_handler)

# Customize logger.info function to include status
def custom_log(level, msg, *args, status=None):
    if status:
        msg = f'({status}) {msg}'  # Concatenate the message and status
    logger.log(level, msg, *args)

# Bind the custom_log function to the logger object for different log levels
logger.info = lambda msg, *args, status=None: custom_log(logging.INFO, msg, *args, status=status)
logger.warning = lambda msg, *args, status=None: custom_log(logging.WARNING, msg, *args, status=status)
logger.error = lambda msg, *args, status=None: custom_log(logging.ERROR, msg, *args, status=status)
logger.debug = lambda msg, *args, status=None: custom_log(logging.DEBUG, msg, *args, status=status)


def read_kraken_reports(files, sample_names=None, study_name=None, min_reads=2, min_uniq=2):
    """
    Read Kraken reports from files and return a DataFrame with the data.

    Parameters:
        files (list): List of file paths containing Kraken reports.
        sample_names (list, optional): List of sample names corresponding to the input files. Default is None.
        study_name (str, optional): Name of the study. Default is None.
        min_reads (int, optional): Minimum number of reads per taxon. Default is 2.
        min_uniq (int, optional): Minimum number of unique sequences per taxon. Default is 2.
        path (str, optional): Path to the files. Default is '.'.

    Returns:
        pd.DataFrame: DataFrame containing the combined data from Kraken reports.
    """
    if sample_names is None:
        sample_names = [f.stem for f in files]  # Use file names without extension as sample names
    if study_name is None:
        study_name = [None] * len(files)

    df = []
    for i, f in enumerate(files):
        try:
            # tmp = pd.read_csv(f, sep="\t", names=['fragments', 'assigned', 'minimizers', 'uniqminimizers', 'ncbi_taxa',
            #                                     'scientific name', 'rank', 'dup', 'max_cov', 'max_minimizers', 'max_uniqminimizers',
            #                                     'kmer_consistency', 'entropy', 'dust_score', 'max_contig', 'mean_contig',
            #                                     'corr_ub_counts', 'p_value_ub_counts', 'corr_kmer_counts', 'p_value_kmer_counts',
            #                                     'superkingdom'])
            tmp = pd.read_csv(f, sep="\t")
        except pd.errors.EmptyDataError:
            logger.warning(f"Empty file: {f}. Skipping this file.")
            continue

        tmp['scientific name'] = tmp['scientific name'].str.strip()
        tmp_df = pd.DataFrame({
            'study': study_name[i],
            'sample': sample_names[i],
            'rank': tmp['classification_rank'],
            'ncbi_taxa': tmp['ncbi_taxa'],
            'main_level_taxid': tmp['main_level_taxid'],
            'sci_name': tmp['scientific name'],
            'reads': tmp['fragments'],
            'minimizers': tmp['max_minimizers'],
            'uniqminimizers': tmp['max_uniqminimizers'],
            'classification_rank': tmp['classification_rank'],
            'genus_level_taxid': tmp['genus_level_taxid'],
            'superkingdom': tmp['superkingdom']
        })

        df.append(tmp_df)

    df = pd.concat(df, ignore_index=True)
    logger.info(f"Successfully read {len(df)} records from {len(files)} files.",status="summary")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                        type=str,
                        help='One or more file path containing custom style Kraken reports')
    parser.add_argument('--out_path',
                        type=str,
                        help='Result output path')
    # parser.add_argument('--sample_name',
    #                     type=str,
    #                     help='One sample name corresponding to the input files')
    parser.add_argument('--study_name',
                        type=str,
                        help='Name of the study')
    parser.add_argument('--min_reads',
                        type=int,
                        default=2,
                        help='Minimum number of reads per taxon')
    parser.add_argument('--min_uniq',
                        type=int,
                        default=2,
                        help='Minimum number of unique sequences per taxon')
    # parser.add_argument('--cell_line',
    #                     type=str,
    #                     help='Cell line path')
    parser.add_argument('--raw_file_list', nargs='+',help='sample raw file list path')
    parser.add_argument('--file_list', nargs='+',help='sample denosing file list path')
    parser.add_argument('--log_file', dest='log_file', 
        required=True, default='logfile_download_genomes.txt',
        help="File to write the log to")
    parser.add_argument('--verbose', action='store_true', help='Detailed print')
    
    args=parser.parse_args()
    
    # Set log level based on command line arguments
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Create a file handler and add the formatter to it
    file_handler = logging.FileHandler(args.log_file)  # Output logs to the specified file
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)


    if args.path:
        path = args.path
        path = Path(path)
        files = list(path.glob('**/*_krak_sample_denosing.txt'))  
    elif args.file_list:
        # Convert the file paths to Path objects
        files = [Path(file_path) for file_path in args.file_list]
    else:
        raise ValueError("Either --path or --file_list must be provided")

    out_path = args.out_path
    # sample_name = args.sample_name
    study_name = args.study_name
    min_reads = args.min_reads
    min_uniq = args.min_uniq
    # celline_file = args.cell_line


    logger.info('Reading kraken sample denosing results', status='run')
    # Read the all krak report
    kraken_reports_all = read_kraken_reports(files, sample_names=None,study_name=study_name, min_reads=min_reads, min_uniq=min_uniq)


    logger.info('Finishing reading kraken sample denosing results', status='complete')
    logger.info('Checking sample number', status='run')

    # 1. Check number of samples
    if len(kraken_reports_all['sample'].unique()) > 5:
        logger.info('Calculating correlations and p-values', status='run')

        kraken_reports_all_species = kraken_reports_all.copy()

        kraken_reports_all_species['taxa_reads'] = np.where(
            kraken_reports_all_species['classification_rank'].str.startswith('S'),
            kraken_reports_all_species.groupby(['sample','main_level_taxid'])['reads'].transform('sum'),
            kraken_reports_all_species.groupby(['sample','genus_level_taxid'])['reads'].transform('sum')
        )
        kraken_reports_all_species['taxa_uniqminimizers'] = np.where(
            kraken_reports_all_species['classification_rank'].str.startswith('S'),
            kraken_reports_all_species.groupby(['sample','main_level_taxid'])['uniqminimizers'].transform('sum'),
            kraken_reports_all_species.groupby(['sample','genus_level_taxid'])['uniqminimizers'].transform('sum')
        )
        kraken_reports_all_species['taxa_minimizers'] = np.where(
            kraken_reports_all_species['classification_rank'].str.startswith('S'),
            kraken_reports_all_species.groupby(['sample','main_level_taxid'])['minimizers'].transform('sum'),
            kraken_reports_all_species.groupby(['sample','genus_level_taxid'])['minimizers'].transform('sum')
        )


        # kraken_reports_all_species = kraken_reports_all.copy().groupby(['sample','species_level_taxid'], as_index=False).agg(
        #     {'reads':'sum',
        #     'minimizers': 'sum',
        #     'uniqminimizers': 'sum'}
        #     ).drop_duplicates()

        kraken_reports_all_species = kraken_reports_all_species[~kraken_reports_all_species.duplicated(subset=['sample', 'main_level_taxid'],  keep='first')]
        # 2. Calculate correlations and p-values
        # Group
        grouped = kraken_reports_all_species.groupby('main_level_taxid') 
        for name, group in grouped:

            if len(group) > 1:

                corr_reads_min, pval_reads_min = spearmanr(group['taxa_reads'], group['taxa_minimizers'])  
                corr_reads_uniq, pval_reads_uniq = spearmanr(group['taxa_reads'], group['taxa_uniqminimizers'])
                corr_min_uniq, pval_min_uniq = spearmanr(group['taxa_minimizers'], group['taxa_uniqminimizers'])

                # 直接赋值
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_reads_min'] = corr_reads_min
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_reads_min'] = pval_reads_min
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_reads_uniq'] = corr_reads_uniq 
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_reads_uniq'] = pval_reads_uniq
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_min_uniq'] = corr_min_uniq
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_min_uniq'] = pval_min_uniq


            else:
                # 处理只有一行的情况
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_reads_min'] = np.nan
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_reads_min'] = np.nan
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_reads_uniq'] = np.nan
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_reads_uniq'] = np.nan
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'corr_min_uniq'] = np.nan
                kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid'] == name, 'pval_min_uniq'] = np.nan


        # Log the completion of correlation and p-value calculations
        logger.info('Correlation and p-value calculations completed', status='complete')

        # # Perform multiple comparison correction (Benjamini-Hochberg method)
        # # Columns that require correction
        # pval_columns = ['pval_reads_min', 'pval_reads_uniq', 'pval_min_uniq']

        # # Perform correction
        # for col in pval_columns:

        #     if kraken_reports_all_species[col].max() < 1:
        #         _, pvals_corrected, _, _ = multipletests(kraken_reports_all_species[col], alpha=0.05, method='fdr_bh')
        #         kraken_reports_all_species[col] = pvals_corrected
        #     else:
        #         # 不进行处理
        #         pass

        # Log the completion of multiple comparison correction
        # logger.info(f'Multiple comparison correction completed', status='complete')

        # kraken_reports_all_species = kraken_reports_all_species[
        # ((kraken_reports_all_species['corr_reads_min'] > 0) &
        # (kraken_reports_all_species['pval_reads_min'] < 0.05) &
        # (kraken_reports_all_species['corr_reads_uniq'] > 0) &
        # (kraken_reports_all_species['pval_reads_uniq'] < 0.05) &
        # (kraken_reports_all_species['corr_min_uniq'] > 0) &
        # (kraken_reports_all_species['pval_min_uniq'] < 0.05))  |
        # (
        #     (kraken_reports_all_species['corr_reads_min']>0) &
        #     (kraken_reports_all_species['pval_reads_min'].isna()) &
        #     (kraken_reports_all_species['corr_reads_uniq']>0) &
        #     (kraken_reports_all_species['pval_reads_uniq'].isna()) &
        #     (kraken_reports_all_species['corr_min_uniq']>0) &
        #     (kraken_reports_all_species['pval_min_uniq'].isna())
        # )
        # |
        # ((kraken_reports_all_species['corr_reads_min'] > 0) &
        # (kraken_reports_all_species['pval_reads_min'] < 0.05) &
        # (kraken_reports_all_species['corr_reads_uniq'] > 0.2) &
        # (kraken_reports_all_species['corr_min_uniq'] > 0.2) )

        kraken_reports_all_species = kraken_reports_all_species[
            ~(
                ((kraken_reports_all_species['corr_reads_min'] < 0) &
                (kraken_reports_all_species['pval_reads_min'] > 0.05) &
                (kraken_reports_all_species['corr_reads_uniq'] < 0) &
                (kraken_reports_all_species['pval_reads_uniq'] > 0.05) &
                (kraken_reports_all_species['corr_min_uniq'] < 0) &
                (kraken_reports_all_species['pval_min_uniq'] > 0.05))  |
                (
                    (kraken_reports_all_species['corr_reads_min'] < 0) &
                    (kraken_reports_all_species['pval_reads_min'].isna()) &
                    (kraken_reports_all_species['corr_reads_uniq'] <0) &
                    (kraken_reports_all_species['pval_reads_uniq'].isna()) &
                    (kraken_reports_all_species['corr_min_uniq'] <0) &
                    (kraken_reports_all_species['pval_min_uniq'].isna())
                )
            )
        ]

        # (
        #     (kraken_reports_all_species['corr_reads_min'].isna()) &
        #     (kraken_reports_all_species['pval_reads_min'].isna()) &
        #     (kraken_reports_all_species['corr_reads_uniq'].isna()) &
        #     (kraken_reports_all_species['pval_reads_uniq'].isna()) &
        #     (kraken_reports_all_species['corr_min_uniq'].isna()) &
        #     (kraken_reports_all_species['pval_min_uniq'].isna())
        # )

        # kraken_reports_all_species = kraken_reports_all_species.loc[kraken_reports_all_species['main_level_taxid']==1763]
        # print(kraken_reports_all_species)

        # logger.info(f'Calculating quantile with containments', status='run')

        # cell_lines = pd.read_csv(celline_file,sep="\t")
        # # remove space
        # cell_lines['name'] = cell_lines['name'].str.strip() 
        # # replace space
        # cell_lines['name'] = cell_lines['name'].str.replace(' ', '_')
        # qtile = 0.99
        # quantiles = cell_lines[['name', 'taxid']]

        # quantiles['CLrpmm_cellline'] = cell_lines.groupby('name')['rpmm'].transform(lambda x: 10 ** np.quantile(np.log10(x),qtile, interpolation='midpoint'))
        # quantiles= quantiles.drop_duplicates(subset=['name', 'taxid'], keep='first')
        candidate_species_all = kraken_reports_all[kraken_reports_all['main_level_taxid'].isin(kraken_reports_all_species["main_level_taxid"])]
        # candidate_species_all = candidate_species_all.loc[candidate_species_all["classification_rank"] == "S"]
        candidate_species_all = kraken_reports_all[kraken_reports_all['classification_rank'].str.startswith('S')]        
        # candidate_species_all = kraken_reports_all_species[['rank', 'species_level_taxid', 'sci_name']]
        # candidate_species_all = candidate_species_all.drop_duplicates()
        # candidate_species_all = candidate_species_all[['ncbi_taxa','rank', 'species_level_taxid', 'sci_name']]
        # candidate_species_all = candidate_species_all.drop_duplicates(subset='species_level_taxid')

        # num_unique_species = len(candidate_species_all['species_level_taxid'].unique())
        # logger.info(f"Number of species after filtering: {num_unique_species}", status='summary')

        # raw_files = [Path(file_path) for file_path in args.raw_file_list]

        # kraken_reports_raw_all = read_kraken_reports(raw_files, sample_names=None,study_name=study_name, min_reads=min_reads, min_uniq=min_uniq)
        # kraken_reports_raw_all['reads'] = kraken_reports_raw_all['reads'].astype(int)
        # kraken_reports_raw_all['sum_reads'] = kraken_reports_raw_all.groupby(['ncbi_taxa'])['reads'].transform('sum')

        # kraken_reports_raw_all_interest = kraken_reports_raw_all[kraken_reports_raw_all['species_level_taxid'].isin(candidate_species_all["species_level_taxid"])]

        # kraken_reports_raw_all_interest_sorted = kraken_reports_raw_all_interest.sort_values(by=['species_level_taxid', 'sum_reads'], ascending=[True, False])
        # # 基于 'ncbi_taxa' 列去除重复行
        # kraken_reports_raw_all_interest_sorted = kraken_reports_raw_all_interest_sorted.drop_duplicates(subset='ncbi_taxa')
        # print(kraken_reports_raw_all_interest_sorted[kraken_reports_raw_all_interest_sorted['species_level_taxid']==851])
        # taxid_counts = {}
        # candidate_data = []
                            
        # for index, row in candidate_species_all.iterrows():
        #     ncbi_taxa = row['ncbi_taxa']
        #     rank = row['rank']
        #     species_level_taxid = row['species_level_taxid']
        #     sci_name = row['sci_name']
        #     if rank == "S":
        #         tax_type = "strong species"
        #         if species_level_taxid not in taxid_counts:
        #             taxid_counts[species_level_taxid] = 1
        #         taxid_counts[species_level_taxid] += 1
        #     else:
        #         tax_type = "strong subspecies"
        #         if species_level_taxid not in taxid_counts:
        #             taxid_counts[species_level_taxid] = 1
        #         taxid_counts[species_level_taxid] += 1

        #     if taxid_counts[species_level_taxid] >= 5:
        #         continue
        #     candidate_data.append([
        #                             ncbi_taxa,species_level_taxid, tax_type,rank,sci_name
        #                             ])
            
        # for index, row in kraken_reports_raw_all_interest_sorted.iterrows():
        #     ncbi_taxa = row['ncbi_taxa']
        #     rank = row['rank']
        #     species_level_taxid = row['species_level_taxid']
        #     sci_name = row['sci_name']
        #     if rank == "S":
        #         continue
        #     else:
        #         tax_type = "subspecies"
        #         print(ncbi_taxa)
        #         taxid_counts[species_level_taxid] += 1
        #     print("count")
        #     print(taxid_counts[species_level_taxid])
        #     if taxid_counts[species_level_taxid] >= 5:
        #         continue
        #     candidate_data.append([
        #                             ncbi_taxa,species_level_taxid, tax_type,rank,sci_name
        #                             ])

        # df_columns = [
        #     "ncbi_taxa","species_level_taxid", "tax_type","rank","sci_name"
        # ]

        # candidate_data_df = pd.DataFrame(candidate_data, columns=df_columns)
        # logger.info(f'Saving the result', status='run')
        # # Save the filtered data to CSV
        # candidate_data_df.to_csv(out_path, sep='\t',index=False)
        # logger.info(f'Finishing saving the result', status='complete')
        # Log the 
        # logger.info(f'Could not caulate correlation and distrubtion since sample less than 5', status='complete')
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].astype(str)
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].str.replace('/.*','')
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].str.replace('_krak_sample_denosing', '')
        # kraken_reports_specific = kraken_reports_all_species.loc[kraken_reports_all_species['sample'] == sample_name]
        # filter_kraken_reports_specific = kraken_reports_specific.copy()

        # logger.info(f'Saving the result', status='run')
        # # Save the filtered data to CSV
        # filter_kraken_reports_specific.to_csv(out_path, sep='\t', index=False)

        candidate_species_all.to_csv(args.out_path, sep='\t', index=False)
    else:
        # # Log the 
        # logger.info(f'Could not caulate correlation and distrubtion since sample less than 4', status='complete')
        # candidate_species_all = kraken_reports_all[['ncbi_taxa','rank', 'species_level_taxid', 'sci_name']]
        # candidate_species_all = candidate_species_all.drop_duplicates()
        # num_unique_species = len(candidate_species_all['ncbi_taxa'].unique())
        # logger.info(f"Number of species after filtering: {num_unique_species}", status='summary')

        # logger.info(f'Saving the result', status='run')
        # # Save the filtered data to CSV
        # candidate_species_all.to_csv(out_path, sep='\t', index=False)
        # logger.info(f'Finishing saving the result', status='complete')
        # kraken_reports_all_species = kraken_reports_all.copy()
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].astype(str)
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].str.replace('/.*','')
        # kraken_reports_all_species['sample'] = kraken_reports_all_species['sample'].str.replace('_krak_sample_denosing', '')
        # kraken_reports_specific = kraken_reports_all_species.loc[kraken_reports_all_species['sample'] == sample_name]
        # filter_kraken_reports_specific = kraken_reports_specific.copy()
        kraken_reports_all_species = kraken_reports_all.copy()

        # candidate_species_all = kraken_reports_all.loc[kraken_reports_all["classification_rank"] == "S"]
        candidate_species_all = kraken_reports_all[kraken_reports_all['classification_rank'].str.startswith('S')]
        logger.info(f'Saving the result', status='run')
        # Save the filtered data to CSV
        # filter_kraken_reports_specific.to_csv(out_path, sep='\t', index=False)
        candidate_species_all.to_csv(args.out_path, sep='\t', index=False)

if __name__ == "__main__":
    main()