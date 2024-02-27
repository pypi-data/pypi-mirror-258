"""GearSetCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3995
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "GearSetCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.stability_analyses import _3824
    from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
        _3903,
        _3910,
        _3915,
        _3928,
        _3931,
        _3946,
        _3952,
        _3961,
        _3965,
        _3968,
        _3971,
        _3981,
        _3998,
        _4004,
        _4007,
        _4022,
        _4025,
        _3897,
        _3976,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="GearSetCompoundStabilityAnalysis")


class GearSetCompoundStabilityAnalysis(
    _3995.SpecialisedAssemblyCompoundStabilityAnalysis
):
    """GearSetCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _GEAR_SET_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_GearSetCompoundStabilityAnalysis")

    class _Cast_GearSetCompoundStabilityAnalysis:
        """Special nested class for casting GearSetCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
            parent: "GearSetCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def specialised_assembly_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3995.SpecialisedAssemblyCompoundStabilityAnalysis":
            return self._parent._cast(
                _3995.SpecialisedAssemblyCompoundStabilityAnalysis
            )

        @property
        def abstract_assembly_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3897.AbstractAssemblyCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3897,
            )

            return self._parent._cast(_3897.AbstractAssemblyCompoundStabilityAnalysis)

        @property
        def part_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3976.PartCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3976,
            )

            return self._parent._cast(_3976.PartCompoundStabilityAnalysis)

        @property
        def part_compound_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3903.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3903,
            )

            return self._parent._cast(
                _3903.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
            )

        @property
        def bevel_differential_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3910.BevelDifferentialGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3910,
            )

            return self._parent._cast(
                _3910.BevelDifferentialGearSetCompoundStabilityAnalysis
            )

        @property
        def bevel_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3915.BevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3915,
            )

            return self._parent._cast(_3915.BevelGearSetCompoundStabilityAnalysis)

        @property
        def concept_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3928.ConceptGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3928,
            )

            return self._parent._cast(_3928.ConceptGearSetCompoundStabilityAnalysis)

        @property
        def conical_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3931.ConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3931,
            )

            return self._parent._cast(_3931.ConicalGearSetCompoundStabilityAnalysis)

        @property
        def cylindrical_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3946.CylindricalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3946,
            )

            return self._parent._cast(_3946.CylindricalGearSetCompoundStabilityAnalysis)

        @property
        def face_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3952.FaceGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3952,
            )

            return self._parent._cast(_3952.FaceGearSetCompoundStabilityAnalysis)

        @property
        def hypoid_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3961.HypoidGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3961,
            )

            return self._parent._cast(_3961.HypoidGearSetCompoundStabilityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3965.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3965,
            )

            return self._parent._cast(
                _3965.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3968.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3968,
            )

            return self._parent._cast(
                _3968.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> (
            "_3971.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis"
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3971,
            )

            return self._parent._cast(
                _3971.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
            )

        @property
        def planetary_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3981.PlanetaryGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3981,
            )

            return self._parent._cast(_3981.PlanetaryGearSetCompoundStabilityAnalysis)

        @property
        def spiral_bevel_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_3998.SpiralBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3998,
            )

            return self._parent._cast(_3998.SpiralBevelGearSetCompoundStabilityAnalysis)

        @property
        def straight_bevel_diff_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_4004.StraightBevelDiffGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4004,
            )

            return self._parent._cast(
                _4004.StraightBevelDiffGearSetCompoundStabilityAnalysis
            )

        @property
        def straight_bevel_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_4007.StraightBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4007,
            )

            return self._parent._cast(
                _4007.StraightBevelGearSetCompoundStabilityAnalysis
            )

        @property
        def worm_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_4022.WormGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4022,
            )

            return self._parent._cast(_4022.WormGearSetCompoundStabilityAnalysis)

        @property
        def zerol_bevel_gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "_4025.ZerolBevelGearSetCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4025,
            )

            return self._parent._cast(_4025.ZerolBevelGearSetCompoundStabilityAnalysis)

        @property
        def gear_set_compound_stability_analysis(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
        ) -> "GearSetCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "GearSetCompoundStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self: Self) -> "List[_3824.GearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.GearSetStabilityAnalysis]

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
    ) -> "List[_3824.GearSetStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.GearSetStabilityAnalysis]

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
    ) -> "GearSetCompoundStabilityAnalysis._Cast_GearSetCompoundStabilityAnalysis":
        return self._Cast_GearSetCompoundStabilityAnalysis(self)
