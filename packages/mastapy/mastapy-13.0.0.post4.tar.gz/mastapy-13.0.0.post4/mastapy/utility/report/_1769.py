"""CustomReportMultiPropertyItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Generic

from mastapy.utility.report import _1770
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItem"
)

if TYPE_CHECKING:
    from mastapy.utility.report import _1773, _1756, _1780, _1771, _1763
    from mastapy.shafts import _20
    from mastapy.gears.gear_designs.cylindrical import _1035
    from mastapy.utility_gui.charts import _1854, _1855
    from mastapy.bearings.bearing_results import _1946, _1950, _1958
    from mastapy.system_model.analyses_and_results.system_deflections.reporting import (
        _2849,
    )
    from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
        _4716,
        _4720,
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItem",)


Self = TypeVar("Self", bound="CustomReportMultiPropertyItem")
TItem = TypeVar("TItem", bound="_1773.CustomReportPropertyItem")


class CustomReportMultiPropertyItem(
    _1770.CustomReportMultiPropertyItemBase, Generic[TItem]
):
    """CustomReportMultiPropertyItem

    This is a mastapy class.

    Generic Types:
        TItem
    """

    TYPE = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_CustomReportMultiPropertyItem")

    class _Cast_CustomReportMultiPropertyItem:
        """Special nested class for casting CustomReportMultiPropertyItem to subclasses."""

        def __init__(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
            parent: "CustomReportMultiPropertyItem",
        ):
            self._parent = parent

        @property
        def custom_report_multi_property_item_base(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1770.CustomReportMultiPropertyItemBase":
            return self._parent._cast(_1770.CustomReportMultiPropertyItemBase)

        @property
        def custom_report_nameable_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1771.CustomReportNameableItem":
            from mastapy.utility.report import _1771

            return self._parent._cast(_1771.CustomReportNameableItem)

        @property
        def custom_report_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1763.CustomReportItem":
            from mastapy.utility.report import _1763

            return self._parent._cast(_1763.CustomReportItem)

        @property
        def shaft_damage_results_table_and_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_20.ShaftDamageResultsTableAndChart":
            from mastapy.shafts import _20

            return self._parent._cast(_20.ShaftDamageResultsTableAndChart)

        @property
        def cylindrical_gear_table_with_mg_charts(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1035.CylindricalGearTableWithMGCharts":
            from mastapy.gears.gear_designs.cylindrical import _1035

            return self._parent._cast(_1035.CylindricalGearTableWithMGCharts)

        @property
        def custom_report_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1756.CustomReportChart":
            from mastapy.utility.report import _1756

            return self._parent._cast(_1756.CustomReportChart)

        @property
        def custom_table(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1780.CustomTable":
            from mastapy.utility.report import _1780

            return self._parent._cast(_1780.CustomTable)

        @property
        def custom_line_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1854.CustomLineChart":
            from mastapy.utility_gui.charts import _1854

            return self._parent._cast(_1854.CustomLineChart)

        @property
        def custom_table_and_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1855.CustomTableAndChart":
            from mastapy.utility_gui.charts import _1855

            return self._parent._cast(_1855.CustomTableAndChart)

        @property
        def loaded_ball_element_chart_reporter(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1946.LoadedBallElementChartReporter":
            from mastapy.bearings.bearing_results import _1946

            return self._parent._cast(_1946.LoadedBallElementChartReporter)

        @property
        def loaded_bearing_temperature_chart(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1950.LoadedBearingTemperatureChart":
            from mastapy.bearings.bearing_results import _1950

            return self._parent._cast(_1950.LoadedBearingTemperatureChart)

        @property
        def loaded_roller_element_chart_reporter(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_1958.LoadedRollerElementChartReporter":
            from mastapy.bearings.bearing_results import _1958

            return self._parent._cast(_1958.LoadedRollerElementChartReporter)

        @property
        def shaft_system_deflection_sections_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_2849.ShaftSystemDeflectionSectionsReport":
            from mastapy.system_model.analyses_and_results.system_deflections.reporting import (
                _2849,
            )

            return self._parent._cast(_2849.ShaftSystemDeflectionSectionsReport)

        @property
        def campbell_diagram_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_4716.CampbellDiagramReport":
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4716,
            )

            return self._parent._cast(_4716.CampbellDiagramReport)

        @property
        def per_mode_results_report(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "_4720.PerModeResultsReport":
            from mastapy.system_model.analyses_and_results.modal_analyses.reporting import (
                _4720,
            )

            return self._parent._cast(_4720.PerModeResultsReport)

        @property
        def custom_report_multi_property_item(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
        ) -> "CustomReportMultiPropertyItem":
            return self._parent

        def __getattr__(
            self: "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem",
            name: str,
        ):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "CustomReportMultiPropertyItem.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "CustomReportMultiPropertyItem._Cast_CustomReportMultiPropertyItem":
        return self._Cast_CustomReportMultiPropertyItem(self)
