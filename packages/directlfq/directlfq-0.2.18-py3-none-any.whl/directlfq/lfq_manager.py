# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbdev_nbs/01_lfq_manager.ipynb.

# %% auto 0
__all__ = ['run_lfq', 'prepare_input_filename', 'get_outfile_basename', 'save_protein_df', 'save_ion_df', 'save_run_config']

# %% ../nbdev_nbs/01_lfq_manager.ipynb 1
import directlfq.config as config
import directlfq.normalization as lfqnorm
import directlfq.protein_intensity_estimation as lfqprot_estimation
import directlfq.utils as lfqutils
import pandas as pd
import directlfq
import os
import logging
import warnings

warnings.filterwarnings(action='once')
config.setup_logging()

LOGGER = logging.getLogger(__name__)


def run_lfq(input_file,  columns_to_add = [], selected_proteins_file :str = None, mq_protein_groups_txt = None, min_nonan = 1, input_type_to_use = None, maximum_number_of_quadratic_ions_to_use_per_protein = 10, 
number_of_quadratic_samples = 50, num_cores = None, filename_suffix = "", deactivate_normalization = False, filter_dict = None, log_processed_proteins = True, protein_id = 'protein', quant_id = 'ion'
,compile_normalized_ion_table = True):
    """Run the directLFQ pipeline on a given input file. The input file is expected to contain ion intensities. The output is a table containing protein intensities.

    Args:
        input_file (_type_): the input file containing the ion intensities. Usually the output of a search engine.
        columns_to_add (list, optional): additional columns to add to the LFQ intensity output table. They are extraced from the input file. Defaults to [].
        selected_proteins_file (str, optional): if you want to perform normalization only on a subset of proteins, you can pass a .txt file containing the protein IDs, separeted by line breaks. No header expected. Defaults to None.
        mq_protein_groups_txt (_type_, optional): In the case of using MaxQuant data, the proteinGroups.txt table is needed in order to map IDs analogous to MaxQuant. Adding this table improves protein mapping, but is not necessary. Defaults to None.
        min_nonan (int, optional): Min number of ion intensities necessary in order to derive a protein intensity. Increasing the number results in more reliable protein quantification at the cost of losing IDs. Defaults to 1.
        input_type_to_use (_type_, optional): If you want to parse data from the input file in a differing way than specified in the defaults (e.g. extracting MS1 intensities only from a DIANN file), you can name the parsing protocol to be used. The parsing protocols are defined in directlfq/configs/intable_configs.yaml Defaults to None.
        maximum_number_of_quadratic_ions_to_use_per_protein (int, optional): How many ions are used to create the anchor intensity trace (see paper). Increasing might marginally increase performance at the cost of runtime. Defaults to 10.
        number_of_quadratic_samples (int, optional): How many samples are are used to create the anchor intensity trace (see paper). Increasing might marginally increase performance at the cost of runtime. Defaults to 50.
        num_cores (_type_, optional): Num cores to use. Maximum feasible number utilized if set to None. Defaults to None.
    """
    config.set_global_protein_and_ion_id(protein_id=protein_id, quant_id=quant_id)
    config.set_log_processed_proteins(log_processed_proteins=log_processed_proteins)
    config.set_compile_normalized_ion_table(compile_normalized_ion_table= compile_normalized_ion_table)

    LOGGER.info("Starting directLFQ analysis.")
    input_file = prepare_input_filename(input_file)
    filter_dict = load_filter_dict_if_given_as_yaml(filter_dict)
    input_file = lfqutils.add_mq_protein_group_ids_if_applicable_and_obtain_annotated_file(input_file, input_type_to_use,mq_protein_groups_txt, columns_to_add)
    input_df = lfqutils.import_data(input_file=input_file, input_type_to_use=input_type_to_use, filter_dict=filter_dict)

    input_df = lfqutils.sort_input_df_by_protein_id(input_df)
    input_df = lfqutils.index_and_log_transform_input_df(input_df)
    input_df = lfqutils.remove_allnan_rows_input_df(input_df)
    
    if not deactivate_normalization:
        LOGGER.info("Performing sample normalization.")
        input_df = lfqnorm.NormalizationManagerSamplesOnSelectedProteins(input_df, num_samples_quadratic=number_of_quadratic_samples, selected_proteins_file=selected_proteins_file).complete_dataframe
    
    LOGGER.info("Estimating lfq intensities.")
    protein_df, ion_df = lfqprot_estimation.estimate_protein_intensities(input_df,min_nonan=min_nonan,num_samples_quadratic=maximum_number_of_quadratic_ions_to_use_per_protein, num_cores = num_cores)
    try:
        protein_df = lfqutils.add_columns_to_lfq_results_table(protein_df, input_file, columns_to_add)
    except:
        LOGGER.info("Could not add additional columns to protein table, printing without additional columns.")
    
    LOGGER.info("Writing results files.")
    outfile_basename = get_outfile_basename(input_file, input_type_to_use, selected_proteins_file, deactivate_normalization,filename_suffix)
    save_run_config(outfile_basename, locals())
    save_protein_df(protein_df,outfile_basename)
    
    if config.COMPILE_NORMALIZED_ION_TABLE:
        save_ion_df(ion_df,outfile_basename)
    
    LOGGER.info("Analysis finished!")

def load_filter_dict_if_given_as_yaml(filter_dict):
    if os.path.isfile(str(filter_dict)):
        #check if filter_dict is a path to a yaml file
        if filter_dict.endswith(".yaml"):
            filter_dict = lfqutils.load_config(filter_dict)
            return filter_dict
    else:
        return filter_dict

def prepare_input_filename(input_file):
    input_file = fr"{input_file}".replace("\ ", " ").rstrip() #replace escaped spaces with normal spaces and remove trailing whitespace
    return input_file

def get_outfile_basename(input_file, input_type_to_use, selected_proteins_file, deactivate_normalization,filename_suffix):
    outfile_basename = input_file
    outfile_basename += "" if input_type_to_use is None else f".{input_type_to_use}"
    outfile_basename += ".selected_proteins" if selected_proteins_file is not None else ""
    outfile_basename += ".no_norm" if deactivate_normalization else ""
    outfile_basename += filename_suffix
    return outfile_basename

def save_protein_df(protein_df, outfile_basename):
    protein_df.to_csv(f"{outfile_basename}.protein_intensities.tsv", sep = "\t", index = None)

def save_ion_df(ion_df, outfile_basename):
    ion_df.to_csv(f"{outfile_basename}.ion_intensities.tsv", sep = "\t")


def save_run_config(outfile_basename, kwargs):
    simple_kwargs = {k: v for k, v in kwargs.items() if is_simple_data(v)}
    try:
        df_configs = pd.DataFrame.from_dict(simple_kwargs, orient='index', columns=['value'])
        # Add row with directlfq version
        df_configs.loc["directlfq_version"] = directlfq.__version__
        df_configs.to_csv(f"{outfile_basename}.run_config.tsv", sep="\t")
    except Exception as e:
        LOGGER.error(f"Could not save run config: {e}")

def is_simple_data(value):
    """Check if the data is a simple data type."""
    return isinstance(value, (int, float, str, bool, type(None), list))


