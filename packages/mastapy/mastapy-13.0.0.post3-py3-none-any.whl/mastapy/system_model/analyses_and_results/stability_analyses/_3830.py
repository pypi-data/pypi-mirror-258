"""InterMountableComponentConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _3798
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "InterMountableComponentConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2281


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionStabilityAnalysis",)


Self = TypeVar("Self", bound="InterMountableComponentConnectionStabilityAnalysis")


class InterMountableComponentConnectionStabilityAnalysis(
    _3798.ConnectionStabilityAnalysis
):
    """InterMountableComponentConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_InterMountableComponentConnectionStabilityAnalysis"
    )

    class _Cast_InterMountableComponentConnectionStabilityAnalysis:
        """Special nested class for casting InterMountableComponentConnectionStabilityAnalysis to subclasses."""

        def __init__(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
            parent: "InterMountableComponentConnectionStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            return self._parent._cast(_3798.ConnectionStabilityAnalysis)

        @property
        def connection_static_load_analysis_case(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7537

            return self._parent._cast(_7537.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2649

            return self._parent._cast(_2649.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3767,
            )

            return self._parent._cast(_3767.AGMAGleasonConicalGearMeshStabilityAnalysis)

        @property
        def belt_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3772,
            )

            return self._parent._cast(_3772.BeltConnectionStabilityAnalysis)

        @property
        def bevel_differential_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3774,
            )

            return self._parent._cast(_3774.BevelDifferentialGearMeshStabilityAnalysis)

        @property
        def bevel_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3779,
            )

            return self._parent._cast(_3779.BevelGearMeshStabilityAnalysis)

        @property
        def clutch_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3784,
            )

            return self._parent._cast(_3784.ClutchConnectionStabilityAnalysis)

        @property
        def concept_coupling_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3789,
            )

            return self._parent._cast(_3789.ConceptCouplingConnectionStabilityAnalysis)

        @property
        def concept_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3792,
            )

            return self._parent._cast(_3792.ConceptGearMeshStabilityAnalysis)

        @property
        def conical_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3795,
            )

            return self._parent._cast(_3795.ConicalGearMeshStabilityAnalysis)

        @property
        def coupling_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3800,
            )

            return self._parent._cast(_3800.CouplingConnectionStabilityAnalysis)

        @property
        def cvt_belt_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3804,
            )

            return self._parent._cast(_3804.CVTBeltConnectionStabilityAnalysis)

        @property
        def cylindrical_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3811,
            )

            return self._parent._cast(_3811.CylindricalGearMeshStabilityAnalysis)

        @property
        def face_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3818,
            )

            return self._parent._cast(_3818.FaceGearMeshStabilityAnalysis)

        @property
        def gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3823,
            )

            return self._parent._cast(_3823.GearMeshStabilityAnalysis)

        @property
        def hypoid_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3827,
            )

            return self._parent._cast(_3827.HypoidGearMeshStabilityAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3831,
            )

            return self._parent._cast(
                _3831.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3834,
            )

            return self._parent._cast(
                _3834.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3837,
            )

            return self._parent._cast(
                _3837.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
            )

        @property
        def part_to_part_shear_coupling_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3845,
            )

            return self._parent._cast(
                _3845.PartToPartShearCouplingConnectionStabilityAnalysis
            )

        @property
        def ring_pins_to_disc_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3855,
            )

            return self._parent._cast(_3855.RingPinsToDiscConnectionStabilityAnalysis)

        @property
        def rolling_ring_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3857,
            )

            return self._parent._cast(_3857.RollingRingConnectionStabilityAnalysis)

        @property
        def spiral_bevel_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3864,
            )

            return self._parent._cast(_3864.SpiralBevelGearMeshStabilityAnalysis)

        @property
        def spring_damper_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3867,
            )

            return self._parent._cast(_3867.SpringDamperConnectionStabilityAnalysis)

        @property
        def straight_bevel_diff_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3873,
            )

            return self._parent._cast(_3873.StraightBevelDiffGearMeshStabilityAnalysis)

        @property
        def straight_bevel_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3876,
            )

            return self._parent._cast(_3876.StraightBevelGearMeshStabilityAnalysis)

        @property
        def torque_converter_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3885,
            )

            return self._parent._cast(_3885.TorqueConverterConnectionStabilityAnalysis)

        @property
        def worm_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3891,
            )

            return self._parent._cast(_3891.WormGearMeshStabilityAnalysis)

        @property
        def zerol_bevel_gear_mesh_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3894,
            )

            return self._parent._cast(_3894.ZerolBevelGearMeshStabilityAnalysis)

        @property
        def inter_mountable_component_connection_stability_analysis(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
        ) -> "InterMountableComponentConnectionStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis",
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
        instance_to_wrap: "InterMountableComponentConnectionStabilityAnalysis.TYPE",
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
    ) -> "InterMountableComponentConnectionStabilityAnalysis._Cast_InterMountableComponentConnectionStabilityAnalysis":
        return self._Cast_InterMountableComponentConnectionStabilityAnalysis(self)
