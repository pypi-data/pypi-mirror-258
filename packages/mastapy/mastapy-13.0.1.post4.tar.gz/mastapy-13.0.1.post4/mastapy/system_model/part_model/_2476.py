"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.part_model import _2434
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model import _2443, _2454, _2468
    from mastapy.system_model.part_model.gears import (
        _2514,
        _2516,
        _2520,
        _2522,
        _2524,
        _2526,
        _2529,
        _2532,
        _2535,
        _2537,
        _2539,
        _2541,
        _2542,
        _2544,
        _2546,
        _2548,
        _2552,
        _2554,
    )
    from mastapy.system_model.part_model.cycloidal import _2568
    from mastapy.system_model.part_model.couplings import (
        _2576,
        _2578,
        _2581,
        _2583,
        _2586,
        _2588,
        _2597,
        _2600,
        _2602,
        _2607,
    )
    from mastapy.system_model import _2203


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


Self = TypeVar("Self", bound="SpecialisedAssembly")


class SpecialisedAssembly(_2434.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE = _SPECIALISED_ASSEMBLY
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_SpecialisedAssembly")

    class _Cast_SpecialisedAssembly:
        """Special nested class for casting SpecialisedAssembly to subclasses."""

        def __init__(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
            parent: "SpecialisedAssembly",
        ):
            self._parent = parent

        @property
        def abstract_assembly(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2434.AbstractAssembly":
            return self._parent._cast(_2434.AbstractAssembly)

        @property
        def part(self: "SpecialisedAssembly._Cast_SpecialisedAssembly") -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def design_entity(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2203.DesignEntity":
            from mastapy.system_model import _2203

            return self._parent._cast(_2203.DesignEntity)

        @property
        def bolted_joint(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2443.BoltedJoint":
            from mastapy.system_model.part_model import _2443

            return self._parent._cast(_2443.BoltedJoint)

        @property
        def flexible_pin_assembly(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2454.FlexiblePinAssembly":
            from mastapy.system_model.part_model import _2454

            return self._parent._cast(_2454.FlexiblePinAssembly)

        @property
        def agma_gleason_conical_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2514.AGMAGleasonConicalGearSet":
            from mastapy.system_model.part_model.gears import _2514

            return self._parent._cast(_2514.AGMAGleasonConicalGearSet)

        @property
        def bevel_differential_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2516.BevelDifferentialGearSet":
            from mastapy.system_model.part_model.gears import _2516

            return self._parent._cast(_2516.BevelDifferentialGearSet)

        @property
        def bevel_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2520.BevelGearSet":
            from mastapy.system_model.part_model.gears import _2520

            return self._parent._cast(_2520.BevelGearSet)

        @property
        def concept_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2522.ConceptGearSet":
            from mastapy.system_model.part_model.gears import _2522

            return self._parent._cast(_2522.ConceptGearSet)

        @property
        def conical_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2524.ConicalGearSet":
            from mastapy.system_model.part_model.gears import _2524

            return self._parent._cast(_2524.ConicalGearSet)

        @property
        def cylindrical_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2526.CylindricalGearSet":
            from mastapy.system_model.part_model.gears import _2526

            return self._parent._cast(_2526.CylindricalGearSet)

        @property
        def face_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2529.FaceGearSet":
            from mastapy.system_model.part_model.gears import _2529

            return self._parent._cast(_2529.FaceGearSet)

        @property
        def gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2532.GearSet":
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.GearSet)

        @property
        def hypoid_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2535.HypoidGearSet":
            from mastapy.system_model.part_model.gears import _2535

            return self._parent._cast(_2535.HypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2537.KlingelnbergCycloPalloidConicalGearSet":
            from mastapy.system_model.part_model.gears import _2537

            return self._parent._cast(_2537.KlingelnbergCycloPalloidConicalGearSet)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2539.KlingelnbergCycloPalloidHypoidGearSet":
            from mastapy.system_model.part_model.gears import _2539

            return self._parent._cast(_2539.KlingelnbergCycloPalloidHypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2541

            return self._parent._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearSet)

        @property
        def planetary_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2542.PlanetaryGearSet":
            from mastapy.system_model.part_model.gears import _2542

            return self._parent._cast(_2542.PlanetaryGearSet)

        @property
        def spiral_bevel_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2544.SpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2544

            return self._parent._cast(_2544.SpiralBevelGearSet)

        @property
        def straight_bevel_diff_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2546.StraightBevelDiffGearSet":
            from mastapy.system_model.part_model.gears import _2546

            return self._parent._cast(_2546.StraightBevelDiffGearSet)

        @property
        def straight_bevel_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2548.StraightBevelGearSet":
            from mastapy.system_model.part_model.gears import _2548

            return self._parent._cast(_2548.StraightBevelGearSet)

        @property
        def worm_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2552.WormGearSet":
            from mastapy.system_model.part_model.gears import _2552

            return self._parent._cast(_2552.WormGearSet)

        @property
        def zerol_bevel_gear_set(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2554.ZerolBevelGearSet":
            from mastapy.system_model.part_model.gears import _2554

            return self._parent._cast(_2554.ZerolBevelGearSet)

        @property
        def cycloidal_assembly(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2568.CycloidalAssembly":
            from mastapy.system_model.part_model.cycloidal import _2568

            return self._parent._cast(_2568.CycloidalAssembly)

        @property
        def belt_drive(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2576.BeltDrive":
            from mastapy.system_model.part_model.couplings import _2576

            return self._parent._cast(_2576.BeltDrive)

        @property
        def clutch(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2578.Clutch":
            from mastapy.system_model.part_model.couplings import _2578

            return self._parent._cast(_2578.Clutch)

        @property
        def concept_coupling(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2581.ConceptCoupling":
            from mastapy.system_model.part_model.couplings import _2581

            return self._parent._cast(_2581.ConceptCoupling)

        @property
        def coupling(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2583.Coupling":
            from mastapy.system_model.part_model.couplings import _2583

            return self._parent._cast(_2583.Coupling)

        @property
        def cvt(self: "SpecialisedAssembly._Cast_SpecialisedAssembly") -> "_2586.CVT":
            from mastapy.system_model.part_model.couplings import _2586

            return self._parent._cast(_2586.CVT)

        @property
        def part_to_part_shear_coupling(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2588.PartToPartShearCoupling":
            from mastapy.system_model.part_model.couplings import _2588

            return self._parent._cast(_2588.PartToPartShearCoupling)

        @property
        def rolling_ring_assembly(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2597.RollingRingAssembly":
            from mastapy.system_model.part_model.couplings import _2597

            return self._parent._cast(_2597.RollingRingAssembly)

        @property
        def spring_damper(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2600.SpringDamper":
            from mastapy.system_model.part_model.couplings import _2600

            return self._parent._cast(_2600.SpringDamper)

        @property
        def synchroniser(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2602.Synchroniser":
            from mastapy.system_model.part_model.couplings import _2602

            return self._parent._cast(_2602.Synchroniser)

        @property
        def torque_converter(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "_2607.TorqueConverter":
            from mastapy.system_model.part_model.couplings import _2607

            return self._parent._cast(_2607.TorqueConverter)

        @property
        def specialised_assembly(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly",
        ) -> "SpecialisedAssembly":
            return self._parent

        def __getattr__(
            self: "SpecialisedAssembly._Cast_SpecialisedAssembly", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "SpecialisedAssembly.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "SpecialisedAssembly._Cast_SpecialisedAssembly":
        return self._Cast_SpecialisedAssembly(self)
