"""VirtualComponent"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.part_model import _2464
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import (
        _2462,
        _2463,
        _2471,
        _2472,
        _2477,
        _2444,
        _2468,
    )
    from mastapy.system_model import _2203


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponent",)


Self = TypeVar("Self", bound="VirtualComponent")


class VirtualComponent(_2464.MountableComponent):
    """VirtualComponent

    This is a mastapy class.
    """

    TYPE = _VIRTUAL_COMPONENT
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_VirtualComponent")

    class _Cast_VirtualComponent:
        """Special nested class for casting VirtualComponent to subclasses."""

        def __init__(
            self: "VirtualComponent._Cast_VirtualComponent", parent: "VirtualComponent"
        ):
            self._parent = parent

        @property
        def mountable_component(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2464.MountableComponent":
            return self._parent._cast(_2464.MountableComponent)

        @property
        def component(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2444.Component":
            from mastapy.system_model.part_model import _2444

            return self._parent._cast(_2444.Component)

        @property
        def part(self: "VirtualComponent._Cast_VirtualComponent") -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def design_entity(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2203.DesignEntity":
            from mastapy.system_model import _2203

            return self._parent._cast(_2203.DesignEntity)

        @property
        def mass_disc(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2462.MassDisc":
            from mastapy.system_model.part_model import _2462

            return self._parent._cast(_2462.MassDisc)

        @property
        def measurement_component(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2463.MeasurementComponent":
            from mastapy.system_model.part_model import _2463

            return self._parent._cast(_2463.MeasurementComponent)

        @property
        def point_load(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2471.PointLoad":
            from mastapy.system_model.part_model import _2471

            return self._parent._cast(_2471.PointLoad)

        @property
        def power_load(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2472.PowerLoad":
            from mastapy.system_model.part_model import _2472

            return self._parent._cast(_2472.PowerLoad)

        @property
        def unbalanced_mass(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "_2477.UnbalancedMass":
            from mastapy.system_model.part_model import _2477

            return self._parent._cast(_2477.UnbalancedMass)

        @property
        def virtual_component(
            self: "VirtualComponent._Cast_VirtualComponent",
        ) -> "VirtualComponent":
            return self._parent

        def __getattr__(self: "VirtualComponent._Cast_VirtualComponent", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "VirtualComponent.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "VirtualComponent._Cast_VirtualComponent":
        return self._Cast_VirtualComponent(self)
