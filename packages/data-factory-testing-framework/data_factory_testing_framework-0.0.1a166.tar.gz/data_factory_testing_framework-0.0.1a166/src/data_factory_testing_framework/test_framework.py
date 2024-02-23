from enum import Enum
from typing import Iterator, List

from azure.core import CaseInsensitiveEnumMeta

from data_factory_testing_framework.exceptions.pipeline_activities_circular_dependency_error import (
    PipelineActivitiesCircularDependencyError,
)
from data_factory_testing_framework.models.activities.activity import Activity
from data_factory_testing_framework.models.activities.control_activity import ControlActivity
from data_factory_testing_framework.models.activities.execute_pipeline_activity import (
    ExecutePipelineActivity,
)
from data_factory_testing_framework.models.activities.fail_activity import FailActivity
from data_factory_testing_framework.models.activities.for_each_activity import ForEachActivity
from data_factory_testing_framework.models.activities.if_condition_activity import (
    IfConditionActivity,
)
from data_factory_testing_framework.models.activities.switch_activity import SwitchActivity
from data_factory_testing_framework.models.activities.until_activity import UntilActivity
from data_factory_testing_framework.models.pipeline import Pipeline
from data_factory_testing_framework.repositories.data_factory_repository import DataFactoryRepository
from data_factory_testing_framework.repositories.data_factory_repository_factory import (
    DataFactoryRepositoryFactory,
)
from data_factory_testing_framework.repositories.fabric_repository_factory import (
    FabricRepositoryFactory,
)
from data_factory_testing_framework.state import PipelineRunState, RunParameter


class TestFrameworkType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """TestFrameworkType."""

    __test__ = False  # Prevent pytest from discovering this class as a test class

    DataFactory = "DataFactory"
    Fabric = "Fabric"
    Synapse = "Synapse"


class TestFramework:
    __test__ = False  # Prevent pytest from discovering this class as a test class

    def __init__(
        self,
        framework_type: TestFrameworkType,
        root_folder_path: str = None,
        should_evaluate_child_pipelines: bool = False,
    ) -> None:
        """Initializes the test framework allowing you to evaluate pipelines and activities.

        Args:
            framework_type: type of the test framework.
            root_folder_path: optional path to the folder containing the data factory files.
            The repository attribute will be populated with the data factory entities if provided.
            should_evaluate_child_pipelines: optional boolean indicating whether child pipelines should be evaluated. Defaults to False.
        """
        if framework_type == TestFrameworkType.Fabric:
            if root_folder_path is not None:
                self.repository = FabricRepositoryFactory().parse_from_folder(root_folder_path)
            else:
                self.repository = DataFactoryRepository([])
        elif framework_type == TestFrameworkType.DataFactory:
            if root_folder_path is not None:
                self.repository = DataFactoryRepositoryFactory().parse_from_folder(root_folder_path)
            else:
                self.repository = DataFactoryRepository([])
        elif framework_type == TestFrameworkType.Synapse:
            raise NotImplementedError("Synapse test framework is not implemented yet.")

        self.should_evaluate_child_pipelines = should_evaluate_child_pipelines

    def evaluate_activity(self, activity: Activity, state: PipelineRunState) -> Iterator[Activity]:
        """Evaluates a single activity given a state. Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activity: The activity to evaluate.
            state: The state to use for evaluating the activity.

        Returns:
             A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        return self.evaluate_activities([activity], state)

    def evaluate_pipeline(self, pipeline: Pipeline, parameters: List[RunParameter]) -> Iterator[Activity]:
        """Evaluates all pipeline activities using the provided parameters.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            pipeline: The pipeline to evaluate.
            parameters: The parameters to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        parameters = pipeline.validate_and_append_default_parameters(parameters)
        state = PipelineRunState(parameters, pipeline.get_run_variables())
        return self.evaluate_activities(pipeline.activities, state)

    def evaluate_activities(self, activities: List[Activity], state: PipelineRunState) -> Iterator[Activity]:
        """Evaluates all activities using the provided state.

        The order of activity execution is simulated based on the dependencies.
        Any expression part of the activity is evaluated based on the state of the pipeline.

        Args:
            activities: The activities to evaluate.
            state: The state to use for evaluating the pipeline.

        Returns:
            A list of evaluated pipelines, which can be more than 1 due to possible child activities.
        """
        fail_activity_evaluated = False
        while len(state.scoped_pipeline_activity_results) != len(activities):
            any_activity_evaluated = False
            for activity in filter(
                lambda a: a.name not in state.scoped_pipeline_activity_results
                and a.are_dependency_condition_met(state),
                activities,
            ):
                evaluated_activity = activity.evaluate(state)
                if not self._is_iteration_activity(evaluated_activity) or (
                    isinstance(evaluated_activity, ExecutePipelineActivity) and not self.should_evaluate_child_pipelines
                ):
                    yield evaluated_activity

                if isinstance(activity, FailActivity):
                    fail_activity_evaluated = True
                    break

                any_activity_evaluated = True
                state.add_activity_result(activity.name, activity.status, activity.output)

                # Check if there are any child activities to evaluate
                if self._is_iteration_activity(activity):
                    activities_iterator = []
                    if isinstance(activity, ExecutePipelineActivity) and self.should_evaluate_child_pipelines:
                        execute_pipeline_activity: ExecutePipelineActivity = activity
                        pipeline = self.repository.get_pipeline_by_name(
                            execute_pipeline_activity.type_properties["pipeline"]["referenceName"],
                        )
                        activities_iterator = execute_pipeline_activity.evaluate_pipeline(
                            pipeline,
                            activity.get_child_run_parameters(state),
                            self.evaluate_activities,
                        )

                    if not isinstance(activity, ExecutePipelineActivity) and isinstance(activity, ControlActivity):
                        control_activity: ControlActivity = activity
                        activities_iterator = control_activity.evaluate_control_activities(
                            state,
                            self.evaluate_activities,
                        )

                    for child_activity in activities_iterator:
                        yield child_activity
                        if isinstance(child_activity, FailActivity):
                            fail_activity_evaluated = True
                            break

            if fail_activity_evaluated:
                break

            if not any_activity_evaluated:
                raise PipelineActivitiesCircularDependencyError()

    @staticmethod
    def _is_iteration_activity(activity: Activity) -> bool:
        return (
            isinstance(activity, UntilActivity)
            or isinstance(activity, ForEachActivity)
            or isinstance(activity, IfConditionActivity)
            or isinstance(activity, SwitchActivity)
            or isinstance(activity, ExecutePipelineActivity)
        )
