"""MountableComponentModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5141
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "MountableComponentModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2464
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5121,
        _5124,
        _5128,
        _5130,
        _5131,
        _5133,
        _5138,
        _5143,
        _5146,
        _5149,
        _5152,
        _5154,
        _5158,
        _5164,
        _5166,
        _5170,
        _5175,
        _5179,
        _5183,
        _5186,
        _5189,
        _5191,
        _5192,
        _5195,
        _5198,
        _5202,
        _5203,
        _5204,
        _5205,
        _5206,
        _5210,
        _5212,
        _5217,
        _5220,
        _5223,
        _5226,
        _5228,
        _5229,
        _5230,
        _5232,
        _5233,
        _5236,
        _5237,
        _5238,
        _5239,
        _5241,
        _5244,
        _5196,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="MountableComponentModalAnalysisAtASpeed")


class MountableComponentModalAnalysisAtASpeed(_5141.ComponentModalAnalysisAtASpeed):
    """MountableComponentModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MountableComponentModalAnalysisAtASpeed"
    )

    class _Cast_MountableComponentModalAnalysisAtASpeed:
        """Special nested class for casting MountableComponentModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
            parent: "MountableComponentModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def component_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5141.ComponentModalAnalysisAtASpeed":
            return self._parent._cast(_5141.ComponentModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5196.PartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5196,
            )

            return self._parent._cast(_5196.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5121.AGMAGleasonConicalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5121,
            )

            return self._parent._cast(_5121.AGMAGleasonConicalGearModalAnalysisAtASpeed)

        @property
        def bearing_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5124.BearingModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5124,
            )

            return self._parent._cast(_5124.BearingModalAnalysisAtASpeed)

        @property
        def bevel_differential_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5128.BevelDifferentialGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5128,
            )

            return self._parent._cast(_5128.BevelDifferentialGearModalAnalysisAtASpeed)

        @property
        def bevel_differential_planet_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5130.BevelDifferentialPlanetGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5130,
            )

            return self._parent._cast(
                _5130.BevelDifferentialPlanetGearModalAnalysisAtASpeed
            )

        @property
        def bevel_differential_sun_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5131.BevelDifferentialSunGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5131,
            )

            return self._parent._cast(
                _5131.BevelDifferentialSunGearModalAnalysisAtASpeed
            )

        @property
        def bevel_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5133.BevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5133,
            )

            return self._parent._cast(_5133.BevelGearModalAnalysisAtASpeed)

        @property
        def clutch_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5138.ClutchHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5138,
            )

            return self._parent._cast(_5138.ClutchHalfModalAnalysisAtASpeed)

        @property
        def concept_coupling_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5143.ConceptCouplingHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5143,
            )

            return self._parent._cast(_5143.ConceptCouplingHalfModalAnalysisAtASpeed)

        @property
        def concept_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5146.ConceptGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5146,
            )

            return self._parent._cast(_5146.ConceptGearModalAnalysisAtASpeed)

        @property
        def conical_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5149.ConicalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5149,
            )

            return self._parent._cast(_5149.ConicalGearModalAnalysisAtASpeed)

        @property
        def connector_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5152.ConnectorModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5152,
            )

            return self._parent._cast(_5152.ConnectorModalAnalysisAtASpeed)

        @property
        def coupling_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5154.CouplingHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5154,
            )

            return self._parent._cast(_5154.CouplingHalfModalAnalysisAtASpeed)

        @property
        def cvt_pulley_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5158.CVTPulleyModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5158,
            )

            return self._parent._cast(_5158.CVTPulleyModalAnalysisAtASpeed)

        @property
        def cylindrical_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5164.CylindricalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5164,
            )

            return self._parent._cast(_5164.CylindricalGearModalAnalysisAtASpeed)

        @property
        def cylindrical_planet_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5166.CylindricalPlanetGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5166,
            )

            return self._parent._cast(_5166.CylindricalPlanetGearModalAnalysisAtASpeed)

        @property
        def face_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5170.FaceGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5170,
            )

            return self._parent._cast(_5170.FaceGearModalAnalysisAtASpeed)

        @property
        def gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5175.GearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5175,
            )

            return self._parent._cast(_5175.GearModalAnalysisAtASpeed)

        @property
        def hypoid_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5179.HypoidGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5179,
            )

            return self._parent._cast(_5179.HypoidGearModalAnalysisAtASpeed)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5183.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5183,
            )

            return self._parent._cast(
                _5183.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5186.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5186,
            )

            return self._parent._cast(
                _5186.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5189.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5189,
            )

            return self._parent._cast(
                _5189.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
            )

        @property
        def mass_disc_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5191.MassDiscModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5191,
            )

            return self._parent._cast(_5191.MassDiscModalAnalysisAtASpeed)

        @property
        def measurement_component_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5192.MeasurementComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5192,
            )

            return self._parent._cast(_5192.MeasurementComponentModalAnalysisAtASpeed)

        @property
        def oil_seal_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5195.OilSealModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5195,
            )

            return self._parent._cast(_5195.OilSealModalAnalysisAtASpeed)

        @property
        def part_to_part_shear_coupling_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5198.PartToPartShearCouplingHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5198,
            )

            return self._parent._cast(
                _5198.PartToPartShearCouplingHalfModalAnalysisAtASpeed
            )

        @property
        def planet_carrier_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5202.PlanetCarrierModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5202,
            )

            return self._parent._cast(_5202.PlanetCarrierModalAnalysisAtASpeed)

        @property
        def point_load_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5203.PointLoadModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5203,
            )

            return self._parent._cast(_5203.PointLoadModalAnalysisAtASpeed)

        @property
        def power_load_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5204.PowerLoadModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5204,
            )

            return self._parent._cast(_5204.PowerLoadModalAnalysisAtASpeed)

        @property
        def pulley_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5205.PulleyModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5205,
            )

            return self._parent._cast(_5205.PulleyModalAnalysisAtASpeed)

        @property
        def ring_pins_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5206.RingPinsModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5206,
            )

            return self._parent._cast(_5206.RingPinsModalAnalysisAtASpeed)

        @property
        def rolling_ring_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5210.RollingRingModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5210,
            )

            return self._parent._cast(_5210.RollingRingModalAnalysisAtASpeed)

        @property
        def shaft_hub_connection_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5212.ShaftHubConnectionModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5212,
            )

            return self._parent._cast(_5212.ShaftHubConnectionModalAnalysisAtASpeed)

        @property
        def spiral_bevel_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5217.SpiralBevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5217,
            )

            return self._parent._cast(_5217.SpiralBevelGearModalAnalysisAtASpeed)

        @property
        def spring_damper_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5220.SpringDamperHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5220,
            )

            return self._parent._cast(_5220.SpringDamperHalfModalAnalysisAtASpeed)

        @property
        def straight_bevel_diff_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5223.StraightBevelDiffGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5223,
            )

            return self._parent._cast(_5223.StraightBevelDiffGearModalAnalysisAtASpeed)

        @property
        def straight_bevel_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5226.StraightBevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5226,
            )

            return self._parent._cast(_5226.StraightBevelGearModalAnalysisAtASpeed)

        @property
        def straight_bevel_planet_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5228.StraightBevelPlanetGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5228,
            )

            return self._parent._cast(
                _5228.StraightBevelPlanetGearModalAnalysisAtASpeed
            )

        @property
        def straight_bevel_sun_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5229.StraightBevelSunGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5229,
            )

            return self._parent._cast(_5229.StraightBevelSunGearModalAnalysisAtASpeed)

        @property
        def synchroniser_half_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5230.SynchroniserHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5230,
            )

            return self._parent._cast(_5230.SynchroniserHalfModalAnalysisAtASpeed)

        @property
        def synchroniser_part_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5232.SynchroniserPartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5232,
            )

            return self._parent._cast(_5232.SynchroniserPartModalAnalysisAtASpeed)

        @property
        def synchroniser_sleeve_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5233.SynchroniserSleeveModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5233,
            )

            return self._parent._cast(_5233.SynchroniserSleeveModalAnalysisAtASpeed)

        @property
        def torque_converter_pump_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5236.TorqueConverterPumpModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5236,
            )

            return self._parent._cast(_5236.TorqueConverterPumpModalAnalysisAtASpeed)

        @property
        def torque_converter_turbine_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5237.TorqueConverterTurbineModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5237,
            )

            return self._parent._cast(_5237.TorqueConverterTurbineModalAnalysisAtASpeed)

        @property
        def unbalanced_mass_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5238.UnbalancedMassModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5238,
            )

            return self._parent._cast(_5238.UnbalancedMassModalAnalysisAtASpeed)

        @property
        def virtual_component_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5239.VirtualComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5239,
            )

            return self._parent._cast(_5239.VirtualComponentModalAnalysisAtASpeed)

        @property
        def worm_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5241.WormGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5241,
            )

            return self._parent._cast(_5241.WormGearModalAnalysisAtASpeed)

        @property
        def zerol_bevel_gear_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "_5244.ZerolBevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5244,
            )

            return self._parent._cast(_5244.ZerolBevelGearModalAnalysisAtASpeed)

        @property
        def mountable_component_modal_analysis_at_a_speed(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
        ) -> "MountableComponentModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed",
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
        self: Self, instance_to_wrap: "MountableComponentModalAnalysisAtASpeed.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2464.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

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
    ) -> "MountableComponentModalAnalysisAtASpeed._Cast_MountableComponentModalAnalysisAtASpeed":
        return self._Cast_MountableComponentModalAnalysisAtASpeed(self)
