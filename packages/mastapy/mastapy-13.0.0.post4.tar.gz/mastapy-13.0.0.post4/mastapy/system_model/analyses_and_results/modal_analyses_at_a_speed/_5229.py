"""StraightBevelSunGearModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5223
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "StraightBevelSunGearModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.gears import _2550
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5133,
        _5121,
        _5149,
        _5175,
        _5194,
        _5141,
        _5196,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="StraightBevelSunGearModalAnalysisAtASpeed")


class StraightBevelSunGearModalAnalysisAtASpeed(
    _5223.StraightBevelDiffGearModalAnalysisAtASpeed
):
    """StraightBevelSunGearModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_StraightBevelSunGearModalAnalysisAtASpeed"
    )

    class _Cast_StraightBevelSunGearModalAnalysisAtASpeed:
        """Special nested class for casting StraightBevelSunGearModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
            parent: "StraightBevelSunGearModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def straight_bevel_diff_gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5223.StraightBevelDiffGearModalAnalysisAtASpeed":
            return self._parent._cast(_5223.StraightBevelDiffGearModalAnalysisAtASpeed)

        @property
        def bevel_gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5133.BevelGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5133,
            )

            return self._parent._cast(_5133.BevelGearModalAnalysisAtASpeed)

        @property
        def agma_gleason_conical_gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5121.AGMAGleasonConicalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5121,
            )

            return self._parent._cast(_5121.AGMAGleasonConicalGearModalAnalysisAtASpeed)

        @property
        def conical_gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5149.ConicalGearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5149,
            )

            return self._parent._cast(_5149.ConicalGearModalAnalysisAtASpeed)

        @property
        def gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5175.GearModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5175,
            )

            return self._parent._cast(_5175.GearModalAnalysisAtASpeed)

        @property
        def mountable_component_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5194.MountableComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5194,
            )

            return self._parent._cast(_5194.MountableComponentModalAnalysisAtASpeed)

        @property
        def component_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5141.ComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5141,
            )

            return self._parent._cast(_5141.ComponentModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_5196.PartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5196,
            )

            return self._parent._cast(_5196.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def straight_bevel_sun_gear_modal_analysis_at_a_speed(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
        ) -> "StraightBevelSunGearModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed",
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
        self: Self, instance_to_wrap: "StraightBevelSunGearModalAnalysisAtASpeed.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2550.StraightBevelSunGear":
        """mastapy.system_model.part_model.gears.StraightBevelSunGear

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
    ) -> "StraightBevelSunGearModalAnalysisAtASpeed._Cast_StraightBevelSunGearModalAnalysisAtASpeed":
        return self._Cast_StraightBevelSunGearModalAnalysisAtASpeed(self)
