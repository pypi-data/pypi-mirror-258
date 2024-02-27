"""MeasurementBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, Union, Tuple, List

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal.implicit import overridable, list_with_selected_item
from mastapy._internal.overridable_constructor import _unpack_overridable
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements import _1610
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_BASE = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements", "MeasurementBase"
)

if TYPE_CHECKING:
    from mastapy.utility import _1598
    from mastapy.utility.units_and_measurements.measurements import (
        _1612,
        _1613,
        _1614,
        _1615,
        _1616,
        _1617,
        _1618,
        _1619,
        _1620,
        _1621,
        _1622,
        _1623,
        _1624,
        _1625,
        _1626,
        _1627,
        _1628,
        _1629,
        _1630,
        _1631,
        _1632,
        _1633,
        _1634,
        _1635,
        _1636,
        _1637,
        _1638,
        _1639,
        _1640,
        _1641,
        _1642,
        _1643,
        _1644,
        _1645,
        _1646,
        _1647,
        _1648,
        _1649,
        _1650,
        _1651,
        _1652,
        _1653,
        _1654,
        _1655,
        _1656,
        _1657,
        _1658,
        _1659,
        _1660,
        _1661,
        _1662,
        _1663,
        _1664,
        _1665,
        _1666,
        _1667,
        _1668,
        _1669,
        _1670,
        _1671,
        _1672,
        _1673,
        _1674,
        _1675,
        _1676,
        _1677,
        _1678,
        _1679,
        _1680,
        _1681,
        _1682,
        _1683,
        _1684,
        _1685,
        _1686,
        _1687,
        _1688,
        _1689,
        _1690,
        _1691,
        _1692,
        _1693,
        _1694,
        _1695,
        _1696,
        _1697,
        _1698,
        _1699,
        _1700,
        _1701,
        _1702,
        _1703,
        _1704,
        _1705,
        _1706,
        _1707,
        _1708,
        _1709,
        _1710,
        _1711,
        _1712,
        _1713,
        _1714,
        _1715,
        _1716,
        _1717,
        _1718,
        _1719,
        _1720,
        _1721,
        _1722,
        _1723,
        _1724,
        _1725,
        _1726,
        _1727,
        _1728,
        _1729,
        _1730,
        _1731,
        _1732,
        _1733,
        _1734,
        _1735,
        _1736,
        _1737,
        _1738,
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementBase",)


Self = TypeVar("Self", bound="MeasurementBase")


class MeasurementBase(_0.APIBase):
    """MeasurementBase

    This is a mastapy class.
    """

    TYPE = _MEASUREMENT_BASE
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_MeasurementBase")

    class _Cast_MeasurementBase:
        """Special nested class for casting MeasurementBase to subclasses."""

        def __init__(
            self: "MeasurementBase._Cast_MeasurementBase", parent: "MeasurementBase"
        ):
            self._parent = parent

        @property
        def acceleration(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1612.Acceleration":
            from mastapy.utility.units_and_measurements.measurements import _1612

            return self._parent._cast(_1612.Acceleration)

        @property
        def angle(self: "MeasurementBase._Cast_MeasurementBase") -> "_1613.Angle":
            from mastapy.utility.units_and_measurements.measurements import _1613

            return self._parent._cast(_1613.Angle)

        @property
        def angle_per_unit_temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1614.AnglePerUnitTemperature":
            from mastapy.utility.units_and_measurements.measurements import _1614

            return self._parent._cast(_1614.AnglePerUnitTemperature)

        @property
        def angle_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1615.AngleSmall":
            from mastapy.utility.units_and_measurements.measurements import _1615

            return self._parent._cast(_1615.AngleSmall)

        @property
        def angle_very_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1616.AngleVerySmall":
            from mastapy.utility.units_and_measurements.measurements import _1616

            return self._parent._cast(_1616.AngleVerySmall)

        @property
        def angular_acceleration(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1617.AngularAcceleration":
            from mastapy.utility.units_and_measurements.measurements import _1617

            return self._parent._cast(_1617.AngularAcceleration)

        @property
        def angular_compliance(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1618.AngularCompliance":
            from mastapy.utility.units_and_measurements.measurements import _1618

            return self._parent._cast(_1618.AngularCompliance)

        @property
        def angular_jerk(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1619.AngularJerk":
            from mastapy.utility.units_and_measurements.measurements import _1619

            return self._parent._cast(_1619.AngularJerk)

        @property
        def angular_stiffness(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1620.AngularStiffness":
            from mastapy.utility.units_and_measurements.measurements import _1620

            return self._parent._cast(_1620.AngularStiffness)

        @property
        def angular_velocity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1621.AngularVelocity":
            from mastapy.utility.units_and_measurements.measurements import _1621

            return self._parent._cast(_1621.AngularVelocity)

        @property
        def area(self: "MeasurementBase._Cast_MeasurementBase") -> "_1622.Area":
            from mastapy.utility.units_and_measurements.measurements import _1622

            return self._parent._cast(_1622.Area)

        @property
        def area_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1623.AreaSmall":
            from mastapy.utility.units_and_measurements.measurements import _1623

            return self._parent._cast(_1623.AreaSmall)

        @property
        def carbon_emission_factor(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1624.CarbonEmissionFactor":
            from mastapy.utility.units_and_measurements.measurements import _1624

            return self._parent._cast(_1624.CarbonEmissionFactor)

        @property
        def current_density(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1625.CurrentDensity":
            from mastapy.utility.units_and_measurements.measurements import _1625

            return self._parent._cast(_1625.CurrentDensity)

        @property
        def current_per_length(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1626.CurrentPerLength":
            from mastapy.utility.units_and_measurements.measurements import _1626

            return self._parent._cast(_1626.CurrentPerLength)

        @property
        def cycles(self: "MeasurementBase._Cast_MeasurementBase") -> "_1627.Cycles":
            from mastapy.utility.units_and_measurements.measurements import _1627

            return self._parent._cast(_1627.Cycles)

        @property
        def damage(self: "MeasurementBase._Cast_MeasurementBase") -> "_1628.Damage":
            from mastapy.utility.units_and_measurements.measurements import _1628

            return self._parent._cast(_1628.Damage)

        @property
        def damage_rate(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1629.DamageRate":
            from mastapy.utility.units_and_measurements.measurements import _1629

            return self._parent._cast(_1629.DamageRate)

        @property
        def data_size(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1630.DataSize":
            from mastapy.utility.units_and_measurements.measurements import _1630

            return self._parent._cast(_1630.DataSize)

        @property
        def decibel(self: "MeasurementBase._Cast_MeasurementBase") -> "_1631.Decibel":
            from mastapy.utility.units_and_measurements.measurements import _1631

            return self._parent._cast(_1631.Decibel)

        @property
        def density(self: "MeasurementBase._Cast_MeasurementBase") -> "_1632.Density":
            from mastapy.utility.units_and_measurements.measurements import _1632

            return self._parent._cast(_1632.Density)

        @property
        def electrical_resistance(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1633.ElectricalResistance":
            from mastapy.utility.units_and_measurements.measurements import _1633

            return self._parent._cast(_1633.ElectricalResistance)

        @property
        def electrical_resistivity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1634.ElectricalResistivity":
            from mastapy.utility.units_and_measurements.measurements import _1634

            return self._parent._cast(_1634.ElectricalResistivity)

        @property
        def electric_current(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1635.ElectricCurrent":
            from mastapy.utility.units_and_measurements.measurements import _1635

            return self._parent._cast(_1635.ElectricCurrent)

        @property
        def energy(self: "MeasurementBase._Cast_MeasurementBase") -> "_1636.Energy":
            from mastapy.utility.units_and_measurements.measurements import _1636

            return self._parent._cast(_1636.Energy)

        @property
        def energy_per_unit_area(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1637.EnergyPerUnitArea":
            from mastapy.utility.units_and_measurements.measurements import _1637

            return self._parent._cast(_1637.EnergyPerUnitArea)

        @property
        def energy_per_unit_area_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1638.EnergyPerUnitAreaSmall":
            from mastapy.utility.units_and_measurements.measurements import _1638

            return self._parent._cast(_1638.EnergyPerUnitAreaSmall)

        @property
        def energy_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1639.EnergySmall":
            from mastapy.utility.units_and_measurements.measurements import _1639

            return self._parent._cast(_1639.EnergySmall)

        @property
        def enum(self: "MeasurementBase._Cast_MeasurementBase") -> "_1640.Enum":
            from mastapy.utility.units_and_measurements.measurements import _1640

            return self._parent._cast(_1640.Enum)

        @property
        def flow_rate(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1641.FlowRate":
            from mastapy.utility.units_and_measurements.measurements import _1641

            return self._parent._cast(_1641.FlowRate)

        @property
        def force(self: "MeasurementBase._Cast_MeasurementBase") -> "_1642.Force":
            from mastapy.utility.units_and_measurements.measurements import _1642

            return self._parent._cast(_1642.Force)

        @property
        def force_per_unit_length(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1643.ForcePerUnitLength":
            from mastapy.utility.units_and_measurements.measurements import _1643

            return self._parent._cast(_1643.ForcePerUnitLength)

        @property
        def force_per_unit_pressure(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1644.ForcePerUnitPressure":
            from mastapy.utility.units_and_measurements.measurements import _1644

            return self._parent._cast(_1644.ForcePerUnitPressure)

        @property
        def force_per_unit_temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1645.ForcePerUnitTemperature":
            from mastapy.utility.units_and_measurements.measurements import _1645

            return self._parent._cast(_1645.ForcePerUnitTemperature)

        @property
        def fraction_measurement_base(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1646.FractionMeasurementBase":
            from mastapy.utility.units_and_measurements.measurements import _1646

            return self._parent._cast(_1646.FractionMeasurementBase)

        @property
        def fraction_per_temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1647.FractionPerTemperature":
            from mastapy.utility.units_and_measurements.measurements import _1647

            return self._parent._cast(_1647.FractionPerTemperature)

        @property
        def frequency(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1648.Frequency":
            from mastapy.utility.units_and_measurements.measurements import _1648

            return self._parent._cast(_1648.Frequency)

        @property
        def fuel_consumption_engine(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1649.FuelConsumptionEngine":
            from mastapy.utility.units_and_measurements.measurements import _1649

            return self._parent._cast(_1649.FuelConsumptionEngine)

        @property
        def fuel_efficiency_vehicle(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1650.FuelEfficiencyVehicle":
            from mastapy.utility.units_and_measurements.measurements import _1650

            return self._parent._cast(_1650.FuelEfficiencyVehicle)

        @property
        def gradient(self: "MeasurementBase._Cast_MeasurementBase") -> "_1651.Gradient":
            from mastapy.utility.units_and_measurements.measurements import _1651

            return self._parent._cast(_1651.Gradient)

        @property
        def heat_conductivity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1652.HeatConductivity":
            from mastapy.utility.units_and_measurements.measurements import _1652

            return self._parent._cast(_1652.HeatConductivity)

        @property
        def heat_transfer(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1653.HeatTransfer":
            from mastapy.utility.units_and_measurements.measurements import _1653

            return self._parent._cast(_1653.HeatTransfer)

        @property
        def heat_transfer_coefficient_for_plastic_gear_tooth(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1654.HeatTransferCoefficientForPlasticGearTooth":
            from mastapy.utility.units_and_measurements.measurements import _1654

            return self._parent._cast(_1654.HeatTransferCoefficientForPlasticGearTooth)

        @property
        def heat_transfer_resistance(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1655.HeatTransferResistance":
            from mastapy.utility.units_and_measurements.measurements import _1655

            return self._parent._cast(_1655.HeatTransferResistance)

        @property
        def impulse(self: "MeasurementBase._Cast_MeasurementBase") -> "_1656.Impulse":
            from mastapy.utility.units_and_measurements.measurements import _1656

            return self._parent._cast(_1656.Impulse)

        @property
        def index(self: "MeasurementBase._Cast_MeasurementBase") -> "_1657.Index":
            from mastapy.utility.units_and_measurements.measurements import _1657

            return self._parent._cast(_1657.Index)

        @property
        def inductance(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1658.Inductance":
            from mastapy.utility.units_and_measurements.measurements import _1658

            return self._parent._cast(_1658.Inductance)

        @property
        def integer(self: "MeasurementBase._Cast_MeasurementBase") -> "_1659.Integer":
            from mastapy.utility.units_and_measurements.measurements import _1659

            return self._parent._cast(_1659.Integer)

        @property
        def inverse_short_length(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1660.InverseShortLength":
            from mastapy.utility.units_and_measurements.measurements import _1660

            return self._parent._cast(_1660.InverseShortLength)

        @property
        def inverse_short_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1661.InverseShortTime":
            from mastapy.utility.units_and_measurements.measurements import _1661

            return self._parent._cast(_1661.InverseShortTime)

        @property
        def jerk(self: "MeasurementBase._Cast_MeasurementBase") -> "_1662.Jerk":
            from mastapy.utility.units_and_measurements.measurements import _1662

            return self._parent._cast(_1662.Jerk)

        @property
        def kinematic_viscosity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1663.KinematicViscosity":
            from mastapy.utility.units_and_measurements.measurements import _1663

            return self._parent._cast(_1663.KinematicViscosity)

        @property
        def length_long(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1664.LengthLong":
            from mastapy.utility.units_and_measurements.measurements import _1664

            return self._parent._cast(_1664.LengthLong)

        @property
        def length_medium(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1665.LengthMedium":
            from mastapy.utility.units_and_measurements.measurements import _1665

            return self._parent._cast(_1665.LengthMedium)

        @property
        def length_per_unit_temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1666.LengthPerUnitTemperature":
            from mastapy.utility.units_and_measurements.measurements import _1666

            return self._parent._cast(_1666.LengthPerUnitTemperature)

        @property
        def length_short(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1667.LengthShort":
            from mastapy.utility.units_and_measurements.measurements import _1667

            return self._parent._cast(_1667.LengthShort)

        @property
        def length_to_the_fourth(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1668.LengthToTheFourth":
            from mastapy.utility.units_and_measurements.measurements import _1668

            return self._parent._cast(_1668.LengthToTheFourth)

        @property
        def length_very_long(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1669.LengthVeryLong":
            from mastapy.utility.units_and_measurements.measurements import _1669

            return self._parent._cast(_1669.LengthVeryLong)

        @property
        def length_very_short(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1670.LengthVeryShort":
            from mastapy.utility.units_and_measurements.measurements import _1670

            return self._parent._cast(_1670.LengthVeryShort)

        @property
        def length_very_short_per_length_short(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1671.LengthVeryShortPerLengthShort":
            from mastapy.utility.units_and_measurements.measurements import _1671

            return self._parent._cast(_1671.LengthVeryShortPerLengthShort)

        @property
        def linear_angular_damping(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1672.LinearAngularDamping":
            from mastapy.utility.units_and_measurements.measurements import _1672

            return self._parent._cast(_1672.LinearAngularDamping)

        @property
        def linear_angular_stiffness_cross_term(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1673.LinearAngularStiffnessCrossTerm":
            from mastapy.utility.units_and_measurements.measurements import _1673

            return self._parent._cast(_1673.LinearAngularStiffnessCrossTerm)

        @property
        def linear_damping(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1674.LinearDamping":
            from mastapy.utility.units_and_measurements.measurements import _1674

            return self._parent._cast(_1674.LinearDamping)

        @property
        def linear_flexibility(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1675.LinearFlexibility":
            from mastapy.utility.units_and_measurements.measurements import _1675

            return self._parent._cast(_1675.LinearFlexibility)

        @property
        def linear_stiffness(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1676.LinearStiffness":
            from mastapy.utility.units_and_measurements.measurements import _1676

            return self._parent._cast(_1676.LinearStiffness)

        @property
        def magnetic_field_strength(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1677.MagneticFieldStrength":
            from mastapy.utility.units_and_measurements.measurements import _1677

            return self._parent._cast(_1677.MagneticFieldStrength)

        @property
        def magnetic_flux(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1678.MagneticFlux":
            from mastapy.utility.units_and_measurements.measurements import _1678

            return self._parent._cast(_1678.MagneticFlux)

        @property
        def magnetic_flux_density(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1679.MagneticFluxDensity":
            from mastapy.utility.units_and_measurements.measurements import _1679

            return self._parent._cast(_1679.MagneticFluxDensity)

        @property
        def magnetic_vector_potential(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1680.MagneticVectorPotential":
            from mastapy.utility.units_and_measurements.measurements import _1680

            return self._parent._cast(_1680.MagneticVectorPotential)

        @property
        def magnetomotive_force(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1681.MagnetomotiveForce":
            from mastapy.utility.units_and_measurements.measurements import _1681

            return self._parent._cast(_1681.MagnetomotiveForce)

        @property
        def mass(self: "MeasurementBase._Cast_MeasurementBase") -> "_1682.Mass":
            from mastapy.utility.units_and_measurements.measurements import _1682

            return self._parent._cast(_1682.Mass)

        @property
        def mass_per_unit_length(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1683.MassPerUnitLength":
            from mastapy.utility.units_and_measurements.measurements import _1683

            return self._parent._cast(_1683.MassPerUnitLength)

        @property
        def mass_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1684.MassPerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1684

            return self._parent._cast(_1684.MassPerUnitTime)

        @property
        def moment_of_inertia(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1685.MomentOfInertia":
            from mastapy.utility.units_and_measurements.measurements import _1685

            return self._parent._cast(_1685.MomentOfInertia)

        @property
        def moment_of_inertia_per_unit_length(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1686.MomentOfInertiaPerUnitLength":
            from mastapy.utility.units_and_measurements.measurements import _1686

            return self._parent._cast(_1686.MomentOfInertiaPerUnitLength)

        @property
        def moment_per_unit_pressure(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1687.MomentPerUnitPressure":
            from mastapy.utility.units_and_measurements.measurements import _1687

            return self._parent._cast(_1687.MomentPerUnitPressure)

        @property
        def number(self: "MeasurementBase._Cast_MeasurementBase") -> "_1688.Number":
            from mastapy.utility.units_and_measurements.measurements import _1688

            return self._parent._cast(_1688.Number)

        @property
        def percentage(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1689.Percentage":
            from mastapy.utility.units_and_measurements.measurements import _1689

            return self._parent._cast(_1689.Percentage)

        @property
        def power(self: "MeasurementBase._Cast_MeasurementBase") -> "_1690.Power":
            from mastapy.utility.units_and_measurements.measurements import _1690

            return self._parent._cast(_1690.Power)

        @property
        def power_per_small_area(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1691.PowerPerSmallArea":
            from mastapy.utility.units_and_measurements.measurements import _1691

            return self._parent._cast(_1691.PowerPerSmallArea)

        @property
        def power_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1692.PowerPerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1692

            return self._parent._cast(_1692.PowerPerUnitTime)

        @property
        def power_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1693.PowerSmall":
            from mastapy.utility.units_and_measurements.measurements import _1693

            return self._parent._cast(_1693.PowerSmall)

        @property
        def power_small_per_area(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1694.PowerSmallPerArea":
            from mastapy.utility.units_and_measurements.measurements import _1694

            return self._parent._cast(_1694.PowerSmallPerArea)

        @property
        def power_small_per_mass(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1695.PowerSmallPerMass":
            from mastapy.utility.units_and_measurements.measurements import _1695

            return self._parent._cast(_1695.PowerSmallPerMass)

        @property
        def power_small_per_unit_area_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1696.PowerSmallPerUnitAreaPerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1696

            return self._parent._cast(_1696.PowerSmallPerUnitAreaPerUnitTime)

        @property
        def power_small_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1697.PowerSmallPerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1697

            return self._parent._cast(_1697.PowerSmallPerUnitTime)

        @property
        def power_small_per_volume(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1698.PowerSmallPerVolume":
            from mastapy.utility.units_and_measurements.measurements import _1698

            return self._parent._cast(_1698.PowerSmallPerVolume)

        @property
        def pressure(self: "MeasurementBase._Cast_MeasurementBase") -> "_1699.Pressure":
            from mastapy.utility.units_and_measurements.measurements import _1699

            return self._parent._cast(_1699.Pressure)

        @property
        def pressure_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1700.PressurePerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1700

            return self._parent._cast(_1700.PressurePerUnitTime)

        @property
        def pressure_velocity_product(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1701.PressureVelocityProduct":
            from mastapy.utility.units_and_measurements.measurements import _1701

            return self._parent._cast(_1701.PressureVelocityProduct)

        @property
        def pressure_viscosity_coefficient(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1702.PressureViscosityCoefficient":
            from mastapy.utility.units_and_measurements.measurements import _1702

            return self._parent._cast(_1702.PressureViscosityCoefficient)

        @property
        def price(self: "MeasurementBase._Cast_MeasurementBase") -> "_1703.Price":
            from mastapy.utility.units_and_measurements.measurements import _1703

            return self._parent._cast(_1703.Price)

        @property
        def price_per_unit_mass(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1704.PricePerUnitMass":
            from mastapy.utility.units_and_measurements.measurements import _1704

            return self._parent._cast(_1704.PricePerUnitMass)

        @property
        def quadratic_angular_damping(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1705.QuadraticAngularDamping":
            from mastapy.utility.units_and_measurements.measurements import _1705

            return self._parent._cast(_1705.QuadraticAngularDamping)

        @property
        def quadratic_drag(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1706.QuadraticDrag":
            from mastapy.utility.units_and_measurements.measurements import _1706

            return self._parent._cast(_1706.QuadraticDrag)

        @property
        def rescaled_measurement(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1707.RescaledMeasurement":
            from mastapy.utility.units_and_measurements.measurements import _1707

            return self._parent._cast(_1707.RescaledMeasurement)

        @property
        def rotatum(self: "MeasurementBase._Cast_MeasurementBase") -> "_1708.Rotatum":
            from mastapy.utility.units_and_measurements.measurements import _1708

            return self._parent._cast(_1708.Rotatum)

        @property
        def safety_factor(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1709.SafetyFactor":
            from mastapy.utility.units_and_measurements.measurements import _1709

            return self._parent._cast(_1709.SafetyFactor)

        @property
        def specific_acoustic_impedance(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1710.SpecificAcousticImpedance":
            from mastapy.utility.units_and_measurements.measurements import _1710

            return self._parent._cast(_1710.SpecificAcousticImpedance)

        @property
        def specific_heat(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1711.SpecificHeat":
            from mastapy.utility.units_and_measurements.measurements import _1711

            return self._parent._cast(_1711.SpecificHeat)

        @property
        def square_root_of_unit_force_per_unit_area(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1712.SquareRootOfUnitForcePerUnitArea":
            from mastapy.utility.units_and_measurements.measurements import _1712

            return self._parent._cast(_1712.SquareRootOfUnitForcePerUnitArea)

        @property
        def stiffness_per_unit_face_width(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1713.StiffnessPerUnitFaceWidth":
            from mastapy.utility.units_and_measurements.measurements import _1713

            return self._parent._cast(_1713.StiffnessPerUnitFaceWidth)

        @property
        def stress(self: "MeasurementBase._Cast_MeasurementBase") -> "_1714.Stress":
            from mastapy.utility.units_and_measurements.measurements import _1714

            return self._parent._cast(_1714.Stress)

        @property
        def temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1715.Temperature":
            from mastapy.utility.units_and_measurements.measurements import _1715

            return self._parent._cast(_1715.Temperature)

        @property
        def temperature_difference(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1716.TemperatureDifference":
            from mastapy.utility.units_and_measurements.measurements import _1716

            return self._parent._cast(_1716.TemperatureDifference)

        @property
        def temperature_per_unit_time(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1717.TemperaturePerUnitTime":
            from mastapy.utility.units_and_measurements.measurements import _1717

            return self._parent._cast(_1717.TemperaturePerUnitTime)

        @property
        def text(self: "MeasurementBase._Cast_MeasurementBase") -> "_1718.Text":
            from mastapy.utility.units_and_measurements.measurements import _1718

            return self._parent._cast(_1718.Text)

        @property
        def thermal_contact_coefficient(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1719.ThermalContactCoefficient":
            from mastapy.utility.units_and_measurements.measurements import _1719

            return self._parent._cast(_1719.ThermalContactCoefficient)

        @property
        def thermal_expansion_coefficient(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1720.ThermalExpansionCoefficient":
            from mastapy.utility.units_and_measurements.measurements import _1720

            return self._parent._cast(_1720.ThermalExpansionCoefficient)

        @property
        def thermo_elastic_factor(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1721.ThermoElasticFactor":
            from mastapy.utility.units_and_measurements.measurements import _1721

            return self._parent._cast(_1721.ThermoElasticFactor)

        @property
        def time(self: "MeasurementBase._Cast_MeasurementBase") -> "_1722.Time":
            from mastapy.utility.units_and_measurements.measurements import _1722

            return self._parent._cast(_1722.Time)

        @property
        def time_short(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1723.TimeShort":
            from mastapy.utility.units_and_measurements.measurements import _1723

            return self._parent._cast(_1723.TimeShort)

        @property
        def time_very_short(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1724.TimeVeryShort":
            from mastapy.utility.units_and_measurements.measurements import _1724

            return self._parent._cast(_1724.TimeVeryShort)

        @property
        def torque(self: "MeasurementBase._Cast_MeasurementBase") -> "_1725.Torque":
            from mastapy.utility.units_and_measurements.measurements import _1725

            return self._parent._cast(_1725.Torque)

        @property
        def torque_converter_inverse_k(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1726.TorqueConverterInverseK":
            from mastapy.utility.units_and_measurements.measurements import _1726

            return self._parent._cast(_1726.TorqueConverterInverseK)

        @property
        def torque_converter_k(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1727.TorqueConverterK":
            from mastapy.utility.units_and_measurements.measurements import _1727

            return self._parent._cast(_1727.TorqueConverterK)

        @property
        def torque_per_current(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1728.TorquePerCurrent":
            from mastapy.utility.units_and_measurements.measurements import _1728

            return self._parent._cast(_1728.TorquePerCurrent)

        @property
        def torque_per_square_root_of_power(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1729.TorquePerSquareRootOfPower":
            from mastapy.utility.units_and_measurements.measurements import _1729

            return self._parent._cast(_1729.TorquePerSquareRootOfPower)

        @property
        def torque_per_unit_temperature(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1730.TorquePerUnitTemperature":
            from mastapy.utility.units_and_measurements.measurements import _1730

            return self._parent._cast(_1730.TorquePerUnitTemperature)

        @property
        def velocity(self: "MeasurementBase._Cast_MeasurementBase") -> "_1731.Velocity":
            from mastapy.utility.units_and_measurements.measurements import _1731

            return self._parent._cast(_1731.Velocity)

        @property
        def velocity_small(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1732.VelocitySmall":
            from mastapy.utility.units_and_measurements.measurements import _1732

            return self._parent._cast(_1732.VelocitySmall)

        @property
        def viscosity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1733.Viscosity":
            from mastapy.utility.units_and_measurements.measurements import _1733

            return self._parent._cast(_1733.Viscosity)

        @property
        def voltage(self: "MeasurementBase._Cast_MeasurementBase") -> "_1734.Voltage":
            from mastapy.utility.units_and_measurements.measurements import _1734

            return self._parent._cast(_1734.Voltage)

        @property
        def voltage_per_angular_velocity(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1735.VoltagePerAngularVelocity":
            from mastapy.utility.units_and_measurements.measurements import _1735

            return self._parent._cast(_1735.VoltagePerAngularVelocity)

        @property
        def volume(self: "MeasurementBase._Cast_MeasurementBase") -> "_1736.Volume":
            from mastapy.utility.units_and_measurements.measurements import _1736

            return self._parent._cast(_1736.Volume)

        @property
        def wear_coefficient(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "_1737.WearCoefficient":
            from mastapy.utility.units_and_measurements.measurements import _1737

            return self._parent._cast(_1737.WearCoefficient)

        @property
        def yank(self: "MeasurementBase._Cast_MeasurementBase") -> "_1738.Yank":
            from mastapy.utility.units_and_measurements.measurements import _1738

            return self._parent._cast(_1738.Yank)

        @property
        def measurement_base(
            self: "MeasurementBase._Cast_MeasurementBase",
        ) -> "MeasurementBase":
            return self._parent

        def __getattr__(self: "MeasurementBase._Cast_MeasurementBase", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "MeasurementBase.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def absolute_tolerance(self: Self) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = self.wrapped.AbsoluteTolerance

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @absolute_tolerance.setter
    @enforce_parameter_types
    def absolute_tolerance(self: Self, value: "Union[float, Tuple[float, bool]]"):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        self.wrapped.AbsoluteTolerance = value

    @property
    def default_unit(self: Self) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = self.wrapped.DefaultUnit

        if temp is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @default_unit.setter
    @enforce_parameter_types
    def default_unit(self: Self, value: "_1610.Unit"):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Unit.wrapper_type()
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        self.wrapped.DefaultUnit = value

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
    def percentage_tolerance(self: Self) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = self.wrapped.PercentageTolerance

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @percentage_tolerance.setter
    @enforce_parameter_types
    def percentage_tolerance(self: Self, value: "Union[float, Tuple[float, bool]]"):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        self.wrapped.PercentageTolerance = value

    @property
    def rounding_digits(self: Self) -> "int":
        """int"""
        temp = self.wrapped.RoundingDigits

        if temp is None:
            return 0

        return temp

    @rounding_digits.setter
    @enforce_parameter_types
    def rounding_digits(self: Self, value: "int"):
        self.wrapped.RoundingDigits = int(value) if value is not None else 0

    @property
    def rounding_method(self: Self) -> "_1598.RoundingMethods":
        """mastapy.utility.RoundingMethods"""
        temp = self.wrapped.RoundingMethod

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Utility.RoundingMethods")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy.utility._1598", "RoundingMethods")(
            value
        )

    @rounding_method.setter
    @enforce_parameter_types
    def rounding_method(self: Self, value: "_1598.RoundingMethods"):
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Utility.RoundingMethods")
        self.wrapped.RoundingMethod = value

    @property
    def current_unit(self: Self) -> "_1610.Unit":
        """mastapy.utility.units_and_measurements.Unit

        Note:
            This property is readonly.
        """
        temp = self.wrapped.CurrentUnit

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def available_units(self: Self) -> "List[_1610.Unit]":
        """List[mastapy.utility.units_and_measurements.Unit]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AvailableUnits

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: Self) -> "MeasurementBase._Cast_MeasurementBase":
        return self._Cast_MeasurementBase(self)
