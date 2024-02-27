"""CouplingHalfModalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.modal_analyses import _4657
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "CouplingHalfModalAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.part_model.couplings import _2584
    from mastapy.system_model.analyses_and_results.system_deflections import _2730
    from mastapy.system_model.analyses_and_results.modal_analyses import (
        _4593,
        _4598,
        _4614,
        _4663,
        _4670,
        _4675,
        _4686,
        _4696,
        _4698,
        _4699,
        _4702,
        _4703,
        _4596,
        _4661,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7547, _7544
    from mastapy.system_model.analyses_and_results import _2657, _2653, _2651


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfModalAnalysis",)


Self = TypeVar("Self", bound="CouplingHalfModalAnalysis")


class CouplingHalfModalAnalysis(_4657.MountableComponentModalAnalysis):
    """CouplingHalfModalAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_HALF_MODAL_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingHalfModalAnalysis")

    class _Cast_CouplingHalfModalAnalysis:
        """Special nested class for casting CouplingHalfModalAnalysis to subclasses."""

        def __init__(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
            parent: "CouplingHalfModalAnalysis",
        ):
            self._parent = parent

        @property
        def mountable_component_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4657.MountableComponentModalAnalysis":
            return self._parent._cast(_4657.MountableComponentModalAnalysis)

        @property
        def component_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4596.ComponentModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4596

            return self._parent._cast(_4596.ComponentModalAnalysis)

        @property
        def part_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4661.PartModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4661

            return self._parent._cast(_4661.PartModalAnalysis)

        @property
        def part_static_load_analysis_case(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_7547.PartStaticLoadAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7547

            return self._parent._cast(_7547.PartStaticLoadAnalysisCase)

        @property
        def part_analysis_case(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_7544.PartAnalysisCase":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.PartAnalysisCase)

        @property
        def part_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_2657.PartAnalysis":
            from mastapy.system_model.analyses_and_results import _2657

            return self._parent._cast(_2657.PartAnalysis)

        @property
        def design_entity_single_context_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_2653.DesignEntitySingleContextAnalysis":
            from mastapy.system_model.analyses_and_results import _2653

            return self._parent._cast(_2653.DesignEntitySingleContextAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def clutch_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4593.ClutchHalfModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4593

            return self._parent._cast(_4593.ClutchHalfModalAnalysis)

        @property
        def concept_coupling_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4598.ConceptCouplingHalfModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4598

            return self._parent._cast(_4598.ConceptCouplingHalfModalAnalysis)

        @property
        def cvt_pulley_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4614.CVTPulleyModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4614

            return self._parent._cast(_4614.CVTPulleyModalAnalysis)

        @property
        def part_to_part_shear_coupling_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4663.PartToPartShearCouplingHalfModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4663

            return self._parent._cast(_4663.PartToPartShearCouplingHalfModalAnalysis)

        @property
        def pulley_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4670.PulleyModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4670

            return self._parent._cast(_4670.PulleyModalAnalysis)

        @property
        def rolling_ring_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4675.RollingRingModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4675

            return self._parent._cast(_4675.RollingRingModalAnalysis)

        @property
        def spring_damper_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4686.SpringDamperHalfModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4686

            return self._parent._cast(_4686.SpringDamperHalfModalAnalysis)

        @property
        def synchroniser_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4696.SynchroniserHalfModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4696

            return self._parent._cast(_4696.SynchroniserHalfModalAnalysis)

        @property
        def synchroniser_part_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4698.SynchroniserPartModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4698

            return self._parent._cast(_4698.SynchroniserPartModalAnalysis)

        @property
        def synchroniser_sleeve_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4699.SynchroniserSleeveModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4699

            return self._parent._cast(_4699.SynchroniserSleeveModalAnalysis)

        @property
        def torque_converter_pump_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4702.TorqueConverterPumpModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4702

            return self._parent._cast(_4702.TorqueConverterPumpModalAnalysis)

        @property
        def torque_converter_turbine_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "_4703.TorqueConverterTurbineModalAnalysis":
            from mastapy.system_model.analyses_and_results.modal_analyses import _4703

            return self._parent._cast(_4703.TorqueConverterTurbineModalAnalysis)

        @property
        def coupling_half_modal_analysis(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis",
        ) -> "CouplingHalfModalAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingHalfModalAnalysis.TYPE"):
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
    def system_deflection_results(self: Self) -> "_2730.CouplingHalfSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SystemDeflectionResults

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingHalfModalAnalysis._Cast_CouplingHalfModalAnalysis":
        return self._Cast_CouplingHalfModalAnalysis(self)
