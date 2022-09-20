import cProfile
from pathlib import Path

from matchms.importing import load_from_mgf, load_from_msp
from matchms.logging_functions import reset_matchms_logger, set_matchms_logger_level

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


def read_data(file: str, loglevel: str = 'INFO', harmonization: bool = True):
    reset_matchms_logger()
    set_matchms_logger_level(loglevel)

    if file.endswith(".msp"):
        spectra = list(load_from_msp(file, metadata_harmonization=harmonization))
    elif file.endswith(".mgf"):
        spectra = list(load_from_mgf(file))
    else:
        raise ValueError(f"File extension not recognized: {Path(file).suffix}")

    return spectra


if __name__ == "__main__":
    cProfile.run('read_data("NIST_EI_MS.msp", harmonization=False)')
