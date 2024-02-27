"""CouplingCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal import conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5626
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_COUPLING_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CouplingCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.mbd_analyses import _5417
    from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
        _5549,
        _5554,
        _5608,
        _5630,
        _5645,
        _5528,
        _5607,
    )
    from mastapy.system_model.analyses_and_results.analysis_cases import _7545, _7542
    from mastapy.system_model.analyses_and_results import _2651


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundMultibodyDynamicsAnalysis",)


Self = TypeVar("Self", bound="CouplingCompoundMultibodyDynamicsAnalysis")


class CouplingCompoundMultibodyDynamicsAnalysis(
    _5626.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
):
    """CouplingCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE = _COUPLING_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    _CastSelf = TypeVar(
        "_CastSelf", bound="_Cast_CouplingCompoundMultibodyDynamicsAnalysis"
    )

    class _Cast_CouplingCompoundMultibodyDynamicsAnalysis:
        """Special nested class for casting CouplingCompoundMultibodyDynamicsAnalysis to subclasses."""

        def __init__(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
            parent: "CouplingCompoundMultibodyDynamicsAnalysis",
        ):
            self._parent = parent

        @property
        def specialised_assembly_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5626.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis":
            return self._parent._cast(
                _5626.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
            )

        @property
        def abstract_assembly_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5528.AbstractAssemblyCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5528,
            )

            return self._parent._cast(
                _5528.AbstractAssemblyCompoundMultibodyDynamicsAnalysis
            )

        @property
        def part_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5607.PartCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5607,
            )

            return self._parent._cast(_5607.PartCompoundMultibodyDynamicsAnalysis)

        @property
        def part_compound_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_7545.PartCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7545

            return self._parent._cast(_7545.PartCompoundAnalysis)

        @property
        def design_entity_compound_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_7542.DesignEntityCompoundAnalysis":
            from mastapy.system_model.analyses_and_results.analysis_cases import _7542

            return self._parent._cast(_7542.DesignEntityCompoundAnalysis)

        @property
        def design_entity_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_2651.DesignEntityAnalysis":
            from mastapy.system_model.analyses_and_results import _2651

            return self._parent._cast(_2651.DesignEntityAnalysis)

        @property
        def clutch_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5549.ClutchCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5549,
            )

            return self._parent._cast(_5549.ClutchCompoundMultibodyDynamicsAnalysis)

        @property
        def concept_coupling_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5554.ConceptCouplingCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5554,
            )

            return self._parent._cast(
                _5554.ConceptCouplingCompoundMultibodyDynamicsAnalysis
            )

        @property
        def part_to_part_shear_coupling_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5608.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5608,
            )

            return self._parent._cast(
                _5608.PartToPartShearCouplingCompoundMultibodyDynamicsAnalysis
            )

        @property
        def spring_damper_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5630.SpringDamperCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5630,
            )

            return self._parent._cast(
                _5630.SpringDamperCompoundMultibodyDynamicsAnalysis
            )

        @property
        def torque_converter_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "_5645.TorqueConverterCompoundMultibodyDynamicsAnalysis":
            from mastapy.system_model.analyses_and_results.mbd_analyses.compound import (
                _5645,
            )

            return self._parent._cast(
                _5645.TorqueConverterCompoundMultibodyDynamicsAnalysis
            )

        @property
        def coupling_compound_multibody_dynamics_analysis(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
        ) -> "CouplingCompoundMultibodyDynamicsAnalysis":
            return self._parent

        def __getattr__(
            self: "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis",
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
        self: Self, instance_to_wrap: "CouplingCompoundMultibodyDynamicsAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_analysis_cases(
        self: Self,
    ) -> "List[_5417.CouplingMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingMultibodyDynamicsAnalysis]

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
    def assembly_analysis_cases_ready(
        self: Self,
    ) -> "List[_5417.CouplingMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingMultibodyDynamicsAnalysis]

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
    ) -> "CouplingCompoundMultibodyDynamicsAnalysis._Cast_CouplingCompoundMultibodyDynamicsAnalysis":
        return self._Cast_CouplingCompoundMultibodyDynamicsAnalysis(self)
