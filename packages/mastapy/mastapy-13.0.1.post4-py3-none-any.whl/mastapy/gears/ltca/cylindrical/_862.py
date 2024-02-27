"""FaceGearSetLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.gears.ltca.cylindrical import _860
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "FaceGearSetLoadDistributionAnalysis"
)

if TYPE_CHECKING:
    from mastapy.gears.ltca import _846
    from mastapy.gears.analysis import _1228, _1229, _1226, _1217


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetLoadDistributionAnalysis",)


Self = TypeVar("Self", bound="FaceGearSetLoadDistributionAnalysis")


class FaceGearSetLoadDistributionAnalysis(
    _860.CylindricalGearSetLoadDistributionAnalysis
):
    """FaceGearSetLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE = _FACE_GEAR_SET_LOAD_DISTRIBUTION_ANALYSIS
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_FaceGearSetLoadDistributionAnalysis")

    class _Cast_FaceGearSetLoadDistributionAnalysis:
        """Special nested class for casting FaceGearSetLoadDistributionAnalysis to subclasses."""

        def __init__(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
            parent: "FaceGearSetLoadDistributionAnalysis",
        ):
            self._parent = parent

        @property
        def cylindrical_gear_set_load_distribution_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_860.CylindricalGearSetLoadDistributionAnalysis":
            return self._parent._cast(_860.CylindricalGearSetLoadDistributionAnalysis)

        @property
        def gear_set_load_distribution_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_846.GearSetLoadDistributionAnalysis":
            from mastapy.gears.ltca import _846

            return self._parent._cast(_846.GearSetLoadDistributionAnalysis)

        @property
        def gear_set_implementation_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_1228.GearSetImplementationAnalysis":
            from mastapy.gears.analysis import _1228

            return self._parent._cast(_1228.GearSetImplementationAnalysis)

        @property
        def gear_set_implementation_analysis_abstract(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_1229.GearSetImplementationAnalysisAbstract":
            from mastapy.gears.analysis import _1229

            return self._parent._cast(_1229.GearSetImplementationAnalysisAbstract)

        @property
        def gear_set_design_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_1226.GearSetDesignAnalysis":
            from mastapy.gears.analysis import _1226

            return self._parent._cast(_1226.GearSetDesignAnalysis)

        @property
        def abstract_gear_set_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "_1217.AbstractGearSetAnalysis":
            from mastapy.gears.analysis import _1217

            return self._parent._cast(_1217.AbstractGearSetAnalysis)

        @property
        def face_gear_set_load_distribution_analysis(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
        ) -> "FaceGearSetLoadDistributionAnalysis":
            return self._parent

        def __getattr__(
            self: "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis",
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
        self: Self, instance_to_wrap: "FaceGearSetLoadDistributionAnalysis.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> (
        "FaceGearSetLoadDistributionAnalysis._Cast_FaceGearSetLoadDistributionAnalysis"
    ):
        return self._Cast_FaceGearSetLoadDistributionAnalysis(self)
