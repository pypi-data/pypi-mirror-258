"""CouplingCompoundPowerFlow"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _4265
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "CouplingCompoundPowerFlow",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.power_flows import _4071
    from mastapy.system_model.analyses_and_results.power_flows.compound import (
        _4188,
        _4193,
        _4247,
        _4269,
        _4284,
        _4167,
        _4246,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7546, _7543
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundPowerFlow",)


Self = TypeVar("Self", bound="CouplingCompoundPowerFlow")


class CouplingCompoundPowerFlow(_4265.SpecialisedAssemblyCompoundPowerFlow):
    """CouplingCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE = _COUPLING_COMPOUND_POWER_FLOW
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CouplingCompoundPowerFlow")

    class _Cast_CouplingCompoundPowerFlow:
        """Special nested class for casting CouplingCompoundPowerFlow to subclasses."""

        def __init__(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
            parent: "CouplingCompoundPowerFlow",
        ):
            self._parent = parent

        @property
        def specialised_assembly_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4265.SpecialisedAssemblyCompoundPowerFlow":
            return self._parent._cast(_4265.SpecialisedAssemblyCompoundPowerFlow)

        @property
        def abstract_assembly_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4167.AbstractAssemblyCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4167,
            )

            return self._parent._cast(_4167.AbstractAssemblyCompoundPowerFlow)

        @property
        def part_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4246.PartCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4246,
            )

            return self._parent._cast(_4246.PartCompoundPowerFlow)

        @property
        def part_compound_analysis(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_7546.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7546

            return self._parent._cast(_7546.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_7543.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7543

            return self._parent._cast(_7543.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def clutch_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4188.ClutchCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4188,
            )

            return self._parent._cast(_4188.ClutchCompoundPowerFlow)

        @property
        def concept_coupling_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4193.ConceptCouplingCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4193,
            )

            return self._parent._cast(_4193.ConceptCouplingCompoundPowerFlow)

        @property
        def part_to_part_shear_coupling_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4247.PartToPartShearCouplingCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4247,
            )

            return self._parent._cast(_4247.PartToPartShearCouplingCompoundPowerFlow)

        @property
        def spring_damper_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4269.SpringDamperCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4269,
            )

            return self._parent._cast(_4269.SpringDamperCompoundPowerFlow)

        @property
        def torque_converter_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "_4284.TorqueConverterCompoundPowerFlow":
            from mastapy.system_model.analyses_and_results.power_flows.compound import (
                _4284,
            )

            return self._parent._cast(_4284.TorqueConverterCompoundPowerFlow)

        @property
        def coupling_compound_power_flow(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow",
        ) -> "CouplingCompoundPowerFlow":
            return self._parent

        def __getattr__(
            self: "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CouplingCompoundPowerFlow.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(self: Self) -> "List[_4071.CouplingPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(self: Self) -> "List[_4071.CouplingPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AssemblyAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow":
        return self._Cast_CouplingCompoundPowerFlow(self)
