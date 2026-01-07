import datetime
import zoneinfo

import dateutil
import pydantic
import pydantic_settings
import upath

ROOT_DIR = upath.UPath("s3://aind-scratch-data/dynamic-routing/psths")


class Params(pydantic_settings.BaseSettings):
    override_date: str | None = pydantic.Field(
        None,
        exclude=True,
        description="Override the default date (today's date) to use add to data folder from previous session (yyyy-mm-dd)",
    )
    intervals_table: str = "trials"
    align_to_col: str = "stim_start_time"
    pre: float = 0.5
    post: float = 0.5
    default_qc_only: bool = True
    as_spike_count: bool = False
    as_binarized_array: bool = True
    bin_size_s: float = 0.001
    max_workers: int | None = pydantic.Field(None, exclude=True)
    skip_existing: bool = pydantic.Field(True, exclude=True)
    largest_to_smallest: bool = pydantic.Field(False, exclude=True)
    areas_to_process: list[str] | None = pydantic.Field(
        default_factory=lambda: ["MOs", "MRN"], exclude=True
    )
    _start_date: datetime.date = pydantic.PrivateAttr(
        datetime.datetime.now(zoneinfo.ZoneInfo("US/Pacific")).date()
    )

    def model_post_init(self, __context) -> None:
        if self.override_date:
            self._start_date = dateutil.parser.parse(self.override_date).date()

    # --------------------------------

    @property
    def dir_path(self) -> upath.UPath:
        return ROOT_DIR / f"{self._start_date}"

    @pydantic.computed_field
    @property
    def spike_col(self) -> str:
        if self.as_spike_count:
            return "spike_count"
        if self.as_binarized_array:
            return "binarized_spike_times"
        return "spike_times"

    # set the priority of the input sources:
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        *args,
        **kwargs,
    ):
        # instantiating the class will use arguments passed directly, or provided via the command line/app panel
        # the order of the sources below defines the priority (highest to lowest):
        # - for each field in the class, the first source that contains a value will be used
        return (
            init_settings,
            pydantic_settings.sources.JsonConfigSettingsSource(
                settings_cls, json_file="parameters.json"
            ),
            pydantic_settings.CliSettingsSource(settings_cls, cli_parse_args=True),
        )
