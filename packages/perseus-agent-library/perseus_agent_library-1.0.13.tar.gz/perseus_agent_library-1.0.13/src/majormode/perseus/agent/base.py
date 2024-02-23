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

import logging
import time
from abc import ABC
from abc import abstractmethod
from typing import Any

from majormode.perseus.constant.logging import LOGGING_LEVELS
from majormode.perseus.constant.logging import LoggingLevelLiteral
from majormode.perseus.model.microrm import RdbmsConnectionProperties
from majormode.perseus.utils import rdbms
from majormode.perseus.utils.logging import set_up_logger
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

        self.__logger = set_up_logger(
            logger_name=logger_name,
            logging_formatter=logging_formatter or self.DEFAULT_LOGGING_FORMATTER,
            logging_level=logging_level or self.DEFAULT_LOGGING_LEVEL
        )

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


class BaseRdbmsAgent(BaseAgent, ABC):
    def __init__(
            self,
            rdbms_connection_properties: RdbmsConnectionProperties,
            agent_name: str = None,
            do_loop: bool = True,
            idle_time: int = None,
            logger_name: str = None,
            logging_formatter: logging.Formatter = None,
            logging_level: LoggingLevelLiteral = None
    ):
        super().__init__(
            agent_name=agent_name,
            do_loop=do_loop,
            idle_time=idle_time,
            logger_name=logger_name,
            logging_formatter=logging_formatter,
            logging_level=logging_level
        )

        self.__rdbms_connection_properties = rdbms_connection_properties

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
            self.__rdbms_connection_properties,
            auto_commit=auto_commit,
            connection=connection
        )
