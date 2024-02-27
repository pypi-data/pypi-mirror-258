"""AbstractGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.gears.analysis import _1215
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearRating"
)

if TYPE_CHECKING:
    from mastapy.gears.rating import _358, _361
    from mastapy.gears.rating.zerol_bevel import _370
    from mastapy.gears.rating.worm import _372, _374
    from mastapy.gears.rating.straight_bevel import _396
    from mastapy.gears.rating.straight_bevel_diff import _399
    from mastapy.gears.rating.spiral_bevel import _403
    from mastapy.gears.rating.klingelnberg_spiral_bevel import _406
    from mastapy.gears.rating.klingelnberg_hypoid import _409
    from mastapy.gears.rating.klingelnberg_conical import _412
    from mastapy.gears.rating.hypoid import _439
    from mastapy.gears.rating.face import _445, _448
    from mastapy.gears.rating.cylindrical import _455, _460
    from mastapy.gears.rating.conical import _538, _540
    from mastapy.gears.rating.concept import _548, _551
    from mastapy.gears.rating.bevel import _555
    from mastapy.gears.rating.agma_gleason_conical import _566


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearRating",)


Self = TypeVar("Self", bound="AbstractGearRating")


class AbstractGearRating(_1215.AbstractGearAnalysis):
    """AbstractGearRating

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_GEAR_RATING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AbstractGearRating")

    class _Cast_AbstractGearRating:
        """Special nested class for casting AbstractGearRating to subclasses."""

        def __init__(
            self: "AbstractGearRating._Cast_AbstractGearRating",
            parent: "AbstractGearRating",
        ):
            self._parent = parent

        @property
        def abstract_gear_analysis(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_1215.AbstractGearAnalysis":
            return self._parent._cast(_1215.AbstractGearAnalysis)

        @property
        def gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_358.GearDutyCycleRating":
            from mastapy.gears.rating import _358

            return self._parent._cast(_358.GearDutyCycleRating)

        @property
        def gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_361.GearRating":
            from mastapy.gears.rating import _361

            return self._parent._cast(_361.GearRating)

        @property
        def zerol_bevel_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_370.ZerolBevelGearRating":
            from mastapy.gears.rating.zerol_bevel import _370

            return self._parent._cast(_370.ZerolBevelGearRating)

        @property
        def worm_gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_372.WormGearDutyCycleRating":
            from mastapy.gears.rating.worm import _372

            return self._parent._cast(_372.WormGearDutyCycleRating)

        @property
        def worm_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_374.WormGearRating":
            from mastapy.gears.rating.worm import _374

            return self._parent._cast(_374.WormGearRating)

        @property
        def straight_bevel_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_396.StraightBevelGearRating":
            from mastapy.gears.rating.straight_bevel import _396

            return self._parent._cast(_396.StraightBevelGearRating)

        @property
        def straight_bevel_diff_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_399.StraightBevelDiffGearRating":
            from mastapy.gears.rating.straight_bevel_diff import _399

            return self._parent._cast(_399.StraightBevelDiffGearRating)

        @property
        def spiral_bevel_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_403.SpiralBevelGearRating":
            from mastapy.gears.rating.spiral_bevel import _403

            return self._parent._cast(_403.SpiralBevelGearRating)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_406.KlingelnbergCycloPalloidSpiralBevelGearRating":
            from mastapy.gears.rating.klingelnberg_spiral_bevel import _406

            return self._parent._cast(
                _406.KlingelnbergCycloPalloidSpiralBevelGearRating
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_409.KlingelnbergCycloPalloidHypoidGearRating":
            from mastapy.gears.rating.klingelnberg_hypoid import _409

            return self._parent._cast(_409.KlingelnbergCycloPalloidHypoidGearRating)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_412.KlingelnbergCycloPalloidConicalGearRating":
            from mastapy.gears.rating.klingelnberg_conical import _412

            return self._parent._cast(_412.KlingelnbergCycloPalloidConicalGearRating)

        @property
        def hypoid_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_439.HypoidGearRating":
            from mastapy.gears.rating.hypoid import _439

            return self._parent._cast(_439.HypoidGearRating)

        @property
        def face_gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_445.FaceGearDutyCycleRating":
            from mastapy.gears.rating.face import _445

            return self._parent._cast(_445.FaceGearDutyCycleRating)

        @property
        def face_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_448.FaceGearRating":
            from mastapy.gears.rating.face import _448

            return self._parent._cast(_448.FaceGearRating)

        @property
        def cylindrical_gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_455.CylindricalGearDutyCycleRating":
            from mastapy.gears.rating.cylindrical import _455

            return self._parent._cast(_455.CylindricalGearDutyCycleRating)

        @property
        def cylindrical_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_460.CylindricalGearRating":
            from mastapy.gears.rating.cylindrical import _460

            return self._parent._cast(_460.CylindricalGearRating)

        @property
        def conical_gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_538.ConicalGearDutyCycleRating":
            from mastapy.gears.rating.conical import _538

            return self._parent._cast(_538.ConicalGearDutyCycleRating)

        @property
        def conical_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_540.ConicalGearRating":
            from mastapy.gears.rating.conical import _540

            return self._parent._cast(_540.ConicalGearRating)

        @property
        def concept_gear_duty_cycle_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_548.ConceptGearDutyCycleRating":
            from mastapy.gears.rating.concept import _548

            return self._parent._cast(_548.ConceptGearDutyCycleRating)

        @property
        def concept_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_551.ConceptGearRating":
            from mastapy.gears.rating.concept import _551

            return self._parent._cast(_551.ConceptGearRating)

        @property
        def bevel_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_555.BevelGearRating":
            from mastapy.gears.rating.bevel import _555

            return self._parent._cast(_555.BevelGearRating)

        @property
        def agma_gleason_conical_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "_566.AGMAGleasonConicalGearRating":
            from mastapy.gears.rating.agma_gleason_conical import _566

            return self._parent._cast(_566.AGMAGleasonConicalGearRating)

        @property
        def abstract_gear_rating(
            self: "AbstractGearRating._Cast_AbstractGearRating",
        ) -> "AbstractGearRating":
            return self._parent

        def __getattr__(self: "AbstractGearRating._Cast_AbstractGearRating", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AbstractGearRating.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def bending_safety_factor_for_fatigue(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.BendingSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def bending_safety_factor_for_static(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.BendingSafetyFactorForStatic

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_fatigue(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ContactSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_safety_factor_for_static(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ContactSafetyFactorForStatic

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.CyclesToFail

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_bending(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.CyclesToFailBending

        if temp is None:
            return 0.0

        return temp

    @property
    def cycles_to_fail_contact(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.CyclesToFailContact

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_bending(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DamageBending

        if temp is None:
            return 0.0

        return temp

    @property
    def damage_contact(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DamageContact

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_bending(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.GearReliabilityBending

        if temp is None:
            return 0.0

        return temp

    @property
    def gear_reliability_contact(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.GearReliabilityContact

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_bending_safety_factor_for_fatigue(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedBendingSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_bending_safety_factor_for_static(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedBendingSafetyFactorForStatic

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_contact_safety_factor_for_fatigue(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedContactSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_contact_safety_factor_for_static(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedContactSafetyFactorForStatic

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_safety_factor_for_fatigue(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedSafetyFactorForFatigue

        if temp is None:
            return 0.0

        return temp

    @property
    def normalized_safety_factor_for_static(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NormalizedSafetyFactorForStatic

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TimeToFail

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_bending(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TimeToFailBending

        if temp is None:
            return 0.0

        return temp

    @property
    def time_to_fail_contact(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TimeToFailContact

        if temp is None:
            return 0.0

        return temp

    @property
    def total_gear_reliability(self: Self) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = self.wrapped.TotalGearReliability

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: Self) -> "AbstractGearRating._Cast_AbstractGearRating":
        return self._Cast_AbstractGearRating(self)
