# Copyright (C) 2021 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from abc import ABC
from abc import abstractmethod
import argparse
import getpass
import logging
import sys
import time
from typing import Any

from majormode.perseus.constant.logging import LOGGING_LEVELS, LOGGING_LEVEL_LITERAL_STRINGS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.utils import cast
from majormode.perseus.utils import env
from majormode.perseus.utils import rdbms
from majormode.perseus.utils.rdbms import RdbmsConnection


class BaseAgent(ABC):
    DEFAULT_IDLE_TIME = 5000

    DEFAULT_LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    DEFAULT_LOGGING_LEVEL = LoggingLevelLiteral.info

    def __init__(
            self,
            agent_name: str = None,
            do_loop: bool = True,
            idle_time: int = None,
            logger_name: str = None,
            logging_formatter: logging.Formatter = None,
            logging_level: LoggingLevelLiteral = None
    ):
        """
        Build a new instance of the agent.


        :param agent_name: The name given to this agent.  If this argument is
            not passed, the name of the agent's class is used.

        :param do_loop: Indicate whether the agent should continually run
            until explicitly requested to stop.  This parameter can be
            overriden when starting the agent.

        :param idle_time: The amount of time in milliseconds the agent pauses
            after completing an execution iteration.

        :param logger_name: The name of the logger to add the logging handler to.
            If `logger_name` is `None`, the function attaches the logging
            handler to the root logger of the hierarchy.

        :param logging_formatter: An object ``Formatter`` to set for this
            handler.  Defaults to ``BaseAgent.DEFAULT_LOGGING_FORMATTER``.

        :param logging_level: An item of the enumeration `LoggingLevelLiteral`
            that specifies the threshold for the logger to `level`.  Logging
            messages which are less severe than `level` will be ignored;
            logging messages which have severity level or higher will be
            emitted by whichever handler or handlers service this logger,
            unless a handler’s level has been set to a higher severity level
            than `level`.  Defaults to `BaseAgent.DEFAULT_LOGGING_LEVEL`.
        """
        self.__agent_name = agent_name or self.__class__.__name__
        self.__do_loop = do_loop
        self.__idle_time = idle_time or self.DEFAULT_IDLE_TIME

        self.__logger = self.__setup_logger(
            logger_name=logger_name,
            logging_formatter=logging_formatter,
            logging_level=logging_level
        )

    @classmethod
    def __get_console_handler(cls, logging_formatter: logging.Formatter = None):
        """
        Return a logging handler that sends logging output to the system's
        standard output.


        :param logging_formatter: An object `Formatter` to set for this
            handler.  Defaults to `BaseAgent.DEFAULT_LOGGING_FORMATTER`.


        :return: An instance of the `StreamHandler` class.
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging_formatter or cls.DEFAULT_LOGGING_FORMATTER)
        return console_handler

    @classmethod
    def __setup_logger(
            cls,
            logger_name: str = None,
            logging_formatter: logging.Formatter = None,
            logging_level: LoggingLevelLiteral = None
    ) -> logging.Logger:
        """
        Set up a logging handler that sends logging output to the system's
        standard output.

        :param logger_name: The name of the logger to add the logging handler to.
            If `logger_name` is `None`, the function attaches the logging
            handler to the root logger of the hierarchy.

        :param logging_formatter: An object ``Formatter`` to set for this
            handler.  Defaults to ``BaseAgent.DEFAULT_LOGGING_FORMATTER``.

        :param logging_level: The threshold for the logger.  Logging messages
            which are less severe than `logging_level` will be ignored;
            logging messages which have severity level or higher will be
            emitted by whichever handler or handlers service this logger,
            unless a handler’s level has been set to a higher severity level
            than ``logging_level``.  Defaults to
            ``BaseAgent.DEFAULT_LOGGING_LEVEL``.


        :return: An object ``Logger``.
        """
        logger = logging.getLogger(logger_name)
        logger.setLevel(LOGGING_LEVELS[logging_level or cls.DEFAULT_LOGGING_LEVEL])
        logger.addHandler(cls.__get_console_handler(logging_formatter=logging_formatter))
        logger.propagate = False
        return logger

    @abstractmethod
    def _run(self, **kwargs) -> bool:
        """
        Execute the agent.


        :param kwargs: Some arguments specific to the execution of this
            agent.


        :return: ``True`` if the agent had some work to do; ``False`` if the
            agent hadn't anything to process.
        """
        raise NotImplementedError("This method MUST be implemented by the inheriting class")

    def _init(self):
        """
        Subclasses SHOULD override this method to initialize some properties
        just before the agent starts.
        """

    def set_logging_formatter(self, logging_formatter: logging.Formatter) -> None:
        """
        Override the logging formatter of the logger.


        :param logging_formatter: The logging formatter responsible for
            converting log records to an output string to be interpreted by a
            human or external system.
        """
        for handler in self.__logger.handlers:
            handler.setFormatter(logging_formatter)

    def set_logging_level(self, logging_level: LoggingLevelLiteral) -> None:
        """
        Override the threshold for the logger.


        :param logging_level: The threshold for the logger.
        """
        self.__logger.setLevel(LOGGING_LEVELS[logging_level or self.DEFAULT_LOGGING_LEVEL])

    def start(
            self,
            do_loop: bool = True,
            logging_formatter: logging.Formatter = None,
            logging_level: LoggingLevelLiteral = None,
            **kwargs: dict[str, Any]
    ) -> None:
        """
        Start the agent.


        :param do_loop: Indicate whether the agent should continually run
            until explicitly requested to stop.  This allows to override the
            argument initially passed to the agent's constructor.

        :param logging_formatter: The logging formatter responsible for
            converting log records to an output string to be interpreted by a
            human or external system.  This allows to override the argument
            initially passed to the agent's constructor.

        :param logging_level: The threshold for the logger.  This allows to
            override the argument initially passed to the agent's constructor.

        :param kwargs: Some specific arguments to pass to the agent.
        """
        self._init()

        # Override the argument initially passed to the agent's constructor.
        if do_loop is not None:
            self.__do_loop = do_loop

        # Override the argument initially passed to the agent's constructor.
        if logging_level:
            self.set_logging_level(logging_level)

        # Override the argument initially passed to the agent's constructor.
        if logging_formatter:
            self.set_logging_formatter(logging_formatter)

        # Run the agent.
        while True:
            was_active = self._run(**kwargs)

            # Stop the agent if it was not requested to continually run, or it has
            # been explicitly requested to stop.
            if not self.__do_loop:
                break

            # If the agent didn't process anything during its last execution, pause
            # it for the requested amount of time.
            if not was_active:
                logging.debug(f"Waiting {float(self.__idle_time) / 1000}ms for more action...")
                time.sleep(float(self.__idle_time) / 1000)

    def stop(self):
        if not self.__do_loop:
            raise ValueError("This agent was not started for running for ever")

        self.__do_loop = False


class BaseCliAgent(BaseAgent, ABC):
    def __init__(
            self,
            description: str = None,
            env_file_path_name: str = None,
            idle_time: int = None,
            name: str = None
    ):
        """
        Build an object `BaseCliAgent`


        :param description: The text to display before the argument help.

        :param name: The name of the agent.
        """
        super().__init__(idle_time=idle_time, name=name)

        env.loadenv(env_file_path_name)

        # Set up the command line argument parser.
        self.__argument_parser = self.__build_argument_parser(description=description)
        self.__arguments = None

    @classmethod
    def __build_argument_parser(
            cls,
            description: str
    ) -> argparse.ArgumentParser:
        """
        Build the command-line parser of the agent.


        :param description: The text to display before the argument help.


        :return: The argument parser instance.
        """
        parser = argparse.ArgumentParser(description=description)

        parser.add_argument(
            '--logging-level',
            dest='logging_level',
            metavar='LEVEL',
            required=False,
            default=str(LoggingLevelLiteral.info),
            type=lambda logging_level: cast.string_to_enum(logging_level, LoggingLevelLiteral),
            help=f"Specify the logging level ({', '.join(LOGGING_LEVEL_LITERAL_STRINGS)})"
        )

        return parser

    @property
    def _argument_parser(self):
        return self.__argument_parser

    def _init(self):
        super()._init()
        # Convert argument strings to objects and assign them as attributes of
        # the namespace.  This is done here to give the chance to the inheriting
        # class to add its custom arguments in its constructor.
        self.__arguments = self.__argument_parser.parse_args()

    @property
    def arguments(self):
        if self.__arguments is None:
            self.__arguments = self.__argument_parser.parse_args()
        return self.__arguments

    # def start(
    #         self,
    #         do_loop=False,
    #         logging_formatter=None,
    #         logging_level=None):
    #     super().start(
    #         do_loop=do_loop,
    #         logging_level=logging_level or cast.string_to_enum(
    #             self.__arguments.logging_level_literal,
    #             LoggingLevelLiteral))


class BaseCliRdbmsAgent(BaseCliAgent, ABC):
    # Environment variables of the connection property to the Relational
    # DataBase Management System (RDBMS) server.
    ENV_RDBMS_HOSTNAME = 'RDBMS_HOSTNAME'
    ENV_RDBMS_PORT = 'RDBMS_PORT'
    ENV_RDBMS_DATABASE_NAME = 'RDBMS_DATABASE_NAME'
    ENV_RDBMS_USERNAME = 'RDBMS_USERNAME'
    ENV_RDBMS_PASSWORD = 'RDBMS_PASSWORD'

    @classmethod
    def __include_rdbms_arguments(cls, parser: argparse.ArgumentParser):
        """
        Add the command line arguments to define the properties to connect to
        a Relational DataBase Management System (RDBMS) server


        :note: The password to connect to the RDBMS server CANNOT be passed as
            an argument on the command line as the password would be leaked
            into the process table, and thus visible to anybody running `ps(1)`
            on the system, and the password would leak into the shell's history
            file.
            [https://www.netmeister.org/blog/passing-passwords.html]


        :param parser: An object `ArgumentParser`.


        :return: The object `ArgumentParser` that has been passed to this
            function.
        """
        default_database_name = env.getenv(cls.ENV_RDBMS_DATABASE_NAME, is_required=False)
        parser.add_argument(
            '--rdbms-database-name',
            required=default_database_name is None,
            default=default_database_name,
            help='Specify the name of the database to connect to.'
        )

        parser.add_argument(
            '--rdbms-hostname',
            required=False,
            default=env.getenv(cls.ENV_RDBMS_HOSTNAME, is_required=False),
            help="Specify the host name of the machine on which the server is running."
        )

        parser.add_argument(
            '--rdbms-port',
            required=False,
            type=int,
            default=env.getenv(cls.ENV_RDBMS_PORT, data_type=env.DataType.integer, is_required=False),
            help="Specify the database TCP port or the local Unix-domain socket file "
                 "extension on which the server is listening for connections. Defaults "
                 "to the port specified at compile time, usually 5432."
        )

        parser.add_argument(
            '--rdbms-username',
            required=False,
            default=env.getenv(cls.ENV_RDBMS_USERNAME, is_required=False) or getpass.getuser(),
            help="Connect to the database as the user username instead of the default."
        )

        return parser

    def __init__(
            self,
            description: str = None,
            idle_time: int = None,
            name: str = None
    ):
        super().__init__(
            description=description,
            idle_time=idle_time,
            name=name
        )

        self.__include_rdbms_arguments(self._argument_parser)

        self.__rdbms_hostname = None
        self.__rdbms_port = None
        self.__rdbms_database_name = None
        self.__rdbms_username = None
        self.__rdbms_password = None

        self.__rdbms_properties = None

    def _acquire_connection(
            self,
            auto_commit: bool = False,
            connection: RdbmsConnection = None
    ) -> RdbmsConnection:
        """
        Return a connection to the relational database management system
        (RDBMS).


        :param auto_commit: Indicate whether the transaction needs to be
           committed at the end of the session.

        :param connection: An existing connection to the database that needs
            to be reused. The caller SHOULD ensure that the ``auto_commit``
            property if this connection matches the desired autocommit.


        :return: A connection to the database.
        """
        return rdbms.RdbmsConnection.acquire_connection(
            self.__rdbms_properties,
            auto_commit=auto_commit,
            connection=connection
        )

    def _init(self):
        super()._init()

        if self.__rdbms_hostname is None:
            self.__rdbms_hostname = self.arguments.rdbms_hostname

        if self.__rdbms_port is None:
            self.__rdbms_port = self.arguments.rdbms_port

        if self.__rdbms_database_name is None:
            self.__rdbms_database_name = self.arguments.rdbms_database_name

        if self.__rdbms_username is None:
            self.__rdbms_username = self.arguments.rdbms_username

        self.__rdbms_password = env.getenv(self.ENV_RDBMS_PASSWORD, is_required=False) \
            or getpass.getpass(f"Password for user {self.__rdbms_username}: ")

        self.__rdbms_properties = {
            None: {
                'rdbms_hostname': self.__rdbms_hostname,
                'rdbms_port': self.__rdbms_port,
                'rdbms_database_name': self.__rdbms_database_name,
                'rdbms_account_username': self.__rdbms_username,
                'rdbms_account_password': self.__rdbms_password,
            },
        }

    # def start(
    #         self,
    #         do_loop=False,
    #         logging_formatter=None,
    #         logging_level=None):
    #     self._init()
    #     super().start(
    #         do_loop=do_loop,
    #         logging_formatter=logging_formatter,
    #         logging_level=logging_level
    #     )


class FakeCliRdbmsAgent(BaseCliRdbmsAgent):
    def _run(self):
        logging.info('Completed work!')


if __name__ == "__main__":
    agent = FakeCliRdbmsAgent()
    agent.start()
