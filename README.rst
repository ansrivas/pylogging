pylogging
~~~~~~~~~

A simple python logger which writes logs to disk with some default
configs.

Compatible with:
~~~~~~~~~~~~~~~~

Python 2.7 and 3.5+

Current stable version:
~~~~~~~~~~~~~~~~~~~~~~~

::

    0.2.6

Installation:
~~~~~~~~~~~~~

Install using pip
^^^^^^^^^^^^^^^^^

::

    pip install git+https://github.com/ansrivas/pylogging.git --upgrade

Install by adding to requirements.txt of your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Add the following lines to your ``requirements.txt`` file.
   ``git+https://github.com/ansrivas/pylogging.git``

-  Install all packages in your ``requirements.txt`` file by running the
   command: ``$ pip install -r requirements.txt``

Install by adding to setup.py of your project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  Add the following to the ``install_requires`` parameter of your setup
   function: ``install_requires=['pylogging==0.2.6'],``

-  Add the following to the ``dependency_links`` parameter of your setup
   function:
   ``dependency_links=['https://github.com/ansrivas/pylogging/tarball/master#egg=pylogging-0.2.6'],``

-  Install your project along with ``pylogging`` by running the command:
   ``python setup.py install``

Usage:
~~~~~~

-  ``setup_logger`` sets up the global logger with the provided
   settings. After calling it once, simply ``import logging`` and create
   a logger for that module ``logger = logging.getLogger(__name__)`` and
   use it at shown below.

::

    from pylogging import HandlerType, setup_logger
    import logging

    logger = logging.getLogger(__name__)

    if __name__ == '__main__':
        setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER, allow_console_logging=True)

        logger.error("Error logs")
        logger.debug("Debug logs")
        logger.info("Info logs")

Development installation
^^^^^^^^^^^^^^^^^^^^^^^^^
::

  pip install -e .[dev]


Important arguments to ``setup_logger`` function:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  log_directory (str)            :directory to write log files to. Applicable only when `allow_file_logging` = True
  file_handler_type              :object of logging handler from HandlerType class. Applicable only when `allow_file_logging` = True
  allow_console_logging (bool)   :Turn off/on the console logging.
  allow_file_logging (bool)      :Turn off/on if logs need to go in files as well.
  backup_count (int)             :Number of files to backup before rotating the logs.
  max_file_size_bytes (int)      :Size of file in bytes before rotating the file. Applicable only to ROTATING_FILE_HANDLER.
  when_to_rotate (str)           :Duration after which a file can be rotated. Applicable only to TIME_ROTATING_FILE_HANDLER
                                  Accepts following values:
                                  'S'	Seconds
                                  'M'	Minutes
                                  'H'	Hours
                                  'D'	Days
                                  'W0'-'W6'	Weekday (0=Monday)
                                  'midnight'	Roll over at midnight
  change_log_level (dict)        :A dictionary of handlers with corresponding log-level ( for eg. {'requests':'warning'} )
  console_log_level (logging)    :Change the LogLevel of console log handler, default is logging.INFO (e.g. logging.DEBUG, logging.INFO)
  gelf_handler                   :An external handler for graylog data publishing.
  log_tags                       :Adding contextual information to a given log handler for e.g. {'app_name': 'My Perfect App'}
