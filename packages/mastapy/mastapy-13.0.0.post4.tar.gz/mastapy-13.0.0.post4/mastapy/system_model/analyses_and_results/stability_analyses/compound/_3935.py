"""CouplingConnectionCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3962
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "CouplingConnectionCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.stability_analyses import _3800
    from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
        _3919,
        _3924,
        _3978,
        _4000,
        _4015,
        _3932,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7538, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundStabilityAnalysis",)


Self = TypeVar("Self", bound="CouplingConnectionCompoundStabilityAnalysis")


class CouplingConnectionCompoundStabilityAnalysis(
    _3962.InterMountableComponentConnectionCompoundStabilityAnalysis
):
    """CouplingConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_CONNECTION_COMPOUND_STABILITY_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CouplingConnectionCompoundStabilityAnalysis"
    )

    class _Cast_CouplingConnectionCompoundStabilityAnalysis:
        """Special nested class for casting CouplingConnectionCompoundStabilityAnalysis to subclasses."""

        def __init__(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
            parent: "CouplingConnectionCompoundStabilityAnalysis",
        ):
            self._parent = parent

        @property
        def inter_mountable_component_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_3962.InterMountableComponentConnectionCompoundStabilityAnalysis":
            return self._parent._cast(
                _3962.InterMountableComponentConnectionCompoundStabilityAnalysis
            )

        @property
        def connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_3932.ConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3932,
            )

            return self._parent._cast(_3932.ConnectionCompoundStabilityAnalysis)

        @property
        def connection_compound_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_7538.ConnectionCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7538

            return self._parent._cast(_7538.ConnectionCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def clutch_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_3919.ClutchConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3919,
            )

            return self._parent._cast(_3919.ClutchConnectionCompoundStabilityAnalysis)

        @property
        def concept_coupling_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_3924.ConceptCouplingConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3924,
            )

            return self._parent._cast(
                _3924.ConceptCouplingConnectionCompoundStabilityAnalysis
            )

        @property
        def part_to_part_shear_coupling_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_3978.PartToPartShearCouplingConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _3978,
            )

            return self._parent._cast(
                _3978.PartToPartShearCouplingConnectionCompoundStabilityAnalysis
            )

        @property
        def spring_damper_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_4000.SpringDamperConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4000,
            )

            return self._parent._cast(
                _4000.SpringDamperConnectionCompoundStabilityAnalysis
            )

        @property
        def torque_converter_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "_4015.TorqueConverterConnectionCompoundStabilityAnalysis":
            from mastapy.system_model.analyses_and_results.stability_analyses.compound import (
                _4015,
            )

            return self._parent._cast(
                _4015.TorqueConverterConnectionCompoundStabilityAnalysis
            )

        @property
        def coupling_connection_compound_stability_analysis(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
        ) -> "CouplingConnectionCompoundStabilityAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis",
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
        self: Self, instance_to_wrap: "CouplingConnectionCompoundStabilityAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_analysis_cases(
        self: Self,
    ) -> "List[_3800.CouplingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CouplingConnectionStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCases

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: Self,
    ) -> "List[_3800.CouplingConnectionStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CouplingConnectionStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ConnectionAnalysisCasesReady

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: Self,
    ) -> "CouplingConnectionCompoundStabilityAnalysis._Cast_CouplingConnectionCompoundStabilityAnalysis":
        return self._Cast_CouplingConnectionCompoundStabilityAnalysis(self)
