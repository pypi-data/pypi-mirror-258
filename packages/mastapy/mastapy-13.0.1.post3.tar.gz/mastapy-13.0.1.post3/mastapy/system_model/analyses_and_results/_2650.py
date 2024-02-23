"""Context"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CONTEXT = python_net_import("SMT.MastaAPI.SystemModel.AnalysesAndResults", "Context")

if TYPE_CHECKING:
    from mastapy.utility import _1583
    from mastapy.system_model import _2200


__docformat__ = "restructuredtext en"
__all__ = ("Context",)


Self = TypeVar("Self", bound="Context")


class Context(_0.APIBase):
    """Context

    This is a mastapy class.
    """

    TYPE = _CONTEXT
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_Context")

    class _Cast_Context:
        """Special nested class for casting Context to subclasses."""

        def __init__(self: "Context._Cast_Context", parent: "Context"):
            self._parent = parent

        @property
        def system_deflection(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2825,
            )

            return self._parent._cast(_2825.SystemDeflection)

        @property
        def torsional_system_deflection(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.system_deflections import (
                _2832,
            )

            return self._parent._cast(_2832.TorsionalSystemDeflection)

        @property
        def dynamic_model_for_steady_state_synchronous_response(
            self: "Context._Cast_Context",
        ):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3035,
            )

            return self._parent._cast(
                _3035.DynamicModelForSteadyStateSynchronousResponse
            )

        @property
        def steady_state_synchronous_response(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import (
                _3089,
            )

            return self._parent._cast(_3089.SteadyStateSynchronousResponse)

        @property
        def steady_state_synchronous_response_on_a_shaft(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
                _3350,
            )

            return self._parent._cast(_3350.SteadyStateSynchronousResponseOnAShaft)

        @property
        def steady_state_synchronous_response_at_a_speed(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
                _3609,
            )

            return self._parent._cast(_3609.SteadyStateSynchronousResponseAtASpeed)

        @property
        def dynamic_model_for_stability_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3816,
            )

            return self._parent._cast(_3816.DynamicModelForStabilityAnalysis)

        @property
        def stability_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.stability_analyses import (
                _3870,
            )

            return self._parent._cast(_3870.StabilityAnalysis)

        @property
        def power_flow(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.power_flows import _4122

            return self._parent._cast(_4122.PowerFlow)

        @property
        def parametric_study_static_load(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4387,
            )

            return self._parent._cast(_4387.ParametricStudyStaticLoad)

        @property
        def parametric_study_tool(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.parametric_study_tools import (
                _4388,
            )

            return self._parent._cast(_4388.ParametricStudyTool)

        @property
        def dynamic_model_for_modal_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4625

            return self._parent._cast(_4625.DynamicModelForModalAnalysis)

        @property
        def modal_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.modal_analyses import _4654

            return self._parent._cast(_4654.ModalAnalysis)

        @property
        def dynamic_model_at_a_stiffness(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4909,
            )

            return self._parent._cast(_4909.DynamicModelAtAStiffness)

        @property
        def modal_analysis_at_a_stiffness(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
                _4935,
            )

            return self._parent._cast(_4935.ModalAnalysisAtAStiffness)

        @property
        def modal_analysis_at_a_speed(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import (
                _5194,
            )

            return self._parent._cast(_5194.ModalAnalysisAtASpeed)

        @property
        def multibody_dynamics_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.mbd_analyses import _5465

            return self._parent._cast(_5465.MultibodyDynamicsAnalysis)

        @property
        def dynamic_model_for_harmonic_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5732,
            )

            return self._parent._cast(_5732.DynamicModelForHarmonicAnalysis)

        @property
        def harmonic_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5761,
            )

            return self._parent._cast(_5761.HarmonicAnalysis)

        @property
        def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
            self: "Context._Cast_Context",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5765,
            )

            return self._parent._cast(
                _5765.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
            )

        @property
        def harmonic_analysis_with_varying_stiffness_static_load_case(
            self: "Context._Cast_Context",
        ):
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5770,
            )

            return self._parent._cast(
                _5770.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
            )

        @property
        def harmonic_analysis_of_single_excitation(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6070,
            )

            return self._parent._cast(_6070.HarmonicAnalysisOfSingleExcitation)

        @property
        def modal_analysis_for_harmonic_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
                _6086,
            )

            return self._parent._cast(_6086.ModalAnalysisForHarmonicAnalysis)

        @property
        def dynamic_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.dynamic_analyses import _6329

            return self._parent._cast(_6329.DynamicAnalysis)

        @property
        def critical_speed_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.critical_speed_analyses import (
                _6583,
            )

            return self._parent._cast(_6583.CriticalSpeedAnalysis)

        @property
        def load_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.static_loads import _6804

            return self._parent._cast(_6804.LoadCase)

        @property
        def static_load_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.static_loads import _6805

            return self._parent._cast(_6805.StaticLoadCase)

        @property
        def time_series_load_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.static_loads import _6806

            return self._parent._cast(_6806.TimeSeriesLoadCase)

        @property
        def advanced_time_stepping_analysis_for_modulation_static_load_case(
            self: "Context._Cast_Context",
        ):
            from mastapy.system_model.analyses_and_results.static_loads import _6812

            return self._parent._cast(
                _6812.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
            )

        @property
        def advanced_time_stepping_analysis_for_modulation(
            self: "Context._Cast_Context",
        ):
            from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
                _7010,
            )

            return self._parent._cast(_7010.AdvancedTimeSteppingAnalysisForModulation)

        @property
        def advanced_system_deflection(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7274,
            )

            return self._parent._cast(_7274.AdvancedSystemDeflection)

        @property
        def advanced_system_deflection_sub_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
                _7276,
            )

            return self._parent._cast(_7276.AdvancedSystemDeflectionSubAnalysis)

        @property
        def analysis_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7535

            return self._parent._cast(_7535.AnalysisCase)

        @property
        def compound_analysis_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7537

            return self._parent._cast(_7537.CompoundAnalysisCase)

        @property
        def fe_analysis(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7544

            return self._parent._cast(_7544.FEAnalysis)

        @property
        def static_load_analysis_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7550

            return self._parent._cast(_7550.StaticLoadAnalysisCase)

        @property
        def time_series_load_analysis_case(self: "Context._Cast_Context"):
            from mastapy.system_model.analyses_and_results.analysis_cases import _7551

            return self._parent._cast(_7551.TimeSeriesLoadAnalysisCase)

        @property
        def context(self: "Context._Cast_Context") -> "Context":
            return self._parent

        def __getattr__(self: "Context._Cast_Context", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "Context.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def comment(self: Self) -> "str":
        """str"""
        temp = self.wrapped.Comment

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: Self, value: "str"):
        self.wrapped.Comment = str(value) if value is not None else ""

    @property
    def name(self: Self) -> "str":
        """str"""
        temp = self.wrapped.Name

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: Self, value: "str"):
        self.wrapped.Name = str(value) if value is not None else ""

    @property
    def save_history_information(self: Self) -> "_1583.FileHistoryItem":
        """mastapy.utility.FileHistoryItem

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SaveHistoryInformation

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def design_properties(self: Self) -> "_2200.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = self.wrapped.DesignProperties

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: Self) -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ReportNames

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else "")

    def get_default_report_with_encoded_images(self: Self) -> "str":
        """str"""
        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else "")

    @enforce_parameter_types
    def output_active_report_as_text_to(self: Self, file_path: "str"):
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else "")

    def get_active_report_with_encoded_images(self: Self) -> "str":
        """str"""
        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    @enforce_parameter_types
    def output_named_report_to(self: Self, report_name: "str", file_path: "str"):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: Self, report_name: "str", file_path: "str"
    ):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: Self, report_name: "str", file_path: "str"
    ):
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(
            report_name if report_name else "", file_path if file_path else ""
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: Self, report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(
            report_name if report_name else ""
        )
        return method_result

    @property
    def cast_to(self: Self) -> "Context._Cast_Context":
        return self._Cast_Context(self)
