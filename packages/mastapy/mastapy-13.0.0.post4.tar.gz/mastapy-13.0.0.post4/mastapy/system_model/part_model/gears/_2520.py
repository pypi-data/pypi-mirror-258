"""BevelGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.part_model.gears import _2514
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import (
        _2516,
        _2544,
        _2546,
        _2548,
        _2554,
        _2524,
        _2532,
    )
    from mastapy.system_model.part_model import _2476, _2434, _2468
    from mastapy.system_model import _2203


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSet",)


Self = TypeVar("Self", bound="BevelGearSet")


class BevelGearSet(_2514.AGMAGleasonConicalGearSet):
    """BevelGearSet

    This is a mastapy class.
    """

    TYPE = _BEVEL_GEAR_SET
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_BevelGearSet")

    class _Cast_BevelGearSet:
        """Special nested class for casting BevelGearSet to subclasses."""

        def __init__(self: "BevelGearSet._Cast_BevelGearSet", parent: "BevelGearSet"):
            self._parent = parent

        @property
        def agma_gleason_conical_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2514.AGMAGleasonConicalGearSet":
            return self._parent._cast(_2514.AGMAGleasonConicalGearSet)

        @property
        def conical_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2524.ConicalGearSet":
            from mastapy.system_model.part_model.gears import _2524

            return self._parent._cast(_2524.ConicalGearSet)

        @property
        def gear_set(self: "BevelGearSet._Cast_BevelGearSet") -> "_2532.GearSet":
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.GearSet)

        @property
        def specialised_assembly(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2476.SpecialisedAssembly":
            from mastapy.system_model.part_model import _2476

            return self._parent._cast(_2476.SpecialisedAssembly)

        @property
        def abstract_assembly(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2434.AbstractAssembly":
            from mastapy.system_model.part_model import _2434

            return self._parent._cast(_2434.AbstractAssembly)

        @property
        def part(self: "BevelGearSet._Cast_BevelGearSet") -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def design_entity(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2203.DesignEntity":
            from mastapy.system_model import _2203

            return self._parent._cast(_2203.DesignEntity)

        @property
        def bevel_differential_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2516.BevelDifferentialGearSet":
            from mastapy.system_model.part_model.gears import _2516

            return self._parent._cast(_2516.BevelDifferentialGearSet)

        @property
        def spiral_bevel_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2544.SpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2544

            return self._parent._cast(_2544.SpiralBevelGearSet)

        @property
        def straight_bevel_diff_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2546.StraightBevelDiffGearSet":
            from mastapy.system_model.part_model.gears import _2546

            return self._parent._cast(_2546.StraightBevelDiffGearSet)

        @property
        def straight_bevel_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2548.StraightBevelGearSet":
            from mastapy.system_model.part_model.gears import _2548

            return self._parent._cast(_2548.StraightBevelGearSet)

        @property
        def zerol_bevel_gear_set(
            self: "BevelGearSet._Cast_BevelGearSet",
        ) -> "_2554.ZerolBevelGearSet":
            from mastapy.system_model.part_model.gears import _2554

            return self._parent._cast(_2554.ZerolBevelGearSet)

        @property
        def bevel_gear_set(self: "BevelGearSet._Cast_BevelGearSet") -> "BevelGearSet":
            return self._parent

        def __getattr__(self: "BevelGearSet._Cast_BevelGearSet", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "BevelGearSet.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "BevelGearSet._Cast_BevelGearSet":
        return self._Cast_BevelGearSet(self)
