"""ComponentParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4393
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COMPONENT_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ComponentParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2444
    from mastapy.system_model.analyses_and_results.parametric_study_tools import (
        _4297,
        _4298,
        _4301,
        _4304,
        _4308,
        _4310,
        _4311,
        _4313,
        _4316,
        _4318,
        _4323,
        _4326,
        _4329,
        _4332,
        _4334,
        _4338,
        _4341,
        _4344,
        _4346,
        _4347,
        _4355,
        _4357,
        _4359,
        _4362,
        _4364,
        _4366,
        _4370,
        _4373,
        _4376,
        _4378,
        _4379,
        _4381,
        _4382,
        _4395,
        _4399,
        _4400,
        _4401,
        _4402,
        _4403,
        _4407,
        _4409,
        _4410,
        _4414,
        _4417,
        _4420,
        _4423,
        _4425,
        _4426,
        _4427,
        _4429,
        _4430,
        _4433,
        _4434,
        _4435,
        _4436,
        _4438,
        _4441,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("ComponentParametricStudyTool",)


Self = TypeVar("Self", bound="ComponentParametricStudyTool")


class ComponentParametricStudyTool(_4393.PartParametricStudyTool):
    """ComponentParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _COMPONENT_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ComponentParametricStudyTool")

    class _Cast_ComponentParametricStudyTool:
        """Special nested class for casting ComponentParametricStudyTool to subclasses."""

        def __init__(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
            parent: "ComponentParametricStudyTool",
        ):
            self._parent = parent

        @property
        def part_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4393.PartParametricStudyTool":
            return self._parent._cast(_4393.PartParametricStudyTool)

        @property
        def part_analysis_case(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_7545.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def abstract_shaft_or_housing_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4297.AbstractShaftOrHousingParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4297,
            )

            return self._parent._cast(_4297.AbstractShaftOrHousingParametricStudyTool)

        @property
        def abstract_shaft_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4298.AbstractShaftParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4298,
            )

            return self._parent._cast(_4298.AbstractShaftParametricStudyTool)

        @property
        def agma_gleason_conical_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4301.AGMAGleasonConicalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4301,
            )

            return self._parent._cast(_4301.AGMAGleasonConicalGearParametricStudyTool)

        @property
        def bearing_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4304.BearingParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4304,
            )

            return self._parent._cast(_4304.BearingParametricStudyTool)

        @property
        def bevel_differential_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4308.BevelDifferentialGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4308,
            )

            return self._parent._cast(_4308.BevelDifferentialGearParametricStudyTool)

        @property
        def bevel_differential_planet_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4310.BevelDifferentialPlanetGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4310,
            )

            return self._parent._cast(
                _4310.BevelDifferentialPlanetGearParametricStudyTool
            )

        @property
        def bevel_differential_sun_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4311.BevelDifferentialSunGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4311,
            )

            return self._parent._cast(_4311.BevelDifferentialSunGearParametricStudyTool)

        @property
        def bevel_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4313.BevelGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4313,
            )

            return self._parent._cast(_4313.BevelGearParametricStudyTool)

        @property
        def bolt_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4316.BoltParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4316,
            )

            return self._parent._cast(_4316.BoltParametricStudyTool)

        @property
        def clutch_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4318.ClutchHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4318,
            )

            return self._parent._cast(_4318.ClutchHalfParametricStudyTool)

        @property
        def concept_coupling_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4323.ConceptCouplingHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4323,
            )

            return self._parent._cast(_4323.ConceptCouplingHalfParametricStudyTool)

        @property
        def concept_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4326.ConceptGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4326,
            )

            return self._parent._cast(_4326.ConceptGearParametricStudyTool)

        @property
        def conical_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4329.ConicalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4329,
            )

            return self._parent._cast(_4329.ConicalGearParametricStudyTool)

        @property
        def connector_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4332.ConnectorParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4332,
            )

            return self._parent._cast(_4332.ConnectorParametricStudyTool)

        @property
        def coupling_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4334.CouplingHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4334,
            )

            return self._parent._cast(_4334.CouplingHalfParametricStudyTool)

        @property
        def cvt_pulley_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4338.CVTPulleyParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4338,
            )

            return self._parent._cast(_4338.CVTPulleyParametricStudyTool)

        @property
        def cycloidal_disc_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4341.CycloidalDiscParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4341,
            )

            return self._parent._cast(_4341.CycloidalDiscParametricStudyTool)

        @property
        def cylindrical_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4344.CylindricalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4344,
            )

            return self._parent._cast(_4344.CylindricalGearParametricStudyTool)

        @property
        def cylindrical_planet_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4346.CylindricalPlanetGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4346,
            )

            return self._parent._cast(_4346.CylindricalPlanetGearParametricStudyTool)

        @property
        def datum_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4347.DatumParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4347,
            )

            return self._parent._cast(_4347.DatumParametricStudyTool)

        @property
        def external_cad_model_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4355.ExternalCADModelParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4355,
            )

            return self._parent._cast(_4355.ExternalCADModelParametricStudyTool)

        @property
        def face_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4357.FaceGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4357,
            )

            return self._parent._cast(_4357.FaceGearParametricStudyTool)

        @property
        def fe_part_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4359.FEPartParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4359,
            )

            return self._parent._cast(_4359.FEPartParametricStudyTool)

        @property
        def gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4362.GearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4362,
            )

            return self._parent._cast(_4362.GearParametricStudyTool)

        @property
        def guide_dxf_model_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4364.GuideDxfModelParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4364,
            )

            return self._parent._cast(_4364.GuideDxfModelParametricStudyTool)

        @property
        def hypoid_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4366.HypoidGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4366,
            )

            return self._parent._cast(_4366.HypoidGearParametricStudyTool)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4370.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4370,
            )

            return self._parent._cast(
                _4370.KlingelnbergCycloPalloidConicalGearParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4373.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4373,
            )

            return self._parent._cast(
                _4373.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4376.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4376,
            )

            return self._parent._cast(
                _4376.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
            )

        @property
        def mass_disc_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4378.MassDiscParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4378,
            )

            return self._parent._cast(_4378.MassDiscParametricStudyTool)

        @property
        def measurement_component_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4379.MeasurementComponentParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4379,
            )

            return self._parent._cast(_4379.MeasurementComponentParametricStudyTool)

        @property
        def mountable_component_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4381.MountableComponentParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4381,
            )

            return self._parent._cast(_4381.MountableComponentParametricStudyTool)

        @property
        def oil_seal_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4382.OilSealParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4382,
            )

            return self._parent._cast(_4382.OilSealParametricStudyTool)

        @property
        def part_to_part_shear_coupling_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4395.PartToPartShearCouplingHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4395,
            )

            return self._parent._cast(
                _4395.PartToPartShearCouplingHalfParametricStudyTool
            )

        @property
        def planet_carrier_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4399.PlanetCarrierParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4399,
            )

            return self._parent._cast(_4399.PlanetCarrierParametricStudyTool)

        @property
        def point_load_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4400.PointLoadParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4400,
            )

            return self._parent._cast(_4400.PointLoadParametricStudyTool)

        @property
        def power_load_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4401.PowerLoadParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4401,
            )

            return self._parent._cast(_4401.PowerLoadParametricStudyTool)

        @property
        def pulley_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4402.PulleyParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4402,
            )

            return self._parent._cast(_4402.PulleyParametricStudyTool)

        @property
        def ring_pins_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4403.RingPinsParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4403,
            )

            return self._parent._cast(_4403.RingPinsParametricStudyTool)

        @property
        def rolling_ring_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4407.RollingRingParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4407,
            )

            return self._parent._cast(_4407.RollingRingParametricStudyTool)

        @property
        def shaft_hub_connection_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4409.ShaftHubConnectionParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4409,
            )

            return self._parent._cast(_4409.ShaftHubConnectionParametricStudyTool)

        @property
        def shaft_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4410.ShaftParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4410,
            )

            return self._parent._cast(_4410.ShaftParametricStudyTool)

        @property
        def spiral_bevel_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4414.SpiralBevelGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4414,
            )

            return self._parent._cast(_4414.SpiralBevelGearParametricStudyTool)

        @property
        def spring_damper_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4417.SpringDamperHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4417,
            )

            return self._parent._cast(_4417.SpringDamperHalfParametricStudyTool)

        @property
        def straight_bevel_diff_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4420.StraightBevelDiffGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4420,
            )

            return self._parent._cast(_4420.StraightBevelDiffGearParametricStudyTool)

        @property
        def straight_bevel_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4423.StraightBevelGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4423,
            )

            return self._parent._cast(_4423.StraightBevelGearParametricStudyTool)

        @property
        def straight_bevel_planet_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4425.StraightBevelPlanetGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4425,
            )

            return self._parent._cast(_4425.StraightBevelPlanetGearParametricStudyTool)

        @property
        def straight_bevel_sun_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4426.StraightBevelSunGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4426,
            )

            return self._parent._cast(_4426.StraightBevelSunGearParametricStudyTool)

        @property
        def synchroniser_half_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4427.SynchroniserHalfParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4427,
            )

            return self._parent._cast(_4427.SynchroniserHalfParametricStudyTool)

        @property
        def synchroniser_part_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4429.SynchroniserPartParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4429,
            )

            return self._parent._cast(_4429.SynchroniserPartParametricStudyTool)

        @property
        def synchroniser_sleeve_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4430.SynchroniserSleeveParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4430,
            )

            return self._parent._cast(_4430.SynchroniserSleeveParametricStudyTool)

        @property
        def torque_converter_pump_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4433.TorqueConverterPumpParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4433,
            )

            return self._parent._cast(_4433.TorqueConverterPumpParametricStudyTool)

        @property
        def torque_converter_turbine_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4434.TorqueConverterTurbineParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4434,
            )

            return self._parent._cast(_4434.TorqueConverterTurbineParametricStudyTool)

        @property
        def unbalanced_mass_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4435.UnbalancedMassParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4435,
            )

            return self._parent._cast(_4435.UnbalancedMassParametricStudyTool)

        @property
        def virtual_component_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4436.VirtualComponentParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4436,
            )

            return self._parent._cast(_4436.VirtualComponentParametricStudyTool)

        @property
        def worm_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4438.WormGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4438,
            )

            return self._parent._cast(_4438.WormGearParametricStudyTool)

        @property
        def zerol_bevel_gear_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "_4441.ZerolBevelGearParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4441,
            )

            return self._parent._cast(_4441.ZerolBevelGearParametricStudyTool)

        @property
        def component_parametric_study_tool(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
        ) -> "ComponentParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ComponentParametricStudyTool.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2444.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ComponentParametricStudyTool._Cast_ComponentParametricStudyTool":
        return self._Cast_ComponentParametricStudyTool(self)
