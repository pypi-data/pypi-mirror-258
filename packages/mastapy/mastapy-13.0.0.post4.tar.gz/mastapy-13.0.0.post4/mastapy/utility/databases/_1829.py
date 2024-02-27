"""NamedDatabaseItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_NAMED_DATABASE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "NamedDatabaseItem"
)

if TYPE_CHECKING:
    from mastapy.utility import _1582
    from mastapy.utility.databases import _1830
    from mastapy.shafts import _24, _40, _43
    from mastapy.nodal_analysis import _50
    from mastapy.materials import _245, _267, _269, _273
    from mastapy.gears import _342
    from mastapy.gears.rating.cylindrical import _454, _470
    from mastapy.gears.materials import (
        _583,
        _585,
        _587,
        _591,
        _594,
        _597,
        _598,
        _601,
        _603,
        _606,
    )
    from mastapy.gears.manufacturing.cylindrical.cutters import (
        _706,
        _707,
        _708,
        _709,
        _710,
        _712,
        _713,
        _714,
        _715,
        _718,
    )
    from mastapy.gears.manufacturing.bevel import _799
    from mastapy.gears.gear_designs import _941, _943, _946
    from mastapy.gears.gear_designs.cylindrical import _1014, _1022
    from mastapy.electric_machines import _1282, _1300, _1313
    from mastapy.detailed_rigid_connectors.splines import _1415
    from mastapy.cycloidal import _1455, _1462
    from mastapy.bolts import _1465, _1467, _1469
    from mastapy.math_utility.optimisation import _1549
    from mastapy.bearings import _1881
    from mastapy.bearings.bearing_results.rolling import _1974
    from mastapy.system_model.optimization import _2226, _2229, _2234, _2235
    from mastapy.system_model.part_model.gears.supercharger_rotor_set import _2563


__docformat__ = "restructuredtext en"
__all__ = ("NamedDatabaseItem",)


Self = TypeVar("Self", bound="NamedDatabaseItem")


class NamedDatabaseItem(_0.APIBase):
    """NamedDatabaseItem

    This is a mastapy class.
    """

    TYPE = _NAMED_DATABASE_ITEM
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_NamedDatabaseItem")

    class _Cast_NamedDatabaseItem:
        """Special nested class for casting NamedDatabaseItem to subclasses."""

        def __init__(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
            parent: "NamedDatabaseItem",
        ):
            self._parent = parent

        @property
        def shaft_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_24.ShaftMaterial":
            from mastapy.shafts import _24

            return self._parent._cast(_24.ShaftMaterial)

        @property
        def shaft_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_40.ShaftSettingsItem":
            from mastapy.shafts import _40

            return self._parent._cast(_40.ShaftSettingsItem)

        @property
        def simple_shaft_definition(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_43.SimpleShaftDefinition":
            from mastapy.shafts import _43

            return self._parent._cast(_43.SimpleShaftDefinition)

        @property
        def analysis_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_50.AnalysisSettingsItem":
            from mastapy.nodal_analysis import _50

            return self._parent._cast(_50.AnalysisSettingsItem)

        @property
        def bearing_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_245.BearingMaterial":
            from mastapy.materials import _245

            return self._parent._cast(_245.BearingMaterial)

        @property
        def lubrication_detail(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_267.LubricationDetail":
            from mastapy.materials import _267

            return self._parent._cast(_267.LubricationDetail)

        @property
        def material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_269.Material":
            from mastapy.materials import _269

            return self._parent._cast(_269.Material)

        @property
        def materials_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_273.MaterialsSettingsItem":
            from mastapy.materials import _273

            return self._parent._cast(_273.MaterialsSettingsItem)

        @property
        def pocketing_power_loss_coefficients(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_342.PocketingPowerLossCoefficients":
            from mastapy.gears import _342

            return self._parent._cast(_342.PocketingPowerLossCoefficients)

        @property
        def cylindrical_gear_design_and_rating_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_454.CylindricalGearDesignAndRatingSettingsItem":
            from mastapy.gears.rating.cylindrical import _454

            return self._parent._cast(_454.CylindricalGearDesignAndRatingSettingsItem)

        @property
        def cylindrical_plastic_gear_rating_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_470.CylindricalPlasticGearRatingSettingsItem":
            from mastapy.gears.rating.cylindrical import _470

            return self._parent._cast(_470.CylindricalPlasticGearRatingSettingsItem)

        @property
        def agma_cylindrical_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_583.AGMACylindricalGearMaterial":
            from mastapy.gears.materials import _583

            return self._parent._cast(_583.AGMACylindricalGearMaterial)

        @property
        def bevel_gear_iso_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_585.BevelGearISOMaterial":
            from mastapy.gears.materials import _585

            return self._parent._cast(_585.BevelGearISOMaterial)

        @property
        def bevel_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_587.BevelGearMaterial":
            from mastapy.gears.materials import _587

            return self._parent._cast(_587.BevelGearMaterial)

        @property
        def cylindrical_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_591.CylindricalGearMaterial":
            from mastapy.gears.materials import _591

            return self._parent._cast(_591.CylindricalGearMaterial)

        @property
        def gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_594.GearMaterial":
            from mastapy.gears.materials import _594

            return self._parent._cast(_594.GearMaterial)

        @property
        def iso_cylindrical_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_597.ISOCylindricalGearMaterial":
            from mastapy.gears.materials import _597

            return self._parent._cast(_597.ISOCylindricalGearMaterial)

        @property
        def isotr1417912001_coefficient_of_friction_constants(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_598.ISOTR1417912001CoefficientOfFrictionConstants":
            from mastapy.gears.materials import _598

            return self._parent._cast(
                _598.ISOTR1417912001CoefficientOfFrictionConstants
            )

        @property
        def klingelnberg_cyclo_palloid_conical_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_601.KlingelnbergCycloPalloidConicalGearMaterial":
            from mastapy.gears.materials import _601

            return self._parent._cast(_601.KlingelnbergCycloPalloidConicalGearMaterial)

        @property
        def plastic_cylindrical_gear_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_603.PlasticCylindricalGearMaterial":
            from mastapy.gears.materials import _603

            return self._parent._cast(_603.PlasticCylindricalGearMaterial)

        @property
        def raw_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_606.RawMaterial":
            from mastapy.gears.materials import _606

            return self._parent._cast(_606.RawMaterial)

        @property
        def cylindrical_gear_abstract_cutter_design(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_706.CylindricalGearAbstractCutterDesign":
            from mastapy.gears.manufacturing.cylindrical.cutters import _706

            return self._parent._cast(_706.CylindricalGearAbstractCutterDesign)

        @property
        def cylindrical_gear_form_grinding_wheel(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_707.CylindricalGearFormGrindingWheel":
            from mastapy.gears.manufacturing.cylindrical.cutters import _707

            return self._parent._cast(_707.CylindricalGearFormGrindingWheel)

        @property
        def cylindrical_gear_grinding_worm(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_708.CylindricalGearGrindingWorm":
            from mastapy.gears.manufacturing.cylindrical.cutters import _708

            return self._parent._cast(_708.CylindricalGearGrindingWorm)

        @property
        def cylindrical_gear_hob_design(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_709.CylindricalGearHobDesign":
            from mastapy.gears.manufacturing.cylindrical.cutters import _709

            return self._parent._cast(_709.CylindricalGearHobDesign)

        @property
        def cylindrical_gear_plunge_shaver(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_710.CylindricalGearPlungeShaver":
            from mastapy.gears.manufacturing.cylindrical.cutters import _710

            return self._parent._cast(_710.CylindricalGearPlungeShaver)

        @property
        def cylindrical_gear_rack_design(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_712.CylindricalGearRackDesign":
            from mastapy.gears.manufacturing.cylindrical.cutters import _712

            return self._parent._cast(_712.CylindricalGearRackDesign)

        @property
        def cylindrical_gear_real_cutter_design(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_713.CylindricalGearRealCutterDesign":
            from mastapy.gears.manufacturing.cylindrical.cutters import _713

            return self._parent._cast(_713.CylindricalGearRealCutterDesign)

        @property
        def cylindrical_gear_shaper(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_714.CylindricalGearShaper":
            from mastapy.gears.manufacturing.cylindrical.cutters import _714

            return self._parent._cast(_714.CylindricalGearShaper)

        @property
        def cylindrical_gear_shaver(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_715.CylindricalGearShaver":
            from mastapy.gears.manufacturing.cylindrical.cutters import _715

            return self._parent._cast(_715.CylindricalGearShaver)

        @property
        def involute_cutter_design(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_718.InvoluteCutterDesign":
            from mastapy.gears.manufacturing.cylindrical.cutters import _718

            return self._parent._cast(_718.InvoluteCutterDesign)

        @property
        def manufacturing_machine(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_799.ManufacturingMachine":
            from mastapy.gears.manufacturing.bevel import _799

            return self._parent._cast(_799.ManufacturingMachine)

        @property
        def bevel_hypoid_gear_design_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_941.BevelHypoidGearDesignSettingsItem":
            from mastapy.gears.gear_designs import _941

            return self._parent._cast(_941.BevelHypoidGearDesignSettingsItem)

        @property
        def bevel_hypoid_gear_rating_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_943.BevelHypoidGearRatingSettingsItem":
            from mastapy.gears.gear_designs import _943

            return self._parent._cast(_943.BevelHypoidGearRatingSettingsItem)

        @property
        def design_constraints_collection(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_946.DesignConstraintsCollection":
            from mastapy.gears.gear_designs import _946

            return self._parent._cast(_946.DesignConstraintsCollection)

        @property
        def cylindrical_gear_design_constraints(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1014.CylindricalGearDesignConstraints":
            from mastapy.gears.gear_designs.cylindrical import _1014

            return self._parent._cast(_1014.CylindricalGearDesignConstraints)

        @property
        def cylindrical_gear_micro_geometry_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1022.CylindricalGearMicroGeometrySettingsItem":
            from mastapy.gears.gear_designs.cylindrical import _1022

            return self._parent._cast(_1022.CylindricalGearMicroGeometrySettingsItem)

        @property
        def magnet_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1282.MagnetMaterial":
            from mastapy.electric_machines import _1282

            return self._parent._cast(_1282.MagnetMaterial)

        @property
        def stator_rotor_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1300.StatorRotorMaterial":
            from mastapy.electric_machines import _1300

            return self._parent._cast(_1300.StatorRotorMaterial)

        @property
        def winding_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1313.WindingMaterial":
            from mastapy.electric_machines import _1313

            return self._parent._cast(_1313.WindingMaterial)

        @property
        def spline_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1415.SplineMaterial":
            from mastapy.detailed_rigid_connectors.splines import _1415

            return self._parent._cast(_1415.SplineMaterial)

        @property
        def cycloidal_disc_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1455.CycloidalDiscMaterial":
            from mastapy.cycloidal import _1455

            return self._parent._cast(_1455.CycloidalDiscMaterial)

        @property
        def ring_pins_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1462.RingPinsMaterial":
            from mastapy.cycloidal import _1462

            return self._parent._cast(_1462.RingPinsMaterial)

        @property
        def bolted_joint_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1465.BoltedJointMaterial":
            from mastapy.bolts import _1465

            return self._parent._cast(_1465.BoltedJointMaterial)

        @property
        def bolt_geometry(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1467.BoltGeometry":
            from mastapy.bolts import _1467

            return self._parent._cast(_1467.BoltGeometry)

        @property
        def bolt_material(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1469.BoltMaterial":
            from mastapy.bolts import _1469

            return self._parent._cast(_1469.BoltMaterial)

        @property
        def pareto_optimisation_strategy(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1549.ParetoOptimisationStrategy":
            from mastapy.math_utility.optimisation import _1549

            return self._parent._cast(_1549.ParetoOptimisationStrategy)

        @property
        def bearing_settings_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1881.BearingSettingsItem":
            from mastapy.bearings import _1881

            return self._parent._cast(_1881.BearingSettingsItem)

        @property
        def iso14179_settings(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_1974.ISO14179Settings":
            from mastapy.bearings.bearing_results.rolling import _1974

            return self._parent._cast(_1974.ISO14179Settings)

        @property
        def conical_gear_optimisation_strategy(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_2226.ConicalGearOptimisationStrategy":
            from mastapy.system_model.optimization import _2226

            return self._parent._cast(_2226.ConicalGearOptimisationStrategy)

        @property
        def cylindrical_gear_optimisation_strategy(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_2229.CylindricalGearOptimisationStrategy":
            from mastapy.system_model.optimization import _2229

            return self._parent._cast(_2229.CylindricalGearOptimisationStrategy)

        @property
        def optimization_strategy(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_2234.OptimizationStrategy":
            from mastapy.system_model.optimization import _2234

            return self._parent._cast(_2234.OptimizationStrategy)

        @property
        def optimization_strategy_base(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_2235.OptimizationStrategyBase":
            from mastapy.system_model.optimization import _2235

            return self._parent._cast(_2235.OptimizationStrategyBase)

        @property
        def supercharger_rotor_set(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "_2563.SuperchargerRotorSet":
            from mastapy.system_model.part_model.gears.supercharger_rotor_set import (
                _2563,
            )

            return self._parent._cast(_2563.SuperchargerRotorSet)

        @property
        def named_database_item(
            self: "NamedDatabaseItem._Cast_NamedDatabaseItem",
        ) -> "NamedDatabaseItem":
            return self._parent

        def __getattr__(self: "NamedDatabaseItem._Cast_NamedDatabaseItem", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "NamedDatabaseItem.TYPE"):
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
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Name

        if temp is None:
            return ""

        return temp

    @property
    def no_history(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.NoHistory

        if temp is None:
            return ""

        return temp

    @property
    def history(self: Self) -> "_1582.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = self.wrapped.History

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def database_key(self: Self) -> "_1830.NamedKey":
        """mastapy.utility.databases.NamedKey"""
        temp = self.wrapped.DatabaseKey

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @database_key.setter
    @enforce_parameter_types
    def database_key(self: Self, value: "_1830.NamedKey"):
        self.wrapped.DatabaseKey = value.wrapped

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
    def cast_to(self: Self) -> "NamedDatabaseItem._Cast_NamedDatabaseItem":
        return self._Cast_NamedDatabaseItem(self)
