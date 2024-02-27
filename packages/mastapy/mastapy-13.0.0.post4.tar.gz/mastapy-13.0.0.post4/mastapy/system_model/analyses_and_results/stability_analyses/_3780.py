"""BevelGearSetStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3768
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "BevelGearSetStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2520
    from mastapy.system_model.analyses_and_results.stability_analyses import (
        _3775,
        _3865,
        _3874,
        _3877,
        _3895,
        _3796,
        _3824,
        _3863,
        _3763,
        _3844,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetStabilityAnalysis",)


Self = TypeVar("Self", bound="BevelGearSetStabilityAnalysis")


class BevelGearSetStabilityAnalysis(_3768.AGMAGleasonConicalGearSetStabilityAnalysis):
    """BevelGearSetStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearSetStabilityAnalysis")

    class _Cast_BevelGearSetStabilityAnalysis:
        """Special nested class for casting BevelGearSetStabilityAnalysis to subclasses."""

        def __init__(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
            parent: "BevelGearSetStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3768.AGMAGleasonConicalGearSetStabilityAnalysis":
            return self._parent._cast(_3768.AGMAGleasonConicalGearSetStabilityAnalysis)

        @property
        def conical_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3796.ConicalGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3796,
            )

            return self._parent._cast(_3796.ConicalGearSetStabilityAnalysis)

        @property
        def gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3824.GearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3824,
            )

            return self._parent._cast(_3824.GearSetStabilityAnalysis)

        @property
        def specialised_assembly_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3863.SpecialisedAssemblyStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3863,
            )

            return self._parent._cast(_3863.SpecialisedAssemblyStabilityAnalysis)

        @property
        def abstract_assembly_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3763.AbstractAssemblyStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3763,
            )

            return self._parent._cast(_3763.AbstractAssemblyStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3844.PartStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3844,
            )

            return self._parent._cast(_3844.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3775.BevelDifferentialGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3775,
            )

            return self._parent._cast(_3775.BevelDifferentialGearSetStabilityAnalysis)

        @property
        def spiral_bevel_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3865.SpiralBevelGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3865,
            )

            return self._parent._cast(_3865.SpiralBevelGearSetStabilityAnalysis)

        @property
        def straight_bevel_diff_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3874.StraightBevelDiffGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3874,
            )

            return self._parent._cast(_3874.StraightBevelDiffGearSetStabilityAnalysis)

        @property
        def straight_bevel_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3877.StraightBevelGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3877,
            )

            return self._parent._cast(_3877.StraightBevelGearSetStabilityAnalysis)

        @property
        def zerol_bevel_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "_3895.ZerolBevelGearSetStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3895,
            )

            return self._parent._cast(_3895.ZerolBevelGearSetStabilityAnalysis)

        @property
        def bevel_gear_set_stability_analysis(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
        ) -> "BevelGearSetStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearSetStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2520.BevelGearSet":
        """mastapy.system_model.part_model.gears.BevelGearSet

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
    ) -> "BevelGearSetStabilityAnalysis._Cast_BevelGearSetStabilityAnalysis":
        return self._Cast_BevelGearSetStabilityAnalysis(self)
