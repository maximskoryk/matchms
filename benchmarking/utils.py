import cProfile
import io
import pandas as pd
from pathlib import Path
import pstats


# from https://gist.github.com/ralfstx/a173a7e4c37afa105a66f371a09aa83e
def prof_to_csv(prof: cProfile.Profile):
    out_stream = io.StringIO()
    pstats.Stats(prof, stream=out_stream).print_stats()
    result = out_stream.getvalue()
    # chop off header lines
    result = 'ncalls' + result.split('ncalls')[-1]
    lines = [','.join(line.rstrip().split(None, 5)) for line in result.split('\n')]
    return '\n'.join(lines)


class Profile:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        self.profile_name = Path(profile_path).stem
        self.profile = pd.read_csv(profile_path)
        self.library, self.fileformat, self.loglevel, self.harmonization = self.parse_profile_metadata()
        self.time = sum(self.profile['tottime'])

    def parse_profile_metadata(self):
        if self.profile_name.startswith("NIST"):
            library = "NIST"
        else:
            library = "GNPS"

        *_, fileformat, loglevel, harmonization = self.profile_name.split("_")
        fileformat = fileformat.lstrip(".")

        return library, fileformat, loglevel, True if harmonization == "True" else False

    def __repr__(self):
        return self.profile_name
