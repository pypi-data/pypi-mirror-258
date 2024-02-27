"""ConicalGearCompoundModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _4785
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ConicalGearCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.modal_analyses import _4604
    from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
        _4731,
        _4738,
        _4741,
        _4742,
        _4743,
        _4789,
        _4793,
        _4796,
        _4799,
        _4826,
        _4832,
        _4835,
        _4838,
        _4839,
        _4853,
        _4804,
        _4752,
        _4806,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearCompoundModalAnalysis",)


Self = TypeVar("Self", bound="ConicalGearCompoundModalAnalysis")


class ConicalGearCompoundModalAnalysis(_4785.GearCompoundModalAnalysis):
    """ConicalGearCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE = _CONICAL_GEAR_COMPOUND_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_ConicalGearCompoundModalAnalysis")

    class _Cast_ConicalGearCompoundModalAnalysis:
        """Special nested class for casting ConicalGearCompoundModalAnalysis to subclasses."""

        def __init__(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
            parent: "ConicalGearCompoundModalAnalysis",
        ):
            self._parent = parent

        @property
        def gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4785.GearCompoundModalAnalysis":
            return self._parent._cast(_4785.GearCompoundModalAnalysis)

        @property
        def mountable_component_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4804.MountableComponentCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4804,
            )

            return self._parent._cast(_4804.MountableComponentCompoundModalAnalysis)

        @property
        def component_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4752.ComponentCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4752,
            )

            return self._parent._cast(_4752.ComponentCompoundModalAnalysis)

        @property
        def part_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4806.PartCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4806,
            )

            return self._parent._cast(_4806.PartCompoundModalAnalysis)

        @property
        def part_compound_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def agma_gleason_conical_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4731.AGMAGleasonConicalGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4731,
            )

            return self._parent._cast(_4731.AGMAGleasonConicalGearCompoundModalAnalysis)

        @property
        def bevel_differential_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4738.BevelDifferentialGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4738,
            )

            return self._parent._cast(_4738.BevelDifferentialGearCompoundModalAnalysis)

        @property
        def bevel_differential_planet_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4741.BevelDifferentialPlanetGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4741,
            )

            return self._parent._cast(
                _4741.BevelDifferentialPlanetGearCompoundModalAnalysis
            )

        @property
        def bevel_differential_sun_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4742.BevelDifferentialSunGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4742,
            )

            return self._parent._cast(
                _4742.BevelDifferentialSunGearCompoundModalAnalysis
            )

        @property
        def bevel_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4743.BevelGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4743,
            )

            return self._parent._cast(_4743.BevelGearCompoundModalAnalysis)

        @property
        def hypoid_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4789.HypoidGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4789,
            )

            return self._parent._cast(_4789.HypoidGearCompoundModalAnalysis)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4793.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4793,
            )

            return self._parent._cast(
                _4793.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4796.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4796,
            )

            return self._parent._cast(
                _4796.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysis
            )

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4799.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4799,
            )

            return self._parent._cast(
                _4799.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysis
            )

        @property
        def spiral_bevel_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4826.SpiralBevelGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4826,
            )

            return self._parent._cast(_4826.SpiralBevelGearCompoundModalAnalysis)

        @property
        def straight_bevel_diff_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4832.StraightBevelDiffGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4832,
            )

            return self._parent._cast(_4832.StraightBevelDiffGearCompoundModalAnalysis)

        @property
        def straight_bevel_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4835.StraightBevelGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4835,
            )

            return self._parent._cast(_4835.StraightBevelGearCompoundModalAnalysis)

        @property
        def straight_bevel_planet_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4838.StraightBevelPlanetGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4838,
            )

            return self._parent._cast(
                _4838.StraightBevelPlanetGearCompoundModalAnalysis
            )

        @property
        def straight_bevel_sun_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4839.StraightBevelSunGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4839,
            )

            return self._parent._cast(_4839.StraightBevelSunGearCompoundModalAnalysis)

        @property
        def zerol_bevel_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "_4853.ZerolBevelGearCompoundModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses.compound import (
                _4853,
            )

            return self._parent._cast(_4853.ZerolBevelGearCompoundModalAnalysis)

        @property
        def conical_gear_compound_modal_analysis(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
        ) -> "ConicalGearCompoundModalAnalysis":
            return self._parent

        def __getattr__(
            self: "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "ConicalGearCompoundModalAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def planetaries(self: Self) -> "List[ConicalGearCompoundModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.compound.ConicalGearCompoundModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Planetaries

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(self: Self) -> "List[_4604.ConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis]

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
    ) -> "List[_4604.ConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis]

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
    ) -> "ConicalGearCompoundModalAnalysis._Cast_ConicalGearCompoundModalAnalysis":
        return self._Cast_ConicalGearCompoundModalAnalysis(self)
