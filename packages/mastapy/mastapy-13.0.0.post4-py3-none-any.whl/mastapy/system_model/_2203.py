"""DesignEntity"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, List

from PIL.Image import Image

from mastapy._internal.type_enforcement import enforce_parameter_types
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from mastapy.system_model import _2200
    from mastapy.utility.model_validation import _1794, _1793
    from mastapy.utility.scripting import _1741
    from mastapy.system_model.connections_and_sockets import (
        _2265,
        _2268,
        _2269,
        _2272,
        _2273,
        _2281,
        _2287,
        _2292,
        _2295,
    )
    from mastapy.system_model.connections_and_sockets.gears import (
        _2299,
        _2301,
        _2303,
        _2305,
        _2307,
        _2309,
        _2311,
        _2313,
        _2315,
        _2318,
        _2319,
        _2320,
        _2323,
        _2325,
        _2327,
        _2329,
        _2331,
    )
    from mastapy.system_model.connections_and_sockets.cycloidal import (
        _2335,
        _2338,
        _2341,
    )
    from mastapy.system_model.connections_and_sockets.couplings import (
        _2342,
        _2344,
        _2346,
        _2348,
        _2350,
        _2352,
    )
    from mastapy.system_model.part_model import (
        _2433,
        _2434,
        _2435,
        _2436,
        _2439,
        _2442,
        _2443,
        _2444,
        _2447,
        _2448,
        _2452,
        _2453,
        _2454,
        _2455,
        _2462,
        _2463,
        _2464,
        _2466,
        _2468,
        _2469,
        _2471,
        _2472,
        _2474,
        _2476,
        _2477,
        _2479,
    )
    from mastapy.system_model.part_model.shaft_model import _2482
    from mastapy.system_model.part_model.gears import (
        _2513,
        _2514,
        _2515,
        _2516,
        _2517,
        _2518,
        _2519,
        _2520,
        _2521,
        _2522,
        _2523,
        _2524,
        _2525,
        _2526,
        _2527,
        _2528,
        _2529,
        _2530,
        _2532,
        _2534,
        _2535,
        _2536,
        _2537,
        _2538,
        _2539,
        _2540,
        _2541,
        _2542,
        _2543,
        _2544,
        _2545,
        _2546,
        _2547,
        _2548,
        _2549,
        _2550,
        _2551,
        _2552,
        _2553,
        _2554,
    )
    from mastapy.system_model.part_model.cycloidal import _2568, _2569, _2570
    from mastapy.system_model.part_model.couplings import (
        _2576,
        _2578,
        _2579,
        _2581,
        _2582,
        _2583,
        _2584,
        _2586,
        _2587,
        _2588,
        _2589,
        _2590,
        _2596,
        _2597,
        _2598,
        _2600,
        _2601,
        _2602,
        _2604,
        _2605,
        _2606,
        _2607,
        _2608,
        _2610,
    )


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


Self = TypeVar("Self", bound="DesignEntity")


class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE = _DESIGN_ENTITY
    _CastSelf = TypeVar("_CastSelf", bound="_Cast_DesignEntity")

    class _Cast_DesignEntity:
        """Special nested class for casting DesignEntity to subclasses."""

        def __init__(self: "DesignEntity._Cast_DesignEntity", parent: "DesignEntity"):
            self._parent = parent

        @property
        def abstract_shaft_to_mountable_component_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2265.AbstractShaftToMountableComponentConnection":
            from mastapy.system_model.connections_and_sockets import _2265

            return self._parent._cast(_2265.AbstractShaftToMountableComponentConnection)

        @property
        def belt_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2268.BeltConnection":
            from mastapy.system_model.connections_and_sockets import _2268

            return self._parent._cast(_2268.BeltConnection)

        @property
        def coaxial_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2269.CoaxialConnection":
            from mastapy.system_model.connections_and_sockets import _2269

            return self._parent._cast(_2269.CoaxialConnection)

        @property
        def connection(self: "DesignEntity._Cast_DesignEntity") -> "_2272.Connection":
            from mastapy.system_model.connections_and_sockets import _2272

            return self._parent._cast(_2272.Connection)

        @property
        def cvt_belt_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2273.CVTBeltConnection":
            from mastapy.system_model.connections_and_sockets import _2273

            return self._parent._cast(_2273.CVTBeltConnection)

        @property
        def inter_mountable_component_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2281.InterMountableComponentConnection":
            from mastapy.system_model.connections_and_sockets import _2281

            return self._parent._cast(_2281.InterMountableComponentConnection)

        @property
        def planetary_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2287.PlanetaryConnection":
            from mastapy.system_model.connections_and_sockets import _2287

            return self._parent._cast(_2287.PlanetaryConnection)

        @property
        def rolling_ring_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2292.RollingRingConnection":
            from mastapy.system_model.connections_and_sockets import _2292

            return self._parent._cast(_2292.RollingRingConnection)

        @property
        def shaft_to_mountable_component_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2295.ShaftToMountableComponentConnection":
            from mastapy.system_model.connections_and_sockets import _2295

            return self._parent._cast(_2295.ShaftToMountableComponentConnection)

        @property
        def agma_gleason_conical_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2299.AGMAGleasonConicalGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2299

            return self._parent._cast(_2299.AGMAGleasonConicalGearMesh)

        @property
        def bevel_differential_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2301.BevelDifferentialGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2301

            return self._parent._cast(_2301.BevelDifferentialGearMesh)

        @property
        def bevel_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2303.BevelGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2303

            return self._parent._cast(_2303.BevelGearMesh)

        @property
        def concept_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2305.ConceptGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2305

            return self._parent._cast(_2305.ConceptGearMesh)

        @property
        def conical_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2307.ConicalGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2307

            return self._parent._cast(_2307.ConicalGearMesh)

        @property
        def cylindrical_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2309.CylindricalGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2309

            return self._parent._cast(_2309.CylindricalGearMesh)

        @property
        def face_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2311.FaceGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2311

            return self._parent._cast(_2311.FaceGearMesh)

        @property
        def gear_mesh(self: "DesignEntity._Cast_DesignEntity") -> "_2313.GearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2313

            return self._parent._cast(_2313.GearMesh)

        @property
        def hypoid_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2315.HypoidGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2315

            return self._parent._cast(_2315.HypoidGearMesh)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2318.KlingelnbergCycloPalloidConicalGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2318

            return self._parent._cast(_2318.KlingelnbergCycloPalloidConicalGearMesh)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2319.KlingelnbergCycloPalloidHypoidGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2319

            return self._parent._cast(_2319.KlingelnbergCycloPalloidHypoidGearMesh)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2320.KlingelnbergCycloPalloidSpiralBevelGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2320

            return self._parent._cast(_2320.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        @property
        def spiral_bevel_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2323.SpiralBevelGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2323

            return self._parent._cast(_2323.SpiralBevelGearMesh)

        @property
        def straight_bevel_diff_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2325.StraightBevelDiffGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2325

            return self._parent._cast(_2325.StraightBevelDiffGearMesh)

        @property
        def straight_bevel_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2327.StraightBevelGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2327

            return self._parent._cast(_2327.StraightBevelGearMesh)

        @property
        def worm_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2329.WormGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2329

            return self._parent._cast(_2329.WormGearMesh)

        @property
        def zerol_bevel_gear_mesh(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2331.ZerolBevelGearMesh":
            from mastapy.system_model.connections_and_sockets.gears import _2331

            return self._parent._cast(_2331.ZerolBevelGearMesh)

        @property
        def cycloidal_disc_central_bearing_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2335.CycloidalDiscCentralBearingConnection":
            from mastapy.system_model.connections_and_sockets.cycloidal import _2335

            return self._parent._cast(_2335.CycloidalDiscCentralBearingConnection)

        @property
        def cycloidal_disc_planetary_bearing_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2338.CycloidalDiscPlanetaryBearingConnection":
            from mastapy.system_model.connections_and_sockets.cycloidal import _2338

            return self._parent._cast(_2338.CycloidalDiscPlanetaryBearingConnection)

        @property
        def ring_pins_to_disc_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2341.RingPinsToDiscConnection":
            from mastapy.system_model.connections_and_sockets.cycloidal import _2341

            return self._parent._cast(_2341.RingPinsToDiscConnection)

        @property
        def clutch_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2342.ClutchConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2342

            return self._parent._cast(_2342.ClutchConnection)

        @property
        def concept_coupling_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2344.ConceptCouplingConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2344

            return self._parent._cast(_2344.ConceptCouplingConnection)

        @property
        def coupling_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2346.CouplingConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2346

            return self._parent._cast(_2346.CouplingConnection)

        @property
        def part_to_part_shear_coupling_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2348.PartToPartShearCouplingConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2348

            return self._parent._cast(_2348.PartToPartShearCouplingConnection)

        @property
        def spring_damper_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2350.SpringDamperConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2350

            return self._parent._cast(_2350.SpringDamperConnection)

        @property
        def torque_converter_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2352.TorqueConverterConnection":
            from mastapy.system_model.connections_and_sockets.couplings import _2352

            return self._parent._cast(_2352.TorqueConverterConnection)

        @property
        def assembly(self: "DesignEntity._Cast_DesignEntity") -> "_2433.Assembly":
            from mastapy.system_model.part_model import _2433

            return self._parent._cast(_2433.Assembly)

        @property
        def abstract_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2434.AbstractAssembly":
            from mastapy.system_model.part_model import _2434

            return self._parent._cast(_2434.AbstractAssembly)

        @property
        def abstract_shaft(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2435.AbstractShaft":
            from mastapy.system_model.part_model import _2435

            return self._parent._cast(_2435.AbstractShaft)

        @property
        def abstract_shaft_or_housing(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2436.AbstractShaftOrHousing":
            from mastapy.system_model.part_model import _2436

            return self._parent._cast(_2436.AbstractShaftOrHousing)

        @property
        def bearing(self: "DesignEntity._Cast_DesignEntity") -> "_2439.Bearing":
            from mastapy.system_model.part_model import _2439

            return self._parent._cast(_2439.Bearing)

        @property
        def bolt(self: "DesignEntity._Cast_DesignEntity") -> "_2442.Bolt":
            from mastapy.system_model.part_model import _2442

            return self._parent._cast(_2442.Bolt)

        @property
        def bolted_joint(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2443.BoltedJoint":
            from mastapy.system_model.part_model import _2443

            return self._parent._cast(_2443.BoltedJoint)

        @property
        def component(self: "DesignEntity._Cast_DesignEntity") -> "_2444.Component":
            from mastapy.system_model.part_model import _2444

            return self._parent._cast(_2444.Component)

        @property
        def connector(self: "DesignEntity._Cast_DesignEntity") -> "_2447.Connector":
            from mastapy.system_model.part_model import _2447

            return self._parent._cast(_2447.Connector)

        @property
        def datum(self: "DesignEntity._Cast_DesignEntity") -> "_2448.Datum":
            from mastapy.system_model.part_model import _2448

            return self._parent._cast(_2448.Datum)

        @property
        def external_cad_model(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2452.ExternalCADModel":
            from mastapy.system_model.part_model import _2452

            return self._parent._cast(_2452.ExternalCADModel)

        @property
        def fe_part(self: "DesignEntity._Cast_DesignEntity") -> "_2453.FEPart":
            from mastapy.system_model.part_model import _2453

            return self._parent._cast(_2453.FEPart)

        @property
        def flexible_pin_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2454.FlexiblePinAssembly":
            from mastapy.system_model.part_model import _2454

            return self._parent._cast(_2454.FlexiblePinAssembly)

        @property
        def guide_dxf_model(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2455.GuideDxfModel":
            from mastapy.system_model.part_model import _2455

            return self._parent._cast(_2455.GuideDxfModel)

        @property
        def mass_disc(self: "DesignEntity._Cast_DesignEntity") -> "_2462.MassDisc":
            from mastapy.system_model.part_model import _2462

            return self._parent._cast(_2462.MassDisc)

        @property
        def measurement_component(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2463.MeasurementComponent":
            from mastapy.system_model.part_model import _2463

            return self._parent._cast(_2463.MeasurementComponent)

        @property
        def mountable_component(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2464.MountableComponent":
            from mastapy.system_model.part_model import _2464

            return self._parent._cast(_2464.MountableComponent)

        @property
        def oil_seal(self: "DesignEntity._Cast_DesignEntity") -> "_2466.OilSeal":
            from mastapy.system_model.part_model import _2466

            return self._parent._cast(_2466.OilSeal)

        @property
        def part(self: "DesignEntity._Cast_DesignEntity") -> "_2468.Part":
            from mastapy.system_model.part_model import _2468

            return self._parent._cast(_2468.Part)

        @property
        def planet_carrier(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2469.PlanetCarrier":
            from mastapy.system_model.part_model import _2469

            return self._parent._cast(_2469.PlanetCarrier)

        @property
        def point_load(self: "DesignEntity._Cast_DesignEntity") -> "_2471.PointLoad":
            from mastapy.system_model.part_model import _2471

            return self._parent._cast(_2471.PointLoad)

        @property
        def power_load(self: "DesignEntity._Cast_DesignEntity") -> "_2472.PowerLoad":
            from mastapy.system_model.part_model import _2472

            return self._parent._cast(_2472.PowerLoad)

        @property
        def root_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2474.RootAssembly":
            from mastapy.system_model.part_model import _2474

            return self._parent._cast(_2474.RootAssembly)

        @property
        def specialised_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2476.SpecialisedAssembly":
            from mastapy.system_model.part_model import _2476

            return self._parent._cast(_2476.SpecialisedAssembly)

        @property
        def unbalanced_mass(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2477.UnbalancedMass":
            from mastapy.system_model.part_model import _2477

            return self._parent._cast(_2477.UnbalancedMass)

        @property
        def virtual_component(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2479.VirtualComponent":
            from mastapy.system_model.part_model import _2479

            return self._parent._cast(_2479.VirtualComponent)

        @property
        def shaft(self: "DesignEntity._Cast_DesignEntity") -> "_2482.Shaft":
            from mastapy.system_model.part_model.shaft_model import _2482

            return self._parent._cast(_2482.Shaft)

        @property
        def agma_gleason_conical_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2513.AGMAGleasonConicalGear":
            from mastapy.system_model.part_model.gears import _2513

            return self._parent._cast(_2513.AGMAGleasonConicalGear)

        @property
        def agma_gleason_conical_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2514.AGMAGleasonConicalGearSet":
            from mastapy.system_model.part_model.gears import _2514

            return self._parent._cast(_2514.AGMAGleasonConicalGearSet)

        @property
        def bevel_differential_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2515.BevelDifferentialGear":
            from mastapy.system_model.part_model.gears import _2515

            return self._parent._cast(_2515.BevelDifferentialGear)

        @property
        def bevel_differential_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2516.BevelDifferentialGearSet":
            from mastapy.system_model.part_model.gears import _2516

            return self._parent._cast(_2516.BevelDifferentialGearSet)

        @property
        def bevel_differential_planet_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2517.BevelDifferentialPlanetGear":
            from mastapy.system_model.part_model.gears import _2517

            return self._parent._cast(_2517.BevelDifferentialPlanetGear)

        @property
        def bevel_differential_sun_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2518.BevelDifferentialSunGear":
            from mastapy.system_model.part_model.gears import _2518

            return self._parent._cast(_2518.BevelDifferentialSunGear)

        @property
        def bevel_gear(self: "DesignEntity._Cast_DesignEntity") -> "_2519.BevelGear":
            from mastapy.system_model.part_model.gears import _2519

            return self._parent._cast(_2519.BevelGear)

        @property
        def bevel_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2520.BevelGearSet":
            from mastapy.system_model.part_model.gears import _2520

            return self._parent._cast(_2520.BevelGearSet)

        @property
        def concept_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2521.ConceptGear":
            from mastapy.system_model.part_model.gears import _2521

            return self._parent._cast(_2521.ConceptGear)

        @property
        def concept_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2522.ConceptGearSet":
            from mastapy.system_model.part_model.gears import _2522

            return self._parent._cast(_2522.ConceptGearSet)

        @property
        def conical_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2523.ConicalGear":
            from mastapy.system_model.part_model.gears import _2523

            return self._parent._cast(_2523.ConicalGear)

        @property
        def conical_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2524.ConicalGearSet":
            from mastapy.system_model.part_model.gears import _2524

            return self._parent._cast(_2524.ConicalGearSet)

        @property
        def cylindrical_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2525.CylindricalGear":
            from mastapy.system_model.part_model.gears import _2525

            return self._parent._cast(_2525.CylindricalGear)

        @property
        def cylindrical_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2526.CylindricalGearSet":
            from mastapy.system_model.part_model.gears import _2526

            return self._parent._cast(_2526.CylindricalGearSet)

        @property
        def cylindrical_planet_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2527.CylindricalPlanetGear":
            from mastapy.system_model.part_model.gears import _2527

            return self._parent._cast(_2527.CylindricalPlanetGear)

        @property
        def face_gear(self: "DesignEntity._Cast_DesignEntity") -> "_2528.FaceGear":
            from mastapy.system_model.part_model.gears import _2528

            return self._parent._cast(_2528.FaceGear)

        @property
        def face_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2529.FaceGearSet":
            from mastapy.system_model.part_model.gears import _2529

            return self._parent._cast(_2529.FaceGearSet)

        @property
        def gear(self: "DesignEntity._Cast_DesignEntity") -> "_2530.Gear":
            from mastapy.system_model.part_model.gears import _2530

            return self._parent._cast(_2530.Gear)

        @property
        def gear_set(self: "DesignEntity._Cast_DesignEntity") -> "_2532.GearSet":
            from mastapy.system_model.part_model.gears import _2532

            return self._parent._cast(_2532.GearSet)

        @property
        def hypoid_gear(self: "DesignEntity._Cast_DesignEntity") -> "_2534.HypoidGear":
            from mastapy.system_model.part_model.gears import _2534

            return self._parent._cast(_2534.HypoidGear)

        @property
        def hypoid_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2535.HypoidGearSet":
            from mastapy.system_model.part_model.gears import _2535

            return self._parent._cast(_2535.HypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_conical_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2536.KlingelnbergCycloPalloidConicalGear":
            from mastapy.system_model.part_model.gears import _2536

            return self._parent._cast(_2536.KlingelnbergCycloPalloidConicalGear)

        @property
        def klingelnberg_cyclo_palloid_conical_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2537.KlingelnbergCycloPalloidConicalGearSet":
            from mastapy.system_model.part_model.gears import _2537

            return self._parent._cast(_2537.KlingelnbergCycloPalloidConicalGearSet)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2538.KlingelnbergCycloPalloidHypoidGear":
            from mastapy.system_model.part_model.gears import _2538

            return self._parent._cast(_2538.KlingelnbergCycloPalloidHypoidGear)

        @property
        def klingelnberg_cyclo_palloid_hypoid_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2539.KlingelnbergCycloPalloidHypoidGearSet":
            from mastapy.system_model.part_model.gears import _2539

            return self._parent._cast(_2539.KlingelnbergCycloPalloidHypoidGearSet)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2540.KlingelnbergCycloPalloidSpiralBevelGear":
            from mastapy.system_model.part_model.gears import _2540

            return self._parent._cast(_2540.KlingelnbergCycloPalloidSpiralBevelGear)

        @property
        def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2541.KlingelnbergCycloPalloidSpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2541

            return self._parent._cast(_2541.KlingelnbergCycloPalloidSpiralBevelGearSet)

        @property
        def planetary_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2542.PlanetaryGearSet":
            from mastapy.system_model.part_model.gears import _2542

            return self._parent._cast(_2542.PlanetaryGearSet)

        @property
        def spiral_bevel_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2543.SpiralBevelGear":
            from mastapy.system_model.part_model.gears import _2543

            return self._parent._cast(_2543.SpiralBevelGear)

        @property
        def spiral_bevel_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2544.SpiralBevelGearSet":
            from mastapy.system_model.part_model.gears import _2544

            return self._parent._cast(_2544.SpiralBevelGearSet)

        @property
        def straight_bevel_diff_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2545.StraightBevelDiffGear":
            from mastapy.system_model.part_model.gears import _2545

            return self._parent._cast(_2545.StraightBevelDiffGear)

        @property
        def straight_bevel_diff_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2546.StraightBevelDiffGearSet":
            from mastapy.system_model.part_model.gears import _2546

            return self._parent._cast(_2546.StraightBevelDiffGearSet)

        @property
        def straight_bevel_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2547.StraightBevelGear":
            from mastapy.system_model.part_model.gears import _2547

            return self._parent._cast(_2547.StraightBevelGear)

        @property
        def straight_bevel_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2548.StraightBevelGearSet":
            from mastapy.system_model.part_model.gears import _2548

            return self._parent._cast(_2548.StraightBevelGearSet)

        @property
        def straight_bevel_planet_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2549.StraightBevelPlanetGear":
            from mastapy.system_model.part_model.gears import _2549

            return self._parent._cast(_2549.StraightBevelPlanetGear)

        @property
        def straight_bevel_sun_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2550.StraightBevelSunGear":
            from mastapy.system_model.part_model.gears import _2550

            return self._parent._cast(_2550.StraightBevelSunGear)

        @property
        def worm_gear(self: "DesignEntity._Cast_DesignEntity") -> "_2551.WormGear":
            from mastapy.system_model.part_model.gears import _2551

            return self._parent._cast(_2551.WormGear)

        @property
        def worm_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2552.WormGearSet":
            from mastapy.system_model.part_model.gears import _2552

            return self._parent._cast(_2552.WormGearSet)

        @property
        def zerol_bevel_gear(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2553.ZerolBevelGear":
            from mastapy.system_model.part_model.gears import _2553

            return self._parent._cast(_2553.ZerolBevelGear)

        @property
        def zerol_bevel_gear_set(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2554.ZerolBevelGearSet":
            from mastapy.system_model.part_model.gears import _2554

            return self._parent._cast(_2554.ZerolBevelGearSet)

        @property
        def cycloidal_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2568.CycloidalAssembly":
            from mastapy.system_model.part_model.cycloidal import _2568

            return self._parent._cast(_2568.CycloidalAssembly)

        @property
        def cycloidal_disc(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2569.CycloidalDisc":
            from mastapy.system_model.part_model.cycloidal import _2569

            return self._parent._cast(_2569.CycloidalDisc)

        @property
        def ring_pins(self: "DesignEntity._Cast_DesignEntity") -> "_2570.RingPins":
            from mastapy.system_model.part_model.cycloidal import _2570

            return self._parent._cast(_2570.RingPins)

        @property
        def belt_drive(self: "DesignEntity._Cast_DesignEntity") -> "_2576.BeltDrive":
            from mastapy.system_model.part_model.couplings import _2576

            return self._parent._cast(_2576.BeltDrive)

        @property
        def clutch(self: "DesignEntity._Cast_DesignEntity") -> "_2578.Clutch":
            from mastapy.system_model.part_model.couplings import _2578

            return self._parent._cast(_2578.Clutch)

        @property
        def clutch_half(self: "DesignEntity._Cast_DesignEntity") -> "_2579.ClutchHalf":
            from mastapy.system_model.part_model.couplings import _2579

            return self._parent._cast(_2579.ClutchHalf)

        @property
        def concept_coupling(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2581.ConceptCoupling":
            from mastapy.system_model.part_model.couplings import _2581

            return self._parent._cast(_2581.ConceptCoupling)

        @property
        def concept_coupling_half(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2582.ConceptCouplingHalf":
            from mastapy.system_model.part_model.couplings import _2582

            return self._parent._cast(_2582.ConceptCouplingHalf)

        @property
        def coupling(self: "DesignEntity._Cast_DesignEntity") -> "_2583.Coupling":
            from mastapy.system_model.part_model.couplings import _2583

            return self._parent._cast(_2583.Coupling)

        @property
        def coupling_half(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2584.CouplingHalf":
            from mastapy.system_model.part_model.couplings import _2584

            return self._parent._cast(_2584.CouplingHalf)

        @property
        def cvt(self: "DesignEntity._Cast_DesignEntity") -> "_2586.CVT":
            from mastapy.system_model.part_model.couplings import _2586

            return self._parent._cast(_2586.CVT)

        @property
        def cvt_pulley(self: "DesignEntity._Cast_DesignEntity") -> "_2587.CVTPulley":
            from mastapy.system_model.part_model.couplings import _2587

            return self._parent._cast(_2587.CVTPulley)

        @property
        def part_to_part_shear_coupling(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2588.PartToPartShearCoupling":
            from mastapy.system_model.part_model.couplings import _2588

            return self._parent._cast(_2588.PartToPartShearCoupling)

        @property
        def part_to_part_shear_coupling_half(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2589.PartToPartShearCouplingHalf":
            from mastapy.system_model.part_model.couplings import _2589

            return self._parent._cast(_2589.PartToPartShearCouplingHalf)

        @property
        def pulley(self: "DesignEntity._Cast_DesignEntity") -> "_2590.Pulley":
            from mastapy.system_model.part_model.couplings import _2590

            return self._parent._cast(_2590.Pulley)

        @property
        def rolling_ring(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2596.RollingRing":
            from mastapy.system_model.part_model.couplings import _2596

            return self._parent._cast(_2596.RollingRing)

        @property
        def rolling_ring_assembly(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2597.RollingRingAssembly":
            from mastapy.system_model.part_model.couplings import _2597

            return self._parent._cast(_2597.RollingRingAssembly)

        @property
        def shaft_hub_connection(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2598.ShaftHubConnection":
            from mastapy.system_model.part_model.couplings import _2598

            return self._parent._cast(_2598.ShaftHubConnection)

        @property
        def spring_damper(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2600.SpringDamper":
            from mastapy.system_model.part_model.couplings import _2600

            return self._parent._cast(_2600.SpringDamper)

        @property
        def spring_damper_half(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2601.SpringDamperHalf":
            from mastapy.system_model.part_model.couplings import _2601

            return self._parent._cast(_2601.SpringDamperHalf)

        @property
        def synchroniser(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2602.Synchroniser":
            from mastapy.system_model.part_model.couplings import _2602

            return self._parent._cast(_2602.Synchroniser)

        @property
        def synchroniser_half(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2604.SynchroniserHalf":
            from mastapy.system_model.part_model.couplings import _2604

            return self._parent._cast(_2604.SynchroniserHalf)

        @property
        def synchroniser_part(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2605.SynchroniserPart":
            from mastapy.system_model.part_model.couplings import _2605

            return self._parent._cast(_2605.SynchroniserPart)

        @property
        def synchroniser_sleeve(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2606.SynchroniserSleeve":
            from mastapy.system_model.part_model.couplings import _2606

            return self._parent._cast(_2606.SynchroniserSleeve)

        @property
        def torque_converter(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2607.TorqueConverter":
            from mastapy.system_model.part_model.couplings import _2607

            return self._parent._cast(_2607.TorqueConverter)

        @property
        def torque_converter_pump(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2608.TorqueConverterPump":
            from mastapy.system_model.part_model.couplings import _2608

            return self._parent._cast(_2608.TorqueConverterPump)

        @property
        def torque_converter_turbine(
            self: "DesignEntity._Cast_DesignEntity",
        ) -> "_2610.TorqueConverterTurbine":
            from mastapy.system_model.part_model.couplings import _2610

            return self._parent._cast(_2610.TorqueConverterTurbine)

        @property
        def design_entity(self: "DesignEntity._Cast_DesignEntity") -> "DesignEntity":
            return self._parent

        def __getattr__(self: "DesignEntity._Cast_DesignEntity", name: str):
            try:
                return self.__dict__[name]
            except KeyError:
                class_name = "".join(n.capitalize() for n in name.split("_"))
                raise CastException(
                    f'Detected an invalid cast. Cannot cast to type "{class_name}"'
                ) from None

    def __init__(self: Self, instance_to_wrap: "DesignEntity.TYPE"):
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
    def id(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.ID

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.Icon

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: Self) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = self.wrapped.SmallIcon

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def unique_name(self: Self) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = self.wrapped.UniqueName

        if temp is None:
            return ""

        return temp

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
    def all_design_entities(self: Self) -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = self.wrapped.AllDesignEntities

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def user_specified_data(self: Self) -> "_1741.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = self.wrapped.UserSpecifiedData

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

    def delete(self: Self):
        """Method does not return."""
        self.wrapped.Delete()

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
    def cast_to(self: Self) -> "DesignEntity._Cast_DesignEntity":
        return self._Cast_DesignEntity(self)
