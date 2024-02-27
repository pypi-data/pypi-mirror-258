"""IndependentReportablePropertiesBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_INDEPENDENT_REPORTABLE_PROPERTIES_BASE = python_net_import(
    "SMT.MastaAPI.Utility", "IndependentReportablePropertiesBase"
)

if TYPE_CHECKING:
    from mastapy.materials.efficiency import _298
    from mastapy.geometry import _309
    from mastapy.gears import _346
    from mastapy.gears.gear_designs.cylindrical import (
        _1020,
        _1051,
        _1059,
        _1060,
        _1063,
        _1070,
        _1078,
        _1080,
        _1084,
        _1088,
    )
    from mastapy.electric_machines import _1260
    from mastapy.electric_machines.load_cases_and_analyses import _1376
    from mastapy.math_utility.measured_data import _1566, _1567, _1568
    from mastapy.bearings.tolerances import _1918
    from mastapy.bearings.bearing_results import _1945
    from mastapy.bearings.bearing_results.rolling import _1976, _2070
    from mastapy.system_model.analyses_and_results.static_loads import _6810


__docformat__ = "restructuredtext en"
__all__ = ("IndependentReportablePropertiesBase",)


Self = TypeVar("Self", bound="IndependentReportablePropertiesBase")
T = TypeVar("T", bound="IndependentReportablePropertiesBase")


class IndependentReportablePropertiesBase(_0.APIBase, Generic[T]):
    """IndependentReportablePropertiesBase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE = _INDEPENDENT_REPORTABLE_PROPERTIES_BASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_IndependentReportablePropertiesBase")

    class _Cast_IndependentReportablePropertiesBase:
        """Special nested class for casting IndependentReportablePropertiesBase to subclasses."""

        def __init__(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
            parent: "IndependentReportablePropertiesBase",
        ):
            self._parent = parent

        @property
        def oil_pump_detail(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_298.OilPumpDetail":
            from mastapy.materials.efficiency import _298

            return self._parent._cast(_298.OilPumpDetail)

        @property
        def packaging_limits(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_309.PackagingLimits":
            from mastapy.geometry import _309

            return self._parent._cast(_309.PackagingLimits)

        @property
        def specification_for_the_effect_of_oil_kinematic_viscosity(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_346.SpecificationForTheEffectOfOilKinematicViscosity":
            from mastapy.gears import _346

            return self._parent._cast(
                _346.SpecificationForTheEffectOfOilKinematicViscosity
            )

        @property
        def cylindrical_gear_micro_geometry_settings(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1020.CylindricalGearMicroGeometrySettings":
            from mastapy.gears.gear_designs.cylindrical import _1020

            return self._parent._cast(_1020.CylindricalGearMicroGeometrySettings)

        @property
        def hardened_material_properties(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1051.HardenedMaterialProperties":
            from mastapy.gears.gear_designs.cylindrical import _1051

            return self._parent._cast(_1051.HardenedMaterialProperties)

        @property
        def ltca_load_case_modifiable_settings(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1059.LTCALoadCaseModifiableSettings":
            from mastapy.gears.gear_designs.cylindrical import _1059

            return self._parent._cast(_1059.LTCALoadCaseModifiableSettings)

        @property
        def ltca_settings(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1060.LTCASettings":
            from mastapy.gears.gear_designs.cylindrical import _1060

            return self._parent._cast(_1060.LTCASettings)

        @property
        def micropitting(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1063.Micropitting":
            from mastapy.gears.gear_designs.cylindrical import _1063

            return self._parent._cast(_1063.Micropitting)

        @property
        def scuffing(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1070.Scuffing":
            from mastapy.gears.gear_designs.cylindrical import _1070

            return self._parent._cast(_1070.Scuffing)

        @property
        def surface_roughness(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1078.SurfaceRoughness":
            from mastapy.gears.gear_designs.cylindrical import _1078

            return self._parent._cast(_1078.SurfaceRoughness)

        @property
        def tiff_analysis_settings(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1080.TiffAnalysisSettings":
            from mastapy.gears.gear_designs.cylindrical import _1080

            return self._parent._cast(_1080.TiffAnalysisSettings)

        @property
        def tooth_flank_fracture_analysis_settings(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1084.ToothFlankFractureAnalysisSettings":
            from mastapy.gears.gear_designs.cylindrical import _1084

            return self._parent._cast(_1084.ToothFlankFractureAnalysisSettings)

        @property
        def usage(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1088.Usage":
            from mastapy.gears.gear_designs.cylindrical import _1088

            return self._parent._cast(_1088.Usage)

        @property
        def eccentricity(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1260.Eccentricity":
            from mastapy.electric_machines import _1260

            return self._parent._cast(_1260.Eccentricity)

        @property
        def temperatures(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1376.Temperatures":
            from mastapy.electric_machines.load_cases_and_analyses import _1376

            return self._parent._cast(_1376.Temperatures)

        @property
        def lookup_table_base(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1566.LookupTableBase":
            from mastapy.math_utility.measured_data import _1566

            return self._parent._cast(_1566.LookupTableBase)

        @property
        def onedimensional_function_lookup_table(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1567.OnedimensionalFunctionLookupTable":
            from mastapy.math_utility.measured_data import _1567

            return self._parent._cast(_1567.OnedimensionalFunctionLookupTable)

        @property
        def twodimensional_function_lookup_table(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1568.TwodimensionalFunctionLookupTable":
            from mastapy.math_utility.measured_data import _1568

            return self._parent._cast(_1568.TwodimensionalFunctionLookupTable)

        @property
        def roundness_specification(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1918.RoundnessSpecification":
            from mastapy.bearings.tolerances import _1918

            return self._parent._cast(_1918.RoundnessSpecification)

        @property
        def equivalent_load_factors(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1945.EquivalentLoadFactors":
            from mastapy.bearings.bearing_results import _1945

            return self._parent._cast(_1945.EquivalentLoadFactors)

        @property
        def iso14179_settings_per_bearing_type(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_1976.ISO14179SettingsPerBearingType":
            from mastapy.bearings.bearing_results.rolling import _1976

            return self._parent._cast(_1976.ISO14179SettingsPerBearingType)

        @property
        def rolling_bearing_friction_coefficients(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_2070.RollingBearingFrictionCoefficients":
            from mastapy.bearings.bearing_results.rolling import _2070

            return self._parent._cast(_2070.RollingBearingFrictionCoefficients)

        @property
        def additional_acceleration_options(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "_6810.AdditionalAccelerationOptions":
            from mastapy.system_model.analyses_and_results.static_loads import _6810

            return self._parent._cast(_6810.AdditionalAccelerationOptions)

        @property
        def independent_reportable_properties_base(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
        ) -> "IndependentReportablePropertiesBase":
            return self._parent

        def __getattr__(
            self: "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase",
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
        self: Self, instance_to_wrap: "IndependentReportablePropertiesBase.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> (
        "IndependentReportablePropertiesBase._Cast_IndependentReportablePropertiesBase"
    ):
        return self._Cast_IndependentReportablePropertiesBase(self)
