import pytest

from imxInsights.domain.models.imxSituations import ImxSituationsEnum
from imxInsights.graph.imxGraph import ImxGraph
from imxInsights.graph.imxGraphBuilder import ImxGraphBuilder
from imxInsights.repo.imxRepo import SituationRepo


@pytest.fixture(scope="module")
def imx_v500_graph_instance_sauwerd(imx_v500_sauwerd_project_instance) -> tuple[ImxGraph, SituationRepo]:
    init_situation = imx_v500_sauwerd_project_instance.get_situation_repository(ImxSituationsEnum.InitialSituation)
    return ImxGraphBuilder(init_situation).build_graph(), init_situation
