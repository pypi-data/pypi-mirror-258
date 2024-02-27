"""MountableComponentCompoundParametricStudyTool"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4468,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "MountableComponentCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.parametric_study_tools import _4381
    from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4447,
        _4451,
        _4454,
        _4457,
        _4458,
        _4459,
        _4466,
        _4471,
        _4472,
        _4475,
        _4479,
        _4482,
        _4485,
        _4490,
        _4493,
        _4496,
        _4501,
        _4505,
        _4509,
        _4512,
        _4515,
        _4518,
        _4519,
        _4521,
        _4525,
        _4528,
        _4529,
        _4530,
        _4531,
        _4532,
        _4535,
        _4539,
        _4542,
        _4547,
        _4548,
        _4551,
        _4554,
        _4555,
        _4557,
        _4558,
        _4559,
        _4562,
        _4563,
        _4564,
        _4565,
        _4566,
        _4569,
        _4522,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundParametricStudyTool",)


Self = TypeVar("Self", bound="MountableComponentCompoundParametricStudyTool")


class MountableComponentCompoundParametricStudyTool(
    _4468.ComponentCompoundParametricStudyTool
):
    """MountableComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MountableComponentCompoundParametricStudyTool"
    )

    class _Cast_MountableComponentCompoundParametricStudyTool:
        """Special nested class for casting MountableComponentCompoundParametricStudyTool to subclasses."""

        def __init__(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
            parent: "MountableComponentCompoundParametricStudyTool",
        ):
            self._parent = parent

        @property
        def component_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4468.ComponentCompoundParametricStudyTool":
            return self._parent._cast(_4468.ComponentCompoundParametricStudyTool)

        @property
        def part_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4522.PartCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4522,
            )

            return self._parent._cast(_4522.PartCompoundParametricStudyTool)

        @property
        def part_compound_analysis(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4447.AGMAGleasonConicalGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4447,
            )

            return self._parent._cast(
                _4447.AGMAGleasonConicalGearCompoundParametricStudyTool
            )

        @property
        def bearing_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4451.BearingCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4451,
            )

            return self._parent._cast(_4451.BearingCompoundParametricStudyTool)

        @property
        def bevel_differential_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4454.BevelDifferentialGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4454,
            )

            return self._parent._cast(
                _4454.BevelDifferentialGearCompoundParametricStudyTool
            )

        @property
        def bevel_differential_planet_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4457.BevelDifferentialPlanetGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4457,
            )

            return self._parent._cast(
                _4457.BevelDifferentialPlanetGearCompoundParametricStudyTool
            )

        @property
        def bevel_differential_sun_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4458.BevelDifferentialSunGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4458,
            )

            return self._parent._cast(
                _4458.BevelDifferentialSunGearCompoundParametricStudyTool
            )

        @property
        def bevel_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4459.BevelGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4459,
            )

            return self._parent._cast(_4459.BevelGearCompoundParametricStudyTool)

        @property
        def clutch_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4466.ClutchHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4466,
            )

            return self._parent._cast(_4466.ClutchHalfCompoundParametricStudyTool)

        @property
        def concept_coupling_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4471.ConceptCouplingHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4471,
            )

            return self._parent._cast(
                _4471.ConceptCouplingHalfCompoundParametricStudyTool
            )

        @property
        def concept_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4472.ConceptGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4472,
            )

            return self._parent._cast(_4472.ConceptGearCompoundParametricStudyTool)

        @property
        def conical_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4475.ConicalGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4475,
            )

            return self._parent._cast(_4475.ConicalGearCompoundParametricStudyTool)

        @property
        def connector_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4479.ConnectorCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4479,
            )

            return self._parent._cast(_4479.ConnectorCompoundParametricStudyTool)

        @property
        def coupling_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4482.CouplingHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4482,
            )

            return self._parent._cast(_4482.CouplingHalfCompoundParametricStudyTool)

        @property
        def cvt_pulley_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4485.CVTPulleyCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4485,
            )

            return self._parent._cast(_4485.CVTPulleyCompoundParametricStudyTool)

        @property
        def cylindrical_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4490.CylindricalGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4490,
            )

            return self._parent._cast(_4490.CylindricalGearCompoundParametricStudyTool)

        @property
        def cylindrical_planet_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4493.CylindricalPlanetGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4493,
            )

            return self._parent._cast(
                _4493.CylindricalPlanetGearCompoundParametricStudyTool
            )

        @property
        def face_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4496.FaceGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4496,
            )

            return self._parent._cast(_4496.FaceGearCompoundParametricStudyTool)

        @property
        def gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4501.GearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4501,
            )

            return self._parent._cast(_4501.GearCompoundParametricStudyTool)

        @property
        def hypoid_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4505.HypoidGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4505,
            )

            return self._parent._cast(_4505.HypoidGearCompoundParametricStudyTool)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4509.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4509,
            )

            return self._parent._cast(
                _4509.KlingelnbergCycloPalloidConicalGearCompoundParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4512.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4512,
            )

            return self._parent._cast(
                _4512.KlingelnbergCycloPalloidHypoidGearCompoundParametricStudyTool
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4515.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4515,
            )

            return self._parent._cast(
                _4515.KlingelnbergCycloPalloidSpiralBevelGearCompoundParametricStudyTool
            )

        @property
        def mass_disc_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4518.MassDiscCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4518,
            )

            return self._parent._cast(_4518.MassDiscCompoundParametricStudyTool)

        @property
        def measurement_component_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4519.MeasurementComponentCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4519,
            )

            return self._parent._cast(
                _4519.MeasurementComponentCompoundParametricStudyTool
            )

        @property
        def oil_seal_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4521.OilSealCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4521,
            )

            return self._parent._cast(_4521.OilSealCompoundParametricStudyTool)

        @property
        def part_to_part_shear_coupling_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4525.PartToPartShearCouplingHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4525,
            )

            return self._parent._cast(
                _4525.PartToPartShearCouplingHalfCompoundParametricStudyTool
            )

        @property
        def planet_carrier_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4528.PlanetCarrierCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4528,
            )

            return self._parent._cast(_4528.PlanetCarrierCompoundParametricStudyTool)

        @property
        def point_load_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4529.PointLoadCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4529,
            )

            return self._parent._cast(_4529.PointLoadCompoundParametricStudyTool)

        @property
        def power_load_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4530.PowerLoadCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4530,
            )

            return self._parent._cast(_4530.PowerLoadCompoundParametricStudyTool)

        @property
        def pulley_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4531.PulleyCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4531,
            )

            return self._parent._cast(_4531.PulleyCompoundParametricStudyTool)

        @property
        def ring_pins_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4532.RingPinsCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4532,
            )

            return self._parent._cast(_4532.RingPinsCompoundParametricStudyTool)

        @property
        def rolling_ring_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4535.RollingRingCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4535,
            )

            return self._parent._cast(_4535.RollingRingCompoundParametricStudyTool)

        @property
        def shaft_hub_connection_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4539.ShaftHubConnectionCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4539,
            )

            return self._parent._cast(
                _4539.ShaftHubConnectionCompoundParametricStudyTool
            )

        @property
        def spiral_bevel_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4542.SpiralBevelGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4542,
            )

            return self._parent._cast(_4542.SpiralBevelGearCompoundParametricStudyTool)

        @property
        def spring_damper_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4547.SpringDamperHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4547,
            )

            return self._parent._cast(_4547.SpringDamperHalfCompoundParametricStudyTool)

        @property
        def straight_bevel_diff_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4548.StraightBevelDiffGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4548,
            )

            return self._parent._cast(
                _4548.StraightBevelDiffGearCompoundParametricStudyTool
            )

        @property
        def straight_bevel_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4551.StraightBevelGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4551,
            )

            return self._parent._cast(
                _4551.StraightBevelGearCompoundParametricStudyTool
            )

        @property
        def straight_bevel_planet_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4554.StraightBevelPlanetGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4554,
            )

            return self._parent._cast(
                _4554.StraightBevelPlanetGearCompoundParametricStudyTool
            )

        @property
        def straight_bevel_sun_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4555.StraightBevelSunGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4555,
            )

            return self._parent._cast(
                _4555.StraightBevelSunGearCompoundParametricStudyTool
            )

        @property
        def synchroniser_half_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4557.SynchroniserHalfCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4557,
            )

            return self._parent._cast(_4557.SynchroniserHalfCompoundParametricStudyTool)

        @property
        def synchroniser_part_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4558.SynchroniserPartCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4558,
            )

            return self._parent._cast(_4558.SynchroniserPartCompoundParametricStudyTool)

        @property
        def synchroniser_sleeve_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4559.SynchroniserSleeveCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4559,
            )

            return self._parent._cast(
                _4559.SynchroniserSleeveCompoundParametricStudyTool
            )

        @property
        def torque_converter_pump_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4562.TorqueConverterPumpCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4562,
            )

            return self._parent._cast(
                _4562.TorqueConverterPumpCompoundParametricStudyTool
            )

        @property
        def torque_converter_turbine_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4563.TorqueConverterTurbineCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4563,
            )

            return self._parent._cast(
                _4563.TorqueConverterTurbineCompoundParametricStudyTool
            )

        @property
        def unbalanced_mass_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4564.UnbalancedMassCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4564,
            )

            return self._parent._cast(_4564.UnbalancedMassCompoundParametricStudyTool)

        @property
        def virtual_component_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4565.VirtualComponentCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4565,
            )

            return self._parent._cast(_4565.VirtualComponentCompoundParametricStudyTool)

        @property
        def worm_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4566.WormGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4566,
            )

            return self._parent._cast(_4566.WormGearCompoundParametricStudyTool)

        @property
        def zerol_bevel_gear_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "_4569.ZerolBevelGearCompoundParametricStudyTool":
            from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import (
                _4569,
            )

            return self._parent._cast(_4569.ZerolBevelGearCompoundParametricStudyTool)

        @property
        def mountable_component_compound_parametric_study_tool(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
        ) -> "MountableComponentCompoundParametricStudyTool":
            return self._parent

        def __getattr__(
            self: "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(
        self: Self,
        instance_to_wrap: "MountableComponentCompoundParametricStudyTool.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_4381.MountableComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_4381.MountableComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "MountableComponentCompoundParametricStudyTool._Cast_MountableComponentCompoundParametricStudyTool":
        return self._Cast_MountableComponentCompoundParametricStudyTool(self)
