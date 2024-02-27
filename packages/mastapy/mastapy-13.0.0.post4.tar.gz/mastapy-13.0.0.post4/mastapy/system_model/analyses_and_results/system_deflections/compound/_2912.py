"""GearSetCompoundSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2951
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "GearSetCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.system_deflections import _2760
    from mastapy.system_model.analyses_and_results.system_deflections.compound import (
        _2857,
        _2864,
        _2869,
        _2882,
        _2885,
        _2900,
        _2907,
        _2916,
        _2920,
        _2923,
        _2926,
        _2936,
        _2954,
        _2960,
        _2963,
        _2978,
        _2981,
        _2851,
        _2931,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundSystemDeflection",)


Self = TypeVar("Self", bound="GearSetCompoundSystemDeflection")


class GearSetCompoundSystemDeflection(
    _2951.SpecialisedAssemblyCompoundSystemDeflection
):
    """GearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_COMPOUND_SYSTEM_DEFLECTION
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_GearSetCompoundSystemDeflection")

    class _Cast_GearSetCompoundSystemDeflection:
        """Special nested class for casting GearSetCompoundSystemDeflection to subclasses."""

        def __init__(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
            parent: "GearSetCompoundSystemDeflection",
        ):
            self._parent = parent

        @property
        def specialised_assembly_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2951.SpecialisedAssemblyCompoundSystemDeflection":
            return self._parent._cast(_2951.SpecialisedAssemblyCompoundSystemDeflection)

        @property
        def abstract_assembly_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2851.AbstractAssemblyCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2851,
            )

            return self._parent._cast(_2851.AbstractAssemblyCompoundSystemDeflection)

        @property
        def part_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2931.PartCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2931,
            )

            return self._parent._cast(_2931.PartCompoundSystemDeflection)

        @property
        def part_compound_analysis(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2857.AGMAGleasonConicalGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2857,
            )

            return self._parent._cast(
                _2857.AGMAGleasonConicalGearSetCompoundSystemDeflection
            )

        @property
        def bevel_differential_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2864.BevelDifferentialGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2864,
            )

            return self._parent._cast(
                _2864.BevelDifferentialGearSetCompoundSystemDeflection
            )

        @property
        def bevel_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2869.BevelGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2869,
            )

            return self._parent._cast(_2869.BevelGearSetCompoundSystemDeflection)

        @property
        def concept_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2882.ConceptGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2882,
            )

            return self._parent._cast(_2882.ConceptGearSetCompoundSystemDeflection)

        @property
        def conical_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2885.ConicalGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2885,
            )

            return self._parent._cast(_2885.ConicalGearSetCompoundSystemDeflection)

        @property
        def cylindrical_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2900.CylindricalGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2900,
            )

            return self._parent._cast(_2900.CylindricalGearSetCompoundSystemDeflection)

        @property
        def face_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2907.FaceGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2907,
            )

            return self._parent._cast(_2907.FaceGearSetCompoundSystemDeflection)

        @property
        def hypoid_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2916.HypoidGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2916,
            )

            return self._parent._cast(_2916.HypoidGearSetCompoundSystemDeflection)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2920.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2920,
            )

            return self._parent._cast(
                _2920.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2923.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2923,
            )

            return self._parent._cast(
                _2923.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2926.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2926,
            )

            return self._parent._cast(
                _2926.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection
            )

        @property
        def planetary_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2936.PlanetaryGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2936,
            )

            return self._parent._cast(_2936.PlanetaryGearSetCompoundSystemDeflection)

        @property
        def spiral_bevel_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2954.SpiralBevelGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2954,
            )

            return self._parent._cast(_2954.SpiralBevelGearSetCompoundSystemDeflection)

        @property
        def straight_bevel_diff_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2960.StraightBevelDiffGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2960,
            )

            return self._parent._cast(
                _2960.StraightBevelDiffGearSetCompoundSystemDeflection
            )

        @property
        def straight_bevel_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2963.StraightBevelGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2963,
            )

            return self._parent._cast(
                _2963.StraightBevelGearSetCompoundSystemDeflection
            )

        @property
        def worm_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2978.WormGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2978,
            )

            return self._parent._cast(_2978.WormGearSetCompoundSystemDeflection)

        @property
        def zerol_bevel_gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "_2981.ZerolBevelGearSetCompoundSystemDeflection":
            from mastapy.system_model.analyses_and_results.system_deflections.compound import (
                _2981,
            )

            return self._parent._cast(_2981.ZerolBevelGearSetCompoundSystemDeflection)

        @property
        def gear_set_compound_system_deflection(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
        ) -> "GearSetCompoundSystemDeflection":
            return self._parent

        def __getattr__(
            self: "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "GearSetCompoundSystemDeflection.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self: Self) -> "List[_2760.GearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: Self,
    ) -> "List[_2760.GearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "GearSetCompoundSystemDeflection._Cast_GearSetCompoundSystemDeflection":
        return self._Cast_GearSetCompoundSystemDeflection(self)
