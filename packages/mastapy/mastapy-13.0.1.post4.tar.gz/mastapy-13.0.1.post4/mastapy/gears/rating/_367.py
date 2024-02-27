"""RateableMesh"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_RATEABLE_MESH = python_net_import("SMT.MastaAPI.Gears.Rating", "RateableMesh")

if TYPE_CHECKING:
    from mastapy.gears.rating.klingelnberg_conical.kn3030 import _415
    from mastapy.gears.rating.iso_10300 import _427
    from mastapy.gears.rating.hypoid.standards import _444
    from mastapy.gears.rating.cylindrical import _471
    from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _493, _498, _499, _500
    from mastapy.gears.rating.cylindrical.iso6336 import _522, _523
    from mastapy.gears.rating.cylindrical.agma import _536
    from mastapy.gears.rating.conical import _547
    from mastapy.gears.rating.bevel.standards import _564
    from mastapy.gears.rating.agma_gleason_conical import _568


__docformat__ = "restructuredtext en"
__all__ = ("RateableMesh",)


Self = TypeVar("Self", bound="RateableMesh")


class RateableMesh(_0.APIBase):
    """RateableMesh

    This is a mastapy class.
    """

    TYPE = _RATEABLE_MESH
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_RateableMesh")

    class _Cast_RateableMesh:
        """Special nested class for casting RateableMesh to subclasses."""

        def __init__(self: "RateableMesh._Cast_RateableMesh", parent: "RateableMesh"):
            self._parent = parent

        @property
        def klingelnberg_conical_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_415.KlingelnbergConicalRateableMesh":
            from mastapy.gears.rating.klingelnberg_conical.kn3030 import _415

            return self._parent._cast(_415.KlingelnbergConicalRateableMesh)

        @property
        def iso10300_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_427.ISO10300RateableMesh":
            from mastapy.gears.rating.iso_10300 import _427

            return self._parent._cast(_427.ISO10300RateableMesh)

        @property
        def hypoid_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_444.HypoidRateableMesh":
            from mastapy.gears.rating.hypoid.standards import _444

            return self._parent._cast(_444.HypoidRateableMesh)

        @property
        def cylindrical_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_471.CylindricalRateableMesh":
            from mastapy.gears.rating.cylindrical import _471

            return self._parent._cast(_471.CylindricalRateableMesh)

        @property
        def plastic_gear_vdi2736_abstract_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_493.PlasticGearVDI2736AbstractRateableMesh":
            from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _493

            return self._parent._cast(_493.PlasticGearVDI2736AbstractRateableMesh)

        @property
        def vdi2736_metal_plastic_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_498.VDI2736MetalPlasticRateableMesh":
            from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _498

            return self._parent._cast(_498.VDI2736MetalPlasticRateableMesh)

        @property
        def vdi2736_plastic_metal_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_499.VDI2736PlasticMetalRateableMesh":
            from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _499

            return self._parent._cast(_499.VDI2736PlasticMetalRateableMesh)

        @property
        def vdi2736_plastic_plastic_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_500.VDI2736PlasticPlasticRateableMesh":
            from mastapy.gears.rating.cylindrical.plastic_vdi2736 import _500

            return self._parent._cast(_500.VDI2736PlasticPlasticRateableMesh)

        @property
        def iso6336_metal_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_522.ISO6336MetalRateableMesh":
            from mastapy.gears.rating.cylindrical.iso6336 import _522

            return self._parent._cast(_522.ISO6336MetalRateableMesh)

        @property
        def iso6336_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_523.ISO6336RateableMesh":
            from mastapy.gears.rating.cylindrical.iso6336 import _523

            return self._parent._cast(_523.ISO6336RateableMesh)

        @property
        def agma2101_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_536.AGMA2101RateableMesh":
            from mastapy.gears.rating.cylindrical.agma import _536

            return self._parent._cast(_536.AGMA2101RateableMesh)

        @property
        def conical_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_547.ConicalRateableMesh":
            from mastapy.gears.rating.conical import _547

            return self._parent._cast(_547.ConicalRateableMesh)

        @property
        def spiral_bevel_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_564.SpiralBevelRateableMesh":
            from mastapy.gears.rating.bevel.standards import _564

            return self._parent._cast(_564.SpiralBevelRateableMesh)

        @property
        def agma_gleason_conical_rateable_mesh(
            self: "RateableMesh._Cast_RateableMesh",
        ) -> "_568.AGMAGleasonConicalRateableMesh":
            from mastapy.gears.rating.agma_gleason_conical import _568

            return self._parent._cast(_568.AGMAGleasonConicalRateableMesh)

        @property
        def rateable_mesh(self: "RateableMesh._Cast_RateableMesh") -> "RateableMesh":
            return self._parent

        def __getattr__(self: "RateableMesh._Cast_RateableMesh", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "RateableMesh.TYPE"):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(self: Self) -> "RateableMesh._Cast_RateableMesh":
        return self._Cast_RateableMesh(self)
