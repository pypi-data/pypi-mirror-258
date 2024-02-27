"""ConicalGearMeshPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4093
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_MESH_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConicalGearMeshPowerFlow"
)

if TYPE_CHECKING:
    from mastapy.system_model.connections_and_sockets.gears import _2307
    from mastapy.system_model.analyses_and_results.power_flows import (
        _4036,
        _4043,
        _4048,
        _4097,
        _4101,
        _4104,
        _4107,
        _4136,
        _4142,
        _4145,
        _4164,
        _4100,
        _4067,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7541, _7538
    from mastapy.system_model.analyses_and_results import _2649, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshPowerFlow",)


Self = TypeVar("Self", bound="ConicalGearMeshPowerFlow")


class ConicalGearMeshPowerFlow(_4093.GearMeshPowerFlow):
    """ConicalGearMeshPowerFlow

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_MESH_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConicalGearMeshPowerFlow")

    class _Cast_ConicalGearMeshPowerFlow:
        """Special nested class for casting ConicalGearMeshPowerFlow to subclasses."""

        def __init__(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
            parent: "ConicalGearMeshPowerFlow",
        ):
            self._parent = parent

        @property
        def gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4093.GearMeshPowerFlow":
            return self._parent._cast(_4093.GearMeshPowerFlow)

        @property
        def inter_mountable_component_connection_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4100.InterMountableComponentConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4100

            return self._parent._cast(_4100.InterMountableComponentConnectionPowerFlow)

        @property
        def connection_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4067.ConnectionPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4067

            return self._parent._cast(_4067.ConnectionPowerFlow)

        @property
        def connection_static_load_analysis_case(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_7541.ConnectionStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7541

            return self._parent._cast(_7541.ConnectionStaticLoadAnalysisCase)

        @property
        def connection_analysis_case(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_7538.ConnectionAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7538

            return self._parent._cast(_7538.ConnectionAnalysisCase)

        @property
        def connection_analysis(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_2649.ConnectionAnalysis":
            from mastapy.system_model.analyses_and_results import _2649

            return self._parent._cast(_2649.ConnectionAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4036.AGMAGleasonConicalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4036

            return self._parent._cast(_4036.AGMAGleasonConicalGearMeshPowerFlow)

        @property
        def bevel_differential_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4043.BevelDifferentialGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4043

            return self._parent._cast(_4043.BevelDifferentialGearMeshPowerFlow)

        @property
        def bevel_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4048.BevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4048

            return self._parent._cast(_4048.BevelGearMeshPowerFlow)

        @property
        def hypoid_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4097.HypoidGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4097

            return self._parent._cast(_4097.HypoidGearMeshPowerFlow)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4101.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4101

            return self._parent._cast(
                _4101.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4104.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4104

            return self._parent._cast(
                _4104.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4107.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4107

            return self._parent._cast(
                _4107.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
            )

        @property
        def spiral_bevel_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4136.SpiralBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4136

            return self._parent._cast(_4136.SpiralBevelGearMeshPowerFlow)

        @property
        def straight_bevel_diff_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4142.StraightBevelDiffGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4142

            return self._parent._cast(_4142.StraightBevelDiffGearMeshPowerFlow)

        @property
        def straight_bevel_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4145.StraightBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4145

            return self._parent._cast(_4145.StraightBevelGearMeshPowerFlow)

        @property
        def zerol_bevel_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "_4164.ZerolBevelGearMeshPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4164

            return self._parent._cast(_4164.ZerolBevelGearMeshPowerFlow)

        @property
        def conical_gear_mesh_power_flow(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow",
        ) -> "ConicalGearMeshPowerFlow":
            return self._parent

        def __getattr__(
            self: "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ConicalGearMeshPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self: Self) -> "_2307.ConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh

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
    ) -> "ConicalGearMeshPowerFlow._Cast_ConicalGearMeshPowerFlow":
        return self._Cast_ConicalGearMeshPowerFlow(self)
