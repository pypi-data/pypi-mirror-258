from __future__ import annotations

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure

from typing import Union, Optional
from prettytable import PrettyTable

from ._pg_cursor import _PgCursor
from ._plotter import _Plotter
from .citros_dict import CitrosDict


class CitrosDB(_PgCursor):
    """
    CitrosDB object allows to get general information about the batch and make queries.

    Parameters
    ----------
    simulation : str, optional
        Name of the simulation. Default is ENV variable "CITROS_SIMULATION" if it is set or None if the variable is not defined.
    batch : str or int, optional
        Batch name.
    sid : int, optional
        Simulation run id.
        Default is ENV variable "CITROS_SIMULATION_RUN_ID" if it is set or None if the variable is not defined.
    host : str
        Database host address.
        Default is citros.database.CitrosDB.db_host.
    port : str, optional
        Default is citros.database.CitrosDB.db_port.
    database : str, optional
        Database name.
        Default is citros.database.CitrosDB.db_name.
    user : str, optional
        User name.
        Default is citros.database.CitrosDB.db_user.
    password : str, optional
        Password.
        Default is citros.database.CitrosDB.db_password.
    debug_connect : bool, default False
        If `True`, the number of connections and queries which were done by all CitrosDB objects with `debug_connect` set `True`
        existing in the current session is recorded.
        The information is recorded to the _stat.Stat() object.
    log : logging.Logger, default None
        Logger to record log. If None, then the new logger is created.
    """

    def __init__(
        self,
        simulation=None,
        batch=None,
        sid=None,
        host=None,
        port=None,
        database=None,
        user=None,
        password=None,
        debug_connect=False,
        log=None,
    ):
        super().__init__(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            simulation=simulation,
            batch=batch,
            debug_connect=debug_connect,
            log=log,
        )

        if sid is None:
            self._set_sid(os.getenv("CITROS_SIMULATION_RUN_ID"))
        else:
            self._set_sid(sid)

        self._topic = None

    def _copy(self):
        """
        Make a copy of the CitrosDB object.

        Returns
        -------
        CitrosDB
        """
        ci = CitrosDB(
            simulation=self._simulation,
            batch=self._batch_name,
            sid=self._sid,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            debug_connect=self._debug_connect,
            log=self.log,
        )

        if self._sid is None:
            if hasattr(self, "_sid_val"):
                ci._sid_val = self._sid_val.copy()
        if hasattr(self, "_error_flag"):
            ci._error_flag = self._error_flag.copy()
        if hasattr(self, "_rid_val"):
            ci._rid_val = self._rid_val.copy()
        if hasattr(self, "_time_val"):
            ci._time_val = self._time_val.copy()
        if hasattr(self, "_filter_by"):
            ci._filter_by = self._filter_by
        if hasattr(self, "_order_by"):
            ci._order_by = self._order_by

        if hasattr(self, "_test_mode"):
            ci._test_mode = self._test_mode

        if isinstance(self._topic, list):
            ci._topic = self._topic.copy()
        elif isinstance(self._topic, str):
            ci._topic = [self._topic]
        else:
            ci._topic = None

        if hasattr(self, "_method"):
            ci._method = self._method
        if hasattr(self, "_n_avg"):
            ci._n_avg = self._n_avg
        if hasattr(self, "_n_skip"):
            ci._n_skip = self._n_skip
        return ci

    def _is_simulation_set(self):
        """
        Check if the simulation is set.

        Returns
        -------
        bool : True if the simulation is set and exists, otherwise False.
        """
        if self._simulation is None:
            self.log.error("Please provide simulation by simulation() method")
            return False
        else:
            return True

    def _is_batch_set(self):
        """
        Check if the batch name is set.

        Returns
        -------
        bool : True if the batch name is set and exists, otherwise False.
        """
        if self._batch_name is None:
            self.log.error("Please provide batch name by batch() method")
            return False
        else:
            return True

    def _is_batch_available(self):
        """
        Check if the batch is set and in the database.
        """
        if hasattr(self, "_test_mode"):
            return True

        # check if the batch name is set.
        if (not self._is_simulation_set()) or (not self._is_batch_set()):
            return False
        else:
            batch_status = self._is_batch_in_database(self._batch_name)
            if batch_status:
                # table is loaded
                return True
            elif batch_status is None:
                return False
            else:
                self.log.error(
                    f"The batch '{self._simulation}'/'{self._batch_name}' is not loaded into the database."
                )
                return False

    def get_connection(self):
        """
        Return connection to the PostgreSQL database.

        Get connection to the database to execute your own queries.

        Returns
        -------
        connection : psycopg2.extensions.connection or None
            The connection object for the database, or None if the connection fails.

        Examples
        --------
        Get connection to the database and query first 5 rows of the batch "batch_1" from the "simulation_cannon_numeric" simulation:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> curs = citros.get_connection().cursor()
        >>> curs.execute('SELECT * FROM "simulation_cannon_numeric"."batch_1" LIMIT 5')
        >>> D = curs.fetchall()
        >>> print(D)
        [(1, 0, 0, 0, '/config', '.citros/data/... ]

        The result of the curs.fetchall() is a list, which can easily be converted into a pandas DataFrame if needed:

        >>> import pandas as pd
        >>> df = pd.DataFrame(D)
        """
        connection = self.connect()
        if self._debug_connect and connection is not None:
            _PgCursor.n_pg_connections += 1
        return connection

    # Simulations

    def simulation(self, simulation: str = None, inplace: bool = False):
        """
        Set batch to the CitrosDB object.

        Parameters
        ----------
        simulation : str
            Name of the simulation.
        inplace : bool, default False
            If True, set simulation name to the current CitrosDB object, otherwise returns new CitrosDB
            object with set simulation.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set simulation or None, if `inplace` = True.

        Examples
        --------
        Show information about the batch 'test' that was created in 'simulation_cannon_analytic' simulation:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.simulation('simulation_cannon_analytic').batch('test').info().print()
        {
         'size': '629 kB',
         'sid_count': 1,
         'sid_list': [0],
         'topic_count': 3,
         'topic_list': ['/cannon/state', '/config', '/scheduler'],
         'message_count': 3835
        }

        Set simulation 'simulation_cannon_analytic' to the already existing `CitrosDB()` object and Show information about the batch 'test':

        >>> citros = CitrosDB()
        >>> citros.simulation('simulation_cannon_analytic', inplace = True)
        >>> citros.batch('test').info().print()
        {
         'size': '629 kB',
         'sid_count': 1,
         'sid_list': [0],
         'topic_count': 3,
         'topic_list': ['/cannon/state', '/config', '/scheduler'],
         'message_count': 3835
        }
        """
        if inplace:
            self._set_simulation(simulation)
            return None
        else:
            ci = self._copy()
            ci._set_simulation(simulation)
            return ci

    def get_simulation(self):
        """
        Get information about the current simulation if the simulation is set.

        Returns
        -------
        simulation : access.citros_dict.CitrosDict
            Dict with the simulation name.

        Examples
        --------
        Get the name of the simulation that was set during initialization of CitrosDB object:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'simulation_cannon_analytic')
        >>> citros.get_simulation()
        {'name': 'simulation_cannon_analytic'}
        """
        return CitrosDict({"name": self._simulation})

    def get_simulation_name(self):
        """
        Get the simulation name if the simulation is set.

        Returns
        -------
        name : str
            Name of the simulation. If the simulation is not set, return None.

        Examples
        --------
        Get the name of the simulation that was set during initialization of CitrosDB object:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'simulation_cannon_analytic')
        >>> citros.get_simulation_name()
        'simulation_cannon_analytic'
        """
        return self._simulation

    # Batches

    def batch(self, batch: str = None, inplace: bool = False) -> Optional[CitrosDB]:
        """
        Set batch name to the CitrosDB object.

        Parameters
        ----------
        batch : str
            Name of the batch.
        inplace : bool, default False
            If True, set batch name to the current CitrosDB object, otherwise returns new CitrosDB object with
            set batch name.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set batch id or None, if `inplace` = True.

        See Also
        --------
        CitrosDB.simulation, CitrosDB.topic, CitrosDB.sid, CitrosDB.rid, CitrosDB.time

        Examples
        --------
        Get data for topic 'A' from the batch 'test' of the simulation 'simulation_cannon_analytic':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('simulation_cannon_analytic').batch('test').topic('A').data()

        Set batch name 'test' to the already existing `CitrosDB()` object and query data for simulation simulation 'simulation_cannon_analytic' from the topic 'A':

        >>> citros = CitrosDB()
        >>> citros.batch('test', inplace = True)
        >>> df = citros.simulation('simulation_cannon_analytic').topic('A').data()
        """
        if inplace:
            self._set_batch(batch)
            return None
        else:
            ci = self._copy()
            ci._set_batch(batch)
            return ci

    def get_batch_name(self):
        """
        Get the name of the current batch if the batch is set.

        Returns
        -------
        name : str
            Name of the current batch. If the batch is not set, return None.

        Examples
        --------
        Get name of the previously set batch:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(batch = 'galaxies')
        >>> citros.get_batch_name()
        'galaxies'
        """
        return self._batch_name

    def get_batch_sizes(self):
        """
        Return sizes of the batches according to simulation() and batch() settings.

        Print table with batch names, batch sizes and total batch sizes with indexes.

        See Also
        --------
        CitrosDB.simulation, CitrosDB.batch

        Examples
        --------
        Display sizes of the all batches:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.get_batch_sizes()
        +-----------+-------------+------------+
        | batch     | size        | total size |
        +-----------+-------------+------------+
        | stars     | 32 kB       | 64 kB      |
        | galaxies  | 8192 bytes  | 16 kB      |
        +-----------+-------------+------------+

        Display sizes of the batches of the simulation 'simulation_star':

        >>> citros.simulation('simulation_star').get_batch_sizes()
        +--------+-------------+------------+
        | batch  | size        | total size |
        +--------+-------------+------------+
        | stars  | 32 kB       | 64 kB      |
        +--------+-------------+------------+

        Display size of the batch "galaxies":

        >>> citros.batch("galaxies").get_batch_sizes()
        +-----------+-------------+------------+
        | batch     | size        | total size |
        +-----------+-------------+------------+
        | galaxies  | 8192 bytes  | 16 kB      |
        +-----------+-------------+------------+
        """
        table_to_display = self._get_batch_sizes()
        table = PrettyTable(field_names=["batch", "size", "total size"], align="l")
        if table_to_display is not None:
            table.add_rows(table_to_display)
        print(table)

    # Filters

    def topic(self, topic_name: Optional[Union[str, list]] = None) -> CitrosDB:
        """
        Select topic.

        Parameters
        ----------
        topic_name : str or list of str
            Name of the topic.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set 'topic' parameter.

        See Also
        --------
        CitrosDB.sid : set sid values to query
        CitrosDB.rid : set rid values to query
        CitrosDB.time : set time constraints
        CitrosDB.set_filter : set constraints on query
        CitrosDB.set_order : set order of the output

        Examples
        --------
        Get data for topic name 'A' from batch 'dynamics' of the simulation 'engine_system':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('engine_system').batch('dynamics').topic('A').data()

        Get maximum value of the 'sid' among topics 'A' and 'B':

        >>> citros.simulation('engine_system').batch('dynamics').topic(['A', 'B']).get_max_value('sid')
        3
        """
        ci = self._copy()
        _PgCursor.topic(ci, topic_name=topic_name)
        return ci

    def sid(
        self,
        value: Optional[Union[int, list]] = None,
        start: int = 0,
        end: int = None,
        count: int = None,
    ) -> CitrosDB:
        """
        Set constraints on sid.

        Parameters
        ----------
        value : int or list of ints, optional
            Exact values of sid.
            If nothing is passed, then the default value of sid is used (ENV parameter "CITROS_SIMULATION_RUN_ID").
            If the default value does not exist, no limits for sid are applied.
        start : int, default 0
            The lower limit for sid values.
        end : int, optional
            The higher limit for sid, the end is included.
        count : int, optional
            Used only if the `end` is not set.
            Number of sid to return in the query, starting form the `start`.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set 'sid' parameter.

        See Also
        --------
        CitrosDB.topic : set topic name to query
        CitrosDB.rid : set rid values to query
        CitrosDB.time : set time constraints
        CitrosDB.set_filter : set constraints on query
        CitrosDB.set_order : set order of the output

        Examples
        --------
        Get data from batch 'robotics' of the simulation 'robot' for topic 'A' where sid values are 1 or 2:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('robot').batch('robotics').topic('A').sid([1,2]).data()

        Get data from batch 'robotics' for for topic 'A' where sid is in the range of 3 <= sid <= 8 :

        >>> citros = CitrosDB()
        >>> df = citros.simulation('robot').batch('robotics').topic('A').sid(start = 3, end = 8).data()

        or the same with `count`:

        >>> df = citros.simulation('robot').batch('robotics').topic('A').sid(start = 3, count = 6).data()

        For sid >= 7:

        >>> df = citros.simulation('robot').batch('robotics').topic('A').sid(start = 7).data()
        """
        ci = self._copy()
        _PgCursor.sid(ci, value=value, start=start, end=end, count=count)
        return ci

    def rid(
        self,
        value: Optional[Union[int, list]] = None,
        start: int = 0,
        end: int = None,
        count: int = None,
    ) -> CitrosDB:
        """
        Set constraints on rid.

        Parameters
        ----------
        value : int or list of ints, optional
            Exact values of rid.
        start : int, default 0
            The lower limit for rid values.
        end : int, optional
            The higher limit for rid, the end is included.
        count : int, optional
            Used only if the `end` is not set.
            Number of rid to return in the query, starting form the `start`.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set 'rid' parameter.

        See Also
        --------
        CitrosDB.topic : set topic name to query
        CitrosDB.sid : set sid values to query
        CitrosDB.time : set time constraints
        CitrosDB.set_filter : set constraints on query
        CitrosDB.set_order : set order of the output

        Examples
        --------
        Get data from the batch 'aero' of the simulation 'plane_test' for topic 'A' where rid values are 10 or 20:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'plane_test')
        >>> df = citros.batch('aero').topic('A').rid([10, 20]).data()

        Get data from batch 'aero' for topic 'A' where rid is in the range of 0 <= rid <= 9 :

        >>> citros = CitrosDB()
        >>> df = citros.simulation('plane_test').batch('aero').topic('A').rid(start = 0, end = 9).data()

        or the same with `count`:

        >>> df = citros.simulation('plane_test').batch('aero').topic('A').rid(start = 0, count = 10).data()

        For rid >= 5:

        >>> df = citros.simulation('plane_test').batch('aero').topic('A').rid(start = 5).data()
        """
        ci = self._copy()
        _PgCursor.rid(ci, value=value, start=start, end=end, count=count)
        return ci

    def time(self, start: int = 0, end: int = None, duration: int = None) -> CitrosDB:
        """
        Set constraints on time.

        Parameters
        ----------
        start : int, default 0
            The lower limit for time values.
        end : int, optional
            The higher limit for time, the end is included.
        duration : int, optional
            Used only if the `end` is not set.
            Time interval to return in the query, starting form the `start`.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set 'time' parameter.

        See Also
        --------
        CitrosDB.topic : set topic name to query
        CitrosDB.sid : set sid values to query
        CitrosDB.rid : set rid values to query
        CitrosDB.set_filter : set constraints on query
        CitrosDB.set_order : set order of the output

        Examples
        --------
        Get data from the batch 'kinematics' of the simulation 'radar' for topic 'A' where time is in the range 10ns <= time <= 20ns:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('radar').batch('kinematics').topic('A').time(start = 10, end = 20).data()

        To set time range 'first 10ns starting from 10th nanosecond', that means 10ns <= time < 20ns:

        >>> df = citros.simulation('radar').batch('kinematics').topic('A').time(start = 10, duration = 10).data()

        For time >= 20:

        >>> df = citros.simulation('radar').batch('kinematics').topic('A').time(start = 20).data()
        """
        ci = self._copy()
        _PgCursor.time(ci, start=start, end=end, duration=duration)
        return ci

    def set_filter(self, filter_by: dict = None) -> CitrosDB:
        """
        Set constraints on query.

        Allows to set constraints on json-data columns before querying.

        Parameters
        ----------
        filter_by : dict
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()` and `time()` and will override them.
            If one of the sampling method is used (`skip()`, `avg()` or `move_avg()`), constraints on additional columns (rid, sid, time) are applied
            BEFORE sampling while constraints on columns from json-data are applied AFTER sampling.

        Returns
        -------
        out : CitrosDB
            CitrosDB with set constraints.

        See Also
        --------
        CitrosDB.topic : set topic name to query
        CitrosDB.sid : set sid values to query
        CitrosDB.rid : set rid values to query
        CitrosDB.time : set time constraints
        CitrosDB.set_order : set order of the output

        Examples
        --------
        If the structure of the data column in the simulation 'simulation_cannon_analytic' is the following:

        ```python
        {x: {x_1: 11}, note: [13, 34]}
        {x: {x_1: 22}, note: [11, 35]}
        {x: {x_1: 12}, note: [12, 36]}
        ...
        ```
        to get data of the batch 'testing' for topic 'A' where values of json-data column 10 < data.x.x_1 <= 20:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'simulation_cannon_analytic')
        >>> citros.batch('testing').topic('A').set_filter({'data.x.x_1': {'>': 10, '<=': 20}}).data()
             sid  rid  time topic type  data.x.x_1     data.note
        0      0    0  4862     A    a          11      [13, 34]
        1      0    2  7879     A    a          12      [12, 36]
        ...

        get data where the value on the first position in the json-array 'note' equals 11 or 12:

        >>> citros.batch('testing').topic('A').set_filter({'data.note[0]': [11, 12]}).data()
             sid  rid  time topic type  data.x.x_1     data.note
        0      0    1  4862     A    a          22      [11, 35]
        1      0    2  7879     A    a          12      [12, 36]
        ...
        """
        ci = self._copy()
        _PgCursor.set_filter(ci, filter_by=filter_by)
        return ci

    def set_order(self, order_by: Optional[Union[str, list, dict]] = None) -> CitrosDB:
        """
        Apply sorting to the result of the data querying.

        Sort the result of the query in ascending or descending order.

        Parameters
        ----------
        order_by : str, list of str or dict, optional
            If `order_by` is a single string or a list of strings, it represents the column label(s) by which the result is sorted in ascending order.
            For more control, use a dictionary with column labels as keys and values ('asc' for ascending, 'desc' for descending) to define the sorting order.

        See Also
        --------
        CitrosDB.topic : set topic name to query
        CitrosDB.sid : set sid values to query
        CitrosDB.rid : set rid values to query
        CitrosDB.time : set time constraints
        CitrosDB.set_filter : set constraints on query

        Examples
        --------
        Get data from the batch 'aerodynamics' of the simulation 'starship' for topic 'A' and sort the result by sid in ascending order and by rid in descending order.

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('starship').batch('aerodynamics').topic('A').set_order({'sid': 'asc', 'rid': 'desc'}).data()

        Sort the result by sid and rid in ascending order:

        >>> citros = CitrosDB(simulation = 'starship')
        >>> df = citros.batch('aerodynamics').topic('A').set_order(['sid', 'rid']).data()
        """
        ci = self._copy()
        _PgCursor.set_order(ci, order_by=order_by)
        return ci

    # Sampling

    def skip(self, s: int = None):
        """
        Select each `s`-th message.

        `skip` is aimed to reduce the number of rows in the query output.
        This method should be called before querying methods `data()` or `data_dict()`.
        Messages with different sids are selected separately.
        If any constraints on 'sid', 'rid', 'time', 'topic' and 'type' columns are set, they are applied before sampling, while constraints on data from json column are applied after sampling.

        Parameters
        ----------
        s : int, optional
            Control number of the messages to skip, only every `s`-th message will be selected.

        Returns
        -------
        out : CitrosDB
            CitrosDB with parameters set for sampling method 'skip'.

        See Also
        --------
        CitrosDB.avg, CitrosDB.move_avg, CitrosDB.data, CitrosDB.data_dict

        Examples
        --------
        Get every 3th message of the topic 'A' of the batch 'velocity' of the simulation 'mechanics':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'mechanics', batch = 'velocity')
        >>> df = citros.topic('A').skip(3).data()
        the 1th, the 4th, the 7th ... messages will be selected
        """
        ci = self._copy()
        _PgCursor.skip(ci, n_skip=s)
        return ci

    def avg(self, n: int = None) -> CitrosDB:
        """
        Set the directive to group and average every set of `n` consecutive messages in the database before querying.

        `avg()` is aimed to reduce number of rows before querying.
        This method should be called before querying methods `data()` or `data_dict()`.
        Messages with different sids are processed separately.
        While averaging, the value in the 'rid' column is determined by taking the minimum 'rid' value from the rows being averaged.
        If any constraints on 'sid', 'rid', 'time', 'topic' and 'type' columns are set, they are applied before sampling, while constraints on data from json column are applied after sampling.

        Parameters
        ----------
        n : int
            Number of messages to average.

        Returns
        -------
        out : CitrosDB
            CitrosDB with parameters set for sampling method 'avg'.

        See Also
        --------
        CitrosDB.skip, CitrosDB.move_avg, CitrosDB.data, CitrosDB.data_dict

        Examples
        --------
        Average each 3 messages of the topic 'A' from the batch 'velocity' from the simulation 'mechanics' and then query the result:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('mechanics').batch('velocity').topic('A').avg(3).data()
        """
        ci = self._copy()
        _PgCursor.avg(ci, n_avg=n)
        return ci

    def move_avg(self, n: int = None, s: int = 1):
        """
        Set the directive to compute moving average with the window size equals `n` and then during querying select each `s`-th message of the result.

        `move_avg()` is aimed to smooth data and reduce number of rows in the query output.
        This method should be called before querying methods `data()` or `data_dict()`.
        Messages with different sids are processed separately.
        While averaging, the value in the 'rid' column is determined by taking the minimum 'rid' value from the rows being averaged.
        If any constraints on 'sid', 'rid', 'time', 'topic' and 'type' columns are set, they are applied before sampling, while constraints on data from json column are applied after sampling.

        Parameters
        ----------
        n : int, optional
            Number of messages to average.
        s : int, default 1
            Control number of the messages to skip, only every `s`-th message will be selected.

        Returns
        -------
        out : CitrosDB
            CitrosDB with parameters set for sampling method 'move_avg'.

        See Also
        --------
        CitrosDB.skip, CitrosDB.avg, CitrosDB.data, CitrosDB.data_dict

        Examples
        --------
        In the batch 'coords' in the simulation 'pendulum' for data in topic 'A' calculate moving average with the window equals 5
        and select every second row of the result:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('pendulum').batch('coords').topic('A').move_avg(5,2).data()
        """
        ci = self._copy()
        _PgCursor.move_avg(ci, n_avg=n, n_skip=s)
        return ci

    # Data Information

    def info(self) -> CitrosDict:
        """
        Return information about the batch, based on the configurations set by topic(), rid(), sid() and time() methods.

        The output is a dictionary, that contains:
        ```python
        'size': size of the selected data,
        'sid_count': number of sids,
        'sid_list': list of the sids,
        'topic_count': number of topics,
        'topic_list': list of topics,
        'message_count': number of messages
        ```
        If specific sid is set, also appends dictionary 'sids', with the following structure:
        ```python
        'sids': {
          <sid, int>: {
            'topics': {
              <topic_name, str>: {
                'message_count': number of messages,
                'start_time': time when simulation started,
                'end_time': time when simulation ended,
                'duration': duration of the simulation process,
                'frequency': frequency of the simulation process (in Hz)}}}}
        ```
        If topic is specified, appends dictionary 'topics':
        ```python
        'topics': {
          <topic_name, str>: {
            'type': type,
            'data_structure': structure of the data,
            'message_count': number of messages}}
        ```
        If the topic has multiple types with the same data structure, they are presented in
        'type' as a list. If the types have different data structures, they are grouped by
        their data structure types and numbered as "type_group_0", "type_group_1", and so on:
        ```python
        'topics': {
          <topic_name, str>: {
            "type_group_0": {
              'type': type,
              'data_structure': structure of the data,
              'message_count': number of messages},
            "type_group_1": {
              'type': type,
              'data_structure': structure of the data,
              'message_count': number of messages}}}
        ```

        Returns
        -------
        out : access.citros_dict.CitrosDict
            Information about the batch.

        Examples
        --------
        Display information about the batch 'dynamics' of the simulation 'mechanics':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.simulation('mechanics').batch('dynamics').info().print()
        {
         'size': '27 kB',
         'sid_count': 3,
         'sid_list': [1, 2, 3],
         'topic_count': 4,
         'topic_list': ['A', 'B', 'C', 'D'],
         'message_count': 100
        }

        Display information about topic 'C' of the batch 'dynamics':

        >>> citros.simulation('mechanics').batch('dynamics').topic('C').info().print()
        {
         'size': '6576 bytes',
         'sid_count': 3,
         'sid_list': [1, 2, 3],
         'topic_count': 1,
         'topic_list': ['C'],
         'message_count': 24,
         'topics': {
           'C': {
             'type': 'c',
             'data_structure': {
               'data': {
                 'x': {
                   'x_1': 'int',
                   'x_2': 'float',
                   'x_3': 'float'
                 },
                 'note': 'list',
                 'time': 'float',
                 'height': 'float'
               }
             },
             'message_count': 24
           }
         }
        }

        Display information about simulation run 1 and 2 of the batch 'dynamics':

        >>> citros.simulation('mechanics').batch('dynamics').sid([1,2]).info().print()
        {
         'size': '20 kB',
         'sid_count': 2,
         'sid_list': [1, 2],
         'topic_count': 4,
         'topic_list': ['A', 'B', 'C', 'D'],
         'message_count': 76,
         'sids': {
           1: {
             'topics': {
               'A': {
                  'message_count': 4,
                  'start_time': 2000000000,
                  'end_time': 17000000000,
                  'duration': 15000000000,
                  'frequency': 0.267
               },
               'B': {
                  'message_count': 9,
        ...
                  'duration': 150000000,
                  'frequency': 60.0
               }
             }
           }
         }
        }

        Display information about simulation run 2 of the topic 'C' of the batch 'dynamics':

        >>> citros.simulation('mechanics').batch('dynamics').topic('C').sid(2).info().print()
        {
         'size': '2192 bytes',
         'sid_count': 1,
         'sid_list': [2],
         'topic_count': 1,
         'topic_list': ['C'],
         'message_count': 8,
         'sids': {
           2: {
             'topics': {
               'C': {
                 'message_count': 8,
                 'start_time': 7000000170,
                 'end_time': 19000000800,
                 'duration': 12000000630,
                 'frequency': 0.667
               }
             }
           }
         },
         'topics': {
           'C': {
             'type': 'c',
             'data_structure': {
               'data': {
                 'x': {
                   'x_1': 'int',
                   'x_2': 'float',
                   'x_3': 'float'
                 },
                 'note': 'list',
                 'time': 'float',
                 'height': 'float'
                 }
               },
             'message_count': 8
           }
         }
        }
        """
        if not self._is_batch_available():
            return CitrosDict({})
        result = _PgCursor._pg_info(self)
        return result

    def get_data_structure(self, topic: str = None):
        """
        Display table with topic names, types and corresponding them data structures of the json-data columns for the specific batch.

        Batch must be set during initialization of CitrosDB object or by `batch()` method.

        Parameters
        ----------
        topic : list or list of str, optional
            List of the topics to show data structure for.
            Have higher priority, than those defined by `topic()` and `set_filter()` methods
            and will override them.
            If not specified, shows data structure for all topics.

        See Also
        --------
        CitrosDB.simulation, CitrosDB.batch

        Examples
        --------
        Print structure of the json-data column for topics 'A' and 'C' of the batch 'kinematics' of the simulation 'mechanics':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'mechanics')
        >>> citros.batch('kinematics').topic(['A', 'C']).get_data_structure()

        or

        >>> citros.batch('kinematics').get_data_structure(['A', 'C'])
        +-------+------+-----------------+
        | topic | type | data            |
        +-------+------+-----------------+
        |     A |    a | {               |
        |       |      |   x: {          |
        |       |      |     x_1: float, |
        |       |      |     x_2: float, |
        |       |      |     x_3: float  |
        |       |      |   },            |
        |       |      |   note: list,   |
        |       |      |   time: float,  |
        |       |      |   height: float |
        |       |      | }               |
        +-------+------+-----------------+
        |     C |    c | {               |
        |       |      |   x: {          |
        |       |      |     x_1: float, |
        |       |      |     x_2: float, |
        |       |      |     x_3: float  |
        |       |      |   },            |
        |       |      |   note: list,   |
        |       |      |   time: float,  |
        |       |      |   height: float |
        |       |      | }               |
        +-------+------+-----------------+
        """
        if not self._is_batch_available():
            return None
        _PgCursor._pg_get_data_structure(self, topic=topic)

    # Query

    def data(
        self, data_names: list = None, additional_columns: list = None
    ) -> pd.DataFrame:
        """
        Return pandas.DataFrame with data.

        Query data according to the constraints set by `batch()`, `topic()`, `rid()`, `sid()` and `time()` methods
        and one of the aggregative methods `skip()`, `avg()` or `move_avg()`.
        The order of the output can be set by `set_order()` method, be default the output is ordered by 'sid' and 'rid' columns.

        Parameters
        ----------
        data_names : list, optional
            Labels of the columns from json data column.
        additional_columns : list, optional
            Columns to download outside the json data column: `sid`, `rid`, `time`, `topic`, `type`.
            `sid` column is always queried.
            If not specified then all additional columns are queried.

        Returns
        -------
        out : pandas.DataFrame
            Table with selected data.

        See Also
        --------
        CitrosDB.batch, CitrosDB.topic, CitrosDB.rid, CitrosDB.sid, CitrosDB.time, CitrosDB.skip, CitrosDB.avg, CitrosDB.move_avg, CitrosDB.set_order,
        CitrosDB.data_dict

        Examples
        --------
        If the structure of the data column in the batch 'dynamics' in the simulation 'airship' in the topic 'A' is the following:
        
        ```python
        {x: {x_1: 1}, note: ['a', 'b']}
        {x: {x_1: 2}, note: ['c', 'd']}
        ...
        ```
        to get the column with the values of json-object 'x_1'
        and the column with the values from the first position in the json-array 'note':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'airship')
        >>> df = citros.batch('dynamics').topic('A').data(["data.x.x_1", "data.note[0]"])
        >>> df
             sid  rid  time topic type  data.x.x_1  data.note[0]
        0      0    0  4862     A    a           1             a
        1      0    1  7749     A    a           2             c
        ...

        Get the whole 'data' column with json-objects divided into separate columns:
        
        >>> df = citros.batch('dynamics').topic('A').data()
        >>> df
             sid  rid  time topic type  data.x.x_1  data.note
        0      0    0  4862     A    a           1     [a, b]
        1      0    1  7749     A    a           2     [c, d]
        ...

        Get the whole 'data' column as a json-object:
        
        >>> df = citros.batch('dynamics').topic('A').data(["data"])
        >>> df
             sid  rid  time topic type                             data
        0      0    0  4862     A    a  {x: {x_1: 1}, note: ['a', 'b']}
        1      0    1  7749     A    a  {x: {x_1: 2}, note: ['c', 'd']}
        ...

        Besides the json data column, there are some additional columns: simulation run id (sid), rid, time, topic, and type. 
        By default, all of them are queried. To select only particular ones, use `additional_columns` parameter 
        (note that the 'sid' column is always queried):

        >>> dfs = citros.batch('dynamics').topic('A').set_order({'rid': 'asc'}).avg(2)\\
                        .data(['data.x.x_1', 'data.x.x_2'], additional_columns = ['rid', 'topic'])
        >>> dfs[2]
             sid  rid  topic  data.x.x_1  data.x.x_2
        0      2    0      A         1.5           8
        1      2    2      A           5          10
        ...
        """
        if not self._is_batch_available():
            return None
        result = _PgCursor._data(
            self, data_names=data_names, additional_columns=additional_columns
        )
        return result

    def data_dict(
        self, data_names: list = None, additional_columns: list = None
    ) -> pd.DataFrame:
        """
        Return a dict where a dict key is a simulation run id (sid), and a dict value is a pandas.DataFrame related to that sid.

        Parameters
        ----------
        data_names : list, optional
            Labels of the columns from json data column.
        additional_columns : list, optional
            Columns to download outside the json data column: `sid`, `rid`, `time`, `topic`, `type`.
            `sid` column is always queried.
            If not specified then all additional columns are queried.

        Returns
        -------
        out : dict of pandas.DataFrames
            dict with tables, key is a value of sid.

        See Also
        --------
        CitrosDB.batch, CitrosDB.topic, CitrosDB.rid, CitrosDB.sid, CitrosDB.time, CitrosDB.skip, CitrosDB.avg, CitrosDB.move_avg, CitrosDB.set_order,
        CitrosDB.data

        Examples
        --------
        Let's suppose that the structure of the data column in the batch 'dynamics' in the simulation 'airship' for simulation run sid = 2 in the topic 'A' is the following:
        
        ```python
        {x: {x_1: 1, x_2: 3}
        {x: {x_1: 2, x_2: 13}
        {x: {x_1: 4, x_2: 15}
        {x: {x_1: 6, x_2: 5}
        ...
        ```

        Download averaged data for each sid separately, return output in ascending order by 'rid':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'airship')
        >>> dfs = citros.batch('dynamics').topic('A').set_order({'rid': 'asc'}).avg(2)\\
                        .data_dict(['data.x.x_1', 'data.x.x_2'])

        Print sid values:

        >>> print(f'sid values are: {list(dfs.keys())}')
        sid values are: [1, 2, 3, 4]

        Get table corresponding to the sid = 2:

        >>> dfs[2]
             sid  rid  time topic type  data.x.x_1  data.x.x_2
        0      2    0  6305     A    a         1.5           8
        1      2    2  7780     A    a           5          10
        ...

        Besides the json data column, there are some additional columns: simulation run id (sid), rid, time, topic, and type. 
        By default, all of them are queried. To select only particular ones, use `additional_columns` parameter 
        (note that the 'sid' column is always queried):

        >>> dfs = citros.batch('dynamics').topic('A').set_order({'rid': 'asc'}).avg(2)\\
                        .data_dict(['data.x.x_1', 'data.x.x_2'], additional_columns = ['rid', 'topic'])
        >>> dfs[2]
             sid  rid  topic  data.x.x_1  data.x.x_2
        0      2    0      A         1.5           8
        1      2    2      A           5          10
        ...
        """
        if not self._is_batch_available():
            return {}
        result_table = _PgCursor._data(
            self, data_names=data_names, additional_columns=additional_columns
        )

        if result_table is not None:
            sid_list = list(set(result_table["sid"]))
            tables = {}
            for s in sid_list:
                flag = result_table["sid"] == s
                tables[s] = result_table[flag].reset_index(drop=True)
            return tables
        else:
            return {}

    def get_min_value(
        self, column_name: str, filter_by: dict = None, return_index: bool = False
    ):
        """
        Return minimum value of the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        return_index : bool, default False
            If True, the pair of sid and rid corresponding to the obtained minimum value is also returned.
            If there are several cases when the maximum or minimum value is reached, the lists of corresponding sids and rids are returned.

        Returns
        -------
        value : int, float, str or None
            Minimum value of the column `column_name`.
        sid : int or list
            Corresponding to the minimum value's sid. Returns only if `return_index` is set to True.
        rid : int or list
            Corresponding to the minimum value's rid. Returns only if `return_index` is set to True.

        Examples
        --------
        For batch 'test_vel' of the simulation 'car_motion' get min value of the column 'data.x.x_2' where topics are 'A' or 'B', 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation ='car_motion', batch = 'test_vel')
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_min_value('data.x.x_2')
        >>> print(result)
        -4.0

        Get also the sid and rid of the minimum value:

        >>> result, sid_min, rid_min = citros.topic(['A', 'B'])\\
        ...                            .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                            .time(start = 10, end = 5000)\\
        ...                            .get_min_value('data.x.x_2', return_index = True)
        >>> print(f"min = {result} at sid = {sid_min}, rid = {rid_min}")
        min = -4.0 at sid = 4, rid = 44

        The same as in the first example, but passing all constraints by `filter_by` parameter:

        >>> result = citros.get_min_value('data.x.x_2',
        ...                               filter_by = {'topic': ['A', 'B'], 
        ...                                            'time': {'>=': 10, '<=': 5000}, 
        ...                                            'data.x.x_1' : {'>':10}})
        >>> print(result)
        -4.0
        """
        if not self._is_batch_available():
            return None, None, None if return_index else None

        result = _PgCursor._get_min_max_value(
            self,
            column_name=column_name,
            filter_by=filter_by,
            return_index=return_index,
            mode="MIN",
        )
        return result

    def get_max_value(
        self, column_name: str, filter_by: dict = None, return_index: bool = False
    ):
        """
        Return maximum value of the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        return_index : bool, default False
            If True, the pair of sid and rid corresponding to the obtained maximum value is also returned.

        Returns
        -------
        value : int, float, str or None
            Maximum value of the column `column_name`.
        sid : int or list
            Corresponding to the maximum value's sid. Returns only if `return_index` is set to True.
        rid : int or list
            Corresponding to the maximum value's rid. Returns only if `return_index` is set to True

        Examples
        --------
        For batch 'test_vel' of the simulation 'car_motion' get max value of the column 'data.x.x_2' where topics are 'A' or 'B', 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation ='car_motion', batch = 'test_vel')
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_max_value('data.x.x_2')
        >>> print(result)
        76.0

        Get also the sid and rid of the maximum value:

        >>> result, sid_max, rid_max = citros.topic(['A', 'B'])\\
        ...                            .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                            .time(start = 10, end = 5000)\\
        ...                            .get_max_value('data.x.x_2', return_index = True)
        >>> print(f"max = {result} at sid = {sid_max}, rid = {rid_max}")
        max = 76.0 at sid = 4, rid = 47

        The same as in the first example, but passing all constraints by `filter_by` parameter:

        >>> result = citros.get_max_value('data.x.x_2',
        ...                               filter_by = {'topic': ['A', 'B'], 
        ...                                            'time': {'>=': 10, '<=': 5000}, 
        ...                                            'data.x.x_1' : {'>':10}})
        >>> print(result)
        76.0
        """
        if not self._is_batch_available():
            return None, None, None if return_index else None
        result = _PgCursor._get_min_max_value(
            self,
            column_name=column_name,
            filter_by=filter_by,
            return_index=return_index,
            mode="MAX",
        )
        return result

    def get_counts(
        self,
        column_name: str = None,
        group_by: Optional[Union[str, list]] = None,
        filter_by: dict = None,
        nan_exclude: bool = False,
    ) -> list:
        """
        Return number of the rows in the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        group_by : list, optional
            Labels of the columns to group by. If blank, do not group.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        nan_exclude : bool, default False
            If True, nan values are excluded from the count.

        Returns
        -------
        out : list of tuples or None
            Number of rows in `column_name`.

        Examples
        --------
        Calculate the total number of rows for batch 'test_vel' of the simulation 'car_engine':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.simulation('car_engine').batch('test_vel').get_counts()
        [(300,)]

        Calculate the total number of rows in the topic 'A':

        >>> citros = CitrosDB()
        >>> citros.simulation('car_engine').batch('test_vel').topic('A').get_counts()
        [(100,)]

        If the structure of the data column for the batch 'test_vel' of the simulation 'car_engine' is the following:

        ```python
        {x: {x_1: 52}, note: ['b', 'e']}
        {x: {x_1: 11}, note: ['a', 'c']}
        {x: {x_1: 92}, note: ['b', 'd']}
        ...
        ```
        to find the number of values from the first position of the json-array 'note' for topics 'A' or 'B',
        where 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> citros = CitrosDB(simulation = 'car_engine', batch = 'test_vel')
        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_counts('data.note[0]')
        [(30,)]

        To perform under the same conditions, but to get values grouped by topics:

        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_counts('data.note[0]', group_by = ['topic'])
        [('A', 17), ('B', 13)]

        The same, but passing all constraints by `filter_by` parameter:
        
        >>> citros.get_counts('data.note[0]',
        ...                    group_by = ['topic'],
        ...                    filter_by = {'topic': ['A', 'B'], 
        ...                                 'time': {'>=': 10, '<=': 5000}, 
        ...                                 'data.x.x_1' : {'>':10}})
        [('A', 17), ('B', 13)]
        """
        if not self._is_batch_available():
            return None
        result = _PgCursor._get_counts(
            self,
            column_name=column_name,
            group_by=group_by,
            filter_by=filter_by,
            nan_exclude=nan_exclude,
        )
        return result

    def get_unique_counts(
        self,
        column_name: str = None,
        group_by: list = None,
        filter_by: dict = None,
        nan_exclude: bool = False,
    ) -> list:
        """
        Return number of the unique values in the column `column_name`.

        Parameters
        ----------
        column_name : str
            Column to count its unique values.
        group_by : list, optional
            Labels of the columns to group by. If blank, do not group.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        nan_exclude : bool, default False
            If True, nan values are excluded from the count.

        Returns
        -------
        out : list of tuples or None
            Counts of the unique values in `column_name`.

        Examples
        --------
        If the structure of the data column for the batch 'test_vel' of the simulation 'car_engine' is the following:

        ```python
        {x: {x_1: 52}, note: ['b', 'e']}
        {x: {x_1: 11}, note: ['a', 'c']}
        {x: {x_1: 92}, note: ['b', 'd']}
        ...
        ```
        to get the number of unique values from the first position of the json-array 'note' for topics 'A' or 'B',
        where 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'car_engine', batch = 'test_vel')
        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_unique_counts('data.note[0]')
        [(2,)]

        To perform under the same conditions, but to get values grouped by topics:

        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_unique_counts('data.note[0]', group_by = ['topic'])
        [('A', 2), ('B', 2)]
        
        The same, but passing all constraints by `filter_by` parameter:

        >>> citros.get_unique_counts('data.note[0]',
        ...                           group_by = ['topic'],
        ...                           filter_by = {'topic': ['A', 'B'], 
        ...                                        'time': {'>=': 10, '<=': 5000}, 
        ...                                        'data.x.x_1' : {'>':10}})
        [('A', 2), ('B', 2)]
        """
        if not self._is_batch_available():
            return None
        result = _PgCursor._get_unique_counts(
            self,
            column_name=column_name,
            group_by=group_by,
            filter_by=filter_by,
            nan_exclude=nan_exclude,
        )
        return result

    def get_unique_values(
        self, column_names: Optional[Union[str, list]], filter_by: dict = None
    ) -> list:
        """
        Return unique values of the columns `column_names`.

        Parameters
        ----------
        column_names : str or list of str
            Columns for which the unique combinations of the values will be found.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}, where:
            - key_n - must match labels of the columns,
            - value_n  - in the case of equality: list of exact values,
                       in the case of inequality: dict with ">", ">=", "<" or "<=".
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.

        Returns
        -------
        out : list or list of tuples
            Each tuple contains unique combinations of the values for `column_names`.

        Examples
        --------
        Get unique values of type for the batch 'angles' of the simulation 'aircraft' for topics 'A' or 'B', where 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'aircraft', batch = 'angles')
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_unique_values(['type'])
        >>> print(result)
        ['a', 'b']

        The same, but passing all constraints by `filter_by` parameter:
        
        >>> result = citros.get_unique_values(['type'], filter_by = {'topic': ['A', 'B'], 
        ...                                       'time': {'>=': 10, '<=': 5000}, 
        ...                                       'data.x.x_1': {'>':10}})
        >>> print(result)
        ['a', 'b']
        """
        if not self._is_batch_available():
            return None
        result = _PgCursor._get_unique_values(
            self, column_names=column_names, filter_by=filter_by
        )
        return result

    # Plots

    def time_plot(
        self,
        ax: plt.Axes,
        *args,
        topic_name: Optional[str] = None,
        var_name: Optional[str] = None,
        time_step: Optional[float] = 1.0,
        sids: list = None,
        y_label: Optional[str] = None,
        title_text: Optional[str] = None,
        legend: bool = True,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        **kwargs,
    ):
        """
        Query data and make plot `var_name` vs. `Time` for each of the sids, where `Time` = `time_step` * rid.

        Both `CitrosDB.time_plot()` and `CitrosDB.xy_plot()` methods are aimed to quickly make plots.
        They allow you to query data and plot it at once, without need to first save data as a separate DataFrame.
        The constraints on data may be set by `batch()`, `topic()`, `rid()`, `sid()` and `time()` methods
        and one of the aggregative methods `skip()`, `avg()` or `move_avg()`.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Figure axis to plot on.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        topic_name : str
            Input topic name. If specified, will override value that was set by `topic()` method.
        var_name : str
            Name of the variable to plot along y-axis.
        time_step : float or int, default 1.0
            Time step, `Time` = `time_step` * rid.
        sids : list
            List of the sids. If specified, will override values that were set by `sid()` method.
            If not specified, data for all sids is used.
        y_label : str
            Label to set to y-axis. Default `var_name`.
        title_text : str
            Title of the figure. Default '`var_y_name` vs. Time'.
        legend : bool, default True
            If True, show the legend with sids.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.xy_plot,
        CitrosDB.batch, CitrosDB.topic, CitrosDB.rid, CitrosDB.sid, CitrosDB.time, CitrosDB.skip, CitrosDB.avg, CitrosDB.move_avg, CitrosDB.set_order

        Examples
        --------
        Import matplotlib and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        For batch 'dynamics', simulation 'pendulum' for topic 'A' plot `data.x.x_1` vs. `Time` for all existing sids, `Time` = 0.5 * rid

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.simulation('pendulum').batch('dynamics').topic('A').time_plot(ax, var_name = 'data.x.x_1', time_step = 0.5)

        ![time_plot_1](../../img_documentation/time_plot_1.png "time_plot_1")

        Create a new figure and plot only part of the data, where 'data.x.x_1' <= 0; plot by dashed line:

        >>> fig, ax = plt.subplots()
        >>> citros.simulation('pendulum').batch('dynamics').topic('A').set_filter({'data.x.x_1':{'<=': 0}})\\
                  .time_plot(ax, '--', var_name = 'data.x.x_1', time_step = 0.5)

        ![time_plot_2](../../img_documentation/time_plot_2.png "time_plot_2")
        """
        if not self._is_batch_available():
            return None

        if sids is None or sids == []:
            if hasattr(self, "_sid"):
                sids = self._sid
            else:
                sids = None
        elif isinstance(sids, int):
            sids = [sids]

        var_df = _PgCursor._data_for_time_plot(
            self, topic_name, var_name, time_step, sids, remove_nan, inf_vals
        )
        if var_df is None:
            return

        plotter = _Plotter(self.log)
        plotter.time_plot(
            var_df, ax, var_name, sids, y_label, title_text, legend, *args, **kwargs
        )

    def xy_plot(
        self,
        ax: plt.Axes,
        *args,
        topic_name: Optional[str] = None,
        var_x_name: Optional[str] = None,
        var_y_name: Optional[str] = None,
        sids: Optional[Union[int, list]] = None,
        x_label: Optional[str] = None,
        y_label: Optional[str] = None,
        title_text: Optional[str] = None,
        legend: bool = True,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        **kwargs,
    ):
        """
        Query data and make plot `var_y_name` vs. `var_x_name` for each of the sids.

        Both `CitrosDB.time_plot()` and `CitrosDB.xy_plot()` methods are aimed to quickly make plots.
        They allow you to query data and plot it at once, without need to first save data as a separate DataFrame.
        The constraints on data may be set by `batch()`, `topic()`, `rid()`, `sid()` and `time()` methods
        and one of the aggregative methods `skip()`, `avg()` or `move_avg()`.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Figure axis to plot on.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        topic_name : str
            Input topic name. If specified, will override value that was set by `topic()` method.
        var_x_name : str
            Name of the variable to plot along x-axis.
        var_y_name : str
            Name of the variable to plot along y-axis.
        sids : int or list of int, optional
            List of the sids. If specified, will override values that were set by `sid()` method.
            If not specified, data for all sids is used.
        x_label : str, optional
            Label to set to x-axis. Default `var_x_name`.
        y_label : str, optional
            Label to set to y-axis. Default `var_y_name`.
        title_text : str, optional
            Title of the figure. Default '`var_y_name` vs. `var_x_name`'.
        legend : bool, default True
            If True, show the legend with sids.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.time_plot,
        CitrosDB.batch, CitrosDB.topic, CitrosDB.rid, CitrosDB.sid, CitrosDB.time, CitrosDB.skip, CitrosDB.avg, CitrosDB.move_avg, CitrosDB.set_order

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        For batch 'dynamics', simulation 'pendulum' for topic 'A' plot 'data.x.x_1' vs. 'data.time' for all existing sids:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> citros.simulation('pendulum').batch('dynamics').topic('A').xy_plot(ax, var_x_name = 'data.x.x_1', var_y_name = 'data.time')

        ![xy_plot_1](../../img_documentation/xy_plot_1.png "xy_plot_1")

        Create new figure and plot only part of the data, where 'data.x.x_1' <= 0, sid = 1 and 2; plot by dashed lines:

        >>> fig, ax = plt.subplots()
        >>> citros.simulation('pendulum').batch('dynamics').topic('A').set_filter({'data.x.x_1':{'<=': 0}}).sid([1,2])\\
                  .xy_plot(ax, '--', var_x_name = 'data.x.x_1', var_y_name = 'data.time')

        ![xy_plot_2](../../img_documentation/xy_plot_2.png "xy_plot_1")
        """
        if not self._is_batch_available():
            return None

        if sids is None or sids == []:
            if hasattr(self, "_sid"):
                sids = self._sid
            else:
                sids = None
        elif isinstance(sids, int):
            sids = [sids]
        xy_df = _PgCursor._data_for_xy_plot(
            self, topic_name, var_x_name, var_y_name, sids, remove_nan, inf_vals
        )
        if xy_df is None:
            return

        plotter = _Plotter(self.log)
        plotter.xy_plot(
            xy_df,
            ax,
            var_x_name,
            var_y_name,
            sids,
            x_label,
            y_label,
            title_text,
            legend,
            *args,
            **kwargs,
        )

    def plot_graph(
        self,
        df: pd.DataFrame,
        x_label: str,
        y_label: str,
        *args,
        ax: Optional[plt.Axes] = None,
        legend: bool = True,
        title: Optional[str] = None,
        set_x_label: Optional[str] = None,
        set_y_label: Optional[str] = None,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        **kwargs,
    ):
        """
        Plot graph '`y_label` vs. `x_label`' for each sid, where `x_label` and `y_label`
        are the labels of columns of the pandas.DataFrame `df`.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_label : str
            Label of the column to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc,
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, default None
            Label to set to the y-axis. If None, label is set according to `y_label`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : matplotlib.axes.Axes
            Created axis if `ax` is not passed.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.plot_3dgraph, CitrosDB.multiple_y_plot, CitrosDB.multiplot, CitrosDB.plot_sigma_ellipse

        Examples
        --------
        Import matplotlib and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        Download from batch 'kinematics', simulation 'cube_system' for topic 'A' from json-data column 'data.x.x_1' and 'data.x.x_2' columns:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('cube_system').batch('kinematics').topic('A').data(['data.x.x_1', 'data.x.x_2'])

        Plot `data.x.x_1` vs. `data.x.x_2`:

        >>> citros.plot_graph(df, 'data.x.x_1', 'data.x.x_2', ax = ax, title = 'Example plot')

        ![plot_graph_1](../../img_documentation/plot_graph_1.png "plot_graph_1")

        If `ax` parameter is not passed, `plot_graph()` generates a pair of (matplotlib.figure.Figure, matplotlib.axes.Axes) objects and
        returns them. Let's plot the previous image without passing `ax` argument, and also let's plot with a dotted line:

        >>> fig, ax = citros.plot_graph(df, 'data.x.x_1', 'data.x.x_2', '.', title = 'Example plot')
        >>> fig.show()

        ![plot_graph_2](../../img_documentation/plot_graph_2.png "plot_graph_2")
        """
        plotter = _Plotter(self.log)
        return plotter.plot_graph(
            df,
            x_label,
            y_label,
            ax,
            legend,
            title,
            set_x_label,
            set_y_label,
            remove_nan,
            inf_vals,
            *args,
            **kwargs,
        )

    def plot_3dgraph(
        self,
        df: pd.DataFrame,
        x_label: str,
        y_label: str,
        z_label: str,
        *args,
        ax: Optional[plt.Axes] = None,
        scale: bool = True,
        legend: bool = True,
        title: Optional[str] = None,
        set_x_label: Optional[str] = None,
        set_y_label: Optional[str] = None,
        set_z_label: Optional[str] = None,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        **kwargs,
    ):
        """
        Plot 3D graph '`z_label` vs. `x_label` and `y_label`' for each sid, where `x_label`, `y_label` and `z_label`
        are the labels of columns of the pandas.DataFrame `df`.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_label : str
            Label of the column to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc,
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created.
        scale : bool, default True
            Specify whether the axis range should be the same for all axes.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, default None
            Label to set to the y-axis. If None, label is set according to `y_label`.
        set_z_label : str, default None
            Label to set to the z-axis. If None, label is set according to `z_label`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : matplotlib.axes.Axes
            Created axis if `ax` is not passed.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.plot_graph, CitrosDB.multiple_y_plot, CitrosDB.multiplot, CitrosDB.plot_sigma_ellipse

        Examples
        --------
        Import matplotlib and mplot3d for 3D plots and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits import mplot3d
        >>> fig = plt.figure(figsize=(6, 6))
        >>> ax = fig.add_subplot(111, projection = '3d')

        For topic 'A' from batch 'testing' of the 'pendulum' simulation from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' columns:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('pendulum').batch('testing').topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        Make 3D plot with dashed lines; `scale` = True aligns all axes to have the same range:

        >>> citros.plot_3dgraph(df, 'data.x.x_1', 'data.x.x_2', 'data.x.x_3', '--', ax = ax, scale = True)

        ![plot_3dgraph_1](../../img_documentation/plot_3dgraph_1.png "plot_3dgraph_1")
        """
        plotter = _Plotter(self.log)
        return plotter.plot_3dgraph(
            df,
            x_label,
            y_label,
            z_label,
            ax,
            scale,
            legend,
            title,
            set_x_label,
            set_y_label,
            set_z_label,
            remove_nan,
            inf_vals,
            *args,
            **kwargs,
        )

    def multiple_y_plot(
        self,
        df: pd.DataFrame,
        x_label: str,
        y_labels: str,
        *args,
        fig: Optional[matplotlib.figure.Figure] = None,
        legend: bool = True,
        title: Optional[str] = None,
        set_x_label: Optional[str] = None,
        set_y_label: Optional[str] = None,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        **kwargs,
    ):
        """
        Plot a series of vertically arranged graphs 'y vs. `x_label`', with the y-axis labels
        specified in the `y_labels` parameter.

        Different colors correspond to different sids.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_labels : list of str
            Labels of the columns to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc,
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        fig : matplotlib.figure.Figure, optional
            If None, a new Figure will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : list of str, default None
            Labels to set to the y-axis. If None, label is set according to `y_labels`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `fig` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `fig` is not passed.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.plot_graph, CitrosDB.plot_3dgraph, CitrosDB.multiplot, CitrosDB.plot_sigma_ellipse

        Examples
        --------
        For topic 'A' from batch 'testing' of the 'pendulum' simulation from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' and 'data.time' columns:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('pendulum').batch('testing').topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3', 'data.time'])

        Plot three subplots with a common x axis: 'data.x.x_1' vs. 'data.time', 'data.x.x_2' vs. 'data.time' and 'data.x.x_3' vs. 'data.time':

        >>> fig, ax = citros.multiple_y_plot(df, 'data.time', ['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        ![multiple_y_plot_1](../../img_documentation/multiple_y_plot_1.png "multiple_y_plot_1")

        If `ax` parameter is not passed, `multiple_y_plot()` generates a pair of (matplotlib.figure.Figure, matplotlib.axes.Axes) objects and
        returns them. Let's make a scatter plot in this manner:

        >>> fig, ax = citros.multiple_y_plot(df, 'data.time', ['data.x.x_1', 'data.x.x_2', 'data.x.x_3'], '.')

        ![multiple_y_plot_2](../../img_documentation/multiple_y_plot_2.png "multiple_y_plot_2")
        """
        plotter = _Plotter(self.log)
        return plotter.multiple_y_plot(
            df,
            x_label,
            y_labels,
            fig,
            legend,
            title,
            set_x_label,
            set_y_label,
            remove_nan,
            inf_vals,
            *args,
            **kwargs,
        )

    def multiplot(
        self,
        df: pd.DataFrame,
        labels: list,
        *args,
        scale: bool = True,
        fig: Optional[matplotlib.figure.Figure] = None,
        legend: bool = True,
        title: Optional[str] = None,
        set_x_label: Optional[str] = None,
        set_y_label: Optional[str] = None,
        remove_nan: bool = True,
        inf_vals: Optional[float] = 1e308,
        label_all_xaxis: bool = False,
        label_all_yaxis: bool = False,
        num: int = 5,
        **kwargs,
    ):
        """
        Plot a matrix of N x N graphs, each displaying either the histogram with values distribution (for graphs on the diogonal) or
        the relationship between variables listed in `labels`, with N being the length of `labels` list.

        For non-diagonal graphs, colors are assigned to points according to sids.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        labels : list of str
            Labels of the columns to plot.
        *args : Any
            Additional arguments to style lines, set color, etc,
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        scale : bool, default True
            Specify whether the axis range should be the same for x and y axes.
        fig : matplotlib.figure.Figure, optional
            If None, a new Figure will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : list of str
            Labels to set to the x-axis. If None, label is set according to `labels`.
        set_y_label : list of str
            Labels to set to the y-axis. If None, label is set according to `labels`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.
        label_all_xaxis : bool, default False
            If True, x labels are set to the x-axes of the all graphs, otherwise only to the graphs in the bottom row.
        label_all_yaxis : bool, default False
            If True, y labels are set to the y-axes of the all graphs, otherwise only to the graphs in the first column.
        num : int, default 5
            Number of bins in the histogram on the diagonal.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `fig` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `fig` is not passed.

        Other Parameters
        ----------------
        kwargs : dict, optional
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        See Also
        --------
        CitrosDB.plot_graph, CitrosDB.plot_3dgraph, CitrosDB.multiple_y_plot, CitrosDB.plot_sigma_ellipse

        Examples
        --------
        For topic 'A' from the batch 'testing_robotics' of the 'robots' simulation from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3':

        >>> from citros import CitrosDB
        >>> citros = CitrosDB()
        >>> df = citros.simulation('robots').batch('testing_robotics').topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        Plot nine graphs: histograms for three graphs on the diagonal, that represent
        distribution of the 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' values, and six graphs that show
        correlation between them; plot by dots and scale x and y axes ranges to one interval for each graph:

        >>> fig, ax = citros.multiplot(df, ['data.x.x_1', 'data.x.x_2', 'data.x.x_3'], '.' , scale = True)
        >>> fig.show()

        ![multiplot](../../img_documentation/multiplot.png "multiplot")
        """
        plotter = _Plotter(self.log)
        return plotter.multiplot(
            df,
            labels,
            scale,
            fig,
            legend,
            title,
            set_x_label,
            set_y_label,
            remove_nan,
            inf_vals,
            label_all_xaxis,
            label_all_yaxis,
            num,
            *args,
            **kwargs,
        )

    def plot_sigma_ellipse(
        self,
        df: pd.DataFrame,
        x_label: str,
        y_label: str,
        ax: plt.Axes = None,
        n_std: int = 3,
        plot_origin: bool = True,
        bounding_error: bool = False,
        inf_vals: Optional[float] = 1e308,
        legend: bool = True,
        title: Optional[str] = None,
        set_x_label: Optional[str] = None,
        set_y_label: Optional[str] = None,
        scale: bool = False,
        return_ellipse_param: bool = False,
    ):
        """
        Plot sigma ellipses for the set of data.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_labels : list of str
            Labels of the columns to plot along y-axis.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created and returned.
        n_std : int or list of ints
            Radius of ellipses in sigmas.
        plot_origin: bool, default True
            If True, depicts origin (0, 0) with black cross.
        bounding_error : bool, default False
            If True, plots bounding error circle for each of the ellipses.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.
        legend : bool, default True
            If True, show the legend.
        title : str, optional
            Set title. If None, title is set as '`x_label` vs. `y_label`'.
        set_x_label : str, optional
            Set label of the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, optional
            Set label of the y-axis. If None, label is set according to `y_label`.
        scale : bool, default False
            Specify whether the axis range should be the same for x and y axes.
        return_ellipse_param : bool, default False
            If True, returns ellipse parameters.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `ax` is not passed.
        ellipse_param : dict or list of dict
            Ellipse parameters if `return_ellipse_param` set True.
            Parameters of the ellipse:
            - x : float - x coordinate of the center.
            - y : float - y coordinate of the center.
            - width : float - total ellipse width (diameter along the longer axis).
            - height : float - total ellipse height (diameter along the shorter axis).
            - alpha : float - angle of rotation, in degrees, anti-clockwise from the shorter axis.

            If bounding_error set True:
            - bounding_error : float - radius of the error circle.

        See Also
        --------
        CitrosDB.plot_graph, CitrosDB.plot_3dgraph, CitrosDB.multiple_y_plot, CitrosDB.multiplot

        Examples
        --------
        Let's assume that in topic 'A', the batch named 'aerostatic' of the simulation 'aircraft' includes the columns 'data.x.x_1' and 'data.x.x_2'.
        We would like to analyze the spread of these values from their mean.
        First, we'll query the data and compute new columns 'X1' and 'X2', which will represent the deviations of 'data.x.x_1' and 'data.x.x_2' from their respective mean values:

        >>> from citros import CitrosDB
        >>> citros = CitrosDB(simulation = 'aircraft')
        >>> df = citros.batch('aerostatic').topic('A').data(['data.x.x_1', 'data.x.x_2'])
        >>> df['X1'] = df['data.x.x_1'] - df['data.x.x_1'].mean()
        >>> df['X2'] = df['data.x.x_2'] - df['data.x.x_2'].mean()

        Let's plot 'X1' vs. 'X2', 3-$\sigma$ ellipse, origin point that has coordinates (0, 0)
        and set the same range for x and y axis:

        >>> fig, ax = citros.plot_sigma_ellipse(df, x_label = 'X1', y_label = 'X2',
        ...                                      n_std = 3, plot_origin=True, scale = True)

        ![plot_sigma_ellipse_1](../../img_documentation/plot_sigma_ellipse_1.png "plot_sigma_ellipse_1")

        If we set `return_ellipse_param` = `True`, the parameters of the error ellipse will be returned:
        >>> fig, ax, param = citros.plot_sigma_ellipse(df, x_label = 'X1', y_label = 'X2', n_std = 3,
        ...                                            plot_origin=True, scale = True, return_ellipse_param = True)
        >>> print(param)
        {'x': 0,
         'y': 0,
         'width': 2.1688175559868204,
         'height': 0.6108213775972502,
         'alpha': -132.38622331887413}

        Plot the same but for 1-, 2- and 3-$\sigma$ ellipses, add bounding error circle (that indicates the maximum distance
        between the ellipse points and the origin), set custom labels and title to the plot:

        >>> fig, ax = citros.plot_sigma_ellipse(df, x_label = 'X1', y_label = 'X2',
        ...                                     n_std = [1,2,3], plot_origin=True, bounding_error=True,
        ...                                     set_x_label='x, [m]', set_y_label = 'y, [m]',
        ...                                     title = 'Coordinates')

        ![plot_sigma_ellipse_2](../../img_documentation/plot_sigma_ellipse_2.png "plot_sigma_ellipse_2")
        """
        plotter = _Plotter(self.log)
        return plotter.plot_sigma_ellipse(
            df,
            x_label,
            y_label,
            ax,
            n_std,
            plot_origin,
            bounding_error,
            inf_vals,
            legend,
            title,
            set_x_label,
            set_y_label,
            scale,
            return_ellipse_param,
        )
