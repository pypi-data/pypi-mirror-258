"""GearCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2929
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "GearCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.gears.rating import _358
    from mastapy.system_model.analyses_and_results.system_deflections import _2761
    from mastapy.system_model.analyses_and_results.system_deflections.compound import (
        _2855,
        _2862,
        _2865,
        _2866,
        _2867,
        _2880,
        _2883,
        _2898,
        _2901,
        _2905,
        _2914,
        _2918,
        _2921,
        _2924,
        _2952,
        _2958,
        _2961,
        _2964,
        _2965,
        _2976,
        _2979,
        _2876,
        _2931,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("GearCompoundSystemDeflection",)


Self = TypeVar("Self", bound="GearCompoundSystemDeflection")


class GearCompoundSystemDeflection(_2929.MountableComponentCompoundSystemDeflection):
    """GearCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _GEAR_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_GearCompoundSystemDeflection")

    class _Cast_GearCompoundSystemDeflection:
        """Special nested class for casting GearCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
            parent: "GearCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def mountable_component_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2929.MountableComponentCompoundSystemDeflection":
            return self._parent._cast(_2929.MountableComponentCompoundSystemDeflection)

        @property
        def component_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2876.ComponentCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2876,
            )

            return self._parent._cast(_2876.ComponentCompoundSystemDeflection)

        @property
        def part_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2931.PartCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2931,
            )

            return self._parent._cast(_2931.PartCompoundSystemDeflection)

        @property
        def part_compound_analysis(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2855.AGMAGleasonConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2855,
            )

            return self._parent._cast(
                _2855.AGMAGleasonConicalGearCompoundSystemDeflection
            )

        @property
        def bevel_differential_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2862.BevelDifferentialGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2862,
            )

            return self._parent._cast(
                _2862.BevelDifferentialGearCompoundSystemDeflection
            )

        @property
        def bevel_differential_planet_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2865.BevelDifferentialPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2865,
            )

            return self._parent._cast(
                _2865.BevelDifferentialPlanetGearCompoundSystemDeflection
            )

        @property
        def bevel_differential_sun_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2866.BevelDifferentialSunGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2866,
            )

            return self._parent._cast(
                _2866.BevelDifferentialSunGearCompoundSystemDeflection
            )

        @property
        def bevel_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2867.BevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2867,
            )

            return self._parent._cast(_2867.BevelGearCompoundSystemDeflection)

        @property
        def concept_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2880.ConceptGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2880,
            )

            return self._parent._cast(_2880.ConceptGearCompoundSystemDeflection)

        @property
        def conical_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2883.ConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2883,
            )

            return self._parent._cast(_2883.ConicalGearCompoundSystemDeflection)

        @property
        def cylindrical_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2898.CylindricalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2898,
            )

            return self._parent._cast(_2898.CylindricalGearCompoundSystemDeflection)

        @property
        def cylindrical_planet_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2901.CylindricalPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2901,
            )

            return self._parent._cast(
                _2901.CylindricalPlanetGearCompoundSystemDeflection
            )

        @property
        def face_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2905.FaceGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2905,
            )

            return self._parent._cast(_2905.FaceGearCompoundSystemDeflection)

        @property
        def hypoid_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2914.HypoidGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2914,
            )

            return self._parent._cast(_2914.HypoidGearCompoundSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2918.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2918,
            )

            return self._parent._cast(
                _2918.KlingelnbergCycloPalloidConicalGearCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2921.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2921,
            )

            return self._parent._cast(
                _2921.KlingelnbergCycloPalloidHypoidGearCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2924.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2924,
            )

            return self._parent._cast(
                _2924.KlingelnbergCycloPalloidSpiralBevelGearCompoundSystemDeflection
            )

        @property
        def spiral_bevel_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2952.SpiralBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2952,
            )

            return self._parent._cast(_2952.SpiralBevelGearCompoundSystemDeflection)

        @property
        def straight_bevel_diff_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2958.StraightBevelDiffGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2958,
            )

            return self._parent._cast(
                _2958.StraightBevelDiffGearCompoundSystemDeflection
            )

        @property
        def straight_bevel_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2961.StraightBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2961,
            )

            return self._parent._cast(_2961.StraightBevelGearCompoundSystemDeflection)

        @property
        def straight_bevel_planet_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2964.StraightBevelPlanetGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2964,
            )

            return self._parent._cast(
                _2964.StraightBevelPlanetGearCompoundSystemDeflection
            )

        @property
        def straight_bevel_sun_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2965.StraightBevelSunGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2965,
            )

            return self._parent._cast(
                _2965.StraightBevelSunGearCompoundSystemDeflection
            )

        @property
        def worm_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2976.WormGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2976,
            )

            return self._parent._cast(_2976.WormGearCompoundSystemDeflection)

        @property
        def zerol_bevel_gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "_2979.ZerolBevelGearCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2979,
            )

            return self._parent._cast(_2979.ZerolBevelGearCompoundSystemDeflection)

        @property
        def gear_compound_system_deflection(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
        ) -> "GearCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "GearCompoundSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def duty_cycle_rating(self: Self) -> "_358.GearDutyCycleRating":
        """mastapy.gears.rating.GearDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DutyCycleRating

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases(self: Self) -> "List[_2761.GearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection]

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
    ) -> "List[_2761.GearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection]

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
    ) -> "GearCompoundSystemDeflection._Cast_GearCompoundSystemDeflection":
        return self._Cast_GearCompoundSystemDeflection(self)
