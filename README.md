# Forbidden Memories Drop Extractor
Extracts and exports card drop rates from **Yu-Gi-Oh! Forbidden Memories** SLUS and WA_MRG binary files.

## Acknowledgements
Massive parts of the data-reading logic were adapted from the [fmlib-cpp's DataReader.cpp](https://github.com/forbidden-memories-coding/fmlib-cpp/blob/master/FMLib/FMLib/src/DataReader.cpp)

## Usage
```bash
python .\drop_extractor.py <SLUS_FILE> <WA_MRG_FILE> <OUTPUT_FILE>
```

- `<SLUS_FILE>`: Path to the SLUS binary.
- `<WA_MRG_FILE>`: Path to the WaMrg file.
- `<OUTPUT_FILE>`: Output file in compatible format.

An example of the vanilla drop file is provided in `output.log`.

You can view and analyze the generated file using the [Drop Table Viewer](https://lundylizard.github.io/drop-table-viewer/).
