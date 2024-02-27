"""CouplingHalfModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5194
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "CouplingHalfModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2584
    from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5138,
        _5143,
        _5158,
        _5198,
        _5205,
        _5210,
        _5220,
        _5230,
        _5232,
        _5233,
        _5236,
        _5237,
        _5141,
        _5196,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfModalAnalysisAtASpeed",)


Self = TypeVar("Self", bound="CouplingHalfModalAnalysisAtASpeed")


class CouplingHalfModalAnalysisAtASpeed(_5194.MountableComponentModalAnalysisAtASpeed):
    """CouplingHalfModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_MODAL_ANALYSIS_AT_A_SPEED
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfModalAnalysisAtASpeed")

    class _Cast_CouplingHalfModalAnalysisAtASpeed:
        """Special nested class for casting CouplingHalfModalAnalysisAtASpeed to subclasses."""

        def __init__(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
            parent: "CouplingHalfModalAnalysisAtASpeed",
        ):
            self._parent = parent

        @property
        def mountable_component_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5194.MountableComponentModalAnalysisAtASpeed":
            return self._parent._cast(_5194.MountableComponentModalAnalysisAtASpeed)

        @property
        def component_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5141.ComponentModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5141,
            )

            return self._parent._cast(_5141.ComponentModalAnalysisAtASpeed)

        @property
        def part_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5196.PartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5196,
            )

            return self._parent._cast(_5196.PartModalAnalysisAtASpeed)

        @property
        def part_static_load_analysis_case(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def clutch_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5138.ClutchHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5138,
            )

            return self._parent._cast(_5138.ClutchHalfModalAnalysisAtASpeed)

        @property
        def concept_coupling_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5143.ConceptCouplingHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5143,
            )

            return self._parent._cast(_5143.ConceptCouplingHalfModalAnalysisAtASpeed)

        @property
        def cvt_pulley_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5158.CVTPulleyModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5158,
            )

            return self._parent._cast(_5158.CVTPulleyModalAnalysisAtASpeed)

        @property
        def part_to_part_shear_coupling_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5198.PartToPartShearCouplingHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5198,
            )

            return self._parent._cast(
                _5198.PartToPartShearCouplingHalfModalAnalysisAtASpeed
            )

        @property
        def pulley_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5205.PulleyModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5205,
            )

            return self._parent._cast(_5205.PulleyModalAnalysisAtASpeed)

        @property
        def rolling_ring_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5210.RollingRingModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5210,
            )

            return self._parent._cast(_5210.RollingRingModalAnalysisAtASpeed)

        @property
        def spring_damper_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5220.SpringDamperHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5220,
            )

            return self._parent._cast(_5220.SpringDamperHalfModalAnalysisAtASpeed)

        @property
        def synchroniser_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5230.SynchroniserHalfModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5230,
            )

            return self._parent._cast(_5230.SynchroniserHalfModalAnalysisAtASpeed)

        @property
        def synchroniser_part_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5232.SynchroniserPartModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5232,
            )

            return self._parent._cast(_5232.SynchroniserPartModalAnalysisAtASpeed)

        @property
        def synchroniser_sleeve_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5233.SynchroniserSleeveModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5233,
            )

            return self._parent._cast(_5233.SynchroniserSleeveModalAnalysisAtASpeed)

        @property
        def torque_converter_pump_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5236.TorqueConverterPumpModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5236,
            )

            return self._parent._cast(_5236.TorqueConverterPumpModalAnalysisAtASpeed)

        @property
        def torque_converter_turbine_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "_5237.TorqueConverterTurbineModalAnalysisAtASpeed":
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5237,
            )

            return self._parent._cast(_5237.TorqueConverterTurbineModalAnalysisAtASpeed)

        @property
        def coupling_half_modal_analysis_at_a_speed(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
        ) -> "CouplingHalfModalAnalysisAtASpeed":
            return self._parent

        def __getattr__(
            self: "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed",
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
        self: Self, instance_to_wrap: "CouplingHalfModalAnalysisAtASpeed.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self: Self) -> "_2584.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

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
    ) -> "CouplingHalfModalAnalysisAtASpeed._Cast_CouplingHalfModalAnalysisAtASpeed":
        return self._Cast_CouplingHalfModalAnalysisAtASpeed(self)
