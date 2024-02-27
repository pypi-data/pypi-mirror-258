"""ConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2532
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)

if TYPE_CHECKING:
    from mastapy.gears.gear_designs.conical import _1156
    from mastapy.system_model.part_model.gears import (
        _2523,
        _2514,
        _2516,
        _2520,
        _2535,
        _2537,
        _2539,
        _2541,
        _2544,
        _2546,
        _2548,
        _2554,
    )
    from mastapy.system_model.part_model import _2476, _2434, _2468
    from mastapy.system_model import _2203


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSet",)


Self = TypeVar("Self", bound="ConicalGearSet")


class ConicalGearSet(_2532.GearSet):
    """ConicalGearSet

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_SET
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConicalGearSet")

    class _Cast_ConicalGearSet:
        """Special nested class for casting ConicalGearSet to subclasses."""

        def __init__(
            self: "ConicalGearSet._Cast_ConicalGearSet", parent: "ConicalGearSet"
        ):
            self._parent = parent

        @property
        def gear_set(self: "ConicalGearSet._Cast_ConicalGearSet") -> "_2532.GearSet":
            return self._parent._cast(_2532.GearSet)

        @property
        def specialised_assembly(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2476.SpecialisedAssembly":
            from mastapy.system_model.part_model import _2476

            return self._parent._cast(_2476.SpecialisedAssembly)

        @property
        def abstract_assembly(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2434.AbstractAssembly":
            from mastapy.system_model.part_model import _2434

            return self._parent._cast(_2434.AbstractAssembly)

        @property
        def part(self: "ConicalGearSet._Cast_ConicalGearSet") -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def design_entity(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2203.DesignEntity":
            from mastapy.system_model import _2203

            return self._parent._cast(_2203.DesignEntity)

        @property
        def agma_gleason_conical_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2514.AGMAGleasonConicalGearSet":
            from mastapy.system_model.part_model.gears import _2514

            return self._parent._cast(_2514.AGMAGleasonConicalGearSet)

        @property
        def bevel_differential_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2516.BevelDifferentialGearSet":
            from mastapy.system_model.part_model.gears import _2516

            return self._parent._cast(_2516.BevelDifferentialGearSet)

        @property
        def bevel_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2520.BevelGearSet":
            from mastapy.system_model.part_model.gears import _2520

            return self._parent._cast(_2520.BevelGearSet)

        @property
        def hypoid_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2535.HypoidGearSet":
            from mastapy.system_model.part_model.gears import _2535

            return self._parent._cast(_2535.HypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2537.KlingelnbergCycloPalloidConicalGearSet":
            from mastapy.system_model.part_model.gears import _2537

            return self._parent._cast(_2537.KlingelnbergCycloPalloidConicalGearSet)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2539.KlingelnbergCycloPalloidHypoidGearSet":
            from mastapy.system_model.part_model.gears import _2539

            return self._parent._cast(_2539.KlingelnbergCycloPalloidHypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2541

            return self._parent._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearSet)

        @property
        def spiral_bevel_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2544.SpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2544

            return self._parent._cast(_2544.SpiralBevelGearSet)

        @property
        def straight_bevel_diff_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2546.StraightBevelDiffGearSet":
            from mastapy.system_model.part_model.gears import _2546

            return self._parent._cast(_2546.StraightBevelDiffGearSet)

        @property
        def straight_bevel_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2548.StraightBevelGearSet":
            from mastapy.system_model.part_model.gears import _2548

            return self._parent._cast(_2548.StraightBevelGearSet)

        @property
        def zerol_bevel_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "_2554.ZerolBevelGearSet":
            from mastapy.system_model.part_model.gears import _2554

            return self._parent._cast(_2554.ZerolBevelGearSet)

        @property
        def conical_gear_set(
            self: "ConicalGearSet._Cast_ConicalGearSet",
        ) -> "ConicalGearSet":
            return self._parent

        def __getattr__(self: "ConicalGearSet._Cast_ConicalGearSet", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ConicalGearSet.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def active_gear_set_design(self: Self) -> "_1156.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ActiveGearSetDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_set_design(self: Self) -> "_1156.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConicalGearSetDesign

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears(self: Self) -> "List[_2523.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConicalGears

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: Self) -> "ConicalGearSet._Cast_ConicalGearSet":
        return self._Cast_ConicalGearSet(self)
