import pandas as pd
from pathlib import Path

def combine_and_export_parquets(input_dir: str, output_filename: str, engine: str = "pyarrow") -> None:
    """
    Combine all parquet files in input_dir and export to a single parquet file named output_filename.
    """
    base_path = Path(input_dir)
    files = sorted(base_path.glob("*.parquet"))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {input_dir}")
    dfs = []
    for file_path in files:
        df = pd.read_parquet(file_path, engine=engine)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)
    output_path = base_path / output_filename
    combined_df.to_parquet(output_path, index=False)
    print(f"Combined parquet file saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    input_dir = r"C:\Users\kathy.zhang\OneDrive - MMC\Documents\Project Setup\Uber\uber-analytics\data\processed\fhvhv"
    output_filename = "tlc_fhvhv_2024_2025.parquet"
    combine_and_export_parquets(input_dir, output_filename)
