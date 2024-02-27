"""BevelDifferentialSunGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.part_model.gears import _2515
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2519, _2513, _2523, _2530
    from mastapy.system_model.part_model import _2464, _2444, _2468
    from mastapy.system_model import _2203


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialSunGear",)


Self = TypeVar("Self", bound="BevelDifferentialSunGear")


class BevelDifferentialSunGear(_2515.BevelDifferentialGear):
    """BevelDifferentialSunGear

    This is a mastapy class.
    """

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelDifferentialSunGear")

    class _Cast_BevelDifferentialSunGear:
        """Special nested class for casting BevelDifferentialSunGear to subclasses."""

        def __init__(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
            parent: "BevelDifferentialSunGear",
        ):
            self._parent = parent

        @property
        def bevel_differential_gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2515.BevelDifferentialGear":
            return self._parent._cast(_2515.BevelDifferentialGear)

        @property
        def bevel_gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2519.BevelGear":
            from mastapy.system_model.part_model.gears import _2519

            return self._parent._cast(_2519.BevelGear)

        @property
        def agma_gleason_conical_gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2513.AGMAGleasonConicalGear":
            from mastapy.system_model.part_model.gears import _2513

            return self._parent._cast(_2513.AGMAGleasonConicalGear)

        @property
        def conical_gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2523.ConicalGear":
            from mastapy.system_model.part_model.gears import _2523

            return self._parent._cast(_2523.ConicalGear)

        @property
        def gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2530.Gear":
            from mastapy.system_model.part_model.gears import _2530

            return self._parent._cast(_2530.Gear)

        @property
        def mountable_component(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2464.MountableComponent":
            from mastapy.system_model.part_model import _2464

            return self._parent._cast(_2464.MountableComponent)

        @property
        def component(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2444.Component":
            from mastapy.system_model.part_model import _2444

            return self._parent._cast(_2444.Component)

        @property
        def part(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def design_entity(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "_2203.DesignEntity":
            from mastapy.system_model import _2203

            return self._parent._cast(_2203.DesignEntity)

        @property
        def bevel_differential_sun_gear(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear",
        ) -> "BevelDifferentialSunGear":
            return self._parent

        def __getattr__(
            self: "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelDifferentialSunGear.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "BevelDifferentialSunGear._Cast_BevelDifferentialSunGear":
        return self._Cast_BevelDifferentialSunGear(self)
