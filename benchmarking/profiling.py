import cProfile
import itertools
from pathlib import Path
import pstats
import os

from matchms.importing import load_from_mgf, load_from_msp
from matchms.logging_functions import reset_matchms_logger, set_matchms_logger_level


def read_data(file: str, harmonization: bool = True):
    if file.endswith(".msp"):
        spectra = list(load_from_msp(file, metadata_harmonization=harmonization))
    elif file.endswith(".mgf"):
        spectra = list(load_from_mgf(file, metadata_harmonization=harmonization))
    else:
        raise ValueError(f"File extension not recognized: {Path(file).suffix}")

    return spectra


def main(filename, loglevel, harmonization):
    reset_matchms_logger()
    set_matchms_logger_level(loglevel)
    read_data(filename, harmonization=harmonization)


if __name__ == "__main__":
    filenames = ["GNPS-LIBRARY.mgf", "GNPS-LIBRARY.msp", "NIST_EI_MS.mgf", "NIST_EI_MS.msp", "WILEY12.mgf", "WILEY12.msp"]
    loglevels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    harmonizations = [True, False]

    grid = itertools.product(filenames, loglevels, harmonizations)
    for filename, loglevel, harmonization in grid:
        print(f"Profiling {filename} with loglevel {loglevel} and harmonization {harmonization}...")
        profiler = cProfile.Profile()
        profiler.enable()
        main(filename=filename, loglevel=loglevel, harmonization=harmonization)
        profiler.disable()

        pstats.Stats(profiler)\
            .strip_dirs()\
            .dump_stats(os.path.join("profiles",
                                     f"{Path(filename).stem}_{Path(filename).suffix}_{loglevel}_{harmonization}.prof"))
