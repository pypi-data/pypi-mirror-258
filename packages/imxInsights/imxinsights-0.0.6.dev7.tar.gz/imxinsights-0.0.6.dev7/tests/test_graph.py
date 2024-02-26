import pytest

from imxInsights.domain.models.imxSituations import ImxSituationsEnum
from imxInsights.graph.imxGraphBuilder import ImxGraphBuilder
from imxInsights.graph.queries.sectionGeometryQuery import SectionGeometryGraphQuery
from imxInsights.utils.shapely_geojson import dump


@pytest.mark.slow
def test_imx_graph_project_v124(imx_v124_project_instance):
    new_situation = imx_v124_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    imx_graph = ImxGraphBuilder(new_situation).build_graph()
    assert len(imx_graph.g.edges) == 370
    assert len(imx_graph.g.nodes) == 150

    from_obj = new_situation.get_by_puic("0aada88e-f8d9-4022-bab1-883666f34b2c")
    to_obj = new_situation.get_by_puic("8cb18979-6b8e-4581-94c4-f4d00c855e6a")
    paths = imx_graph.get_paths_between_imx_objects(from_obj, to_obj)
    assert len(paths) == 2
    SectionGeometryGraphQuery(imx_graph).create_geojson_files()


@pytest.mark.slow
def test_imx_graph_plot_project_v124(imx_v124_project_instance):
    new_situation = imx_v124_project_instance.get_situation_repository(ImxSituationsEnum.NewSituation)
    imx_graph = ImxGraphBuilder(new_situation).build_graph()
    imx_graph._get_plot()


@pytest.mark.slow
def test_imx_graph_project_v500(imx_v500_graph_instance_sauwerd):
    assert len(imx_v500_graph_instance_sauwerd[0].g.edges) == 268
    assert len(imx_v500_graph_instance_sauwerd[0].g.nodes) == 121


@pytest.mark.slow
def test_imx_graph_route(imx_v500_graph_instance_sauwerd):
    from_obj = imx_v500_graph_instance_sauwerd[1].get_by_puic("5e05d312-5b1b-4c7f-af2f-39b186e9443f")
    to_obj = imx_v500_graph_instance_sauwerd[1].get_by_puic("b19afecc-fcf5-44f7-aaae-d8bb6929f8a8")
    to_obj = imx_v500_graph_instance_sauwerd[1].get_by_puic("dc88c55a-0963-4e41-9916-8da3795a544e")
    # to_obj = imx_v500_graph_instance_sauwerd[1].get_by_puic("b19afecc-fcf5-44f7-aaae-d8bb6929f8a8")

    paths = imx_v500_graph_instance_sauwerd[0].get_paths_between_imx_objects(from_obj, to_obj)

    # todo: remove after creation
    for idx, path in enumerate(paths[:10]):
        fc = path.as_feature_collection()
        with open(f"route {path.lr_string}.geojson", "w") as file:
            dump(fc, file)


@pytest.mark.slow
def test_imx_graph_create_sections(imx_v500_graph_instance_sauwerd):
    # todo: remove after creation
    SectionGeometryGraphQuery(imx_v500_graph_instance_sauwerd[0]).create_geojson_files()
