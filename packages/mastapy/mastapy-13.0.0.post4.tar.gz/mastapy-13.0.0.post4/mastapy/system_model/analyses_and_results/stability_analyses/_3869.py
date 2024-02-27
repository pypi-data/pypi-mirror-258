"""SpringDamperStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3802
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "SpringDamperStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2600
    from mastapy.system_model.analyses_and_results.static_loads import _6958
    from mastapy.system_model.analyses_and_results.stability_analyses import (
        _3863,
        _3763,
        _3844,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("SpringDamperStabilityAnalysis",)


Self = TypeVar("Self", bound="SpringDamperStabilityAnalysis")


class SpringDamperStabilityAnalysis(_3802.CouplingStabilityAnalysis):
    """SpringDamperStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _SPRING_DAMPER_STABILITY_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpringDamperStabilityAnalysis")

    class _Cast_SpringDamperStabilityAnalysis:
        """Special nested class for casting SpringDamperStabilityAnalysis to subclasses."""

        def __init__(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
            parent: "SpringDamperStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def coupling_stability_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_3802.CouplingStabilityAnalysis":
            return self._parent._cast(_3802.CouplingStabilityAnalysis)

        @property
        def specialised_assembly_stability_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_3863.SpecialisedAssemblyStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3863,
            )

            return self._parent._cast(_3863.SpecialisedAssemblyStabilityAnalysis)

        @property
        def abstract_assembly_stability_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_3763.AbstractAssemblyStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3763,
            )

            return self._parent._cast(_3763.AbstractAssemblyStabilityAnalysis)

        @property
        def part_stability_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_3844.PartStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3844,
            )

            return self._parent._cast(_3844.PartStabilityAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def spring_damper_stability_analysis(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
        ) -> "SpringDamperStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpringDamperStabilityAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2600.SpringDamper":
        """mastapy.system_model.part_model.couplings.SpringDamper

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: Self) -> "_6958.SpringDamperLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "SpringDamperStabilityAnalysis._Cast_SpringDamperStabilityAnalysis":
        return self._Cast_SpringDamperStabilityAnalysis(self)
