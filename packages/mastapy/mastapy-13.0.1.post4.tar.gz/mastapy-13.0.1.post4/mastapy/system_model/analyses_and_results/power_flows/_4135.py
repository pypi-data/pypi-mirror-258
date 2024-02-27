"""SpecialisedAssemblyPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4032
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "SpecialisedAssemblyPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2476
    from mastapy.system_model.analyses_and_results.power_flows import (
        _4038,
        _4042,
        _4045,
        _4050,
        _4051,
        _4055,
        _4060,
        _4063,
        _4066,
        _4071,
        _4073,
        _4075,
        _4082,
        _4088,
        _4092,
        _4095,
        _4099,
        _4103,
        _4106,
        _4109,
        _4117,
        _4119,
        _4128,
        _4138,
        _4141,
        _4144,
        _4147,
        _4152,
        _4156,
        _4163,
        _4166,
        _4114,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7548, _7545
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyPowerFlow",)


Self = TypeVar("Self", bound="SpecialisedAssemblyPowerFlow")


class SpecialisedAssemblyPowerFlow(_4032.AbstractAssemblyPowerFlow):
    """SpecialisedAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpecialisedAssemblyPowerFlow")

    class _Cast_SpecialisedAssemblyPowerFlow:
        """Special nested class for casting SpecialisedAssemblyPowerFlow to subclasses."""

        def __init__(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
            parent: "SpecialisedAssemblyPowerFlow",
        ):
            self._parent = parent

        @property
        def abstract_assembly_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4032.AbstractAssemblyPowerFlow":
            return self._parent._cast(_4032.AbstractAssemblyPowerFlow)

        @property
        def part_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4114.PartPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4114

            return self._parent._cast(_4114.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_7548.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7548

            return self._parent._cast(_7548.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_7545.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4038.AGMAGleasonConicalGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4038

            return self._parent._cast(_4038.AGMAGleasonConicalGearSetPowerFlow)

        @property
        def belt_drive_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4042.BeltDrivePowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4042

            return self._parent._cast(_4042.BeltDrivePowerFlow)

        @property
        def bevel_differential_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4045.BevelDifferentialGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4045

            return self._parent._cast(_4045.BevelDifferentialGearSetPowerFlow)

        @property
        def bevel_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4050.BevelGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4050

            return self._parent._cast(_4050.BevelGearSetPowerFlow)

        @property
        def bolted_joint_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4051.BoltedJointPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4051

            return self._parent._cast(_4051.BoltedJointPowerFlow)

        @property
        def clutch_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4055.ClutchPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4055

            return self._parent._cast(_4055.ClutchPowerFlow)

        @property
        def concept_coupling_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4060.ConceptCouplingPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4060

            return self._parent._cast(_4060.ConceptCouplingPowerFlow)

        @property
        def concept_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4063.ConceptGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4063

            return self._parent._cast(_4063.ConceptGearSetPowerFlow)

        @property
        def conical_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4066.ConicalGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4066

            return self._parent._cast(_4066.ConicalGearSetPowerFlow)

        @property
        def coupling_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4071.CouplingPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4071

            return self._parent._cast(_4071.CouplingPowerFlow)

        @property
        def cvt_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4073.CVTPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4073

            return self._parent._cast(_4073.CVTPowerFlow)

        @property
        def cycloidal_assembly_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4075.CycloidalAssemblyPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4075

            return self._parent._cast(_4075.CycloidalAssemblyPowerFlow)

        @property
        def cylindrical_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4082.CylindricalGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4082

            return self._parent._cast(_4082.CylindricalGearSetPowerFlow)

        @property
        def face_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4088.FaceGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4088

            return self._parent._cast(_4088.FaceGearSetPowerFlow)

        @property
        def flexible_pin_assembly_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4092.FlexiblePinAssemblyPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4092

            return self._parent._cast(_4092.FlexiblePinAssemblyPowerFlow)

        @property
        def gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4095.GearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4095

            return self._parent._cast(_4095.GearSetPowerFlow)

        @property
        def hypoid_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4099.HypoidGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4099

            return self._parent._cast(_4099.HypoidGearSetPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4103.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4103

            return self._parent._cast(
                _4103.KlingelnbergCycloPalloidConicalGearSetPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4106.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4106

            return self._parent._cast(
                _4106.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4109.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4109

            return self._parent._cast(
                _4109.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
            )

        @property
        def part_to_part_shear_coupling_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4117.PartToPartShearCouplingPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4117

            return self._parent._cast(_4117.PartToPartShearCouplingPowerFlow)

        @property
        def planetary_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4119.PlanetaryGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4119

            return self._parent._cast(_4119.PlanetaryGearSetPowerFlow)

        @property
        def rolling_ring_assembly_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4128.RollingRingAssemblyPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4128

            return self._parent._cast(_4128.RollingRingAssemblyPowerFlow)

        @property
        def spiral_bevel_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4138.SpiralBevelGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4138

            return self._parent._cast(_4138.SpiralBevelGearSetPowerFlow)

        @property
        def spring_damper_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4141.SpringDamperPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4141

            return self._parent._cast(_4141.SpringDamperPowerFlow)

        @property
        def straight_bevel_diff_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4144.StraightBevelDiffGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4144

            return self._parent._cast(_4144.StraightBevelDiffGearSetPowerFlow)

        @property
        def straight_bevel_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4147.StraightBevelGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4147

            return self._parent._cast(_4147.StraightBevelGearSetPowerFlow)

        @property
        def synchroniser_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4152.SynchroniserPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4152

            return self._parent._cast(_4152.SynchroniserPowerFlow)

        @property
        def torque_converter_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4156.TorqueConverterPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4156

            return self._parent._cast(_4156.TorqueConverterPowerFlow)

        @property
        def worm_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4163.WormGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4163

            return self._parent._cast(_4163.WormGearSetPowerFlow)

        @property
        def zerol_bevel_gear_set_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "_4166.ZerolBevelGearSetPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4166

            return self._parent._cast(_4166.ZerolBevelGearSetPowerFlow)

        @property
        def specialised_assembly_power_flow(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
        ) -> "SpecialisedAssemblyPowerFlow":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpecialisedAssemblyPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2476.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "SpecialisedAssemblyPowerFlow._Cast_SpecialisedAssemblyPowerFlow":
        return self._Cast_SpecialisedAssemblyPowerFlow(self)
