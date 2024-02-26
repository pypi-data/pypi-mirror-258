import json
import glob
import shutil
import importlib_resources

from os import linesep
from pathlib import Path

from citros.parsers import ParserRos2
from citros.utils import validate_dir, validate_file

# from .ros import Ros
from .settings import Settings
from .simulation import Simulation
from .parameter_setup import ParameterSetup
from .citros_obj import (
    CitrosObj,
    CitrosException,
    FileNotFoundException,
    CitrosNotFoundException,
    NoValidException,
)

from rich.traceback import install
from rich.logging import RichHandler
from rich import print, inspect, print_json
from rich.panel import Panel
from rich.padding import Padding
import shutil

install()

from .batch import Batch


class Citros(CitrosObj):
    """Object representing .citros/simulations/{name}.json file."""

    # def __enter__(self):
    #     """
    #     Returns the Citros instance. This allows the class to be used in a `with` statement.
    #     """
    #     return self

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     """
    #     Makes sure the stats collecting thread is stopped and handles exceptions.

    #     Args:
    #     exc_type: The type of exception.
    #     exc_val: The exception instance.
    #     exc_tb: A traceback object encapsulating the call stack at the point
    #             where the exception originally occurred.
    #     """
    #     self.events.on_shutdown()

    #     self.systemStatsRecorder.stop()

    #     if exc_type is not None:
    #         self._handle_exceptions(exc_val, exit=True)

    def __init__(
        self,
        name="project",
        root=None,
        new=False,
        log=None,
        citros=None,
        verbose=False,
        debug=False,
        level=0,
    ):
        ###################
        ##### .citros #####
        ###################
        # init settings
        self.settings = None

        # init parameter_setups
        self.parameter_setups = []

        # init simulations
        self.simulations = []

        #################
        ##### utils #####
        #################
        self._ros = None

        super().__init__(name, root, new, log, citros, verbose, debug, level)

    def __str__(self):
        # print_json(data=self.data)
        return json.dumps(self.data, indent=4)

    ###################
    ##### private #####
    ###################
    # overriding
    def _validate(self):
        """Validate the json file."""

        # TODO[enhancement]: check that the project.json file is valid

        return True

    # overriding
    def _load(self):
        self.log.debug(f"{'   '*self.level}{self.__class__.__name__}.load()")

        # loads the main file (project.json)
        try:
            self.log.debug(f"loading .citros/project.json")
            super()._load()
        except FileNotFoundException as ex:
            self.log.error(f"simulation file {self.file} does not exist.")
            raise CitrosNotFoundException(
                f"simulation file {self.file} does not exist."
            )

        self.copy_default_citros_files()

        # loads the settings.json file
        self.log.debug(f"loading .citros/settings.json")
        self.settings = Settings(
            "settings",
            root=self.root,
            log=self.log,
            citros=self,
            new=self.new,
            debug=self.debug,
            verbose=self.verbose,
            level=self.level + 1,
        )

        # loads the parameter_setups
        for file in glob.glob(f"{self.root_citros}/parameter_setups/*.json"):
            file = file.split("/")[-1]
            self.log.debug(f"loading parameter_setup: {file}")
            self.parameter_setups.append(
                ParameterSetup(
                    file,
                    root=self.root,
                    new=self.new,
                    log=self.log,
                    citros=self,
                    debug=self.debug,
                    verbose=self.verbose,
                    level=self.level + 1,
                )
            )

        # loads the simulations
        for file in glob.glob(f"{self.root_citros}/simulations/*.json"):
            file = file.split("/")[-1]
            # self.simulations.append(Simulation(self.root, file, self.log, citros=self))
            self.log.debug(f"loading simulation: {file}")
            self.simulations.append(
                Simulation(
                    file,
                    root=self.root,
                    new=self.new,
                    log=self.log,
                    citros=self,
                    debug=self.debug,
                    verbose=self.verbose,
                    level=self.level + 1,
                )
            )

        # utils
        # self.ros = Ros(self.root, "ros.json", self.log)

    # overriding
    def _new(self):
        self.log.debug(f"{'   '*self.level}{self.__class__.__name__}._new()")

        # create the .citros folder
        Path(self.root_citros).mkdir(parents=True, exist_ok=True)
        # copy data files.
        self.copy_default_citros_files()

        # settings
        self.log.debug(f"creating .citros/settings.json")
        self.settings = Settings(
            "settings",
            root=self.root,
            log=self.log,
            citros=self,
            new=self.new,
            verbose=self.verbose,
            debug=self.debug,
            level=self.level + 1,
        )

        self._parser_ros2 = ParserRos2(self.log, self.get_citros_ignore_list())
        # get data from ros2
        project_data = self._parser_ros2.parse(str(self.root))
        with open(self.path(), "w") as file:
            json.dump(project_data, file, sort_keys=True, indent=4)

        self.data = project_data
        self._save()

        # parameter setups
        self.log.debug(f"creating .citros/parameter_setups/default_param_setup.json")
        self.parameter_setups = ParameterSetup(
            "default_param_setup",
            root=self.root,
            log=self.log,
            citros=self,
            new=self.new,
            verbose=self.verbose,
            debug=self.debug,
            level=self.level + 1,
        )

        # create simulation per launch file as default
        self.log.debug(f"creating .citros/simulations/*")
        self._create_simulations()

    #################
    ##### utils #####
    #################
    def _get_launches(self):
        """returns a list of launch objects

        Args:
            proj_json (Path): path to project.json file

        Returns:
            [{
                package: str,
                name: str
            }]: array of launch info
        """

        launch_info = []

        for package in self.citros.get("packages", []):
            for launch in package.get("launches", []):
                if "name" in launch:
                    launch_info.append(
                        {"package": package.get("name", ""), "name": launch["name"]}
                    )

        return launch_info

    def _create_simulations(self):
        launch_infos = self._get_launches()
        if not launch_infos:
            self.log.warning("No launch files found in user's project.")
            print(
                Panel.fit(
                    Padding(
                        "[yellow]No launch files found. [white]If you have launch files in your project, make sure they are of the form [green]*.launch.py ",
                        1,
                    ),
                    title="help",
                )
            )

            return

        # inspect(launch_infos)
        for launch in launch_infos:
            package_name = launch["package"]
            launch_file = launch["name"]

            # print("vova", self.root, f"simulation_{launch_file.split('.')[0]}.json")
            self.simulations.append(
                Simulation(
                    f"simulation_{launch_file.split('.')[0]}",
                    root=self.root,
                    new=self.new,
                    log=self.log,
                    citros=self,
                    package_name=package_name,
                    launch_file=launch_file,
                    verbose=self.verbose,
                    debug=self.debug,
                    level=self.level + 1,
                )
            )

    def get_citros_ignore_list(self):
        if Path(self.root_citros, ".citrosignore").exists():
            with open(Path(self.root_citros, ".citrosignore"), "r") as file:
                lines = [line.strip() for line in file if "#" not in line]
                self.log.debug(f".citrosignore contenrs: {lines}")
                return lines
        else:
            self.log.debug(f"Could not find .citrosignore in {self.root_citros}")
            return []

    def copy_default_citros_files(self):
        self.log.debug(
            f"{'   '*self.level}{self.__class__.__name__}.copy_default_citros_files()"
        )

        source_folder = importlib_resources.files("data.defaults.citros")

        self.log.debug(f"copying {source_folder} to {self.root_citros}")

        import os

        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            destination_folder = os.path.join(self.root_citros, relative_path)
            os.makedirs(destination_folder, exist_ok=True)
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)
                if not os.path.exists(destination_file):
                    shutil.copy2(source_file, destination_file)

        self.log.debug(f"Done copying default Citros files.")

    ###################
    ##### public ######
    ###################
    def delete_batch(self, simulation: str, name: str, version: str):
        import shutil

        shutil.rmtree(self.root_citros / "data" / simulation / name / version)

    def get_batch(self, simulation: str, name: str, version=-1):
        batch = Batch(
            self.root_citros / "data",
            simulation,
            name=name,
            version=version if type(version) is str else None,
            index=version if type(version) is int else None,
            debug=self.debug,
            verbose=self.verbose,
        )

        return batch

    def unload_batch(self, simulation, batch):
        versions = glob.glob(f"{simulation}/{batch}/*")
        for ver in versions:
            batch = self.get_batch(simulation, batch, ver)
            batch.unload()

    def get_batches(self, simulation=None, batch=None, filter: str = None):
        batches = []
        if simulation:
            simulations = sorted(
                glob.glob(f"{str(self.root_citros / 'data' / simulation)}")
            )
        else:
            simulations = sorted(glob.glob(f"{str(self.root_citros / 'data')}/*/"))

        for sim in simulations:
            if batch:
                batch_names = sorted(glob.glob(f"{sim}/{batch}/"))
            else:
                batch_names = sorted(glob.glob(f"{sim}/*/"))

            for batch_name in batch_names:
                versions = sorted(glob.glob(f"{batch_name}/*/"), reverse=True)

                batches.append(
                    {
                        "simulation": (sim if sim[-1] != "/" else sim[:-1]).split("/")[
                            -1
                        ],
                        "name": (
                            batch_name if batch_name[-1] != "/" else batch_name[:-1]
                        ).split("/")[-1],
                        "versions": [
                            (v if v[-1] != "/" else v[:-1]).split("/")[-1]
                            for v in versions
                        ],
                    }
                )

        return batches

    def get_batches_flat(self):

        from .database import CitrosDB

        hot_reload_info = {}
        try:
            citrosDB = CitrosDB(log=self.log, debug=self.debug, verbose=self.verbose)
            hot_reload_info = citrosDB.hot_reload_get_info()
        except Exception as ex:
            self.log.error(ex)

        # inspect(hot_reload_info)

        batches = []
        simulations = sorted(glob.glob(f"{str(self.root_citros / 'data')}/*/"))
        for sim in simulations:
            if not Path(sim).is_dir():
                continue
            names = sorted(glob.glob(f"{sim}/*/"))
            simulation = (sim if sim[-1] != "/" else sim[:-1]).split("/")[-1]
            _simulation_print = simulation

            for name in names:
                if not Path(name).is_dir():
                    continue
                versions = sorted(glob.glob(f"{name}/*/"), reverse=True)
                # print(versions)
                name = (name if name[-1] != "/" else name[:-1]).split("/")[-1]
                name_print = name

                for version in versions:
                    batch = json.loads((Path(version) / "info.json").read_text())

                    version = (version if version[-1] != "/" else version[:-1]).split(
                        "/"
                    )[-1]

                    batches.append(
                        {
                            "created_at": batch["created_at"],
                            "simulation": _simulation_print,
                            "name": name_print,
                            "version": version,
                            "message": batch["message"],
                            f"status": (
                                "UNKNOWN"
                                if hot_reload_info is None
                                else hot_reload_info.get(simulation, {})
                                .get(name, {})
                                .get(version, {})
                                .get("status", "UNLOADED")
                            ),
                            "completions": str(batch["completions"]),
                            "path": version,
                        }
                    )

                    # for printing.
                    _simulation_print = None
                    _name_print = None

        return batches, hot_reload_info

    def get_reports_flat(self):
        ret = []
        reports = sorted(glob.glob(f"{str(self.root_citros / 'reports')}/*/"))
        for report in reports:
            if not Path(report).is_dir():
                continue
            versions = sorted(glob.glob(f"{report}/*/"), reverse=True)

            for version in versions:
                report_version = json.loads((Path(version) / "info.json").read_text())

                notebooks = ""
                if (
                    report_version.get("notebooks") == None
                    or report_version["notebooks"] == None
                    or len(report_version["notebooks"]) == 0
                ):
                    continue
                else:
                    report_version_notebook = (
                        report_version["notebooks"][0]
                        if report_version["notebooks"][0][-1] != "/"
                        else report_version["notebooks"][0][:-1]
                    )
                    notebooks = str(
                        Path(version) / report_version_notebook.split("/")[-1]
                    )
                    if notebooks.endswith(".ipynb"):
                        notebooks = notebooks[: -len(".ipynb")]

                ret.append(
                    {
                        "started_at": report_version["started_at"],
                        "finished_at": report_version["finished_at"],
                        "name": report_version["name"],
                        "version": (
                            version if version[-1] != "/" else version[:-1]
                        ).split("/")[-1],
                        "message": report_version["message"],
                        "path": f'{str(self.root_citros / "reports" / report_version["name"]/ (version if version[-1] != "/" else version[:-1]).split("/")[-1])}',
                        "progress": report_version["progress"],
                        "status": report_version["status"],
                    }
                )

        return ret
