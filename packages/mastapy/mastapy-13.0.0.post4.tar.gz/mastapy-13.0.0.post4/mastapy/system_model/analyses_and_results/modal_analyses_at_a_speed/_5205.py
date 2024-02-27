"""PulleyModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5154
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PULLEY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "PulleyModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2590
    from mastapy.system_model.analyses_and_results.static_loads import _6940
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5158,
        _5194,
        _5141,
        _5196,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("PulleyModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="PulleyModalAnalysisAtASpeed")


class PulleyModalAnalysisAtASpeed(_5154.CouplingHalfModalAnalysisAtASpeed):
    """PulleyModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _PULLEY_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PulleyModalAnalysisAtASpeed")

    class _Cast_PulleyModalAnalysisAtASpeed:
        """Special nested class for casting PulleyModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
            parent: "PulleyModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def coupling_half_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_5154.CouplingHalfModalAnalysisAtASpeed":
            return self._parent._cast(_5154.CouplingHalfModalAnalysisAtASpeed)

        @property
        def mountable_component_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_5194.MountableComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5194,
            )

            return self._parent._cast(_5194.MountableComponentModalAnalysisAtASpeed)

        @property
        def component_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_5141.ComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5141,
            )

            return self._parent._cast(_5141.ComponentModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_5196.PartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5196,
            )

            return self._parent._cast(_5196.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def cvt_pulley_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "_5158.CVTPulleyModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5158,
            )

            return self._parent._cast(_5158.CVTPulleyModalAnalysisAtASpeed)

        @property
        def pulley_modal_analysis_at_a_speed(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
        ) -> "PulleyModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "PulleyModalAnalysisAtASpeed.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2590.Pulley":
        """mastapy.system_model.part_model.couplings.Pulley

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: Self) -> "_6940.PulleyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "PulleyModalAnalysisAtASpeed._Cast_PulleyModalAnalysisAtASpeed":
        return self._Cast_PulleyModalAnalysisAtASpeed(self)
