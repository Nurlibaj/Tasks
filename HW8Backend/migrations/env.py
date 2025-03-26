from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.sql_models import Base

config = context.config


fileConfig(config.config_file_name)

target_metadata = Base.metadata
