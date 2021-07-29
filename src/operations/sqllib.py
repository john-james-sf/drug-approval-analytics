# -*- coding:utf-8 -*-
# =========================================================================== #
# Project  : Drug Approval Analytics                                          #
# Version  : 0.1.0                                                            #
# File     : \src\platform\sqllib.py                                          #
# Language : Python 3.9.5                                                     #
# --------------------------------------------------------------------------  #
# Author   : John James                                                       #
# Company  : nov8.ai                                                          #
# Email    : john.james@nov8.ai                                               #
# URL      : https://github.com/john-james-sf/drug-approval-analytics         #
# --------------------------------------------------------------------------  #
# Created  : Saturday, July 24th 2021, 2:15:04 pm                             #
# Modified : Thursday, July 29th 2021, 5:46:48 am                             #
# Modifier : John James (john.james@nov8.ai)                                  #
# --------------------------------------------------------------------------- #
# License  : BSD 3-clause "New" or "Revised" License                          #
# Copyright: (c) 2021 nov8.ai                                                 #
# =========================================================================== #
"""Module containing database administration query language."""
from collections import OrderedDict
from psycopg2 import sql

from .sqlgen import SQLCommand
# --------------------------------------------------------------------------- #
#                           OPERATIONS TABLES                                 #
# --------------------------------------------------------------------------- #
operations_tables = OrderedDict()
operations_tables['parameter_set'] = SQLCommand(
    name='parameter_set',
    description="Sets the table of Parameter Sets",
    cmd=sql.SQL("""CREATE TABLE parameter_set (
        param_set_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
        name VARCHAR(64),
        description VARCHAR(255),
        created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP
    );
    """)
),
operations_tables['parameter'] = SQLCommand(
    name='parameter',
    description="Sets the table of Parameters",
    cmd=sql.SQL("""
    CREATE TABLE parameter (
        param_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
        param_type VARCHAR(64) REFERENCES param_set(param_set_id),
        name VARCHAR(64) UNIQUE NOT NULL,
        value FLOAT,
        created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP
    );
""")
),
operations_tables['artifact_type'] = SQLCommand(
    name='artifact_type',
    description="Sets the table of Artifact Types",
    cmd=sql.SQL("""CREATE TABLE artifact_type (
        name VARCHAR(64) PRIMARY KEY,
        description VARCHAR(255),
        created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP
    );
    """)
),
operations_tables['artifact'] = SQLCommand(
    name='artifact',
    description="Sets the table of Artifacts",
    cmd=sql.SQL("""
    CREATE TABLE artifact (
        artifact_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
        artifact_type_name VARCHAR(64) REFERENCES artifact_type(name),
        name VARCHAR(64) UNIQUE NOT NULL,
        value FLOAT,
        title VARCHAR(120),
        description VARCHAR(255),
        creator VARCHAR(128),
        maintainer VARCHAR(128),
        webpage VARCHAR(255),
        uri VARCHAR(255),
        uri_type VARCHAR(32),
        media_type VARCHAR(32),
        frequency VARCHAR(32),
        lifecycle INTEGER,
        created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP,
        extracted TIMESTAMP
    );
""")
),

operations_tables['step'] = SQLCommand(
    name='step',
    description="Creates the Step table",
    cmd=sql.SQL("""
    CREATE TABLE step (
        step_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
        name VARCHAR(64) NOT NULL,
        description VARCHAR(255),
        input_artifact_type VARCHAR(64) REFERENCES artifact_type(name),
        output_artifact_type VARCHAR(64) REFERENCES artifact_type(name),
        param_ids ARRAY(INTEGER),
        created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP

    );
""")
),

operations_tables['pipeline'] = SQLCommand(
    name='pipeline',
    description="Creates the Pipeline table",
    cmd=sql.SQL("""
        CREATE TABLE pipeline (
            pipeline_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
            name VARCHAR(64) NOT NULL,
            description VARCHAR(255),
            created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP
        );
    """)
),

operations_tables['event'] = SQLCommand(
    name='event',
    description="Creates the Event table",
    cmd=sql.SQL("""
        CREATE TABLE event(
            event_id INTEGER GENERATED BY DEFAULT AS IDENTITY,
            name VARCHAR(64) NOT NULL,
            description VARCHAR(255),
            pipeline_id INTEGER REFERENCES pipeline(pipeline_id),
            step_seq INTEGER NOT NULL,
            step_id INTEGER REFERENCES step(step_id),
            step_input_id INTEGER REFERENCES artifact(artifact_id),
            step_output_id INTEGER REFERENCES artifact(artifact_id),
            step_param_set_id INTEGER REFERENCES param_set(param_set_id),
            return_code INTEGER,
            return_description VARCHAR(128),
            created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP,
            executed TIMESTAMP
        );
    """)
)
