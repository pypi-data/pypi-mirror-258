"""InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3280,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2281
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3249,
        _3254,
        _3256,
        _3261,
        _3266,
        _3271,
        _3274,
        _3277,
        _3282,
        _3285,
        _3292,
        _3298,
        _3303,
        _3307,
        _3311,
        _3314,
        _3317,
        _3325,
        _3335,
        _3337,
        _3344,
        _3347,
        _3351,
        _3354,
        _3363,
        _3369,
        _3372,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7540, _7537
    from mastapy.system_model.analyses_and_results import _2649, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",)


Self = TypeVar(
    "Self",
    bound="InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
)


class InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft(
    _3280.ConnectionSteadyStateSynchronousResponseOnAShaft
):
    """InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
    )

    class _Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft:
        """Special nested class for casting InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft to subclasses."""

        def __init__(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
            parent: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ):
            self._parent = parent

        @property
        def connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3280.ConnectionSteadyStateSynchronousResponseOnAShaft":
            return self._parent._cast(
                _3280.ConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def connection_static_load_analysis_case(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_7540.ConnectionStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_7537.ConnectionAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7537

            return self._parent._cast(_7537.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_2649.ConnectionAnalysis":
            from mastapy.system_model.analyses_and_results import _2649

            return self._parent._cast(_2649.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3249.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3249,
            )

            return self._parent._cast(
                _3249.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def belt_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3254.BeltConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3254,
            )

            return self._parent._cast(
                _3254.BeltConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3256.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3256,
            )

            return self._parent._cast(
                _3256.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3261.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3261,
            )

            return self._parent._cast(
                _3261.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def clutch_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3266.ClutchConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3266,
            )

            return self._parent._cast(
                _3266.ClutchConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def concept_coupling_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3271.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3271,
            )

            return self._parent._cast(
                _3271.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def concept_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3274.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3274,
            )

            return self._parent._cast(
                _3274.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3277.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3277,
            )

            return self._parent._cast(
                _3277.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def coupling_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3282.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3282,
            )

            return self._parent._cast(
                _3282.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def cvt_belt_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3285.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3285,
            )

            return self._parent._cast(
                _3285.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def cylindrical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3292.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3292,
            )

            return self._parent._cast(
                _3292.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def face_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3298.FaceGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3298,
            )

            return self._parent._cast(
                _3298.FaceGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3303.GearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3303,
            )

            return self._parent._cast(
                _3303.GearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3307.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3307,
            )

            return self._parent._cast(
                _3307.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3311.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3311,
            )

            return self._parent._cast(
                _3311.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3314.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3314,
            )

            return self._parent._cast(
                _3314.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3317.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3317,
            )

            return self._parent._cast(
                _3317.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3325.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3325,
            )

            return self._parent._cast(
                _3325.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def ring_pins_to_disc_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3335.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3335,
            )

            return self._parent._cast(
                _3335.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def rolling_ring_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3337.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3337,
            )

            return self._parent._cast(
                _3337.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3344.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3344,
            )

            return self._parent._cast(
                _3344.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def spring_damper_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3347.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3347,
            )

            return self._parent._cast(
                _3347.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3351.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3351,
            )

            return self._parent._cast(
                _3351.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def straight_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3354.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3354,
            )

            return self._parent._cast(
                _3354.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def torque_converter_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3363.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3363,
            )

            return self._parent._cast(
                _3363.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def worm_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3369.WormGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3369,
            )

            return self._parent._cast(
                _3369.WormGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def zerol_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "_3372.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3372,
            )

            return self._parent._cast(
                _3372.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft
            )

        @property
        def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
        ) -> "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
            return self._parent

        def __getattr__(
            self: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft",
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
        instance_to_wrap: "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2281.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        return self._Cast_InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft(
            self
        )
