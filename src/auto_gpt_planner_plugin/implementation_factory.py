from .planner_protocol import PlannerProtocol

from .implementations.file_planner import FilePlanner


class ImplementationFactory:
    """this class is supposed to be used to get the planner implementation to be used by the plugin"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImplementationFactory, cls).__new__(cls)
        return cls.instance

    def get_planner(self, implementation_name: str, agent_id: str) -> PlannerProtocol:
        """returns the planner implementation to be used by the plugin

        Args:

            implementation_name (str): the name of the planner implementation to be used
            param agent_id (str): the id of the agent that is using the planner (for example the name of the AI,
            this can be used to namespace planner data for different agents within the storage implementation)
        """
        if implementation_name == "FilePlanner":
            return FilePlanner()
        else:
            raise Exception(f"Planner with name {implementation_name} is not supported")

