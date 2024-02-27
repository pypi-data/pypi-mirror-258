"""InterMountableComponentConnectionPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4067
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "InterMountableComponentConnectionPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets import _2281
    from mastapy.system_model.analyses_and_results.power_flows import (
        _4036,
        _4041,
        _4043,
        _4048,
        _4053,
        _4058,
        _4061,
        _4064,
        _4069,
        _4072,
        _4080,
        _4086,
        _4092,
        _4096,
        _4100,
        _4103,
        _4106,
        _4114,
        _4126,
        _4128,
        _4135,
        _4138,
        _4141,
        _4144,
        _4154,
        _4160,
        _4163,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7540, _7537
    from mastapy.system_model.analyses_and_results import _2649, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionPowerFlow",)


Self = TypeVar("Self", bound="InterMountableComponentConnectionPowerFlow")


class InterMountableComponentConnectionPowerFlow(_4067.ConnectionPowerFlow):
    """InterMountableComponentConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE = _INTER_MOUNTABLE_COMPONENT_CONNECTION_POWER_FLOW
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_InterMountableComponentConnectionPowerFlow"
    )

    class _Cast_InterMountableComponentConnectionPowerFlow:
        """Special nested class for casting InterMountableComponentConnectionPowerFlow to subclasses."""

        def __init__(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
            parent: "InterMountableComponentConnectionPowerFlow",
        ):
            self._parent = parent

        @property
        def connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4067.ConnectionPowerFlow":
            return self._parent._cast(_4067.ConnectionPowerFlow)

        @property
        def connection_static_load_analysis_case(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_7540.ConnectionStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7540

            return self._parent._cast(_7540.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_7537.ConnectionAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7537

            return self._parent._cast(_7537.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_2649.ConnectionAnalysis":
            from mastapy.system_model.analyses_and_results import _2649

            return self._parent._cast(_2649.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4036.AGMAGleasonConicalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4036

            return self._parent._cast(_4036.AGMAGleasonConicalGearMeshPowerFlow)

        @property
        def belt_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4041.BeltConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4041

            return self._parent._cast(_4041.BeltConnectionPowerFlow)

        @property
        def bevel_differential_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4043.BevelDifferentialGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4043

            return self._parent._cast(_4043.BevelDifferentialGearMeshPowerFlow)

        @property
        def bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4048.BevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4048

            return self._parent._cast(_4048.BevelGearMeshPowerFlow)

        @property
        def clutch_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4053.ClutchConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4053

            return self._parent._cast(_4053.ClutchConnectionPowerFlow)

        @property
        def concept_coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4058.ConceptCouplingConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4058

            return self._parent._cast(_4058.ConceptCouplingConnectionPowerFlow)

        @property
        def concept_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4061.ConceptGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4061

            return self._parent._cast(_4061.ConceptGearMeshPowerFlow)

        @property
        def conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4064.ConicalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4064

            return self._parent._cast(_4064.ConicalGearMeshPowerFlow)

        @property
        def coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4069.CouplingConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4069

            return self._parent._cast(_4069.CouplingConnectionPowerFlow)

        @property
        def cvt_belt_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4072.CVTBeltConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4072

            return self._parent._cast(_4072.CVTBeltConnectionPowerFlow)

        @property
        def cylindrical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4080.CylindricalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4080

            return self._parent._cast(_4080.CylindricalGearMeshPowerFlow)

        @property
        def face_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4086.FaceGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4086

            return self._parent._cast(_4086.FaceGearMeshPowerFlow)

        @property
        def gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4092.GearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4092

            return self._parent._cast(_4092.GearMeshPowerFlow)

        @property
        def hypoid_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4096.HypoidGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4096

            return self._parent._cast(_4096.HypoidGearMeshPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4100.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4100

            return self._parent._cast(
                _4100.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4103.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4103

            return self._parent._cast(
                _4103.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4106.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4106

            return self._parent._cast(
                _4106.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
            )

        @property
        def part_to_part_shear_coupling_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4114.PartToPartShearCouplingConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4114

            return self._parent._cast(_4114.PartToPartShearCouplingConnectionPowerFlow)

        @property
        def ring_pins_to_disc_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4126.RingPinsToDiscConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4126

            return self._parent._cast(_4126.RingPinsToDiscConnectionPowerFlow)

        @property
        def rolling_ring_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4128.RollingRingConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4128

            return self._parent._cast(_4128.RollingRingConnectionPowerFlow)

        @property
        def spiral_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4135.SpiralBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4135

            return self._parent._cast(_4135.SpiralBevelGearMeshPowerFlow)

        @property
        def spring_damper_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4138.SpringDamperConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4138

            return self._parent._cast(_4138.SpringDamperConnectionPowerFlow)

        @property
        def straight_bevel_diff_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4141.StraightBevelDiffGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4141

            return self._parent._cast(_4141.StraightBevelDiffGearMeshPowerFlow)

        @property
        def straight_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4144.StraightBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4144

            return self._parent._cast(_4144.StraightBevelGearMeshPowerFlow)

        @property
        def torque_converter_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4154.TorqueConverterConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4154

            return self._parent._cast(_4154.TorqueConverterConnectionPowerFlow)

        @property
        def worm_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4160.WormGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4160

            return self._parent._cast(_4160.WormGearMeshPowerFlow)

        @property
        def zerol_bevel_gear_mesh_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "_4163.ZerolBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4163

            return self._parent._cast(_4163.ZerolBevelGearMeshPowerFlow)

        @property
        def inter_mountable_component_connection_power_flow(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
        ) -> "InterMountableComponentConnectionPowerFlow":
            return self._parent

        def __getattr__(
            self: "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow",
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
        self: Self, instance_to_wrap: "InterMountableComponentConnectionPowerFlow.TYPE"
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
    ) -> "InterMountableComponentConnectionPowerFlow._Cast_InterMountableComponentConnectionPowerFlow":
        return self._Cast_InterMountableComponentConnectionPowerFlow(self)
