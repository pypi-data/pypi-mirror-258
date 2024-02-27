"""VirtualComponentPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.power_flows import _4111
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "VirtualComponentPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2479
    from mastapy.system_model.analyses_and_results.power_flows import (
        _4109,
        _4110,
        _4120,
        _4123,
        _4158,
        _4057,
        _4113,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentPowerFlow",)


Self = TypeVar("Self", bound="VirtualComponentPowerFlow")


class VirtualComponentPowerFlow(_4111.MountableComponentPowerFlow):
    """VirtualComponentPowerFlow

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_VirtualComponentPowerFlow")

    class _Cast_VirtualComponentPowerFlow:
        """Special nested class for casting VirtualComponentPowerFlow to subclasses."""

        def __init__(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
            parent: "VirtualComponentPowerFlow",
        ):
            self._parent = parent

        @property
        def mountable_component_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4111.MountableComponentPowerFlow":
            return self._parent._cast(_4111.MountableComponentPowerFlow)

        @property
        def component_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4057.ComponentPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4057

            return self._parent._cast(_4057.ComponentPowerFlow)

        @property
        def part_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4113.PartPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4113

            return self._parent._cast(_4113.PartPowerFlow)

        @property
        def part_static_load_analysis_case(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def mass_disc_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4109.MassDiscPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4109

            return self._parent._cast(_4109.MassDiscPowerFlow)

        @property
        def measurement_component_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4110.MeasurementComponentPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4110

            return self._parent._cast(_4110.MeasurementComponentPowerFlow)

        @property
        def point_load_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4120.PointLoadPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4120

            return self._parent._cast(_4120.PointLoadPowerFlow)

        @property
        def power_load_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4123.PowerLoadPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4123

            return self._parent._cast(_4123.PowerLoadPowerFlow)

        @property
        def unbalanced_mass_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "_4158.UnbalancedMassPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows import _4158

            return self._parent._cast(_4158.UnbalancedMassPowerFlow)

        @property
        def virtual_component_power_flow(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow",
        ) -> "VirtualComponentPowerFlow":
            return self._parent

        def __getattr__(
            self: "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "VirtualComponentPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def power(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Power

        if temp is None:
            return 0.0

        return temp

    @property
    def torque(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Torque

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: Self) -> "_2479.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "VirtualComponentPowerFlow._Cast_VirtualComponentPowerFlow":
        return self._Cast_VirtualComponentPowerFlow(self)
