"""ConicalGearSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2761
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "ConicalGearSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2523
    from mastapy.gears.ltca.conical import _867
    from mastapy.system_model.analyses_and_results.power_flows import _4065
    from mastapy.system_model.analyses_and_results.system_deflections import (
        _2691,
        _2703,
        _2704,
        _2705,
        _2708,
        _2765,
        _2770,
        _2773,
        _2776,
        _2809,
        _2815,
        _2818,
        _2819,
        _2820,
        _2841,
        _2782,
        _2715,
        _2785,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import (
        _7546,
        _7547,
        _7544,
    )
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSystemDeflection",)


Self = TypeVar("Self", bound="ConicalGearSystemDeflection")


class ConicalGearSystemDeflection(_2761.GearSystemDeflection):
    """ConicalGearSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConicalGearSystemDeflection")

    class _Cast_ConicalGearSystemDeflection:
        """Special nested class for casting ConicalGearSystemDeflection to subclasses."""

        def __init__(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
            parent: "ConicalGearSystemDeflection",
        ):
            self._parent = parent

        @property
        def gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2761.GearSystemDeflection":
            return self._parent._cast(_2761.GearSystemDeflection)

        @property
        def mountable_component_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2782.MountableComponentSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2782,
            )

            return self._parent._cast(_2782.MountableComponentSystemDeflection)

        @property
        def component_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2715.ComponentSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2715,
            )

            return self._parent._cast(_2715.ComponentSystemDeflection)

        @property
        def part_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2785.PartSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2785,
            )

            return self._parent._cast(_2785.PartSystemDeflection)

        @property
        def part_fe_analysis(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_7546.PartFEAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartFEAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2691.AGMAGleasonConicalGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2691,
            )

            return self._parent._cast(_2691.AGMAGleasonConicalGearSystemDeflection)

        @property
        def bevel_differential_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2703.BevelDifferentialGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2703,
            )

            return self._parent._cast(_2703.BevelDifferentialGearSystemDeflection)

        @property
        def bevel_differential_planet_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2704.BevelDifferentialPlanetGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2704,
            )

            return self._parent._cast(_2704.BevelDifferentialPlanetGearSystemDeflection)

        @property
        def bevel_differential_sun_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2705.BevelDifferentialSunGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2705,
            )

            return self._parent._cast(_2705.BevelDifferentialSunGearSystemDeflection)

        @property
        def bevel_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2708.BevelGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2708,
            )

            return self._parent._cast(_2708.BevelGearSystemDeflection)

        @property
        def hypoid_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2765.HypoidGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2765,
            )

            return self._parent._cast(_2765.HypoidGearSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2770.KlingelnbergCycloPalloidConicalGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2770,
            )

            return self._parent._cast(
                _2770.KlingelnbergCycloPalloidConicalGearSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2773.KlingelnbergCycloPalloidHypoidGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2773,
            )

            return self._parent._cast(
                _2773.KlingelnbergCycloPalloidHypoidGearSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2776.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2776,
            )

            return self._parent._cast(
                _2776.KlingelnbergCycloPalloidSpiralBevelGearSystemDeflection
            )

        @property
        def spiral_bevel_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2809.SpiralBevelGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2809,
            )

            return self._parent._cast(_2809.SpiralBevelGearSystemDeflection)

        @property
        def straight_bevel_diff_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2815.StraightBevelDiffGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2815,
            )

            return self._parent._cast(_2815.StraightBevelDiffGearSystemDeflection)

        @property
        def straight_bevel_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2818.StraightBevelGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2818,
            )

            return self._parent._cast(_2818.StraightBevelGearSystemDeflection)

        @property
        def straight_bevel_planet_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2819.StraightBevelPlanetGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2819,
            )

            return self._parent._cast(_2819.StraightBevelPlanetGearSystemDeflection)

        @property
        def straight_bevel_sun_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2820.StraightBevelSunGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2820,
            )

            return self._parent._cast(_2820.StraightBevelSunGearSystemDeflection)

        @property
        def zerol_bevel_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "_2841.ZerolBevelGearSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2841,
            )

            return self._parent._cast(_2841.ZerolBevelGearSystemDeflection)

        @property
        def conical_gear_system_deflection(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
        ) -> "ConicalGearSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ConicalGearSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2523.ConicalGear":
        """mastapy.system_model.part_model.gears.ConicalGear

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_ltca_results(
        self: Self,
    ) -> "_867.ConicalGearLoadDistributionAnalysis":
        """mastapy.gears.ltca.conical.ConicalGearLoadDistributionAnalysis

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConicalGearLTCAResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: Self) -> "List[ConicalGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_flow_results(self: Self) -> "_4065.ConicalGearPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow

        Note:
            This property is readonly.
        """
        temp = self.wrapped.PowerFlowResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "ConicalGearSystemDeflection._Cast_ConicalGearSystemDeflection":
        return self._Cast_ConicalGearSystemDeflection(self)
