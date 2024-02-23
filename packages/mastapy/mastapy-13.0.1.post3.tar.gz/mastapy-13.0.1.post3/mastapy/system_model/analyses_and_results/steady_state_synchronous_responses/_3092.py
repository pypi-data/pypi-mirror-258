"""StraightBevelDiffGearMeshSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _2999,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2325
    from mastapy.system_model.analyses_and_results.static_loads import _6961


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshSteadyStateSynchronousResponse",)


Self = TypeVar("Self", bound="StraightBevelDiffGearMeshSteadyStateSynchronousResponse")


class StraightBevelDiffGearMeshSteadyStateSynchronousResponse(
    _2999.BevelGearMeshSteadyStateSynchronousResponse
):
    """StraightBevelDiffGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
    )

    class _Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse:
        """Special nested class for casting StraightBevelDiffGearMeshSteadyStateSynchronousResponse to subclasses."""

        def __init__(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
            parent: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            self._parent = parent

        @property
        def bevel_gear_mesh_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            return self._parent._cast(_2999.BevelGearMeshSteadyStateSynchronousResponse)

        @property
        def agma_gleason_conical_gear_mesh_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _2987,
            )

            return self._parent._cast(
                _2987.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse
            )

        @property
        def conical_gear_mesh_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3015,
            )

            return self._parent._cast(
                _3015.ConicalGearMeshSteadyStateSynchronousResponse
            )

        @property
        def gear_mesh_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3042,
            )

            return self._parent._cast(_3042.GearMeshSteadyStateSynchronousResponse)

        @property
        def inter_mountable_component_connection_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3049,
            )

            return self._parent._cast(
                _3049.InterMountableComponentConnectionSteadyStateSynchronousResponse
            )

        @property
        def connection_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3018,
            )

            return self._parent._cast(_3018.ConnectionSteadyStateSynchronousResponse)

        @property
        def connection_static_load_analysis_case(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7541

            return self._parent._cast(_7541.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7538

            return self._parent._cast(_7538.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2649

            return self._parent._cast(_2649.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def straight_bevel_diff_gear_mesh_steady_state_synchronous_response(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
        ) -> "StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
            return self._parent

        def __getattr__(
            self: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse",
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
        instance_to_wrap: "StraightBevelDiffGearMeshSteadyStateSynchronousResponse.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2325.StraightBevelDiffGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: Self) -> "_6961.StraightBevelDiffGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionLoadCase

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "StraightBevelDiffGearMeshSteadyStateSynchronousResponse._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
        return self._Cast_StraightBevelDiffGearMeshSteadyStateSynchronousResponse(self)
