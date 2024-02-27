"""AbstractGearSetAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_ABSTRACT_GEAR_SET_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "AbstractGearSetAnalysis"
)

if TYPE_CHECKING:
    from mastapy.utility.model_validation import _1794, _1793
    from mastapy.gears.rating import _355, _362, _363
    from mastapy.gears.rating.zerol_bevel import _371
    from mastapy.gears.rating.worm import _375, _376
    from mastapy.gears.rating.straight_bevel import _397
    from mastapy.gears.rating.straight_bevel_diff import _400
    from mastapy.gears.rating.spiral_bevel import _404
    from mastapy.gears.rating.klingelnberg_spiral_bevel import _407
    from mastapy.gears.rating.klingelnberg_hypoid import _410
    from mastapy.gears.rating.klingelnberg_conical import _413
    from mastapy.gears.rating.hypoid import _440
    from mastapy.gears.rating.face import _449, _450
    from mastapy.gears.rating.cylindrical import _463, _464, _480
    from mastapy.gears.rating.conical import _541, _542
    from mastapy.gears.rating.concept import _552, _553
    from mastapy.gears.rating.bevel import _556
    from mastapy.gears.rating.agma_gleason_conical import _567
    from mastapy.gears.manufacturing.cylindrical import _620, _621, _625
    from mastapy.gears.manufacturing.bevel import _790, _791, _792, _793
    from mastapy.gears.ltca import _846
    from mastapy.gears.ltca.cylindrical import _860, _862
    from mastapy.gears.ltca.conical import _868
    from mastapy.gears.load_case import _874
    from mastapy.gears.load_case.worm import _877
    from mastapy.gears.load_case.face import _880
    from mastapy.gears.load_case.cylindrical import _883
    from mastapy.gears.load_case.conical import _886
    from mastapy.gears.load_case.concept import _889
    from mastapy.gears.load_case.bevel import _893
    from mastapy.gears.gear_two_d_fe_analysis import _896, _897
    from mastapy.gears.gear_designs.face import _996
    from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1107, _1108
    from mastapy.gears.fe_model import _1200
    from mastapy.gears.fe_model.cylindrical import _1203
    from mastapy.gears.fe_model.conical import _1206
    from mastapy.gears.analysis import _1226, _1228, _1229, _1230, _1231


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearSetAnalysis",)


Self = TypeVar("Self", bound="AbstractGearSetAnalysis")


class AbstractGearSetAnalysis(_0.APIBase):
    """AbstractGearSetAnalysis

    This is a mastapy class.
    """

    TYPE = _ABSTRACT_GEAR_SET_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_AbstractGearSetAnalysis")

    class _Cast_AbstractGearSetAnalysis:
        """Special nested class for casting AbstractGearSetAnalysis to subclasses."""

        def __init__(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
            parent: "AbstractGearSetAnalysis",
        ):
            self._parent = parent

        @property
        def abstract_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_355.AbstractGearSetRating":
            from mastapy.gears.rating import _355

            return self._parent._cast(_355.AbstractGearSetRating)

        @property
        def gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_362.GearSetDutyCycleRating":
            from mastapy.gears.rating import _362

            return self._parent._cast(_362.GearSetDutyCycleRating)

        @property
        def gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_363.GearSetRating":
            from mastapy.gears.rating import _363

            return self._parent._cast(_363.GearSetRating)

        @property
        def zerol_bevel_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_371.ZerolBevelGearSetRating":
            from mastapy.gears.rating.zerol_bevel import _371

            return self._parent._cast(_371.ZerolBevelGearSetRating)

        @property
        def worm_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_375.WormGearSetDutyCycleRating":
            from mastapy.gears.rating.worm import _375

            return self._parent._cast(_375.WormGearSetDutyCycleRating)

        @property
        def worm_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_376.WormGearSetRating":
            from mastapy.gears.rating.worm import _376

            return self._parent._cast(_376.WormGearSetRating)

        @property
        def straight_bevel_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_397.StraightBevelGearSetRating":
            from mastapy.gears.rating.straight_bevel import _397

            return self._parent._cast(_397.StraightBevelGearSetRating)

        @property
        def straight_bevel_diff_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_400.StraightBevelDiffGearSetRating":
            from mastapy.gears.rating.straight_bevel_diff import _400

            return self._parent._cast(_400.StraightBevelDiffGearSetRating)

        @property
        def spiral_bevel_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_404.SpiralBevelGearSetRating":
            from mastapy.gears.rating.spiral_bevel import _404

            return self._parent._cast(_404.SpiralBevelGearSetRating)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_407.KlingelnbergCycloPalloidSpiralBevelGearSetRating":
            from mastapy.gears.rating.klingelnberg_spiral_bevel import _407

            return self._parent._cast(
                _407.KlingelnbergCycloPalloidSpiralBevelGearSetRating
            )

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_410.KlingelnbergCycloPalloidHypoidGearSetRating":
            from mastapy.gears.rating.klingelnberg_hypoid import _410

            return self._parent._cast(_410.KlingelnbergCycloPalloidHypoidGearSetRating)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_413.KlingelnbergCycloPalloidConicalGearSetRating":
            from mastapy.gears.rating.klingelnberg_conical import _413

            return self._parent._cast(_413.KlingelnbergCycloPalloidConicalGearSetRating)

        @property
        def hypoid_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_440.HypoidGearSetRating":
            from mastapy.gears.rating.hypoid import _440

            return self._parent._cast(_440.HypoidGearSetRating)

        @property
        def face_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_449.FaceGearSetDutyCycleRating":
            from mastapy.gears.rating.face import _449

            return self._parent._cast(_449.FaceGearSetDutyCycleRating)

        @property
        def face_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_450.FaceGearSetRating":
            from mastapy.gears.rating.face import _450

            return self._parent._cast(_450.FaceGearSetRating)

        @property
        def cylindrical_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_463.CylindricalGearSetDutyCycleRating":
            from mastapy.gears.rating.cylindrical import _463

            return self._parent._cast(_463.CylindricalGearSetDutyCycleRating)

        @property
        def cylindrical_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_464.CylindricalGearSetRating":
            from mastapy.gears.rating.cylindrical import _464

            return self._parent._cast(_464.CylindricalGearSetRating)

        @property
        def reduced_cylindrical_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_480.ReducedCylindricalGearSetDutyCycleRating":
            from mastapy.gears.rating.cylindrical import _480

            return self._parent._cast(_480.ReducedCylindricalGearSetDutyCycleRating)

        @property
        def conical_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_541.ConicalGearSetDutyCycleRating":
            from mastapy.gears.rating.conical import _541

            return self._parent._cast(_541.ConicalGearSetDutyCycleRating)

        @property
        def conical_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_542.ConicalGearSetRating":
            from mastapy.gears.rating.conical import _542

            return self._parent._cast(_542.ConicalGearSetRating)

        @property
        def concept_gear_set_duty_cycle_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_552.ConceptGearSetDutyCycleRating":
            from mastapy.gears.rating.concept import _552

            return self._parent._cast(_552.ConceptGearSetDutyCycleRating)

        @property
        def concept_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_553.ConceptGearSetRating":
            from mastapy.gears.rating.concept import _553

            return self._parent._cast(_553.ConceptGearSetRating)

        @property
        def bevel_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_556.BevelGearSetRating":
            from mastapy.gears.rating.bevel import _556

            return self._parent._cast(_556.BevelGearSetRating)

        @property
        def agma_gleason_conical_gear_set_rating(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_567.AGMAGleasonConicalGearSetRating":
            from mastapy.gears.rating.agma_gleason_conical import _567

            return self._parent._cast(_567.AGMAGleasonConicalGearSetRating)

        @property
        def cylindrical_manufactured_gear_set_duty_cycle(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_620.CylindricalManufacturedGearSetDutyCycle":
            from mastapy.gears.manufacturing.cylindrical import _620

            return self._parent._cast(_620.CylindricalManufacturedGearSetDutyCycle)

        @property
        def cylindrical_manufactured_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_621.CylindricalManufacturedGearSetLoadCase":
            from mastapy.gears.manufacturing.cylindrical import _621

            return self._parent._cast(_621.CylindricalManufacturedGearSetLoadCase)

        @property
        def cylindrical_set_manufacturing_config(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_625.CylindricalSetManufacturingConfig":
            from mastapy.gears.manufacturing.cylindrical import _625

            return self._parent._cast(_625.CylindricalSetManufacturingConfig)

        @property
        def conical_set_manufacturing_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_790.ConicalSetManufacturingAnalysis":
            from mastapy.gears.manufacturing.bevel import _790

            return self._parent._cast(_790.ConicalSetManufacturingAnalysis)

        @property
        def conical_set_manufacturing_config(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_791.ConicalSetManufacturingConfig":
            from mastapy.gears.manufacturing.bevel import _791

            return self._parent._cast(_791.ConicalSetManufacturingConfig)

        @property
        def conical_set_micro_geometry_config(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_792.ConicalSetMicroGeometryConfig":
            from mastapy.gears.manufacturing.bevel import _792

            return self._parent._cast(_792.ConicalSetMicroGeometryConfig)

        @property
        def conical_set_micro_geometry_config_base(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_793.ConicalSetMicroGeometryConfigBase":
            from mastapy.gears.manufacturing.bevel import _793

            return self._parent._cast(_793.ConicalSetMicroGeometryConfigBase)

        @property
        def gear_set_load_distribution_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_846.GearSetLoadDistributionAnalysis":
            from mastapy.gears.ltca import _846

            return self._parent._cast(_846.GearSetLoadDistributionAnalysis)

        @property
        def cylindrical_gear_set_load_distribution_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_860.CylindricalGearSetLoadDistributionAnalysis":
            from mastapy.gears.ltca.cylindrical import _860

            return self._parent._cast(_860.CylindricalGearSetLoadDistributionAnalysis)

        @property
        def face_gear_set_load_distribution_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_862.FaceGearSetLoadDistributionAnalysis":
            from mastapy.gears.ltca.cylindrical import _862

            return self._parent._cast(_862.FaceGearSetLoadDistributionAnalysis)

        @property
        def conical_gear_set_load_distribution_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_868.ConicalGearSetLoadDistributionAnalysis":
            from mastapy.gears.ltca.conical import _868

            return self._parent._cast(_868.ConicalGearSetLoadDistributionAnalysis)

        @property
        def gear_set_load_case_base(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_874.GearSetLoadCaseBase":
            from mastapy.gears.load_case import _874

            return self._parent._cast(_874.GearSetLoadCaseBase)

        @property
        def worm_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_877.WormGearSetLoadCase":
            from mastapy.gears.load_case.worm import _877

            return self._parent._cast(_877.WormGearSetLoadCase)

        @property
        def face_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_880.FaceGearSetLoadCase":
            from mastapy.gears.load_case.face import _880

            return self._parent._cast(_880.FaceGearSetLoadCase)

        @property
        def cylindrical_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_883.CylindricalGearSetLoadCase":
            from mastapy.gears.load_case.cylindrical import _883

            return self._parent._cast(_883.CylindricalGearSetLoadCase)

        @property
        def conical_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_886.ConicalGearSetLoadCase":
            from mastapy.gears.load_case.conical import _886

            return self._parent._cast(_886.ConicalGearSetLoadCase)

        @property
        def concept_gear_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_889.ConceptGearSetLoadCase":
            from mastapy.gears.load_case.concept import _889

            return self._parent._cast(_889.ConceptGearSetLoadCase)

        @property
        def bevel_set_load_case(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_893.BevelSetLoadCase":
            from mastapy.gears.load_case.bevel import _893

            return self._parent._cast(_893.BevelSetLoadCase)

        @property
        def cylindrical_gear_set_tiff_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_896.CylindricalGearSetTIFFAnalysis":
            from mastapy.gears.gear_two_d_fe_analysis import _896

            return self._parent._cast(_896.CylindricalGearSetTIFFAnalysis)

        @property
        def cylindrical_gear_set_tiff_analysis_duty_cycle(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_897.CylindricalGearSetTIFFAnalysisDutyCycle":
            from mastapy.gears.gear_two_d_fe_analysis import _897

            return self._parent._cast(_897.CylindricalGearSetTIFFAnalysisDutyCycle)

        @property
        def face_gear_set_micro_geometry(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_996.FaceGearSetMicroGeometry":
            from mastapy.gears.gear_designs.face import _996

            return self._parent._cast(_996.FaceGearSetMicroGeometry)

        @property
        def cylindrical_gear_set_micro_geometry(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1107.CylindricalGearSetMicroGeometry":
            from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1107

            return self._parent._cast(_1107.CylindricalGearSetMicroGeometry)

        @property
        def cylindrical_gear_set_micro_geometry_duty_cycle(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1108.CylindricalGearSetMicroGeometryDutyCycle":
            from mastapy.gears.gear_designs.cylindrical.micro_geometry import _1108

            return self._parent._cast(_1108.CylindricalGearSetMicroGeometryDutyCycle)

        @property
        def gear_set_fe_model(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1200.GearSetFEModel":
            from mastapy.gears.fe_model import _1200

            return self._parent._cast(_1200.GearSetFEModel)

        @property
        def cylindrical_gear_set_fe_model(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1203.CylindricalGearSetFEModel":
            from mastapy.gears.fe_model.cylindrical import _1203

            return self._parent._cast(_1203.CylindricalGearSetFEModel)

        @property
        def conical_set_fe_model(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1206.ConicalSetFEModel":
            from mastapy.gears.fe_model.conical import _1206

            return self._parent._cast(_1206.ConicalSetFEModel)

        @property
        def gear_set_design_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1226.GearSetDesignAnalysis":
            from mastapy.gears.analysis import _1226

            return self._parent._cast(_1226.GearSetDesignAnalysis)

        @property
        def gear_set_implementation_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1228.GearSetImplementationAnalysis":
            from mastapy.gears.analysis import _1228

            return self._parent._cast(_1228.GearSetImplementationAnalysis)

        @property
        def gear_set_implementation_analysis_abstract(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1229.GearSetImplementationAnalysisAbstract":
            from mastapy.gears.analysis import _1229

            return self._parent._cast(_1229.GearSetImplementationAnalysisAbstract)

        @property
        def gear_set_implementation_analysis_duty_cycle(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1230.GearSetImplementationAnalysisDutyCycle":
            from mastapy.gears.analysis import _1230

            return self._parent._cast(_1230.GearSetImplementationAnalysisDutyCycle)

        @property
        def gear_set_implementation_detail(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "_1231.GearSetImplementationDetail":
            from mastapy.gears.analysis import _1231

            return self._parent._cast(_1231.GearSetImplementationDetail)

        @property
        def abstract_gear_set_analysis(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis",
        ) -> "AbstractGearSetAnalysis":
            return self._parent

        def __getattr__(
            self: "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis", name: str
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "AbstractGearSetAnalysis.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

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
    def all_status_errors(self: Self) -> "List[_1794.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AllStatusErrors

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: Self) -> "_1793.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Status

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
    def cast_to(self: Self) -> "AbstractGearSetAnalysis._Cast_AbstractGearSetAnalysis":
        return self._Cast_AbstractGearSetAnalysis(self)
