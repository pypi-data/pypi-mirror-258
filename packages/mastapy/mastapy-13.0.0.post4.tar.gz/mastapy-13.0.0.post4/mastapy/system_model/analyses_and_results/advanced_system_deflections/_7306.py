"""ConicalGearSetAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _7334
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "ConicalGearSetAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2524
    from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
        _7278,
        _7285,
        _7290,
        _7338,
        _7342,
        _7345,
        _7348,
        _7376,
        _7382,
        _7385,
        _7404,
        _7373,
        _7269,
        _7354,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetAdvancedSystemDeflection",)


Self = TypeVar("Self", bound="ConicalGearSetAdvancedSystemDeflection")


class ConicalGearSetAdvancedSystemDeflection(_7334.GearSetAdvancedSystemDeflection):
    """ConicalGearSetAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_ConicalGearSetAdvancedSystemDeflection"
    )

    class _Cast_ConicalGearSetAdvancedSystemDeflection:
        """Special nested class for casting ConicalGearSetAdvancedSystemDeflection to subclasses."""

        def __init__(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
            parent: "ConicalGearSetAdvancedSystemDeflection",
        ):
            self._parent = parent

        @property
        def gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7334.GearSetAdvancedSystemDeflection":
            return self._parent._cast(_7334.GearSetAdvancedSystemDeflection)

        @property
        def specialised_assembly_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7373.SpecialisedAssemblyAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7373,
            )

            return self._parent._cast(_7373.SpecialisedAssemblyAdvancedSystemDeflection)

        @property
        def abstract_assembly_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7269.AbstractAssemblyAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7269,
            )

            return self._parent._cast(_7269.AbstractAssemblyAdvancedSystemDeflection)

        @property
        def part_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7354.PartAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7354,
            )

            return self._parent._cast(_7354.PartAdvancedSystemDeflection)

        @property
        def part_static_load_analysis_case(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7278.AGMAGleasonConicalGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7278,
            )

            return self._parent._cast(
                _7278.AGMAGleasonConicalGearSetAdvancedSystemDeflection
            )

        @property
        def bevel_differential_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7285.BevelDifferentialGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7285,
            )

            return self._parent._cast(
                _7285.BevelDifferentialGearSetAdvancedSystemDeflection
            )

        @property
        def bevel_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7290.BevelGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7290,
            )

            return self._parent._cast(_7290.BevelGearSetAdvancedSystemDeflection)

        @property
        def hypoid_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7338.HypoidGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7338,
            )

            return self._parent._cast(_7338.HypoidGearSetAdvancedSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7342.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7342,
            )

            return self._parent._cast(
                _7342.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7345.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7345,
            )

            return self._parent._cast(
                _7345.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7348.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7348,
            )

            return self._parent._cast(
                _7348.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
            )

        @property
        def spiral_bevel_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7376.SpiralBevelGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7376,
            )

            return self._parent._cast(_7376.SpiralBevelGearSetAdvancedSystemDeflection)

        @property
        def straight_bevel_diff_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7382.StraightBevelDiffGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7382,
            )

            return self._parent._cast(
                _7382.StraightBevelDiffGearSetAdvancedSystemDeflection
            )

        @property
        def straight_bevel_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7385.StraightBevelGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7385,
            )

            return self._parent._cast(
                _7385.StraightBevelGearSetAdvancedSystemDeflection
            )

        @property
        def zerol_bevel_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "_7404.ZerolBevelGearSetAdvancedSystemDeflection":
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7404,
            )

            return self._parent._cast(_7404.ZerolBevelGearSetAdvancedSystemDeflection)

        @property
        def conical_gear_set_advanced_system_deflection(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
        ) -> "ConicalGearSetAdvancedSystemDeflection":
            return self._parent

        def __getattr__(
            self: "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection",
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
        self: Self, instance_to_wrap: "ConicalGearSetAdvancedSystemDeflection.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2524.ConicalGearSet":
        """mastapy.system_model.part_model.gears.ConicalGearSet

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
    ) -> "ConicalGearSetAdvancedSystemDeflection._Cast_ConicalGearSetAdvancedSystemDeflection":
        return self._Cast_ConicalGearSetAdvancedSystemDeflection(self)
