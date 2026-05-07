from parquet_read import ParquetFileHelper, BASE_PATH

def main():
    # Use ParquetFileHelper with BASE_PATH and no specific filename to process all parquet files in folder
    helper = ParquetFileHelper(BASE_PATH, engine="fastparquet")  # Use fastparquet to avoid pyarrow extension error if installed

    try:
        results = helper.process_folder(frac_sample=0.1)

        print("Per file row counts:")
        for fname, count in results["per_file_row_counts"].items():
            print(f"  {fname}: {count}")

        print(f"Total rows across all files: {results['total_rows']}")

        print("Combined NA counts across all files:")
        print(results["combined_na_counts"])

        print("Sampled 10% combined data shape:", results["combined_sample"].shape)
        print("Sample rows (up to 10):")
        print(results["combined_sample"].head(10))

    except Exception as e:
        print("Error during parquet processing:", e)

if __name__ == "__main__":
    main()
