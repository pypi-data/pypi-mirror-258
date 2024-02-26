from imxInsights.graph.imxGraphJunction import ImxGraphJunction


def test_double_diamond_switch():
    # flake8: noqa E501  F841

    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
                <DoubleDiamondCrossing puic="f3c68657-7dcc-44ac-9107-05f0eefbffa7" name="251/253" angleRatio="1:9" isReadRedundantly="Unknown">
                  <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                  <Location>
                    <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                      <gml:Point srsName="EPSG:28992">
                        <gml:coordinates>248546.016,608117.625,2.337</gml:coordinates>
                      </gml:Point>
                    </GeographicLocation>
                  </Location>
                  <MathematicalPoint dataAcquisitionMethod="Constructed">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>248546.016,608117.625,2.337</gml:coordinates>
                    </gml:Point>
                  </MathematicalPoint>
                  <SwitchBlades puic="e01947d0-d258-4bdd-ad4e-d2ed16c8f8f1" name="E/G" switchCheckerAmount="0">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248551.167,608126.167,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </SwitchBlades>
                  <SwitchBlades puic="5454f88a-486c-472b-8bfa-1e68f6ac13cf" name="B/D" switchCheckerAmount="0">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248540.865,608109.082,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </SwitchBlades>
                  <SwitchBlades puic="c79e2052-b27e-4e4a-967d-88304aa805a7" name="F/H" switchCheckerAmount="0">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248552.084,608125.542,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </SwitchBlades>
                  <SwitchBlades puic="eb97d334-92ed-4beb-91a6-0fed6f791f2a" name="A/C" switchCheckerAmount="0">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248539.948,608109.707,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </SwitchBlades>
                  <FoulingPoint puic="64251adf-11d4-488b-b54e-c887e1de1d56">
                    <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248566.428,608147.312,2.476</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </FoulingPoint>
                  <FoulingPoint puic="b9ee3808-82d8-412f-a1ee-e7030af1ff25">
                    <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248525.764,608087.663,2.471</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </FoulingPoint>
                  <SwitchMechanism puic="afa7d8b7-dc50-4117-a3eb-f50e052e5bac" name="253" fixType="Locked" operatingType="Central" normalPosition="Left" preferredPosition="Unknown" isSpringSwitch="False">
                    <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248552.626,608124.854,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                    <Lock puic="00000000-0000-4000-aaad-000000000000" lockType="Unknown">
                      <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                      <Location>
                        <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                          <gml:Point srsName="EPSG:28992">
                            <gml:coordinates>248552.626,608124.854,9.917</gml:coordinates>
                          </gml:Point>
                        </GeographicLocation>
                      </Location>
                    </Lock>
                  </SwitchMechanism>
                  <SwitchMechanism puic="4d0db99e-e7fa-4987-abc0-39fe41c0b474" name="251" fixType="None" operatingType="Central" normalPosition="Left" preferredPosition="Unknown" isSpringSwitch="False">
                    <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248539.407,608110.395,9.917</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </SwitchMechanism>
                  <Passage puic="30ccd72c-8bfd-4698-b0a7-b69be4dd74d6" name="253Q" sideTag="Q" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248546.016,608117.625,2.337 248551.167,608126.167,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="d8a86e05-f6a3-43f9-aa59-023659075103" name="S" sideTag="S" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248552.084,608125.542,2.337 248560.013,608135.888,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="51ee750a-e2b8-412e-87c0-109cb1db568f" name="P-Q" sideTag="P_Q" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248539.948,608109.707,2.337 248545.722,608117.798,2.337 248551.167,608126.167,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="53ee4b7d-e034-4f8f-aca5-1c07d8e514fd" name="S-T" sideTag="S_T" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248540.865,608109.082,2.337 248546.295,608117.454,2.337 248552.084,608125.542,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="72bd2660-86a2-4307-ad14-ef4ba1e31ae7" name="251P" sideTag="P" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248539.948,608109.707,2.337 248546.016,608117.625,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="0cb8723c-db37-4d50-8c3d-1c690176d483" name="P" sideTag="P" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248532.019,608099.361,2.337 248539.948,608109.707,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="02256772-7b3c-4578-aec5-cbdef7ae3803" name="251T" sideTag="T" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248540.865,608109.082,2.337 248546.016,608117.625,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="c54c078d-47fa-4d6e-9f1f-2e4850652d33" name="T" sideTag="T" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248534.134,608097.92,2.337 248540.865,608109.082,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="a3f7b3d3-92f4-46d2-89f6-f862d05a62d7" name="Q" sideTag="Q" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248551.167,608126.167,2.337 248557.898,608137.329,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <Passage puic="37b06506-fce1-464f-98cf-0ca2e861b51e" name="253S" sideTag="S" passageSpeed="40" unrestricted="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:LineString srsName="EPSG:28992">
                          <gml:coordinates>248546.016,608117.625,2.337 248552.084,608125.542,2.337</gml:coordinates>
                        </gml:LineString>
                      </GeographicLocation>
                    </Location>
                  </Passage>
                  <DivergingPassageRefs>51ee750a-e2b8-412e-87c0-109cb1db568f 53ee4b7d-e034-4f8f-aca5-1c07d8e514fd</DivergingPassageRefs>
                  <KCrossing puic="b531f309-e946-4bf4-a2a7-58129ece9991" name="251/253" isMovable="Unknown">
                    <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                    <Location>
                      <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                        <gml:Point srsName="EPSG:28992">
                          <gml:coordinates>248546.016,608117.625,0</gml:coordinates>
                        </gml:Point>
                      </GeographicLocation>
                    </Location>
                  </KCrossing>
                </DoubleDiamondCrossing>
    </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)
    # PUICs for the specified path
    path_puics = [
        "0cb8723c-db37-4d50-8c3d-1c690176d483",
        "72bd2660-86a2-4307-ad14-ef4ba1e31ae7",
        "30ccd72c-8bfd-4698-b0a7-b69be4dd74d6",
        "a3f7b3d3-92f4-46d2-89f6-f862d05a62d7",
    ]

    path_geometries = imx_junction._get_path_geometry(path_puics)
    path = imx_junction.get_path(path_puics)

    # imx_junction.plot_path_with_elements(path_geometries)

    switch_253_pos_for_P = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["afa7d8b7-dc50-4117-a3eb-f50e052e5bac"], imx_junction.passages["0cb8723c-db37-4d50-8c3d-1c690176d483"]
    )
    assert switch_253_pos_for_P == "right"

    switch_253_pos_for_251P = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["afa7d8b7-dc50-4117-a3eb-f50e052e5bac"], imx_junction.passages["72bd2660-86a2-4307-ad14-ef4ba1e31ae7"]
    )
    assert switch_253_pos_for_251P == "right"

    switch_253_pos_for_T = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["afa7d8b7-dc50-4117-a3eb-f50e052e5bac"], imx_junction.passages["c54c078d-47fa-4d6e-9f1f-2e4850652d33"]
    )
    assert switch_253_pos_for_T == "left"

    switch_253_pos_for_251T = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["afa7d8b7-dc50-4117-a3eb-f50e052e5bac"], imx_junction.passages["02256772-7b3c-4578-aec5-cbdef7ae3803"]
    )
    assert switch_253_pos_for_251T == "left"

    switch_251_pos_for_Q = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["4d0db99e-e7fa-4987-abc0-39fe41c0b474"], imx_junction.passages["a3f7b3d3-92f4-46d2-89f6-f862d05a62d7"]
    )
    assert switch_251_pos_for_Q == "left"

    switch_251_pos_for_253Q = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["4d0db99e-e7fa-4987-abc0-39fe41c0b474"], imx_junction.passages["30ccd72c-8bfd-4698-b0a7-b69be4dd74d6"]
    )
    assert switch_251_pos_for_253Q == "left"

    switch_251_pos_for_S = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["4d0db99e-e7fa-4987-abc0-39fe41c0b474"], imx_junction.passages["d8a86e05-f6a3-43f9-aa59-023659075103"]
    )
    assert switch_251_pos_for_S == "right"

    switch_251_pos_for_253S = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["4d0db99e-e7fa-4987-abc0-39fe41c0b474"], imx_junction.passages["37b06506-fce1-464f-98cf-0ca2e861b51e"]
    )
    assert switch_251_pos_for_253S == "right"


def test_crossing():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <Crossing puic="323aea00-843f-4d43-8556-5f9f8e7201df" name="K212" angleRatio="1:9" hasMovableOverheadLine="False">
              <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>231900.937,590192.029,1.132</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
              <KCrossing puic="38eca962-6c9f-4f9f-baab-3061c91860d5" name="K212" isMovable="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>231900.937,590192.029,1.132</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </KCrossing>
              <Passage puic="4fbea176-aa17-4fae-98e9-7faa5a4dca4f" name="Q" sideTag="Q" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>231900.937,590192.029,1.132 231900.34,590205.027,1.132</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="89149879-3be0-45e8-8c58-2612efdafea9" name="T" sideTag="T" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>231900.937,590192.029,1.132 231901.511,590178.882,1.139</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="cb63a3e0-77a0-4cd0-be8a-f1b966c8c4f2" name="S" sideTag="S" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>231900.937,590192.029,1.132 231902.058,590205.055,1.127</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="137e8ecc-3dd3-4c9c-aac1-c0786d03ac6d" name="P" sideTag="P" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>231900.937,590192.029,1.132 231899.818,590178.968,1.132</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <FoulingPoint puic="fc0fe256-49e7-450f-ab66-6783fec70765">
                <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>231900.236,590158.712,1.223</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
              <FoulingPoint puic="f1e5f05f-deae-48b5-82f4-1746607b1ed4">
                <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>231901.551,590225.539,1.18</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
            </Crossing>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)

    path_puics = ["137e8ecc-3dd3-4c9c-aac1-c0786d03ac6d", "cb63a3e0-77a0-4cd0-be8a-f1b966c8c4f2"]
    path_geometries = imx_junction._get_path_geometry(path_puics)
    # imx_junction.plot_path_with_elements(path_geometries)


def test_single():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <SingleSwitch puic="bdfe49d0-43fc-45dd-8ee2-d6672cf632bd" name="943" angleRatio="1:9" isReadRedundantly="Unknown">
              <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>246308.707,604541.52,1.765</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
              <MathematicalPoint dataAcquisitionMethod="Constructed">
                <gml:Point srsName="EPSG:28992">
                  <gml:coordinates>246316.187,604548.221,1.765</gml:coordinates>
                </gml:Point>
              </MathematicalPoint>
              <SwitchBlades puic="dba05cf2-711a-4a42-a30d-a9f87edadc33" name="A/B" switchCheckerAmount="0">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>246308.707,604541.52,1.765</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <FoulingPoint puic="c5ee760c-1328-4c22-857a-4dd56df69347">
                <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>246341.511,604568.348,1.872</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
              <SwitchMechanism puic="e0951801-bbf8-4eb6-bdc8-24ae151377c3" name="943" fixType="None" operatingType="Manual" normalPosition="Left" preferredPosition="Unknown" isSpringSwitch="False">
                <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>246308.93,604541.758,0</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchMechanism>
              <Passage puic="bc2435a1-4a94-4df4-87f3-ab0a885c829e" name="R" sideTag="R" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>246335.703,604562.129,1.765 246331.101,604558.867,1.765 246326.223,604555.439,1.765 246320.799,604551.498,1.765 246315.247,604547.067,1.765 246311.611,604543.973,1.765 246308.707,604541.52,1.765</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="71bc74a0-e11b-45f9-ad7c-2beeaa5dae5b" name="V" sideTag="V" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>246305.355,604538.518,1.765 246308.707,604541.52,1.765</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="fc4ba9f6-8937-4ee9-b6e7-4cf30cae25c6" name="L" sideTag="L" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>246308.707,604541.52,1.765 246334.08,604564.251,1.765</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <DivergingPassageRefs>bc2435a1-4a94-4df4-87f3-ab0a885c829e</DivergingPassageRefs>
            </SingleSwitch>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)

    path_puics = ["71bc74a0-e11b-45f9-ad7c-2beeaa5dae5b", "bc2435a1-4a94-4df4-87f3-ab0a885c829e"]
    path_geometries = imx_junction._get_path_geometry(path_puics)
    # imx_junction.plot_path_with_elements(path_geometries)

    right = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["e0951801-bbf8-4eb6-bdc8-24ae151377c3"], imx_junction.passages["bc2435a1-4a94-4df4-87f3-ab0a885c829e"]
    )
    assert right == "right"

    left = imx_junction._passage_left_or_right_of_switch(
        imx_junction.switch_mechanisms["e0951801-bbf8-4eb6-bdc8-24ae151377c3"], imx_junction.passages["fc4ba9f6-8937-4ee9-b6e7-4cf30cae25c6"]
    )
    assert left == "left"


def test_buffer():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <BufferStop puic="950dced8-a4fd-4f02-a105-70809380b05a" name="SJ_23L" signRef="0f904b5e-b411-42e4-8b21-ba812a544daf">
              <Metadata originType="SharedMatched" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" azimuth="-274" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>233548.863,581108.156,2.15</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
            </BufferStop>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)


def test_track_end():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <TrackEnd puic="0d65e93e-87d5-4e88-9056-7f1d4e9c12ac" name="ES_927L">
              <Metadata originType="SharedBBKOnly" source="Arcadis" lifeCycleStatus="Existing" isInService="True" />
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>249512.254,608340.799,5.381</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
            </TrackEnd>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)


def test_double_2():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <DoubleDiamondCrossing puic="50131dbf-3950-458d-abcf-e401c72ea314" name="79B/81A" angleRatio="1:9" divergingSpeed="40" divergingDirection="None">
              <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>210484.228,462379.352,10.454</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
              <MathematicalPoint dataAcquisitionMethod="Constructed">
                <gml:Point srsName="EPSG:28992">
                  <gml:coordinates>210484.228,462379.352,10.454</gml:coordinates>
                </gml:Point>
              </MathematicalPoint>
              <SwitchBlades puic="ef607d81-5e04-43cc-bf97-6a1985a4a38c" name="A/C">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210477.857,462371.677,10.499</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="57b86b12-3936-4a8f-9b0b-c008b6e30054" name="E/G">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210489.708,462387.688,10.409</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="f56df1a3-ad0f-4818-8b01-ec01ff990e41" name="B/D">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210478.749,462371.017,10.5</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="1cf9ec0d-c487-4716-89ec-e27b1438abb6" name="F/H">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210490.6,462387.028,10.409</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <FoulingPoint puic="48b70e68-9464-4cf3-a42e-df90a03e4e00">
                <Metadata originType="Unknown" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210506.043,462408.896,10.448</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
              <SwitchMechanism puic="28ba93a1-d2f3-41b2-881f-9e42b3f1efbe" name="79B" switchMechanismType="Central" normalPosition="Right" preferredPosition="Unknown" hasSwitchChecker="True" isSpringSwitch="False" lockType="None" interconnectedSwitchMechanismRef="d25dd061-6235-4e2e-8ce4-20f128af554e">
                <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210478.303,462371.347,10.5</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchMechanism>
              <SwitchMechanism puic="a344ddbe-9a0e-46c5-a026-abbfb09cf45f" name="81A" switchMechanismType="Central" normalPosition="Right" preferredPosition="Unknown" hasSwitchChecker="True" isSpringSwitch="False" lockType="None" interconnectedSwitchMechanismRef="d9f9dd69-fe4c-4b10-b4a4-2cf23e305f8d">
                <Metadata originType="SharedMatched" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210490.154,462387.358,10.409</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchMechanism>
              <Passage puic="1843f845-cc72-4b04-9f81-851e165f759e" name="S-T" sideTag="S_T">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210478.749,462371.017,10.5 210484.501,462379.171,10.454 210490.6,462387.028,10.409</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="d7cf7f6b-616c-47e8-a6d6-8004623dbd55" name="79BT" sideTag="T">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210478.749,462371.017,10.5 210484.228,462379.352,10.454</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="233ef88c-df66-4b4f-88a6-039aee883782" name="Q" sideTag="Q">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210489.708,462387.688,10.409 210495.344,462396.243,10.361</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="a3e6a898-3104-471d-b181-d1300252750c" name="T" sideTag="T">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210474.981,462365.285,10.531 210478.749,462371.017,10.5</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="574b3b7b-a305-4c6d-bd1d-0ad31a4655de" name="P-Q" sideTag="P_Q">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210477.857,462371.677,10.499 210483.942,462379.537,10.454 210489.708,462387.688,10.409</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="f1cd10b6-9770-4db1-817e-3fe67f74d53a" name="P" sideTag="P">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210471.495,462364.012,10.545 210477.857,462371.677,10.499</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="ef1e749b-4d49-459f-94cb-807cc437df22" name="79BP" sideTag="P">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210477.857,462371.677,10.499 210484.228,462379.352,10.454</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="1c573839-85c9-4ca0-ae08-736c2f688e63" name="81AS" sideTag="S">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210484.228,462379.352,10.454 210490.6,462387.028,10.409</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="a58c7cf4-3d4c-4aa9-844e-955560178212" name="S" sideTag="S">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210490.6,462387.028,10.409 210500.878,462399.308,10.313</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="c1db359f-6073-4d4e-9b33-a97df2506764" name="81AQ" sideTag="Q">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>210484.228,462379.352,10.454 210489.708,462387.688,10.409</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <KCrossing puic="2ef7a317-9b23-4537-99af-337d5f026374" name="79B/81A">
                <Metadata originType="BBK" source="Arcadis" lifeCycleStatus="Existing" registrationTime="2022-09-06T00:00:00Z" isInService="True"/>
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>210484.228,462379.352,10.454</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </KCrossing>
            </DoubleDiamondCrossing>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)
    # imx_junction.plot_path_with_elements()


def test_double_3():
    xml_data = """<ImSpoor xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" imxVersion="5.0.0" xsi:schemaLocation="http://www.prorail.nl/IMSpoor ImSpoor-Communication.xsd" xmlns="http://www.prorail.nl/IMSpoor">
    <!-- Insert passages XML here -->
            <DoubleDiamondCrossing puic="4883c8b4-4f22-42e0-8eb3-cee8ebb666f6" name="19B/25" angleRatio="1:9" isReadRedundantly="Unknown">
              <Metadata originType="SharedMatched" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
              <Location>
                <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                  <gml:Point srsName="EPSG:28992">
                    <gml:coordinates>233370.31,581078.355,2.297</gml:coordinates>
                  </gml:Point>
                </GeographicLocation>
              </Location>
              <MathematicalPoint dataAcquisitionMethod="Constructed">
                <gml:Point srsName="EPSG:28992">
                  <gml:coordinates>233370.31,581078.355,2.297</gml:coordinates>
                </gml:Point>
              </MathematicalPoint>
              <SwitchBlades puic="3ddfc5c7-0ce4-46f8-ac2e-7a02b4272519" name="F/H" switchCheckerAmount="0">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233360.343,581078.754,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="2c14a097-eda9-4629-a2a1-0c76cac19636" name="A/C" switchCheckerAmount="0">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233380.277,581077.955,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="37736608-7e54-4c06-b7a2-c0cb8bfbd728" name="B/D" switchCheckerAmount="0">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233380.26,581079.064,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <SwitchBlades puic="81451500-de97-43ab-9657-d345ff3f2362" name="E/G" switchCheckerAmount="0">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233360.361,581077.645,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchBlades>
              <FoulingPoint puic="db0c7748-d4c5-4ec1-bcd1-dbb0c674bb4a">
                <Metadata originType="Unknown" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="Unknown" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233407.362,581078.921,2.601</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
              <FoulingPoint puic="f6b572ed-7b36-4402-ac5a-933de421aa50">
                <Metadata originType="Unknown" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="Unknown" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233334.893,581077.686,2.595</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </FoulingPoint>
              <SwitchMechanism puic="36a95b57-6fa9-4025-b997-bb6d0ed4cb5f" name="19B" fixType="None" operatingType="Central" normalPosition="Left" preferredPosition="Unknown" isSpringSwitch="False" interconnectedSwitchMechanismRef="74006b3b-9d31-4d80-8edf-07f923b2df5b">
                <Metadata originType="SharedMatched" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233380.269,581078.51,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchMechanism>
              <SwitchMechanism puic="26be12d3-ca7b-494e-98b4-bdc9f97a2349" name="25" fixType="None" operatingType="Central" normalPosition="Left" preferredPosition="Unknown" isSpringSwitch="False">
                <Metadata originType="SharedMatched" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233360.352,581078.2,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </SwitchMechanism>
              <Passage puic="a9b7fc19-9be7-433a-ac9d-1574103cf7ed" name="S" sideTag="S" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233360.343,581078.754,2.297 233352.474,581079.074,2.311</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="aceca7a3-cf5f-492a-8ea9-a5021f5e7014" name="25Q" sideTag="Q" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233370.31,581078.355,2.297 233360.361,581077.645,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="68a4341c-9afa-42d9-b6b8-0a3b5f5a24ce" name="Q" sideTag="Q" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233360.361,581077.645,2.297 233352.502,581077.082,2.311</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="1838c882-eec9-4728-b8f0-1dbd24ad47af" name="T" sideTag="T" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233393.262,581079.992,2.297 233380.26,581079.064,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="84b4cc35-2386-48c8-b603-80cc6f7b28b2" name="19BT" sideTag="T" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233380.26,581079.064,2.297 233370.31,581078.355,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="fa24ccfe-f9b2-4fe8-9121-38fd739d6a51" name="P" sideTag="P" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233393.302,581077.433,2.297 233380.277,581077.955,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="3a73559e-b968-44cd-b956-d037cb638c51" name="19BP" sideTag="P" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233380.277,581077.955,2.297 233370.31,581078.355,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="6fa21f61-96a5-49a7-a778-613a965569ac" name="25S" sideTag="S" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233370.31,581078.355,2.297 233360.343,581078.754,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="5e595d2f-0203-42a5-936e-febabe9dc475" name="P-Q" sideTag="P_Q" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233380.277,581077.955,2.297 233370.338,581078.015,2.297 233360.361,581077.645,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <Passage puic="8acd0915-025d-40cd-a354-72673777740f" name="S-T" sideTag="S_T" passageSpeed="40" unrestricted="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:LineString srsName="EPSG:28992">
                      <gml:coordinates>233380.26,581079.064,2.297 233370.289,581078.681,2.297 233360.343,581078.754,2.297</gml:coordinates>
                    </gml:LineString>
                  </GeographicLocation>
                </Location>
              </Passage>
              <DivergingPassageRefs>5e595d2f-0203-42a5-936e-febabe9dc475 8acd0915-025d-40cd-a354-72673777740f</DivergingPassageRefs>
              <KCrossing puic="9166ba49-2bc2-4957-a2e7-cd3d85a51330" name="19B/25" isMovable="Unknown">
                <Metadata originType="BBK" source="Arcadis" registrationTime="2020-11-06T00:00:00Z" lifeCycleStatus="Existing" isInService="True" />
                <Location>
                  <GeographicLocation dataAcquisitionMethod="Photogrammetry" accuracy="60">
                    <gml:Point srsName="EPSG:28992">
                      <gml:coordinates>233370.31,581078.355,2.297</gml:coordinates>
                    </gml:Point>
                  </GeographicLocation>
                </Location>
              </KCrossing>
            </DoubleDiamondCrossing>
        </ImSpoor>
    """

    imx_junction = ImxGraphJunction(xml_data)
    # imx_junction.plot_path_with_elements()
