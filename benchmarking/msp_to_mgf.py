import sys

from matchms.importing import load_from_msp
from matchms.exporting import save_as_mgf


def msp_to_mgf(msp_file: str, mgf_file: str):
    spectra = list(load_from_msp(msp_file, metadata_harmonization=False))
    save_as_mgf(spectra, mgf_file)


if __name__ == "__main__":
    msp_to_mgf(sys.argv[1], sys.argv[2])
