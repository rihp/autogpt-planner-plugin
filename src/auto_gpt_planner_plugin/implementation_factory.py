from .planner_protocol import PlannerProtocol
from autogpt.config import Config
from .implementations.file_planner import FilePlanner
from .implementations.sqlite_planner import SqlitePlanner

import re


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s


def get_planner(implementation_name: str, agent_id: str) -> PlannerProtocol:
    CFG = Config()
    """returns the planner implementation to be used by the plugin

    Args:
        implementation_name (str): the name of the planner implementation to be used
        agent_id (str): the id of the agent that is using the planner (for example the name of the AI,
        this can be used to namespace planner data for different agents within the storage implementation)
    """
    if implementation_name == "FilePlanner":
        return FilePlanner()
    if implementation_name == "SqlitePlanner":
        return SqlitePlanner(db_path=f"{CFG.workspace_path}/planner_{slugify(agent_id)}.db")

    else:
        raise Exception(f"Planner with name {implementation_name} is not supported")
