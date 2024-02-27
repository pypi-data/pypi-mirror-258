"""NonLinearBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.bearings.bearing_designs import _2130
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_NON_LINEAR_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "NonLinearBearing"
)

if TYPE_CHECKING:
    from mastapy.bearings.bearing_designs import _2131
    from mastapy.bearings.bearing_designs.rolling import (
        _2135,
        _2136,
        _2137,
        _2138,
        _2139,
        _2140,
        _2142,
        _2148,
        _2149,
        _2150,
        _2154,
        _2159,
        _2160,
        _2161,
        _2162,
        _2165,
        _2166,
        _2169,
        _2170,
        _2171,
        _2172,
        _2173,
        _2174,
    )
    from mastapy.bearings.bearing_designs.fluid_film import (
        _2187,
        _2189,
        _2191,
        _2193,
        _2194,
        _2195,
    )
    from mastapy.bearings.bearing_designs.concept import _2197, _2198, _2199


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearBearing",)


Self = TypeVar("Self", bound="NonLinearBearing")


class NonLinearBearing(_2130.BearingDesign):
    """NonLinearBearing

    This is a mastapy class.
    """

    TYPE = _NON_LINEAR_BEARING
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_NonLinearBearing")

    class _Cast_NonLinearBearing:
        """Special nested class for casting NonLinearBearing to subclasses."""

        def __init__(
            self: "NonLinearBearing._Cast_NonLinearBearing", parent: "NonLinearBearing"
        ):
            self._parent = parent

        @property
        def bearing_design(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2130.BearingDesign":
            return self._parent._cast(_2130.BearingDesign)

        @property
        def detailed_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2131.DetailedBearing":
            from mastapy.bearings.bearing_designs import _2131

            return self._parent._cast(_2131.DetailedBearing)

        @property
        def angular_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2135.AngularContactBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2135

            return self._parent._cast(_2135.AngularContactBallBearing)

        @property
        def angular_contact_thrust_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2136.AngularContactThrustBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2136

            return self._parent._cast(_2136.AngularContactThrustBallBearing)

        @property
        def asymmetric_spherical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2137.AsymmetricSphericalRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2137

            return self._parent._cast(_2137.AsymmetricSphericalRollerBearing)

        @property
        def axial_thrust_cylindrical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2138.AxialThrustCylindricalRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2138

            return self._parent._cast(_2138.AxialThrustCylindricalRollerBearing)

        @property
        def axial_thrust_needle_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2139.AxialThrustNeedleRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2139

            return self._parent._cast(_2139.AxialThrustNeedleRollerBearing)

        @property
        def ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2140.BallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2140

            return self._parent._cast(_2140.BallBearing)

        @property
        def barrel_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2142.BarrelRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2142

            return self._parent._cast(_2142.BarrelRollerBearing)

        @property
        def crossed_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2148.CrossedRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2148

            return self._parent._cast(_2148.CrossedRollerBearing)

        @property
        def cylindrical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2149.CylindricalRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2149

            return self._parent._cast(_2149.CylindricalRollerBearing)

        @property
        def deep_groove_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2150.DeepGrooveBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2150

            return self._parent._cast(_2150.DeepGrooveBallBearing)

        @property
        def four_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2154.FourPointContactBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2154

            return self._parent._cast(_2154.FourPointContactBallBearing)

        @property
        def multi_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2159.MultiPointContactBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2159

            return self._parent._cast(_2159.MultiPointContactBallBearing)

        @property
        def needle_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2160.NeedleRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2160

            return self._parent._cast(_2160.NeedleRollerBearing)

        @property
        def non_barrel_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2161.NonBarrelRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2161

            return self._parent._cast(_2161.NonBarrelRollerBearing)

        @property
        def roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2162.RollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2162

            return self._parent._cast(_2162.RollerBearing)

        @property
        def rolling_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2165.RollingBearing":
            from mastapy.bearings.bearing_designs.rolling import _2165

            return self._parent._cast(_2165.RollingBearing)

        @property
        def self_aligning_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2166.SelfAligningBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2166

            return self._parent._cast(_2166.SelfAligningBallBearing)

        @property
        def spherical_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2169.SphericalRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2169

            return self._parent._cast(_2169.SphericalRollerBearing)

        @property
        def spherical_roller_thrust_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2170.SphericalRollerThrustBearing":
            from mastapy.bearings.bearing_designs.rolling import _2170

            return self._parent._cast(_2170.SphericalRollerThrustBearing)

        @property
        def taper_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2171.TaperRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2171

            return self._parent._cast(_2171.TaperRollerBearing)

        @property
        def three_point_contact_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2172.ThreePointContactBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2172

            return self._parent._cast(_2172.ThreePointContactBallBearing)

        @property
        def thrust_ball_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2173.ThrustBallBearing":
            from mastapy.bearings.bearing_designs.rolling import _2173

            return self._parent._cast(_2173.ThrustBallBearing)

        @property
        def toroidal_roller_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2174.ToroidalRollerBearing":
            from mastapy.bearings.bearing_designs.rolling import _2174

            return self._parent._cast(_2174.ToroidalRollerBearing)

        @property
        def pad_fluid_film_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2187.PadFluidFilmBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2187

            return self._parent._cast(_2187.PadFluidFilmBearing)

        @property
        def plain_grease_filled_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2189.PlainGreaseFilledJournalBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2189

            return self._parent._cast(_2189.PlainGreaseFilledJournalBearing)

        @property
        def plain_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2191.PlainJournalBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2191

            return self._parent._cast(_2191.PlainJournalBearing)

        @property
        def plain_oil_fed_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2193.PlainOilFedJournalBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2193

            return self._parent._cast(_2193.PlainOilFedJournalBearing)

        @property
        def tilting_pad_journal_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2194.TiltingPadJournalBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2194

            return self._parent._cast(_2194.TiltingPadJournalBearing)

        @property
        def tilting_pad_thrust_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2195.TiltingPadThrustBearing":
            from mastapy.bearings.bearing_designs.fluid_film import _2195

            return self._parent._cast(_2195.TiltingPadThrustBearing)

        @property
        def concept_axial_clearance_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2197.ConceptAxialClearanceBearing":
            from mastapy.bearings.bearing_designs.concept import _2197

            return self._parent._cast(_2197.ConceptAxialClearanceBearing)

        @property
        def concept_clearance_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2198.ConceptClearanceBearing":
            from mastapy.bearings.bearing_designs.concept import _2198

            return self._parent._cast(_2198.ConceptClearanceBearing)

        @property
        def concept_radial_clearance_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "_2199.ConceptRadialClearanceBearing":
            from mastapy.bearings.bearing_designs.concept import _2199

            return self._parent._cast(_2199.ConceptRadialClearanceBearing)

        @property
        def non_linear_bearing(
            self: "NonLinearBearing._Cast_NonLinearBearing",
        ) -> "NonLinearBearing":
            return self._parent

        def __getattr__(self: "NonLinearBearing._Cast_NonLinearBearing", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "NonLinearBearing.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "NonLinearBearing._Cast_NonLinearBearing":
        return self._Cast_NonLinearBearing(self)
