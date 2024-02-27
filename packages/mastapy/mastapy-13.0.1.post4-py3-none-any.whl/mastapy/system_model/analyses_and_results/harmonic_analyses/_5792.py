"""PeriodicExcitationWithReferenceShaft"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5679
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "PeriodicExcitationWithReferenceShaft",
)

if TYPE_CHECKING:
    from mastapy.system_model.analyses_and_results.harmonic_analyses import (
        _5733,
        _5734,
        _5735,
        _5736,
        _5737,
        _5738,
        _5739,
        _5740,
        _5741,
        _5742,
        _5743,
        _5744,
        _5759,
        _5809,
        _5835,
    )


__docformat__ = "restructuredtext en"
__all__ = ("PeriodicExcitationWithReferenceShaft",)


Self = TypeVar("Self", bound="PeriodicExcitationWithReferenceShaft")


class PeriodicExcitationWithReferenceShaft(_5679.AbstractPeriodicExcitationDetail):
    """PeriodicExcitationWithReferenceShaft

    This is a mastapy class.
    """

    TYPE = _PERIODIC_EXCITATION_WITH_REFERENCE_SHAFT
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_PeriodicExcitationWithReferenceShaft")

    class _Cast_PeriodicExcitationWithReferenceShaft:
        """Special nested class for casting PeriodicExcitationWithReferenceShaft to subclasses."""

        def __init__(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
            parent: "PeriodicExcitationWithReferenceShaft",
        ):
            self._parent = parent

        @property
        def abstract_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5679.AbstractPeriodicExcitationDetail":
            return self._parent._cast(_5679.AbstractPeriodicExcitationDetail)

        @property
        def electric_machine_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5733.ElectricMachinePeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5733,
            )

            return self._parent._cast(_5733.ElectricMachinePeriodicExcitationDetail)

        @property
        def electric_machine_rotor_x_force_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5734.ElectricMachineRotorXForcePeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5734,
            )

            return self._parent._cast(
                _5734.ElectricMachineRotorXForcePeriodicExcitationDetail
            )

        @property
        def electric_machine_rotor_x_moment_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5735.ElectricMachineRotorXMomentPeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5735,
            )

            return self._parent._cast(
                _5735.ElectricMachineRotorXMomentPeriodicExcitationDetail
            )

        @property
        def electric_machine_rotor_y_force_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5736.ElectricMachineRotorYForcePeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5736,
            )

            return self._parent._cast(
                _5736.ElectricMachineRotorYForcePeriodicExcitationDetail
            )

        @property
        def electric_machine_rotor_y_moment_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5737.ElectricMachineRotorYMomentPeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5737,
            )

            return self._parent._cast(
                _5737.ElectricMachineRotorYMomentPeriodicExcitationDetail
            )

        @property
        def electric_machine_rotor_z_force_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5738.ElectricMachineRotorZForcePeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5738,
            )

            return self._parent._cast(
                _5738.ElectricMachineRotorZForcePeriodicExcitationDetail
            )

        @property
        def electric_machine_stator_tooth_axial_loads_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5739.ElectricMachineStatorToothAxialLoadsExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5739,
            )

            return self._parent._cast(
                _5739.ElectricMachineStatorToothAxialLoadsExcitationDetail
            )

        @property
        def electric_machine_stator_tooth_loads_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5740.ElectricMachineStatorToothLoadsExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5740,
            )

            return self._parent._cast(
                _5740.ElectricMachineStatorToothLoadsExcitationDetail
            )

        @property
        def electric_machine_stator_tooth_moments_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5741.ElectricMachineStatorToothMomentsExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5741,
            )

            return self._parent._cast(
                _5741.ElectricMachineStatorToothMomentsExcitationDetail
            )

        @property
        def electric_machine_stator_tooth_radial_loads_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5742.ElectricMachineStatorToothRadialLoadsExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5742,
            )

            return self._parent._cast(
                _5742.ElectricMachineStatorToothRadialLoadsExcitationDetail
            )

        @property
        def electric_machine_stator_tooth_tangential_loads_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5743.ElectricMachineStatorToothTangentialLoadsExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5743,
            )

            return self._parent._cast(
                _5743.ElectricMachineStatorToothTangentialLoadsExcitationDetail
            )

        @property
        def electric_machine_torque_ripple_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5744.ElectricMachineTorqueRipplePeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5744,
            )

            return self._parent._cast(
                _5744.ElectricMachineTorqueRipplePeriodicExcitationDetail
            )

        @property
        def general_periodic_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5759.GeneralPeriodicExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5759,
            )

            return self._parent._cast(_5759.GeneralPeriodicExcitationDetail)

        @property
        def single_node_periodic_excitation_with_reference_shaft(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5809.SingleNodePeriodicExcitationWithReferenceShaft":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5809,
            )

            return self._parent._cast(
                _5809.SingleNodePeriodicExcitationWithReferenceShaft
            )

        @property
        def unbalanced_mass_excitation_detail(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "_5835.UnbalancedMassExcitationDetail":
            from mastapy.system_model.analyses_and_results.harmonic_analyses import (
                _5835,
            )

            return self._parent._cast(_5835.UnbalancedMassExcitationDetail)

        @property
        def periodic_excitation_with_reference_shaft(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
        ) -> "PeriodicExcitationWithReferenceShaft":
            return self._parent

        def __getattr__(
            self: "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft",
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
        self: Self, instance_to_wrap: "PeriodicExcitationWithReferenceShaft.TYPE"
    ):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def cast_to(
        self: Self,
    ) -> "PeriodicExcitationWithReferenceShaft._Cast_PeriodicExcitationWithReferenceShaft":
        return self._Cast_PeriodicExcitationWithReferenceShaft(self)
