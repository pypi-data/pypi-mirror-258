"""RootAssemblySteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3511,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "RootAssemblySteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2474
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3609,
        _3504,
        _3583,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblySteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar("Self", bound="RootAssemblySteadyStateSynchronousResponseAtASpeed")


class RootAssemblySteadyStateSynchronousResponseAtASpeed(
    _3511.AssemblySteadyStateSynchronousResponseAtASpeed
):
    """RootAssemblySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = _ROOT_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed"
    )

    class _Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting RootAssemblySteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
            parent: "RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_3511.AssemblySteadyStateSynchronousResponseAtASpeed":
            return self._parent._cast(
                _3511.AssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def abstract_assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_3504.AbstractAssemblySteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3504,
            )

            return self._parent._cast(
                _3504.AbstractAssemblySteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_3583.PartSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3583,
            )

            return self._parent._cast(_3583.PartSteadyStateSynchronousResponseAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def root_assembly_steady_state_synchronous_response_at_a_speed(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
        ) -> "RootAssemblySteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed",
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
        self: Self,
        instance_to_wrap: "RootAssemblySteadyStateSynchronousResponseAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self: Self) -> "_2474.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response_at_a_speed_inputs(
        self: Self,
    ) -> "_3609.SteadyStateSynchronousResponseAtASpeed":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.SteadyStateSynchronousResponseAtASpeed

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SteadyStateSynchronousResponseAtASpeedInputs

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "RootAssemblySteadyStateSynchronousResponseAtASpeed._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed":
        return self._Cast_RootAssemblySteadyStateSynchronousResponseAtASpeed(self)
