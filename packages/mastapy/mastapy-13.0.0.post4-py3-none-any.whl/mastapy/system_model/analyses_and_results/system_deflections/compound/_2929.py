"""MountableComponentCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2876
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MOUNTABLE_COMPONENT_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "MountableComponentCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.system_deflections import _2782
    from mastapy.system_model.analyses_and_results.system_deflections.compound import (
        _2855,
        _2859,
        _2862,
        _2865,
        _2866,
        _2867,
        _2874,
        _2879,
        _2880,
        _2883,
        _2887,
        _2890,
        _2893,
        _2898,
        _2901,
        _2905,
        _2910,
        _2914,
        _2918,
        _2921,
        _2924,
        _2927,
        _2928,
        _2930,
        _2934,
        _2937,
        _2938,
        _2939,
        _2940,
        _2941,
        _2944,
        _2949,
        _2952,
        _2957,
        _2958,
        _2961,
        _2964,
        _2965,
        _2967,
        _2968,
        _2969,
        _2972,
        _2973,
        _2974,
        _2975,
        _2976,
        _2979,
        _2931,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundSystemDeflection",)


Self = TypeVar("Self", bound="MountableComponentCompoundSystemDeflection")


class MountableComponentCompoundSystemDeflection(
    _2876.ComponentCompoundSystemDeflection
):
    """MountableComponentCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _MOUNTABLE_COMPONENT_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_MountableComponentCompoundSystemDeflection"
    )

    class _Cast_MountableComponentCompoundSystemDeflection:
        """Special nested class for casting MountableComponentCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
            parent: "MountableComponentCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def component_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2876.ComponentCompoundSystemDeflection":
            return self._parent._cast(_2876.ComponentCompoundSystemDeflection)

        @property
        def part_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2931.PartCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2931,
            )

            return self._parent._cast(_2931.PartCompoundSystemDeflection)

        @property
        def part_compound_analysis(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2855.AGMAGleasonConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2855,
            )

            return self._parent._cast(
                _2855.AGMAGleasonConicalGearCompoundSystemDeflection
            )

        @property
        def bearing_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2859.BearingCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2859,
            )

            return self._parent._cast(_2859.BearingCompoundSystemDeflection)

        @property
        def bevel_differential_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2862.BevelDifferentialGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2862,
            )

            return self._parent._cast(
                _2862.BevelDifferentialGearCompoundSystemDeflection
            )

        @property
        def bevel_differential_planet_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2865.BevelDifferentialPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2865,
            )

            return self._parent._cast(
                _2865.BevelDifferentialPlanetGearCompoundSystemDeflection
            )

        @property
        def bevel_differential_sun_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2866.BevelDifferentialSunGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2866,
            )

            return self._parent._cast(
                _2866.BevelDifferentialSunGearCompoundSystemDeflection
            )

        @property
        def bevel_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2867.BevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2867,
            )

            return self._parent._cast(_2867.BevelGearCompoundSystemDeflection)

        @property
        def clutch_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2874.ClutchHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2874,
            )

            return self._parent._cast(_2874.ClutchHalfCompoundSystemDeflection)

        @property
        def concept_coupling_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2879.ConceptCouplingHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2879,
            )

            return self._parent._cast(_2879.ConceptCouplingHalfCompoundSystemDeflection)

        @property
        def concept_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2880.ConceptGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2880,
            )

            return self._parent._cast(_2880.ConceptGearCompoundSystemDeflection)

        @property
        def conical_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2883.ConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2883,
            )

            return self._parent._cast(_2883.ConicalGearCompoundSystemDeflection)

        @property
        def connector_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2887.ConnectorCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2887,
            )

            return self._parent._cast(_2887.ConnectorCompoundSystemDeflection)

        @property
        def coupling_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2890.CouplingHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2890,
            )

            return self._parent._cast(_2890.CouplingHalfCompoundSystemDeflection)

        @property
        def cvt_pulley_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2893.CVTPulleyCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2893,
            )

            return self._parent._cast(_2893.CVTPulleyCompoundSystemDeflection)

        @property
        def cylindrical_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2898.CylindricalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2898,
            )

            return self._parent._cast(_2898.CylindricalGearCompoundSystemDeflection)

        @property
        def cylindrical_planet_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2901.CylindricalPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2901,
            )

            return self._parent._cast(
                _2901.CylindricalPlanetGearCompoundSystemDeflection
            )

        @property
        def face_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2905.FaceGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2905,
            )

            return self._parent._cast(_2905.FaceGearCompoundSystemDeflection)

        @property
        def gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2910.GearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2910,
            )

            return self._parent._cast(_2910.GearCompoundSystemDeflection)

        @property
        def hypoid_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2914.HypoidGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2914,
            )

            return self._parent._cast(_2914.HypoidGearCompoundSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2918.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2918,
            )

            return self._parent._cast(
                _2918.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2921.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2921,
            )

            return self._parent._cast(
                _2921.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2924.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2924,
            )

            return self._parent._cast(
                _2924.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection
            )

        @property
        def mass_disc_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2927.MassDiscCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2927,
            )

            return self._parent._cast(_2927.MassDiscCompoundSystemDeflection)

        @property
        def measurement_component_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2928.MeasurementComponentCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2928,
            )

            return self._parent._cast(
                _2928.MeasurementComponentCompoundSystemDeflection
            )

        @property
        def oil_seal_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2930.OilSealCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2930,
            )

            return self._parent._cast(_2930.OilSealCompoundSystemDeflection)

        @property
        def part_to_part_shear_coupling_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2934.PartToPartShearCouplingHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2934,
            )

            return self._parent._cast(
                _2934.PartToPartShearCouplingHalfCompoundSystemDeflection
            )

        @property
        def planet_carrier_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2937.PlanetCarrierCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2937,
            )

            return self._parent._cast(_2937.PlanetCarrierCompoundSystemDeflection)

        @property
        def point_load_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2938.PointLoadCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2938,
            )

            return self._parent._cast(_2938.PointLoadCompoundSystemDeflection)

        @property
        def power_load_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2939.PowerLoadCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2939,
            )

            return self._parent._cast(_2939.PowerLoadCompoundSystemDeflection)

        @property
        def pulley_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2940.PulleyCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2940,
            )

            return self._parent._cast(_2940.PulleyCompoundSystemDeflection)

        @property
        def ring_pins_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2941.RingPinsCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2941,
            )

            return self._parent._cast(_2941.RingPinsCompoundSystemDeflection)

        @property
        def rolling_ring_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2944.RollingRingCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2944,
            )

            return self._parent._cast(_2944.RollingRingCompoundSystemDeflection)

        @property
        def shaft_hub_connection_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2949.ShaftHubConnectionCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2949,
            )

            return self._parent._cast(_2949.ShaftHubConnectionCompoundSystemDeflection)

        @property
        def spiral_bevel_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2952.SpiralBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2952,
            )

            return self._parent._cast(_2952.SpiralBevelGearCompoundSystemDeflection)

        @property
        def spring_damper_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2957.SpringDamperHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2957,
            )

            return self._parent._cast(_2957.SpringDamperHalfCompoundSystemDeflection)

        @property
        def straight_bevel_diff_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2958.StraightBevelDiffGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2958,
            )

            return self._parent._cast(
                _2958.StraightBevelDiffGearCompoundSystemDeflection
            )

        @property
        def straight_bevel_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2961.StraightBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2961,
            )

            return self._parent._cast(_2961.StraightBevelGearCompoundSystemDeflection)

        @property
        def straight_bevel_planet_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2964.StraightBevelPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2964,
            )

            return self._parent._cast(
                _2964.StraightBevelPlanetGearCompoundSystemDeflection
            )

        @property
        def straight_bevel_sun_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2965.StraightBevelSunGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2965,
            )

            return self._parent._cast(
                _2965.StraightBevelSunGearCompoundSystemDeflection
            )

        @property
        def synchroniser_half_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2967.SynchroniserHalfCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2967,
            )

            return self._parent._cast(_2967.SynchroniserHalfCompoundSystemDeflection)

        @property
        def synchroniser_part_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2968.SynchroniserPartCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2968,
            )

            return self._parent._cast(_2968.SynchroniserPartCompoundSystemDeflection)

        @property
        def synchroniser_sleeve_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2969.SynchroniserSleeveCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2969,
            )

            return self._parent._cast(_2969.SynchroniserSleeveCompoundSystemDeflection)

        @property
        def torque_converter_pump_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2972.TorqueConverterPumpCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2972,
            )

            return self._parent._cast(_2972.TorqueConverterPumpCompoundSystemDeflection)

        @property
        def torque_converter_turbine_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2973.TorqueConverterTurbineCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2973,
            )

            return self._parent._cast(
                _2973.TorqueConverterTurbineCompoundSystemDeflection
            )

        @property
        def unbalanced_mass_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2974.UnbalancedMassCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2974,
            )

            return self._parent._cast(_2974.UnbalancedMassCompoundSystemDeflection)

        @property
        def virtual_component_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2975.VirtualComponentCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2975,
            )

            return self._parent._cast(_2975.VirtualComponentCompoundSystemDeflection)

        @property
        def worm_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2976.WormGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2976,
            )

            return self._parent._cast(_2976.WormGearCompoundSystemDeflection)

        @property
        def zerol_bevel_gear_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "_2979.ZerolBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2979,
            )

            return self._parent._cast(_2979.ZerolBevelGearCompoundSystemDeflection)

        @property
        def mountable_component_compound_system_deflection(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
        ) -> "MountableComponentCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection",
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
        self: Self, instance_to_wrap: "MountableComponentCompoundSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_2782.MountableComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection]

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
    ) -> "List[_2782.MountableComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection]

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
    ) -> "MountableComponentCompoundSystemDeflection._Cast_MountableComponentCompoundSystemDeflection":
        return self._Cast_MountableComponentCompoundSystemDeflection(self)
