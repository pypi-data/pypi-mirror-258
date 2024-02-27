"""AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3666,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3510,
    )
    from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3645,
        _3648,
        _3649,
        _3650,
        _3696,
        _3733,
        _3739,
        _3742,
        _3745,
        _3746,
        _3760,
        _3692,
        _3711,
        _3659,
        _3713,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",)


Self = TypeVar(
    "Self", bound="AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed"
)


class AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed(
    _3666.ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed
):
    """AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE = (
        _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
    )

    class _Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed:
        """Special nested class for casting AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
            parent: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ):
            self._parent = parent

        @property
        def conical_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3666.ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed":
            return self._parent._cast(
                _3666.ConicalGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3692.GearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3692,
            )

            return self._parent._cast(
                _3692.GearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def mountable_component_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3711.MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3711,
            )

            return self._parent._cast(
                _3711.MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def component_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3659.ComponentCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3659,
            )

            return self._parent._cast(
                _3659.ComponentCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3713.PartCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3713,
            )

            return self._parent._cast(
                _3713.PartCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def part_compound_analysis(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> (
            "_3645.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3645,
            )

            return self._parent._cast(
                _3645.BevelDifferentialGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def bevel_differential_planet_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3648.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3648,
            )

            return self._parent._cast(
                _3648.BevelDifferentialPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def bevel_differential_sun_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3649.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3649,
            )

            return self._parent._cast(
                _3649.BevelDifferentialSunGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def bevel_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3650.BevelGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3650,
            )

            return self._parent._cast(
                _3650.BevelGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def hypoid_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3696.HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3696,
            )

            return self._parent._cast(
                _3696.HypoidGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def spiral_bevel_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3733.SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3733,
            )

            return self._parent._cast(
                _3733.SpiralBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def straight_bevel_diff_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> (
            "_3739.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed"
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3739,
            )

            return self._parent._cast(
                _3739.StraightBevelDiffGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def straight_bevel_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3742.StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3742,
            )

            return self._parent._cast(
                _3742.StraightBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def straight_bevel_planet_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3745.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3745,
            )

            return self._parent._cast(
                _3745.StraightBevelPlanetGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def straight_bevel_sun_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3746.StraightBevelSunGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3746,
            )

            return self._parent._cast(
                _3746.StraightBevelSunGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def zerol_bevel_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "_3760.ZerolBevelGearCompoundSteadyStateSynchronousResponseAtASpeed":
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
                _3760,
            )

            return self._parent._cast(
                _3760.ZerolBevelGearCompoundSteadyStateSynchronousResponseAtASpeed
            )

        @property
        def agma_gleason_conical_gear_compound_steady_state_synchronous_response_at_a_speed(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
        ) -> "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed",
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
        self: Self,
        instance_to_wrap: "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_3510.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: Self,
    ) -> "List[_3510.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ComponentAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed":
        return self._Cast_AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponseAtASpeed(
            self
        )
