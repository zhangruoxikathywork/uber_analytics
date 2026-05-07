import os
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd



class ParquetFileHelper:
    def __init__(self, base_path: str, filename: Optional[str] = None, engine: Optional[str] = None):
        """
        base_path: folder containing parquet files
        filename: specific parquet filename (optional). If None, you can pass file paths to methods or use process_folder.
        engine: pandas parquet engine, e.g., 'pyarrow' or 'fastparquet'. If None, pandas selects.
        """
        self.base_path = Path(base_path)
        self.engine = engine
        self.filename = filename
        if filename:
            self.filepath = self.base_path / filename
        else:
            self.filepath = None

    def combine_and_save(self, output_filename: str) -> None:
        """
        Combine all parquet files in base_path and save to output_filename.
        """
        files = sorted(self.base_path.glob("*.parquet"))
        if not files:
            raise FileNotFoundError(f"No parquet files found in {self.base_path}")
        dfs = []
        for p in files:
            df = pd.read_parquet(p, engine=self.engine)
            dfs.append(df)
        combined_df = pd.concat(dfs, ignore_index=True)
        output_path = self.base_path / output_filename
        combined_df.to_parquet(output_path, index=False)
        print(f"Combined parquet file saved to {output_path}")

    def _read(self, path: Optional[Path] = None, columns: Optional[List[str]] = None) -> pd.DataFrame:
        p = path if path is not None else self.filepath
        if p is None:
            raise ValueError("No file path provided.")
        if not Path(p).exists():
            raise FileNotFoundError(f"Parquet file not found: {p}")
        # Read to pandas DataFrame
        return pd.read_parquet(p, columns=columns, engine=self.engine)

    def row_count(self, path: Optional[Path] = None) -> int:
        df = self._read(path)
        return len(df)

    def na_counts(self, path: Optional[Path] = None) -> pd.Series:
        df = self._read(path)
        return df.isna().sum()

    def sample_fraction(self, frac: float = 0.1, random_state: Optional[int] = 42, path: Optional[Path] = None) -> pd.DataFrame:
        df = self._read(path)
        # Add source file column if filename known
        s = df.sample(frac=frac, random_state=random_state).copy()
        if path is not None:
            s['_source_file'] = Path(path).name
        elif self.filepath is not None:
            s['_source_file'] = Path(self.filepath).name
        return s

    # Helper to process a folder with multiple parquet files (non-recursive)
    def process_folder(self, frac_sample: float = 0.1) -> Dict[str, object]:
        files = sorted(self.base_path.glob("*.parquet"))
        if not files:
            raise FileNotFoundError(f"No parquet files found in {self.base_path}")
        per_file_counts = {}
        per_file_nas = {}
        samples = []
        for p in files:
            df = pd.read_parquet(p, engine=self.engine)
            per_file_counts[p.name] = len(df)
            per_file_nas[p.name] = df.isna().sum()
            s = df.sample(frac=frac_sample, random_state=42).copy()
            s['_source_file'] = p.name
            samples.append(s)
        combined_sample = pd.concat(samples, ignore_index=True) if samples else pd.DataFrame()
        total_rows = sum(per_file_counts.values())
        # Combine NA counts across files (sum)
        combined_nas = None
        for series in per_file_nas.values():
            combined_nas = series if combined_nas is None else combined_nas.add(series, fill_value=0)
        if combined_nas is not None:
            combined_nas = combined_nas.astype(int)
        return {
            "per_file_row_counts": per_file_counts,
            "total_rows": total_rows,
            "per_file_na_counts": per_file_nas,
            "combined_na_counts": combined_nas,
            "combined_sample": combined_sample
        }

    def sample_and_export_files(self, filenames: List[str], frac_sample: float = 0.05, random_state: int = 42) -> None:
        """
        For each parquet file in filenames, take a frac_sample random sample and export it as a new parquet file
        in the base_path directory with suffix '_sample.parquet'.
        """
        for fname in filenames:
            file_path = self.base_path / fname
            if not file_path.exists():
                print(f"File not found, skipping: {file_path}")
                continue
            df = pd.read_parquet(file_path, engine=self.engine)
            sample_df = df.sample(frac=frac_sample, random_state=random_state).copy()
            sample_fname = f"{file_path.stem}_sample.parquet"
            sample_path = self.base_path / sample_fname
            sample_df.to_parquet(sample_path, index=False)
            print(f"Sampled {frac_sample*100:.1f}% of {fname}, saved to {sample_path}")

    def sample_and_export_detected_files(self, frac_sample: float = 0.05, random_state: int = 42) -> None:
        """
        Automatically detect parquet files matching 'fhvhv_tripdata_*.parquet' in base_path,
        take a frac_sample random sample of each, and export to 'TLC_sample_<original_filename>'.
        """
        pattern = "*.parquet"
        files = sorted(self.base_path.glob(pattern))
        if not files:
            print(f"No parquet files found matching pattern {pattern} in {self.base_path}")
            return
        for file_path in files:
            df = pd.read_parquet(file_path, engine=self.engine)
            sample_df = df.sample(frac=frac_sample, random_state=random_state).copy()
            sample_fname = f"TLC_sample_{file_path.name}"
            sample_path = self.base_path / sample_fname
            sample_df.to_parquet(sample_path, index=False)
            print(f"Sampled {frac_sample*100:.1f}% of {file_path.name}, saved to {sample_path}")

# Example usage for your specific file:
if __name__ == "__main__":
    BASE_PATH = r"C:\Users\kathy.zhang\OneDrive - MMC\Documents\Project Setup\Uber\uber-analytics\data\raw\fhvhv"
    helper = ParquetFileHelper(BASE_PATH, engine="pyarrow")
    try:
        helper.sample_and_export_detected_files(frac_sample=0.05, random_state=42)
    except Exception as e:
        print("Error:", e)
