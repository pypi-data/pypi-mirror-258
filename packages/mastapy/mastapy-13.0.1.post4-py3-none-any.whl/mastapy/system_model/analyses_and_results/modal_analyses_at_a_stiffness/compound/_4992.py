"""AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5020,
)
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4862,
    )
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _4999,
        _5002,
        _5003,
        _5004,
        _5050,
        _5087,
        _5093,
        _5096,
        _5099,
        _5100,
        _5114,
        _5046,
        _5065,
        _5013,
        _5067,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",)


Self = TypeVar("Self", bound="AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness")


class AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness(
    _5020.ConicalGearCompoundModalAnalysisAtAStiffness
):
    """AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    _CastSelf = TypeVar(
        "_CastSelf",
        bound="_Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
    )

    class _Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness:
        """Special nested class for casting AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness to subclasses."""

        def __init__(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
            parent: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ):
            self._parent = parent

        @property
        def conical_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5020.ConicalGearCompoundModalAnalysisAtAStiffness":
            return self._parent._cast(
                _5020.ConicalGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5046.GearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5046,
            )

            return self._parent._cast(_5046.GearCompoundModalAnalysisAtAStiffness)

        @property
        def mountable_component_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5065.MountableComponentCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5065,
            )

            return self._parent._cast(
                _5065.MountableComponentCompoundModalAnalysisAtAStiffness
            )

        @property
        def component_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5013.ComponentCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5013,
            )

            return self._parent._cast(_5013.ComponentCompoundModalAnalysisAtAStiffness)

        @property
        def part_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5067.PartCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5067,
            )

            return self._parent._cast(_5067.PartCompoundModalAnalysisAtAStiffness)

        @property
        def part_compound_analysis(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def bevel_differential_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_4999.BevelDifferentialGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _4999,
            )

            return self._parent._cast(
                _4999.BevelDifferentialGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def bevel_differential_planet_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5002.BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5002,
            )

            return self._parent._cast(
                _5002.BevelDifferentialPlanetGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def bevel_differential_sun_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5003.BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5003,
            )

            return self._parent._cast(
                _5003.BevelDifferentialSunGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def bevel_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5004.BevelGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5004,
            )

            return self._parent._cast(_5004.BevelGearCompoundModalAnalysisAtAStiffness)

        @property
        def hypoid_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5050.HypoidGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5050,
            )

            return self._parent._cast(_5050.HypoidGearCompoundModalAnalysisAtAStiffness)

        @property
        def spiral_bevel_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5087.SpiralBevelGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5087,
            )

            return self._parent._cast(
                _5087.SpiralBevelGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def straight_bevel_diff_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5093.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5093,
            )

            return self._parent._cast(
                _5093.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def straight_bevel_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5096.StraightBevelGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5096,
            )

            return self._parent._cast(
                _5096.StraightBevelGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def straight_bevel_planet_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5099.StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5099,
            )

            return self._parent._cast(
                _5099.StraightBevelPlanetGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def straight_bevel_sun_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5100.StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5100,
            )

            return self._parent._cast(
                _5100.StraightBevelSunGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def zerol_bevel_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "_5114.ZerolBevelGearCompoundModalAnalysisAtAStiffness":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
                _5114,
            )

            return self._parent._cast(
                _5114.ZerolBevelGearCompoundModalAnalysisAtAStiffness
            )

        @property
        def agma_gleason_conical_gear_compound_modal_analysis_at_a_stiffness(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
        ) -> "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
            return self._parent

        def __getattr__(
            self: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness",
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
        instance_to_wrap: "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness.TYPE",
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_analysis_cases(
        self: Self,
    ) -> "List[_4862.AGMAGleasonConicalGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.AGMAGleasonConicalGearModalAnalysisAtAStiffness]

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
    ) -> "List[_4862.AGMAGleasonConicalGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.AGMAGleasonConicalGearModalAnalysisAtAStiffness]

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
    ) -> "AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
        return self._Cast_AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness(self)
