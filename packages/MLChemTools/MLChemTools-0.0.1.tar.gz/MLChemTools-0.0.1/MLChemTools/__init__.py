

"""# Calculate RDKit descriptors"""

import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
from rdkit.ML.Descriptors import MoleculeDescriptors
from padelpy import padeldescriptor
from sklearn.preprocessing import StandardScaler
from lazypredict.Supervised import LazyClassifier
from lazypredict.Supervised import LazyRegressor
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, ExtraTreesClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, confusion_matrix, classification_report
from chembl_webresource_client.new_client import new_client
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import glob
from pandas.plotting import scatter_matrix
from imblearn.over_sampling import SMOTE



def process_and_calculate_descriptors(input_file, output_file, smiles_column):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Add a new column 'mol' to store the RDKit molecule objects
    df['mol'] = df[smiles_column].apply(Chem.MolFromSmiles)

    # Remove duplicates based on the specified SMILES column
    df.drop_duplicates(subset=smiles_column, inplace=True)

    # Calculate RDKit descriptors for each molecule
    calc = MoleculeDescriptors.MolecularDescriptorCalculator([x[0] for x in Descriptors._descList])
    desc_names = calc.GetDescriptorNames()

    # Calculate descriptors and add them to the DataFrame
    Mol_descriptors = [calc.CalcDescriptors(Chem.AddHs(mol)) for mol in df['mol']]
    df_with_descriptors = pd.concat([df.reset_index(drop=True), pd.DataFrame(Mol_descriptors, columns=desc_names)], axis=1)

    # Save the cleaned data with descriptors to a new CSV file
    df_with_descriptors.to_csv(output_file, index=False)
    print("yoyr data with Rdkit is saved in csv file")

    # Display the DataFrame with calculated descriptors
    display(df_with_descriptors)
    return



"""# Calculate pubchem fingerprint"""




def calculate_pubchem_fingerprints(df_unique, smiles_column):

    xml_files = glob.glob("*.xml")
    xml_files.sort()

    FP_list = ['AtomPairs2DCount', 'AtomPairs2D', 'EState', 'CDKextended', 'CDK', 'CDKgraphonly',
               'KlekotaRothCount', 'KlekotaRoth', 'MACCS', 'PubChem', 'SubstructureCount', 'Substructure']

    fp = dict(zip(FP_list, xml_files))
    fingerprint = 'PubChem'
    fingerprint_output_file = f'{fingerprint}.csv'
    fingerprint_descriptortypes = fp[fingerprint]

    df2 = pd.concat([df_unique[smiles_column]], axis=1)
    df2.to_csv('molecule.smi', sep='\t', index=False, header=False)

    padeldescriptor(mol_dir='molecule.smi', d_file=fingerprint_output_file,
                    descriptortypes=fingerprint_descriptortypes, detectaromaticity=True,
                    standardizenitro=True, standardizetautomers=True, threads=2, removesalt=True,
                    log=True, fingerprints=True)

    descriptors = pd.read_csv(fingerprint_output_file)

    return descriptors

def process_and_calculate_pubchem_fingerprints(input_file, output_file, smiles_column):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)
    # Drop rows from 1 to 5 (inclusive)
    df = df.drop(df.index[0:5])
    #df = df.drop([ 'PUBCHEM_ACTIVITY_SCORE', 'PUBCHEM_ACTIVITY_URL', 'PUBCHEM_ASSAYDATA_COMMENT',"PUBCHEM_RESULT_TAG",	"PUBCHEM_SID",	"PUBCHEM_CID","Inhibition",	"Standard Deviation"], axis=1)

    # Remove duplicates based on the specified SMILES column
    df.drop_duplicates(subset=smiles_column, inplace=True)

    # Calculate PubChem fingerprints for each molecule
    pubchem_fingerprints = calculate_pubchem_fingerprints(df, smiles_column)

    # Add the PubChem fingerprints to the DataFrame
    df_with_pubchem_fingerprints = pd.concat([df.reset_index(drop=True), pubchem_fingerprints.reset_index(drop=True)], axis=1)

    # Save the cleaned data with PubChem fingerprints to a new CSV file
    df_with_pubchem_fingerprints.to_csv(output_file, index=False)
    print("your data with PubChem fingerprints is saved")
    display(df_with_pubchem_fingerprints)

    return


"""# calculate lipinski descriptors"""


def calculate_lipinski_descriptors(file_path, smiles_column, verbose=False):
    """
    Calculate Lipinski descriptors for a SMILES column in a CSV file.

    Parameters:
    - file_path (str): Path to the CSV file.
    - smiles_column (str): Name of the SMILES column in the CSV file.
    - verbose (bool, optional): If True, print additional information. Default is False.

    Returns:
    - pd.DataFrame: DataFrame containing Lipinski descriptors for each molecule.
    """

    df = pd.read_csv(file_path)
    smiles_column = smiles_column

    mol_data = []
    for smiles in df[smiles_column]:
        mol = Chem.MolFromSmiles(smiles)
        mol_data.append(mol)

    base_data = np.arange(1, 1)
    i = 0

    for mol in mol_data:
        desc_mol_wt = Descriptors.MolWt(mol)
        desc_mol_logp = Descriptors.MolLogP(mol)
        desc_num_h_donors = Lipinski.NumHDonors(mol)
        desc_num_h_acceptors = Lipinski.NumHAcceptors(mol)

        row = np.array([desc_mol_wt,
                        desc_mol_logp,
                        desc_num_h_donors,
                        desc_num_h_acceptors])

        if i == 0:
            base_data = row
        else:
            base_data = np.vstack([base_data, row])
        i += 1

    column_names = ["MW", "LogP", "NumHDonors", "NumHAcceptors"]
    descriptors = pd.DataFrame(data=base_data, columns=column_names)
    df = pd.concat([df, descriptors], axis=1)
    display(df)

    # Save the concatenated DataFrame to a CSV file
    df.to_csv('output.csv', index=False)  # Change 'output.csv' to your desired output file name
    print("your data with lipinski descriptors is saved")


    return pd.concat([df, descriptors], axis=1)


"""# Calculate Morgan Fingerprint"""

def calculate_morgan_fpts(data):
    Morgan_fpts = []
    for i in data:
        mol = Chem.MolFromSmiles(i)
        fpts =  AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048)
        mfpts = np.array(fpts)
        Morgan_fpts.append(mfpts)
    return np.array(Morgan_fpts)

def process_and_calculate_morgan_fpts(input_file, output_file, smiles_column):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Add a new column 'mol' to store the RDKit molecule objects
    df['mol'] = df[smiles_column].apply(Chem.MolFromSmiles)

    # Remove duplicates based on the specified SMILES column
    df.drop_duplicates(subset=smiles_column, inplace=True)

    # Calculate Morgan fingerprints for each molecule
    morgan_fpts = calculate_morgan_fpts(df[smiles_column])

    # Add the Morgan fingerprints to the DataFrame
    morgan_fpt_names = [f'MorganFpt_{i}' for i in range(morgan_fpts.shape[1])]
    df_with_morgan_fpts = pd.concat([df.reset_index(drop=True), pd.DataFrame(morgan_fpts, columns=morgan_fpt_names)], axis=1)

    # Save the cleaned data with Morgan fingerprints to a new CSV file
    df_with_morgan_fpts.to_csv(output_file, index=False)
    display(df_with_morgan_fpts)
    print("your data with morgan fpts descriptors is saved")


    return


"""# calculate_mordred_descriptors"""


def calculate_mordred_descriptors(smiles_column):
    calc = Calculator(descriptors, ignore_3D=False)

    # Get Mordred descriptors
    mols = [Chem.MolFromSmiles(smi) for smi in smiles_column]
    mordred_descriptors = calc.pandas(mols)

    return mordred_descriptors

def process_and_calculate_mordred_descriptors(input_file, output_file, smiles_column):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Remove duplicates based on the specified SMILES column
    df.drop_duplicates(subset=smiles_column, inplace=True)

    # Calculate Mordred descriptors for each molecule
    mordred_descriptors = calculate_mordred_descriptors(df[smiles_column])

    # Add the Mordred descriptors to the DataFrame
    df_with_mordred_descriptors = pd.concat([df.reset_index(drop=True), mordred_descriptors.reset_index(drop=True)], axis=1)

    # Save the cleaned data with Mordred descriptors to a new CSV file
    df_with_mordred_descriptors.to_csv(output_file, index=False)
    display(df_with_mordred_descriptors)
    print("your data with mordred descriptors is saved")

    return


"""# preprocessing"""

print("""preprocess_csv_1
1- Converts all columns to float (if possible).
2- Applies StandardScaler to numeric columns.
3- Converts specified object columns to numerical codes using cat.codes.
4- Displays unique values in object columns before and after preprocessing.
5- Saves the preprocessed DataFrame to a new CSV file.""")

import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_csv_1(csv_file_path, object_columns):
    print("The preprocess_and_standardize_csv function takes a CSV file path and a list of object columns, attempts to convert columns to float, standardizes numeric columns using StandardScaler, converts specified object columns to numerical codes using cat.codes, and displays unique values in object columns before and after preprocessing, along with the DataFrame before and after preprocessing, ultimately saving the preprocessed DataFrame to a new CSV file prefixed by 'preprocessed_'")
    """The function preprocess_csv_1 takes a CSV file path and a list of object columns as input.
    It loads the CSV file into a pandas DataFrame, displays the DataFrame before preprocessing,
    and then performs the following tasks:

    1- Attempts to convert each column to float, leaving the column as is if the conversion fails.
    2- Applies StandardScaler to numeric columns (columns with data types 'float64' or 'int64') for standardization.
    3- Converts specified object columns to numerical codes using cat.codes.
    4- Displays the unique values in specified object columns before and after preprocessing.
    5- Displays the DataFrame after preprocessing.
    6- Saves the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Print unique values in specified object columns before preprocessing
    for col in object_columns:
        unique_values_before = df[col].unique()
        print(f"\nUnique values in '{col}' before preprocessing: {unique_values_before}")

    # Convert each column to float (if possible)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass  # If conversion to float fails, leave the column as is

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Convert specified object columns using cat.codes
    df[object_columns] = df[object_columns].apply(lambda x: x.astype('category').cat.codes)

    # Display the unique values in specified object columns after preprocessing
    print("\nUnique values in specified object columns after preprocessing:")
    for col in object_columns:
        unique_values_after = df[col].unique()
        print(f"Unique values in '{col}' after preprocessing: {unique_values_after}")

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)
    return


print("""preprocess_csv_2:

1- Converts all columns to float (if possible).
2- Applies StandardScaler to numeric columns.
3- Converts specified object columns to numerical codes using cat.codes if provided.

4- Otherwise, converts all object columns to numerical codes using cat.codes.

5- Displays the DataFrame before and after preprocessing.
6- Saves the preprocessed DataFrame to a new CSV file.
""")


def preprocess_csv_2(csv_file_path, object_columns=None):
    """
  1- Load Data:

Load the CSV file into a pandas DataFrame.
Display Initial DataFrame:

2- Show the DataFrame before any preprocessing.
Convert Columns to Float:

3- Attempt to convert each column to a float type.
If the conversion fails, leave the column as is.
Standardize Numeric Columns:

4- Use StandardScaler to standardize numeric columns (float64 or int64 types).
Convert Object Columns:

5- Convert specified object columns to categorical codes using cat.codes.
If no specific object columns are specified, convert all object columns.
Display Processed DataFrame:

6- Show the DataFrame after preprocessing.
Save Processed DataFrame:

7- Save the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
"""
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Convert each column to float (if possible)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass  # If conversion to float fails, leave the column as is

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Convert specified object columns using cat.codes or all object columns if not specified
    if object_columns is not None:
        df[object_columns] = df[object_columns].apply(lambda x: x.astype('category').cat.codes)
    else:
        object_columns = df.select_dtypes(include=['object']).columns
        df[object_columns] = df[object_columns].apply(lambda x: x.astype('category').cat.codes)

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)


    return

print("""preprocess_csv_3:

1- Converts all columns to float (if possible).
2- Applies StandardScaler to numeric columns.
3- Converts specified object columns to numerical codes using cat.codes if provided.

4- If specified object columns not  provided leave any object columns unchanged.

5- Displays the DataFrame before and after preprocessing.
6- Saves the preprocessed DataFrame to a new CSV file.
""")


def preprocess_csv_3(csv_file_path, object_columns=None):
    """
    Load Data:
    Load the CSV file into a pandas DataFrame.

    Display Initial DataFrame:
    Present the DataFrame before any preprocessing.

    Convert Columns to Float:
    Attempt to convert each column to a float type.
    If the conversion fails, leave the column as is.

    Standardize Numeric Columns:
    Use StandardScaler to standardize numeric columns (float64 or int64 types).

    Convert Object Columns:
    Convert specified object columns to categorical codes using cat.codes.
    If no specific object columns are specified, leave them unchanged.

    Display Processed DataFrame:
    Present the DataFrame after preprocessing.

    Save Processed DataFrame:
    Save the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Convert each column to float (if possible)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass  # If conversion to float fails, leave the column as is

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Convert specified object columns using cat.codes or leave them as is if not specified
    if object_columns is not None:
        df[object_columns] = df[object_columns].apply(lambda x: x.astype('category').cat.codes)

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)

    return

print(""" preprocess_csv_4:

1- Deletes specified columns (if provided).

2- Converts all columns to float (if possible), If the conversion fails, leave the column as is.


3- Applies StandardScaler to numeric columns.


4- Converts specified object columns to numerical codes using cat.codes if provided.

5- If no specific object columns are specified, leave them unchanged.

5- Displays the DataFrame before and after preprocessing.
6- Saves the preprocessed DataFrame to a new CSV file.


""")

import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_csv_4(csv_file_path, object_columns=None, columns_to_delete=None):
    """Load Data:

    Load the CSV file into a pandas DataFrame.

    Display Initial DataFrame:
    Show the DataFrame before any preprocessing.

    Delete Specified Columns:
    If specified, delete the specified columns from the DataFrame.

    Convert Columns to Float:
    Attempt to convert each column to a float type.
    If the conversion fails, leave the column as is.

    Standardize Numeric Columns:
    Use StandardScaler to standardize numeric columns (float64 or int64 types).

    Convert Object Columns:
    Convert specified object columns to categorical codes using cat.codes.
    If no specific object columns are specified, leave them unchanged.

    Display Processed DataFrame:
    Present the DataFrame after preprocessing.

    Save Processed DataFrame:
    Save the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
    """

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Delete specified columns
    if columns_to_delete is not None:
        df.drop(columns=columns_to_delete, inplace=True)

    # Convert each column to float (if possible)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass  # If conversion to float fails, leave the column as is

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Convert specified object columns using cat.codes or leave them as is if not specified
    if object_columns is not None:
        df[object_columns] = df[object_columns].apply(lambda x: x.astype('category').cat.codes)

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)
    return


print("""preprocess_csv_5:

1- Converts columns to float;

2- if conversion fails, it checks if specific columns are specified for conversion using cat.codes.

3- If specified, convert the object columns to categorical codes using cat.codes.

4- If not specified, delete the columns that cannot be converted to float or using cat.codes.

5- Applies StandardScaler to numeric columns.
6- Displays the DataFrame before and after preprocessing.
7- Saves the preprocessed DataFrame to a new CSV file.
8- Identifies and displays columns deleted from the original DataFrame during the conversion.


""")

def preprocess_csv_5(csv_file_path, object_columns=None):
    """
Load Data:

Load the CSV file into a pandas DataFrame.
Display Initial DataFrame:

Present the DataFrame before any preprocessing.
Save Original DataFrame:

Create a copy of the original DataFrame for reference.
Convert Columns to Float or Cat.Codes:

Attempt to convert each column to a float type.
If the conversion fails:
Check if specific columns are specified for conversion using cat.codes.
If specified, convert the object columns to categorical codes using cat.codes.
If not specified, delete the columns that cannot be converted to float or using cat.codes.
Standardize Numeric Columns:

Use StandardScaler to standardize numeric columns (float64 or int64 types).
Display Processed DataFrame:

Present the DataFrame after preprocessing.
Save Processed DataFrame:

Save the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
Display Deleted Columns:

Identify and display columns deleted from the original DataFrame during the conversion.

    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Save a copy of the original DataFrame for reference
    original_df = df.copy()

    # Convert each column to float or use cat.codes (if specified)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            if object_columns is not None and col in object_columns:
                df[col] = df[col].astype('category').cat.codes
            else:
                del df[col]  # Delete columns not converted to float or using cat.codes

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)

    # Display the deleted columns from the original DataFrame
    deleted_columns = original_df.columns.difference(df.columns)
    print("\nDeleted columns:")
    print(deleted_columns)

    return


print("""preprocess_csv_5:

1- Converts columns to float;

2- if conversion fails, it checks if specific columns are specified for conversion using cat.codes.

3- If specified, convert the object columns to categorical codes using cat.codes.

4- If not specified, delete the columns that cannot be converted to float or using cat.codes.

5- If specified, delete a specific column from the DataFrame.

6- Applies StandardScaler to numeric columns.

7- Displays the DataFrame before and after preprocessing.
8- Saves the preprocessed DataFrame to a new CSV file.
9- Identifies and displays columns deleted from the original DataFrame during the conversion.


""")


def preprocess_csv_6(csv_file_path, object_columns=None, delete_column=None):
    """
    Load Data:

Load the CSV file into a pandas DataFrame.
Display Initial DataFrame:

Present the DataFrame before any preprocessing.
Save Original DataFrame:

Create a copy of the original DataFrame for reference.
Convert Columns to Float or Cat.Codes:

Attempt to convert each column to a float type.
If the conversion fails:
Check if specific columns are specified for conversion using cat.codes.
If specified, convert the object columns to categorical codes using cat.codes.
If not specified, delete the columns that cannot be converted to float or using cat.codes.
Standardize Numeric Columns:

Use StandardScaler to standardize numeric columns (float64 or int64 types).
Delete a Specific Column:

If specified, delete a specific column from the DataFrame.
Display Processed DataFrame:

Present the DataFrame after preprocessing.
Save Processed DataFrame:

Save the preprocessed DataFrame to a new CSV file with a filename prefixed by 'preprocessed_'.
Display Deleted Columns:

Identify and display columns deleted from the original DataFrame during the conversion.

    """
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before preprocessing
    print("DataFrame before preprocessing:")
    display(df)

    # Save a copy of the original DataFrame for reference
    original_df = df.copy()

    # Convert each column to float or use cat.codes (if specified)
    for col in df.columns:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            if object_columns is not None and col in object_columns:
                df[col] = df[col].astype('category').cat.codes
            else:
                del df[col]  # Delete columns not converted to float or using cat.codes

    # Use StandardScaler for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    # Delete a specific column if specified
    if delete_column is not None:
        del df[delete_column]

    # Display the DataFrame after preprocessing
    print("\nDataFrame after preprocessing:")
    display(df)

    # Save the preprocessed DataFrame to a new CSV file
    df.to_csv('preprocessed_' + csv_file_path, index=False)

    # Display the deleted columns from the original DataFrame
    deleted_columns = original_df.columns.difference(df.columns)
    print("\nDeleted columns:")
    print(deleted_columns)
    return




def remove_duplicates(csv_file_path, column_name):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before removing duplicates
    print("DataFrame before removing duplicates:")
    display(df)

    # Remove duplicates in the specified column
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    # Display the DataFrame after removing duplicates
    print("\nDataFrame after removing duplicates:")
    display(df)

    # Save the DataFrame with duplicates removed to a new CSV file
    df.to_csv('duplicates_removed_' + csv_file_path, index=False)
    return


def delete_columns(csv_file_path, columns_to_delete):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Display the DataFrame before deleting columns
    print("DataFrame before deleting columns:")
    display(df)

    # Delete specified columns
    df.drop(columns=columns_to_delete, inplace=True, errors='ignore')

    # Display the DataFrame after deleting columns
    print("\nDataFrame after deleting columns:")
    display(df)

    # Save the DataFrame with specified columns deleted to a new CSV file
    df.to_csv('columns_deleted_' + csv_file_path, index=False)

    return

def prepare_analyze_and_lazy_predict(file_path, target_column):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        # Missing Values Overview
        missing_values = df.isnull().sum()
        missing_percentage = (missing_values / len(df)) * 100
        missing_summary = pd.DataFrame({'Missing Values': missing_values, 'Missing Percentage': missing_percentage})
        print("\nMissing Values Overview:")
        display(missing_summary)

        # Drop rows with missing values
        df = df.dropna()

        # Display information about the cleaned DataFrame
        print("\nCleaned Info:")
        display(df.info())

        # Display statistical summary of the cleaned DataFrame
        print("\nCleaned Describe:")
        display(df.describe())

        # Categorical Columns Overview
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            print(f"\nUnique values in '{col}': {df[col].unique()}")
            print(df[col].value_counts())

        # Plot histograms for float and int columns in the cleaned DataFrame
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_columns:
            plt.figure(figsize=(8, 5))
            df[col].plot(kind='hist', bins=20, title=f'Histogram for {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()

        # Plot scatter matrix for numeric columns in the cleaned DataFrame
        scatter_matrix(df[numeric_columns], figsize=(12, 8), alpha=0.5)
        plt.show()

        # Display correlation matrix as a heatmap for the cleaned DataFrame
        correlation_matrix = df[numeric_columns].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title("Correlation Matrix (Cleaned)")
        plt.show()

        # Outlier Detection using IQR
        outliers = pd.DataFrame()
        for col in numeric_columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            column_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outliers = pd.concat([outliers, column_outliers])
            print(f"\nOutliers in '{col}':")
            display(column_outliers)


        print("\nOutliers Detected:")
        display(outliers)

        # Prepare data by standardizing numeric columns
        scaler = StandardScaler()
        df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

        # Display statistical summary of the standardized DataFrame
        print("\nStandardized Describe:")
        display(df.describe())



    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return

"""# General mahine leaning function

**LazyRegressor**
"""


def Lazy_Regressor_analysis(csv_file_path, target_column_name):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Separate features (X) and target variable (y)
    X = df.drop(columns=[target_column_name])
    y = df[target_column_name]

    # Split the dataset into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # Defines and builds the lazyregressor
    clf = LazyRegressor(verbose=0,ignore_warnings=True, custom_metric=None)
    models_train,predictions_train = clf.fit(X_train, X_train, Y_train, Y_train)
    display(models_train)
    # Bar plot of R-squared values
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=predictions_train.index, x="R-Squared", data=predictions_train)
    ax.set(xlim=(0, 1))
    plt.show()

    # Bar plot of RMSE values
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=predictions_train.index, x="RMSE", data=predictions_train)
    ax.set(xlim=(0, 10))
    plt.show()

  # Bar plot of calculation time
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=predictions_train.index, x="Time Taken", data=predictions_train)
    ax.set(xlim=(0, 10))
    plt.show()
    return

"""**LazyClassifier**"""


def Lazy_Classifier_analysis(csv_file_path, target_column_name):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Separate features (X) and target variable (y)
    X = df.drop(columns=[target_column_name])
    y = df[target_column_name]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1, stratify=y)

    # Use LazyClassifier for a quick analysis of various models
    clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None)
    models, predictions = clf.fit(X_train, X_test, y_train, y_test)

    # Display the models
    display(models)

    # Plot the accuracy of the models
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=models.index, x="Accuracy", data=models)
    ax.set(xlim=(0, 1))
    plt.show()

    # Train an ExtraTreesClassifier
    clf_extra_trees = ExtraTreesClassifier(n_estimators=100, random_state=0)
    clf_extra_trees.fit(X_train, y_train)

    # Make predictions using the ExtraTreesClassifier
    y_pred_class = clf_extra_trees.predict(X_test)

    # Display the predicted classes
    #display(y_pred_class)

    # Evaluate the model using confusion matrix and classification report
    cf_matrix = confusion_matrix(y_test, y_pred_class)
    sns.heatmap(cf_matrix, annot=True, cmap='Blues')
    plt.show()

    print(classification_report(y_test, y_pred_class))
    return



def Random_Forest_Regressor_analysis(csv_file_path, target_column_name):#BRandomForestRegressor
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: File '{csv_file_path}' is empty.")
        return

    if target_column_name not in df.columns:
        print(f"Error: Target column '{target_column_name}' not found in the CSV file.")
        return

    # Separate features (X) and target variable (Y)
    X = df.drop(columns=[target_column_name])
    Y = df[target_column_name]

    # Split the dataset into training and testing sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.7, random_state=1)



    # RandomForestRegressor hyperparameter tuning using GridSearchCV
    forest = RandomForestRegressor(random_state=0, n_estimators=80)
    n_estimators = [100, 300, 500, 800, 1200]
    max_depth = [5, 8, 15, 25, 30]
    hyperF = dict(n_estimators=n_estimators, max_depth=max_depth)

    gridF = GridSearchCV(forest, hyperF, cv=3, verbose=1, n_jobs=-1)
    bestF = gridF.fit(X_test, Y_test)

    hyperparameters=bestF.best_params_
    # Display the best hyperparameters for RandomForestRegressor
    print("Best Hyperparameters for RandomForestRegressor:")
    print(bestF.best_params_)
    print("max_depth:", hyperparameters['max_depth'])
    print("n_estimators:", hyperparameters['n_estimators'])
    max_depth=hyperparameters['max_depth']

    n_estimators=hyperparameters['n_estimators']
    forestOpt = RandomForestRegressor(random_state = 1, max_depth = 8,n_estimators = 800)
    modelOpt = forestOpt.fit(X_test, Y_test)
    y_pred = modelOpt.predict(X_test)
    r2_forestOpt = forestOpt.score(X_test, Y_test)
    print(r2_forestOpt)
    start = time.time()
    Y_pred = forestOpt.predict(X_test)
    end = time.time()
    print(end - start)
    maeOpt=mean_absolute_error(y_pred, Y_test)
    print(maeOpt)
    sns.set(color_codes=True)
    sns.set_style("white")

    ax = sns.regplot(x=Y_test, y=y_pred, scatter_kws={'alpha':0.4})
    ax.set_xlabel('Experimental Values', fontsize='large', fontweight='bold')
    ax.set_ylabel('Predicted Values', fontsize='large', fontweight='bold')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.figure.set_size_inches(5, 5)
    plt.show
    return





"""# Pubchem classification"""


def get_target_values_meanings(y):
    unique_values = y.unique()
    meanings = {}
    for val in unique_values:
        meaning = input(f"Enter the meaning of '{val}': ")
        meanings[val] = meaning
    return meanings

def classification_analysis(csv_file_path, target_column):
    # Read the CSV file
    data = pd.read_csv(csv_file_path)

    X = data.drop([target_column], axis=1)
    y = data[target_column]

    # Get target values meanings
    target_meanings = get_target_values_meanings(y)

    # Apply SMOTE to handle class imbalance
    sm = SMOTE(sampling_strategy='auto', random_state=42)
    X_res, y_res = sm.fit_resample(X.astype(float), y)


    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.25, random_state=123, stratify=y_res)

    clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None, predictions=True)
    models, predictions = clf.fit(X_train, X_test, y_train, y_test)
    display(models)

    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=models.index, x="Accuracy", data=models)
    ax.set(xlim=(0, 1))
    plt.show()

    clf = RandomForestClassifier(n_estimators=500, random_state=1)
    clf.fit(X_train, y_train)
    y_pred_class = clf.predict(X_test)

    xgbc = XGBClassifier()
    xgbc.fit(X_train, y_train)
    y_pred_classX = xgbc.predict(X_test)

    scores = cross_val_score(xgbc, X_train, y_train, cv=5)
    print("Mean cross-validation score: %.2f" % scores.mean())

    kfold = KFold(n_splits=10, shuffle=True)
    kf_cv_scores = cross_val_score(xgbc, X_train, y_train, cv=kfold)
    print("K-fold CV average score: %.2f" % kf_cv_scores.mean())

    # get importance with Random Forest
    importance = clf.feature_importances_

    fp = X.columns[sorted(range(len(importance)), key=lambda i: importance[i], reverse=True)[:20]]
    imp_values = sorted(importance, reverse=True)[:20]

    fake = pd.DataFrame({'ind': fp, 'importance__': imp_values})

    sns.set_color_codes("pastel")
    ax = sns.barplot(x='ind', y='importance__', data=fake)
    ax.set(xlabel='Features', ylabel='importance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    unique_labels = y.unique()

    cf_matrix = confusion_matrix(y_test, y_pred_class)
    sns.heatmap(cf_matrix, annot=True, cmap='Blues', xticklabels=list(target_meanings.values()), yticklabels=list(target_meanings.values()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    print(classification_report(y_test, y_pred_class))

    return


"""# classification_padel regressor"""


def get_target_values_meanings(y):
    unique_values = y.unique()
    meanings = {}
    for val in unique_values:
        meaning = input(f"Enter the meaning of '{val}': ")
        meanings[val] = meaning
    return meanings

def analyze_and_visualize_data(file_path=None, target_column=None):
    # Read data
    if file_path is None:
        file_path = input("Enter the CSV file path: ")
    df = pd.read_csv(file_path)

    # Features and target variable
    if target_column is None:
        target_column = input("Enter the target column name: ")
    X = df.drop([target_column], axis=1)
    y = df[target_column]

    # Get target values meanings
    target_meanings = get_target_values_meanings(y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)

    # LazyClassifier
    clf = LazyClassifier(verbose=0, ignore_warnings=True, custom_metric=None, predictions=True)
    models, _ = clf.fit(X_train, X_test, y_train, y_test)

    # Plot the model accuracies
    plt.figure(figsize=(5, 10))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(y=models.index, x="Accuracy", data=models, palette='viridis')
    ax.set(xlim=(0, 1))
    plt.show()

    # RandomForestClassifier
    clf_rf = RandomForestClassifier(n_estimators=500, random_state=1)
    clf_rf.fit(X_train, y_train)
    y_pred_class_rf = clf_rf.predict(X_test)

    # XGBClassifier
    xgbc = XGBClassifier()
    xgbc.fit(X_train, y_train)
    y_pred_class_xgb = xgbc.predict(X_test)

    # Cross-validation scores
    scores_rf = cross_val_score(clf_rf, X_train, y_train, cv=5)
    print("Random Forest Mean cross-validation score: %.2f" % scores_rf.mean())

    kfold = KFold(n_splits=10, shuffle=True)
    kf_cv_scores_xgb = cross_val_score(xgbc, X_train, y_train, cv=kfold)
    print("XGBClassifier K-fold CV average score: %.2f" % kf_cv_scores_xgb.mean())

    # Feature Importance with Random Forest
    importance_rf = clf_rf.feature_importances_
    feature_names = X.columns
    fp_rf = sorted(range(len(importance_rf)), key=lambda i: importance_rf[i], reverse=True)[:20]
    imp_values_rf = sorted(importance_rf, reverse=True)[:20]

    feature_names_rf = [feature_names[i] for i in fp_rf]
    imp_values_rf

    fake_rf = pd.DataFrame({'ind': feature_names_rf, 'importance__': imp_values_rf})

    # Plot Feature Importance
    sns.set_color_codes("pastel")
    ax_rf = sns.barplot(x='ind', y='importance__', data=fake_rf)
    ax_rf.set(xlabel='Features', ylabel='importance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

    clf = RandomForestClassifier(n_estimators=500, random_state=1)
    clf.fit(X_train, y_train)
    y_pred_class = clf.predict(X_test)

    cf_matrix = confusion_matrix(y_test, y_pred_class)

    # Plot confusion matrix with target values meanings as titles
    sns.heatmap(cf_matrix, annot=True, cmap='Blues', xticklabels=list(target_meanings.values()), yticklabels=list(target_meanings.values()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

    print(classification_report(y_test, y_pred_class))
    return



def retrive_data_from_chembl(search_term, condition_column, condition_value, result_column):
    # Search for the target proteins
    target = new_client.target
    target_query = target.search(search_term)

    # Convert the result to a DataFrame
    targets_df = pd.DataFrame.from_dict(target_query)

    # Display information about the DataFrame
    targets_df.info()

    # Find corresponding values based on the condition
    corresponding_values = targets_df.loc[targets_df[condition_column] == condition_value, result_column].tolist()

    # Print the corresponding values
    print(f"Corresponding {result_column} values for {condition_value}:")
    print(corresponding_values)

    # Retrieve activity information for the selected target
    target_selected = corresponding_values[0]  # Assuming there is only one corresponding value
    activity = new_client.activity

    # Display unique activity types for all activities associated with the target
    all_activity_types = pd.DataFrame.from_dict(activity.filter(target_chembl_id=target_selected)).type.unique()
    print("All Activity Types:")
    print(all_activity_types)

    # Filter activity for the selected target and standard_type="IC50"
    res = activity.filter(target_chembl_id=target_selected).filter(standard_type="IC50")

    # Display unique activity types for the filtered activities
    df_types = pd.DataFrame.from_dict(res).type.unique()
    print("Unique Activity Types for IC50:")
    print(df_types)

    # Display the activity information DataFrame for IC50
    display(pd.DataFrame.from_dict(res))

    # Create a DataFrame with the protein and its activity
    df = pd.DataFrame.from_dict(res)

    # Further processing of bioactivity data
    df.standard_value = df.standard_value.astype(float)

    # Display the head of the DataFrame
    print("Head of the DataFrame:")
    display(df.head())

    # Display the shape of the DataFrame
    print("Shape of the DataFrame:")
    print(df.shape)

    # Display statistics of the 'standard_value' column
    print("Statistics of 'standard_value' column:")
    print(df.standard_value.describe())
    display(df.standard_value.describe())

    # Save the extracted data into a .csv file with index=False
    df.to_csv('QSAR_Alzheimer.csv', index=False)
    print("Data saved to QSAR_Alzheimer.csv")

    return targets_df, corresponding_values, pd.DataFrame.from_dict(res), df



def finding_important_features_regressor(file_path=None, target_column=None):
    # Read data
    if file_path is None:
        file_path = input("Enter the CSV file path: ")
    df = pd.read_csv(file_path)

    # Features and target variable
    if target_column is None:
        target_column = input("Enter the target column name: ")
    X = df.drop([target_column], axis=1)
    y = df[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)

    # RandomForestRegressor
    reg_rf = RandomForestRegressor(n_estimators=500, random_state=1)
    reg_rf.fit(X_train, y_train)
    y_pred_rf = reg_rf.predict(X_test)

    # XGBRegressor
    xgbr = XGBRegressor()
    xgbr.fit(X_train, y_train)
    y_pred_xgb = xgbr.predict(X_test)

    # Cross-validation scores
    scores_rf = cross_val_score(reg_rf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print("Random Forest Mean cross-validation score (negative mean squared error): %.2f" % scores_rf.mean())

    kfold = KFold(n_splits=10, shuffle=True)
    kf_cv_scores_xgb = cross_val_score(xgbr, X_train, y_train, cv=kfold, scoring='neg_mean_squared_error')
    print("XGBRegressor K-fold CV average score (negative mean squared error): %.2f" % kf_cv_scores_xgb.mean())

    # Feature Importance with Random Forest
    importance_rf = reg_rf.feature_importances_
    feature_names = X.columns
    fp_rf = np.argsort(importance_rf)[::-1][:20]
    imp_values_rf = sorted(importance_rf, reverse=True)[:20]

    feature_names_rf = [feature_names[i] for i in fp_rf]
    imp_values_rf

    fake_rf = pd.DataFrame({'ind': feature_names_rf, 'importance__': imp_values_rf})

    # Plot Feature Importance
    sns.set_color_codes("pastel")
    ax_rf = sns.barplot(x='ind', y='importance__', data=fake_rf)
    ax_rf.set(xlabel='feature', ylabel='importance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return


def finding_important_features_classifier(file_path=None, target_column=None):
    # Read data
    if file_path is None:
        file_path = input("Enter the CSV file path: ")
    df = pd.read_csv(file_path)

    # Features and target variable
    if target_column is None:
        target_column = input("Enter the target column name: ")
    X = df.drop([target_column], axis=1)
    y = df[target_column]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=2)

    # RandomForestRegressor
    reg_rf = randomforestclassifier(n_estimators=500, random_state=1)
    reg_rf.fit(X_train, y_train)
    y_pred_rf = reg_rf.predict(X_test)

    # XGBRegressor
    xgbr = XGBRegressor()
    xgbr.fit(X_train, y_train)
    y_pred_xgb = xgbr.predict(X_test)

    # Cross-validation scores
    scores_rf = cross_val_score(reg_rf, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    print("Random Forest Mean cross-validation score (negative mean squared error): %.2f" % scores_rf.mean())

    kfold = KFold(n_splits=10, shuffle=True)
    kf_cv_scores_xgb = cross_val_score(xgbr, X_train, y_train, cv=kfold, scoring='neg_mean_squared_error')
    print("XGBRegressor K-fold CV average score (negative mean squared error): %.2f" % kf_cv_scores_xgb.mean())

    # Feature Importance with Random Forest
    importance_rf = reg_rf.feature_importances_
    feature_names = X.columns
    fp_rf = np.argsort(importance_rf)[::-1][:20]
    imp_values_rf = sorted(importance_rf, reverse=True)[:20]

    feature_names_rf = [feature_names[i] for i in fp_rf]
    imp_values_rf

    fake_rf = pd.DataFrame({'ind': feature_names_rf, 'importance__': imp_values_rf})

    # Plot Feature Importance
    sns.set_color_codes("pastel")
    ax_rf = sns.barplot(x='ind', y='importance__', data=fake_rf)
    ax_rf.set(xlabel='feature', ylabel='importance')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
    return

