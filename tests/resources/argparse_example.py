import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--override-date",
    type=str,
    default=None,
    help="Override the default date (today's date) to use add to data folder from previous session (yyyy-mm-dd)",
)
parser.add_argument(
    "--intervals-table",
    type=str,
    default="trials",
)
parser.add_argument(
    "--align-to-col",
    type=str,
    default="stim_start_time",
)
parser.add_argument(
    "--pre",
    type=float,
    default=0.5,
)
parser.add_argument(
    "--post",
    type=float,
    default=0.5,
)
parser.add_argument(
    "--default-qc-only",
    type=int,
    default=1,
)
parser.add_argument(
    "--as-spike-count",
    type=int,
    default=0,
)
parser.add_argument(
    "--as-binarized-array",
    type=int,
    default=1,
)
parser.add_argument(
    "--bin-size-s",
    type=float,
    default=0.001,
)
parser.add_argument(
    "--max-workers",
    type=int,
    default=None,
)
parser.add_argument(
    "--skip-existing",
    type=int,
    default=1,
)
parser.add_argument(
    "--largest-to-smallest",
    type=int,
    default=0,
)
# parser.add_argument(
#     "--areas-to-process",
#     type=list[str],
#     default=["MOs", "MRN"],
# )
