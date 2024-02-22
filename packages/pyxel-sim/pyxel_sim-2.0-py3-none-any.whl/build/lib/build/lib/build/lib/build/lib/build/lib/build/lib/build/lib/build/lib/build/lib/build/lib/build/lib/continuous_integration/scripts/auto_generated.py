#  Copyright (c) European Space Agency, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

######################################
# Note: This code is auto-generated. #
#       Don't modify it !            #
######################################

import collections
import json
import pathlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Any, Iterator, Literal, Mapping, Optional, Sequence, Tuple, Union

import click
from apischema import schema
from apischema.json_schema import JsonSchemaVersion, deserialization_schema


@schema(title='Parameters')
@dataclass
class ModelLoadSaveDetectorArguments(Mapping[str, Any]):
    filename: float = field(
    metadata=schema(title='filename', description='Filename to load/save.')
)

@dataclass
class ModelLoadDetector:
    name: str
    arguments: ModelLoadSaveDetectorArguments
    func: Literal['pyxel.models.load_detector'] = 'pyxel.models.load_detector'
    enabled: bool = True

@dataclass
class ModelSaveDetector:
    name: str
    arguments: ModelLoadSaveDetectorArguments
    func: Literal['pyxel.models.save_detector'] = 'pyxel.models.save_detector'
    enabled: bool = True

@dataclass
class ModelFunction:
    name: str
    func: str = field(metadata=schema(pattern='^(?!pyxel\.models\.)'))
    arguments: Optional[Mapping[str, Any]] = None
    enabled: bool = True


@dataclass
class ModelGroup:
    models: Sequence[ModelFunction]
    name: str


@dataclass
class DetectionPipeline:
    scene_generation: Optional[Sequence[ModelFunction]] = None
    photon_collection: Optional[Sequence[ModelFunction]] = None
    phasing: Optional[Sequence[ModelFunction]] = None
    charge_generation: Optional[Sequence[ModelFunction]] = None
    charge_collection: Optional[Sequence[ModelFunction]] = None
    charge_transfer: Optional[Sequence[ModelFunction]] = None
    charge_measurement: Optional[Sequence[ModelFunction]] = None
    signal_transfer: Optional[Sequence[ModelFunction]] = None
    readout_electronics: Optional[Sequence[ModelFunction]] = None
    data_processing: Optional[Sequence[ModelFunction]] = None


#
# Model: Scene Generation / Load Star Map
#
@schema(title='Parameters')
@dataclass
class ModelSceneGenerationLoadStarMapArguments(Mapping[str, Any]):
    right_ascension: float = field(
        metadata=schema(
            title='right_ascension'
            ,description='RA coordinate in degree.'
        )
    )
    declination: float = field(
        metadata=schema(
            title='declination'
            ,description='DEC coordinate in degree.'
        )
    )
    fov_radius: float = field(
        metadata=schema(
            title='fov_radius'
            ,description='FOV radius of telescope optics.'
        )
    )
    band: Literal['blue_photometer', 'gaia_band', 'red_photometer'] = field(
        default='blue_photometer',
        metadata=schema(
            title='band'
            ,description=(
                    "Define the band to use. Available values:  * 'blue_photometer' is the "
                    "band from 330 nm to 680 nm * 'gaia_band' is the band from 330 nm to "
                    "1050 nm * 'red_photometer' is the band from 640 nm to 1050 nm"
                )
        )
    )
    with_caching: bool = field(
        default=True,
        metadata=schema(
            title='with_caching'
            ,description='Enable/Disable caching request to GAIA catalog.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('right_ascension', 'declination', 'fov_radius', 'band', 'with_caching'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'load_star_map'"
    ,description=(
        'Generate scene from scopesim Source object loading stars from the GAIA'
        ' catalog.'
    )
)
@dataclass
class ModelSceneGenerationLoadStarMap:
    name: str
    arguments: ModelSceneGenerationLoadStarMapArguments
    func: Literal['pyxel.models.scene_generation.load_star_map'] = 'pyxel.models.scene_generation.load_star_map'
    enabled: bool = True


#
# Model: Photon Collection / Illumination
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionIlluminationArguments(Mapping[str, Any]):
    level: float = field(
        metadata=schema(
            title='level'
            ,description='Flux of photon per pixel.'
        )
    )
    option: Literal['uniform', 'rectangular', 'elliptic'] = field(
        default='uniform',
        metadata=schema(
            title='option'
            ,description=(
                    'A string indicating the type of illumination: - ``uniform`` Uniformly '
                    'fill the entire array with photon. (Default) - ``elliptic`` Mask with '
                    'elliptic object. - ``rectangular`` Mask with rectangular object.'
                )
        )
    )
    object_size: Optional[collections.abc.Sequence[int]] = field(
        default=None,
        metadata=schema(
            title='object_size'
            ,description=(
                    'List or tuple of length 2, integers defining the diameters of the '
                    'elliptic or rectangular object in vertical and horizontal directions.'
                )
        )
    )
    object_center: Optional[collections.abc.Sequence[int]] = field(
        default=None,
        metadata=schema(
            title='object_center'
            ,description=(
                    'List or tuple of length 2, two integers (row and column number), '
                    'defining the coordinates of the center of the elliptic or rectangular '
                    'object.'
                )
        )
    )
    time_scale: float = field(
        default=1.0,
        metadata=schema(
            title='time_scale'
            ,description='Time scale of the photon flux, default is 1 second. 0.001 would be ms.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('level', 'option', 'object_size', 'object_center', 'time_scale'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'illumination'"
    ,description=(
        'Generate photon uniformly over the entire array or over an elliptic or'
        ' rectangular object.'
    )
)
@dataclass
class ModelPhotonCollectionIllumination:
    name: str
    arguments: ModelPhotonCollectionIlluminationArguments
    func: Literal['pyxel.models.photon_collection.illumination'] = 'pyxel.models.photon_collection.illumination'
    enabled: bool = True


#
# Model: Photon Collection / Load Image
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionLoadImageArguments(Mapping[str, Any]):
    image_file: str = field(
        metadata=schema(
            title='image_file'
            ,description='Path to image file.'
        )
    )
    position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='position'
            ,description=(
                    'Indices of starting row and column, used when fitting image to '
                    'detector.'
                )
        )
    )
    align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='align'
            ,description=(
                    'Keyword to align the image to detector. Can be any from: ("center", '
                    '"top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    convert_to_photons: bool = field(
        default=False,
        metadata=schema(
            title='convert_to_photons'
            ,description=(
                    'If ``True``, the model converts the values of loaded image array from '
                    'ADU to photon numbers for each pixel using the Photon Transfer '
                    'Function: :math:`\\mathit{PTF} = \\mathit{quantum\\_efficiency} \\cdot '
                    '\\mathit{charge\\_to\\_voltage\\_conversion} \\cdot '
                    '\\mathit{pre\\_amplification} \\cdot \\mathit{adc\\_factor}`.'
                )
        )
    )
    multiplier: float = field(
        default=1.0,
        metadata=schema(
            title='multiplier'
            ,description='Multiply photon array level with a custom number.'
        )
    )
    time_scale: float = field(
        default=1.0,
        metadata=schema(
            title='time_scale'
            ,description='Time scale of the photon flux, default is 1 second. 0.001 would be ms.'
        )
    )
    bit_resolution: Optional[int] = field(
        default=None,
        metadata=schema(
            title='bit_resolution'
            ,description='Bit resolution of the loaded image.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('image_file', 'position', 'align', 'convert_to_photons', 'multiplier', 'time_scale', 'bit_resolution'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 7


@schema(
    title="Model 'load_image'"
    ,description=(
        'Load :term:`FITS` file as a numpy array and add to the detector as '
        'input image.'
    )
)
@dataclass
class ModelPhotonCollectionLoadImage:
    name: str
    arguments: ModelPhotonCollectionLoadImageArguments
    func: Literal['pyxel.models.photon_collection.load_image'] = 'pyxel.models.photon_collection.load_image'
    enabled: bool = True


#
# Model: Photon Collection / Load Psf
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionLoadPsfArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='Input filename of the point spread function.'
        )
    )
    normalize_kernel: bool = field(
        default=True,
        metadata=schema(
            title='normalize_kernel'
            ,description='Normalize kernel.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'normalize_kernel'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'load_psf'"
    ,description=(
        'Load a point spread function from file and convolve the photon array '
        'with the PSF.'
    )
)
@dataclass
class ModelPhotonCollectionLoadPsf:
    name: str
    arguments: ModelPhotonCollectionLoadPsfArguments
    func: Literal['pyxel.models.photon_collection.load_psf'] = 'pyxel.models.photon_collection.load_psf'
    enabled: bool = True


#
# Model: Photon Collection / Load Wavelength Psf
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionLoadWavelengthPsfArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='Input filename of the point spread function.'
        )
    )
    wavelength_col: str = field(
        metadata=schema(
            title='wavelength_col'
            ,description='Dimension name in the file that contains the wavelength information.'
        )
    )
    y_col: str = field(
        metadata=schema(
            title='y_col'
            ,description='Dimension name in the file that contains the y information.'
        )
    )
    x_col: str = field(
        metadata=schema(
            title='x_col'
            ,description='Dimension name in the file that contains the x information.'
        )
    )
    wavelength_table_name: str = field(
        metadata=schema(
            title='wavelength_table_name'
            ,description='Column name in the file that contains the wavelength information.'
        )
    )
    normalize_kernel: bool = field(
        default=True,
        metadata=schema(
            title='normalize_kernel'
            ,description='Normalize kernel.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'wavelength_col', 'y_col', 'x_col', 'wavelength_table_name', 'normalize_kernel'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 6


@schema(
    title="Model 'load_wavelength_psf'"
    ,description='Read psf files depending on simulation and instrument parameters.'
)
@dataclass
class ModelPhotonCollectionLoadWavelengthPsf:
    name: str
    arguments: ModelPhotonCollectionLoadWavelengthPsfArguments
    func: Literal['pyxel.models.photon_collection.load_wavelength_psf'] = 'pyxel.models.photon_collection.load_wavelength_psf'
    enabled: bool = True


#
# Model: Photon Collection / Optical Psf
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionOpticalPsfArguments(Mapping[str, Any]):
    fov_arcsec: float = field(
        metadata=schema(
            title='fov_arcsec'
            ,description='Field Of View on detector plane in arcsec.'
        )
    )
    optical_system: collections.abc.Sequence[collections.abc.Mapping[str, Any]] = field(
        metadata=schema(
            title='optical_system'
            ,description=(
                    'List of optical elements before detector with their specific '
                    'arguments.'
                )
        )
    )
    wavelength: Union[float, tuple[float, float], None] = field(
        default=None,
        metadata=schema(
            title='wavelength'
            ,description='Wavelength of incoming light in meters, default is None.'
        )
    )
    pixel_scale: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_scale'
            ,description='Pixel scale of detector in arcsec/pix.'
        )
    )
    apply_jitter: bool = field(
        default=False,
        metadata=schema(
            title='apply_jitter'
            ,description='Defines whether jitter should be applied, default is False.'
        )
    )
    jitter_sigma: float = field(
        default=0.007,
        metadata=schema(
            title='jitter_sigma'
            ,description='Jitter sigma value in arcsec per axis, default is 0.007.'
        )
    )
    extract_psf: bool = field(
        default=False,
        metadata=schema(
            title='extract_psf'
            ,description=(
                    'Copy the computed PSF into the data bucket '
                    "``detector.data['/photon_collection/optical_psf/[name of the "
                    "model]/psf']``"
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('fov_arcsec', 'optical_system', 'wavelength', 'pixel_scale', 'apply_jitter', 'jitter_sigma', 'extract_psf'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 7


@schema(
    title="Model 'optical_psf'"
    ,description='Model function for poppy optics model: convolve photon array with psf.'
)
@dataclass
class ModelPhotonCollectionOpticalPsf:
    name: str
    arguments: ModelPhotonCollectionOpticalPsfArguments
    func: Literal['pyxel.models.photon_collection.optical_psf'] = 'pyxel.models.photon_collection.optical_psf'
    enabled: bool = True


#
# Model: Photon Collection / Shot Noise
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionShotNoiseArguments(Mapping[str, Any]):
    type: Literal['poisson', 'normal'] = field(
        default='poisson',
        metadata=schema(
            title='type'
            ,description="Choose either 'poisson' or 'normal'. Default is Poisson noise."
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('type', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'shot_noise'"
    ,description=(
        'Add shot noise to the flux of photon per pixel. It can be either '
        'Poisson noise or Gaussian.'
    )
)
@dataclass
class ModelPhotonCollectionShotNoise:
    name: str
    arguments: ModelPhotonCollectionShotNoiseArguments = field(default_factory=ModelPhotonCollectionShotNoiseArguments)
    func: Literal['pyxel.models.photon_collection.shot_noise'] = 'pyxel.models.photon_collection.shot_noise'
    enabled: bool = True


#
# Model: Photon Collection / Simple Collection
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionSimpleCollectionArguments(Mapping[str, Any]):
    aperture: float = field(
        metadata=schema(
            title='aperture'
            ,description='Collecting area of the telescope. Unit: m.'
        )
    )
    filter_band: Optional[tuple[float, float]] = field(
        default=None,
        metadata=schema(
            title='filter_band'
            ,description='Wavelength range of selected filter band, default is None. Unit: nm.'
        )
    )
    resolution: Optional[int] = field(
        default=None,
        metadata=schema(
            title='resolution'
            ,description='Resolution of provided wavelength range in filter band. Unit: nm.'
        )
    )
    pixel_scale: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_scale'
            ,description='Pixel scale of detector, default is None. Unit: arcsec/pixel.'
        )
    )
    integrate_wavelength: bool = field(
        default=True,
        metadata=schema(
            title='integrate_wavelength'
            ,description=(
                    'If true, integrates along the wavelength else multiwavelength, default'
                    ' is True.'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('aperture', 'filter_band', 'resolution', 'pixel_scale', 'integrate_wavelength'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'simple_collection'"
    ,description='Convert scene in ph/(cm2 nm s) to photon in ph/nm s or ph s.'
)
@dataclass
class ModelPhotonCollectionSimpleCollection:
    name: str
    arguments: ModelPhotonCollectionSimpleCollectionArguments
    func: Literal['pyxel.models.photon_collection.simple_collection'] = 'pyxel.models.photon_collection.simple_collection'
    enabled: bool = True


#
# Model: Photon Collection / Stripe Pattern
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionStripePatternArguments(Mapping[str, Any]):
    period: int = field(
        default=10,
        metadata=schema(
            title='period'
            ,description='Period of the periodic pattern in pixels.'
        )
    )
    level: float = field(
        default=1.0,
        metadata=schema(
            title='level'
            ,description='Amplitude of the periodic pattern.'
        )
    )
    angle: int = field(
        default=0,
        metadata=schema(
            title='angle'
            ,description='Angle of the pattern in degrees.'
        )
    )
    startwith: int = field(
        default=0,
        metadata=schema(
            title='startwith'
            ,description='1 to start with high level or 0 for 0.'
        )
    )
    time_scale: float = field(
        default=1.0,
        metadata=schema(
            title='time_scale'
            ,description='Time scale of the photon flux, default is 1 second. 0.001 would be ms.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('period', 'level', 'angle', 'startwith', 'time_scale'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'stripe_pattern'"
    ,description='Stripe pattern model.'
)
@dataclass
class ModelPhotonCollectionStripePattern:
    name: str
    arguments: ModelPhotonCollectionStripePatternArguments = field(default_factory=ModelPhotonCollectionStripePatternArguments)
    func: Literal['pyxel.models.photon_collection.stripe_pattern'] = 'pyxel.models.photon_collection.stripe_pattern'
    enabled: bool = True


#
# Model: Photon Collection / Wavelength Dependence Airs
#
@schema(title='Parameters')
@dataclass
class ModelPhotonCollectionWavelengthDependenceAirsArguments(Mapping[str, Any]):
    psf_filename: str = field(
        metadata=schema(
            title='psf_filename'
            ,description='The location and the filename where the PSFs are located.'
        )
    )
    target_filename: str = field(
        metadata=schema(
            title='target_filename'
            ,description=(
                    'The location and the filename of the target file used in the '
                    'simulation.'
                )
        )
    )
    telescope_diameter_m1: float = field(
        metadata=schema(
            title='telescope_diameter_m1'
            ,description='Diameter of the M1 mirror of the TA in m.'
        )
    )
    telescope_diameter_m2: float = field(
        metadata=schema(
            title='telescope_diameter_m2'
            ,description='Diameter of the M2 mirror of the TA in m.'
        )
    )
    expand_factor: int = field(
        metadata=schema(
            title='expand_factor'
            ,description='Expansion factor used.'
        )
    )
    time_scale: float = field(
        default=1.0,
        metadata=schema(
            title='time_scale'
            ,description='Time scale in seconds.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('psf_filename', 'target_filename', 'telescope_diameter_m1', 'telescope_diameter_m2', 'expand_factor', 'time_scale'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 6


@schema(
    title="Model 'wavelength_dependence_airs'"
    ,description=(
        'Generate the photon over the array according to a specific dispersion '
        'pattern (ARIEL-AIRS).'
    )
)
@dataclass
class ModelPhotonCollectionWavelengthDependenceAirs:
    name: str
    arguments: ModelPhotonCollectionWavelengthDependenceAirsArguments
    func: Literal['pyxel.models.photon_collection.wavelength_dependence_airs'] = 'pyxel.models.photon_collection.wavelength_dependence_airs'
    enabled: bool = True


#
# Model: Phasing / Pulse Processing
#
@schema(title='Parameters')
@dataclass
class ModelPhasingPulseProcessingArguments(Mapping[str, Any]):
    wavelength: float = field(
        metadata=schema(
            title='wavelength'
            ,description='Wavelength. Unit: um.'
        )
    )
    responsivity: float = field(
        metadata=schema(
            title='responsivity'
            ,description='Responsivity of the pixel.'
        )
    )
    scaling_factor: float = field(
        default=250.0,
        metadata=schema(
            title='scaling_factor'
            ,description=(
                    'Scaling factor taking into account the missing pieces of '
                    'superconducting physics, as well as the resonator quality factor, the '
                    'bias power, the quasi-particle losses, etc.'
                )
        )
    )
    t_c: float = field(
        default=1.26,
        metadata=schema(
            title='t_c'
            ,description='Material dependent critical temperature. Unit: K'
        )
    )
    eta_pb: float = field(
        default=0.59,
        metadata=schema(
            title='eta_pb'
            ,description='Superconducting pair-breaking efficiency.'
        )
    )
    f: float = field(
        default=0.2,
        metadata=schema(
            title='f'
            ,description="Fano's factor."
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('wavelength', 'responsivity', 'scaling_factor', 't_c', 'eta_pb', 'f'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 6


@schema(
    title="Model 'pulse_processing'"
    ,description='Phase-pulse processor.'
)
@dataclass
class ModelPhasingPulseProcessing:
    name: str
    arguments: ModelPhasingPulseProcessingArguments
    func: Literal['pyxel.models.phasing.pulse_processing'] = 'pyxel.models.phasing.pulse_processing'
    enabled: bool = True


#
# Model: Charge Generation / Apd Gain
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationApdGainArguments(Mapping[str, Any]):
    def __iter__(self) -> Iterator[str]:
        return iter(())
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 0


@schema(
    title="Model 'apd_gain'"
    ,description='Apply APD gain.'
)
@dataclass
class ModelChargeGenerationApdGain:
    name: str
    arguments: ModelChargeGenerationApdGainArguments = field(default_factory=ModelChargeGenerationApdGainArguments)
    func: Literal['pyxel.models.charge_generation.apd_gain'] = 'pyxel.models.charge_generation.apd_gain'
    enabled: bool = True


#
# Model: Charge Generation / Apply Qe Curve
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationApplyQeCurveArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='CSV File path.'
        )
    )
    wavelength_col_name: Union[str, int] = field(
        metadata=schema(
            title='wavelength_col_name'
            ,description='Column name of wavelength in loaded file.'
        )
    )
    qe_col_name: Union[str, int] = field(
        metadata=schema(
            title='qe_col_name'
            ,description='Column name of quantum efficiency in loaded file.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'wavelength_col_name', 'qe_col_name'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'apply_qe_curve'"
    ,description='Apply wavelength dependent QE with loading a file.'
)
@dataclass
class ModelChargeGenerationApplyQeCurve:
    name: str
    arguments: ModelChargeGenerationApplyQeCurveArguments
    func: Literal['pyxel.models.charge_generation.apply_qe_curve'] = 'pyxel.models.charge_generation.apply_qe_curve'
    enabled: bool = True


#
# Model: Charge Generation / Charge Blocks
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationChargeBlocksArguments(Mapping[str, Any]):
    charge_level: float = field(
        metadata=schema(
            title='charge_level'
            ,description='Value of charges.'
        )
    )
    block_start: int = field(
        default=0,
        metadata=schema(
            title='block_start'
            ,description='Starting row of the injected charge.'
        )
    )
    block_end: Optional[int] = field(
        default=None,
        metadata=schema(
            title='block_end'
            ,description='Ending row for the injected charge.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('charge_level', 'block_start', 'block_end'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'charge_blocks'"
    ,description='Inject a block of charge into the :term:`CCD` detector.'
)
@dataclass
class ModelChargeGenerationChargeBlocks:
    name: str
    arguments: ModelChargeGenerationChargeBlocksArguments
    func: Literal['pyxel.models.charge_generation.charge_blocks'] = 'pyxel.models.charge_generation.charge_blocks'
    enabled: bool = True


#
# Model: Charge Generation / Charge Deposition
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationChargeDepositionArguments(Mapping[str, Any]):
    flux: float = field(
        metadata=schema(
            title='flux'
            ,description='the flux of incoming particles in particle/s'
        )
    )
    step_size: float = field(
        default=1.0,
        metadata=schema(
            title='step_size'
            ,description=(
                    'the size of the considered unitary step in unit length along which '
                    'energy is deposited'
                )
        )
    )
    energy_mean: float = field(
        default=1.0,
        metadata=schema(
            title='energy_mean'
            ,description='the mean energy of the incoming ionizing particles in MeV'
        )
    )
    energy_spread: float = field(
        default=0.1,
        metadata=schema(
            title='energy_spread'
            ,description='the spread in energy of the incoming ionizing particles in MeV'
        )
    )
    energy_spectrum: Union[str, pathlib.Path, None] = field(
        default=None,
        metadata=schema(
            title='energy_spectrum'
            ,description=(
                    'the location of the file describing the energy spectrum of incident '
                    'particles if no spectrum is provided energies are randomly drawn from '
                    'a normal distribution with mean and spread defined above note that the'
                    ' energy spectrum is assumed to be a txt file with two columns [energy,'
                    ' flux] with the energy in MeV'
                )
        )
    )
    energy_spectrum_sampling: Literal['linear', 'log'] = field(
        default='log',
        metadata=schema(
            title='energy_spectrum_sampling'
            ,description=(
                    '"log" or None: the energy spectrum is sampled in log space "linear" : '
                    'the energy spectrum is sampled in linear space'
                )
        )
    )
    ehpair_creation: float = field(
        default=3.65,
        metadata=schema(
            title='ehpair_creation'
            ,description=(
                    'the energy required to generate a electron-hole pair in eV by default '
                    'the Si value at room temperature is parsed i.e. 3.65 eV'
                )
        )
    )
    material_density: float = field(
        default=2.329,
        metadata=schema(
            title='material_density'
            ,description=(
                    'the material density in g/cm3 by default he Si value at room '
                    'temperature is parsed i.e. 2.3290 g/cm3'
                )
        )
    )
    particle_direction: Literal['isotropic', 'orthogonal'] = field(
        default='isotropic',
        metadata=schema(
            title='particle_direction'
            ,description=(
                    '"isotropic" : particles are coming from all directions (outside of the'
                    ' sensor) "orthogonal" : particles are coming from the top of the '
                    'sensor (thickness = 0) and orthogonal to its surface'
                )
        )
    )
    stopping_power_curve: Union[str, pathlib.Path, None] = field(
        default=None,
        metadata=schema(
            title='stopping_power_curve'
            ,description=(
                    'the location of the file describing the total massive stopping power '
                    'energetic loss per mass of material and per unit path length versus '
                    'particle energy note that the the stopping power curve is assumed to '
                    'be a csv file with two columns [energy, stopping power] energy in MeV,'
                    ' stopping power in MeV cm2/g'
                )
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('flux', 'step_size', 'energy_mean', 'energy_spread', 'energy_spectrum', 'energy_spectrum_sampling', 'ehpair_creation', 'material_density', 'particle_direction', 'stopping_power_curve', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 11


@schema(
    title="Model 'charge_deposition'"
    ,description=(
        'Simulate charge deposition by ionizing particles using a stopping '
        'power curve.'
    )
)
@dataclass
class ModelChargeGenerationChargeDeposition:
    name: str
    arguments: ModelChargeGenerationChargeDepositionArguments
    func: Literal['pyxel.models.charge_generation.charge_deposition'] = 'pyxel.models.charge_generation.charge_deposition'
    enabled: bool = True


#
# Model: Charge Generation / Charge Deposition In Mct
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationChargeDepositionInMctArguments(Mapping[str, Any]):
    flux: float = field(
        metadata=schema(
            title='flux'
            ,description='the flux of incoming particles in particle/s'
        )
    )
    step_size: float = field(
        default=1.0,
        metadata=schema(
            title='step_size'
            ,description=(
                    'the size of the considered unitary step in unit length along which '
                    'energy is deposited'
                )
        )
    )
    energy_mean: float = field(
        default=1.0,
        metadata=schema(
            title='energy_mean'
            ,description='the mean energy of the incoming ionizing particles in MeV'
        )
    )
    energy_spread: float = field(
        default=0.1,
        metadata=schema(
            title='energy_spread'
            ,description='the spread in energy of the incoming ionizing particles in MeV'
        )
    )
    energy_spectrum: Union[str, pathlib.Path, None] = field(
        default=None,
        metadata=schema(
            title='energy_spectrum'
            ,description=(
                    'the location of the file describing the energy spectrum of incident '
                    'particles if no spectrum is provided energies are randomly drawn from '
                    'a normal distribution with mean and spread defined above note that the'
                    ' energy spectrum is assumed to be a txt file with two columns [energy,'
                    ' flux] with the energy in MeV'
                )
        )
    )
    energy_spectrum_sampling: Literal['linear', 'log'] = field(
        default='log',
        metadata=schema(
            title='energy_spectrum_sampling'
            ,description=(
                    '"log" : the energy spectrum is sampled in log space "linear" : the '
                    'energy spectrum is sampled in linear space'
                )
        )
    )
    cutoff_wavelength: float = field(
        default=2.5,
        metadata=schema(
            title='cutoff_wavelength'
            ,description=(
                    'the longest wavelength in micrometer at which the QE reaches 50% of '
                    'its maximum, used to compute the bandgap energy, and the corresponding'
                    ' fraction of cadmium'
                )
        )
    )
    particle_direction: Literal['isotropic', 'orthogonal'] = field(
        default='isotropic',
        metadata=schema(
            title='particle_direction'
            ,description=(
                    '"isotropic" : particles are coming from all directions (outside of the'
                    ' sensor) "orthogonal" : particles are coming from the top of the '
                    'sensor (thickness = 0) and orthogonal to its surface'
                )
        )
    )
    stopping_power_curve: Union[str, pathlib.Path, None] = field(
        default=None,
        metadata=schema(
            title='stopping_power_curve'
            ,description=(
                    'the location of the file describing the total massive stopping power '
                    'energetic loss per mass of material and per unit path length versus '
                    'particle energy note that the the stopping power curve is assumed to '
                    'be a csv file with two columns [energy, stopping power] energy in MeV,'
                    ' stopping power in MeV cm2/g'
                )
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('flux', 'step_size', 'energy_mean', 'energy_spread', 'energy_spectrum', 'energy_spectrum_sampling', 'cutoff_wavelength', 'particle_direction', 'stopping_power_curve', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 10


@schema(
    title="Model 'charge_deposition_in_mct'"
    ,description=(
        'Simulate charge deposition by ionizing particles using a stopping '
        'power curve.'
    )
)
@dataclass
class ModelChargeGenerationChargeDepositionInMct:
    name: str
    arguments: ModelChargeGenerationChargeDepositionInMctArguments
    func: Literal['pyxel.models.charge_generation.charge_deposition_in_mct'] = 'pyxel.models.charge_generation.charge_deposition_in_mct'
    enabled: bool = True


#
# Model: Charge Generation / Conversion With 3d Qe Map
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationConversionWith3dQeMapArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='File path.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'conversion_with_3d_qe_map'"
    ,description='Generate charge from incident photon via photoelectric effect.'
)
@dataclass
class ModelChargeGenerationConversionWith3dQeMap:
    name: str
    arguments: ModelChargeGenerationConversionWith3dQeMapArguments
    func: Literal['pyxel.models.charge_generation.conversion_with_3d_qe_map'] = 'pyxel.models.charge_generation.conversion_with_3d_qe_map'
    enabled: bool = True


#
# Model: Charge Generation / Conversion With Qe Map
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationConversionWithQeMapArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='File path.'
        )
    )
    position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='position'
            ,description=(
                    'Indices of starting row and column, used when fitting :term:`QE` map '
                    'to detector.'
                )
        )
    )
    align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='align'
            ,description=(
                    'Keyword to align the :term:`QE` map to detector. Can be any from: '
                    '("center", "top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    binomial_sampling: bool = field(
        default=True,
        metadata=schema(
            title='binomial_sampling'
            ,description='Binomial sampling. Default is True.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'position', 'align', 'seed', 'binomial_sampling'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'conversion_with_qe_map'"
    ,description=(
        'Generate charge from incident photon via photoelectric effect, simple '
        'model with custom :term:`QE` map.'
    )
)
@dataclass
class ModelChargeGenerationConversionWithQeMap:
    name: str
    arguments: ModelChargeGenerationConversionWithQeMapArguments
    func: Literal['pyxel.models.charge_generation.conversion_with_qe_map'] = 'pyxel.models.charge_generation.conversion_with_qe_map'
    enabled: bool = True


#
# Model: Charge Generation / Cosmix
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationCosmixArguments(Mapping[str, Any]):
    simulation_mode: Optional[Literal['cosmic_ray', 'cosmics', 'radioactive_decay', 'snowflakes']] = field(
        default=None,
        metadata=schema(
            title='simulation_mode'
            ,description='Simulation mode: ``cosmic_rays``, ``radioactive_decay``.'
        )
    )
    running_mode: Optional[Literal['stopping', 'stepsize', 'geant4', 'plotting']] = field(
        default=None,
        metadata=schema(
            title='running_mode'
            ,description='Mode: ``stopping``, ``stepsize``, ``geant4``, ``plotting``.'
        )
    )
    particle_type: Optional[Literal['proton', 'alpha', 'ion']] = field(
        default=None,
        metadata=schema(
            title='particle_type'
            ,description='Type of particle: ``proton``, ``alpha``, ``ion``.'
        )
    )
    initial_energy: Union[int, float, Literal['random'], None] = field(
        default=None,
        metadata=schema(
            title='initial_energy'
            ,description='Kinetic energy of particle, set `random` for random.'
        )
    )
    particles_per_second: Optional[float] = field(
        default=None,
        metadata=schema(
            title='particles_per_second'
            ,description='Number of particles per second.'
        )
    )
    incident_angles: Optional[tuple[str, str]] = field(
        default=None,
        metadata=schema(
            title='incident_angles'
            ,description='Incident angles: ``(α, β)``.'
        )
    )
    starting_position: Optional[tuple[str, str, str]] = field(
        default=None,
        metadata=schema(
            title='starting_position'
            ,description='Starting position: ``(x, y, z)``.'
        )
    )
    spectrum_file: Optional[str] = field(
        default=None,
        metadata=schema(
            title='spectrum_file'
            ,description='Path to input spectrum'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    ionization_energy: float = field(
        default=3.6,
        metadata=schema(
            title='ionization_energy'
            ,description='Mean ionization energy of the semiconductor lattice.'
        )
    )
    progressbar: bool = field(
        default=True,
        metadata=schema(
            title='progressbar'
            ,description='Progressbar.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('simulation_mode', 'running_mode', 'particle_type', 'initial_energy', 'particles_per_second', 'incident_angles', 'starting_position', 'spectrum_file', 'seed', 'ionization_energy', 'progressbar'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 11


@schema(
    title="Model 'cosmix'"
    ,description='Apply CosmiX model.'
)
@dataclass
class ModelChargeGenerationCosmix:
    name: str
    arguments: ModelChargeGenerationCosmixArguments = field(default_factory=ModelChargeGenerationCosmixArguments)
    func: Literal['pyxel.models.charge_generation.cosmix'] = 'pyxel.models.charge_generation.cosmix'
    enabled: bool = True


#
# Model: Charge Generation / Dark Current
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationDarkCurrentArguments(Mapping[str, Any]):
    figure_of_merit: float = field(
        metadata=schema(
            title='figure_of_merit'
            ,description='Dark current figure of merit. Unit: nA/cm^2'
        )
    )
    spatial_noise_factor: Optional[float] = field(
        default=None,
        metadata=schema(
            title='spatial_noise_factor'
            ,description='Dark current fixed pattern noise factor.'
        )
    )
    band_gap: Optional[float] = field(
        default=None,
        metadata=schema(
            title='band_gap'
            ,description='Semiconductor band_gap. If none, the one for silicon is used. Unit: eV'
        )
    )
    band_gap_room_temperature: Optional[float] = field(
        default=None,
        metadata=schema(
            title='band_gap_room_temperature'
            ,description=(
                    'Semiconductor band gap at 300K. If none, the one for silicon is used. '
                    'Unit: eV'
                )
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    temporal_noise: bool = field(
        default=True,
        metadata=schema(
            title='temporal_noise'
            ,description='Shot noise.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('figure_of_merit', 'spatial_noise_factor', 'band_gap', 'band_gap_room_temperature', 'seed', 'temporal_noise'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 6


@schema(
    title="Model 'dark_current'"
    ,description='Add dark current to the detector charge.'
)
@dataclass
class ModelChargeGenerationDarkCurrent:
    name: str
    arguments: ModelChargeGenerationDarkCurrentArguments
    func: Literal['pyxel.models.charge_generation.dark_current'] = 'pyxel.models.charge_generation.dark_current'
    enabled: bool = True


#
# Model: Charge Generation / Dark Current Rule07
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationDarkCurrentRule07Arguments(Mapping[str, Any]):
    cutoff_wavelength: float = field(
        default=2.5,
        metadata=schema(
            title='cutoff_wavelength'
            ,description='Cutoff wavelength. Unit: um'
        )
    )
    spatial_noise_factor: Optional[float] = field(
        default=None,
        metadata=schema(
            title='spatial_noise_factor'
            ,description='Dark current fixed pattern noise factor.'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    temporal_noise: bool = field(
        default=True,
        metadata=schema(
            title='temporal_noise'
            ,description='Shot noise.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('cutoff_wavelength', 'spatial_noise_factor', 'seed', 'temporal_noise'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 4


@schema(
    title="Model 'dark_current_rule07'"
    ,description='Generate charge from dark current process.'
)
@dataclass
class ModelChargeGenerationDarkCurrentRule07:
    name: str
    arguments: ModelChargeGenerationDarkCurrentRule07Arguments = field(default_factory=ModelChargeGenerationDarkCurrentRule07Arguments)
    func: Literal['pyxel.models.charge_generation.dark_current_rule07'] = 'pyxel.models.charge_generation.dark_current_rule07'
    enabled: bool = True


#
# Model: Charge Generation / Dark Current Saphira
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationDarkCurrentSaphiraArguments(Mapping[str, Any]):
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('seed',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'dark_current_saphira'"
    ,description='Simulate dark current in a Saphira APD detector.'
)
@dataclass
class ModelChargeGenerationDarkCurrentSaphira:
    name: str
    arguments: ModelChargeGenerationDarkCurrentSaphiraArguments = field(default_factory=ModelChargeGenerationDarkCurrentSaphiraArguments)
    func: Literal['pyxel.models.charge_generation.dark_current_saphira'] = 'pyxel.models.charge_generation.dark_current_saphira'
    enabled: bool = True


#
# Model: Charge Generation / Load Charge
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationLoadChargeArguments(Mapping[str, Any]):
    filename: Union[str, pathlib.Path] = field(
        metadata=schema(
            title='filename'
            ,description='File path.'
        )
    )
    position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='position'
            ,description=(
                    'Indices of starting row and column, used when fitting charge to '
                    'detector.'
                )
        )
    )
    align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='align'
            ,description=(
                    'Keyword to align the charge to detector. Can be any from: ("center", '
                    '"top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    time_scale: float = field(
        default=1.0,
        metadata=schema(
            title='time_scale'
            ,description=(
                    'Time scale of the input charge, default is 1 second. 0.001 would be '
                    'ms.'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'position', 'align', 'time_scale'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 4


@schema(
    title="Model 'load_charge'"
    ,description=(
        'Load charge from txt file for detector, mostly for but not limited to '
        ':term:`CCDs<CCD>`.'
    )
)
@dataclass
class ModelChargeGenerationLoadCharge:
    name: str
    arguments: ModelChargeGenerationLoadChargeArguments
    func: Literal['pyxel.models.charge_generation.load_charge'] = 'pyxel.models.charge_generation.load_charge'
    enabled: bool = True


#
# Model: Charge Generation / Radiation Induced Dark Current
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationRadiationInducedDarkCurrentArguments(Mapping[str, Any]):
    depletion_volume: float = field(
        metadata=schema(
            title='depletion_volume'
            ,description='Depletion volume parameter. Unit: µm3.'
        )
    )
    annealing_time: float = field(
        metadata=schema(
            title='annealing_time'
            ,description='Annealing time. Unit: weeks'
        )
    )
    displacement_dose: float = field(
        metadata=schema(
            title='displacement_dose'
            ,description='Displacement dose parameter. Unit: TeV/g'
        )
    )
    shot_noise: bool = field(
        metadata=schema(
            title='shot_noise'
            ,description='True to enable shot noise.'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('depletion_volume', 'annealing_time', 'displacement_dose', 'shot_noise', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'radiation_induced_dark_current'"
    ,description='Model to add dark current induced by radiation to the detector charge.'
)
@dataclass
class ModelChargeGenerationRadiationInducedDarkCurrent:
    name: str
    arguments: ModelChargeGenerationRadiationInducedDarkCurrentArguments
    func: Literal['pyxel.models.charge_generation.radiation_induced_dark_current'] = 'pyxel.models.charge_generation.radiation_induced_dark_current'
    enabled: bool = True


#
# Model: Charge Generation / Simple Conversion
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationSimpleConversionArguments(Mapping[str, Any]):
    quantum_efficiency: Optional[float] = field(
        default=None,
        metadata=schema(
            title='quantum_efficiency'
            ,description='Quantum efficiency.'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    binomial_sampling: bool = field(
        default=True,
        metadata=schema(
            title='binomial_sampling'
            ,description='Binomial sampling. Default is True.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('quantum_efficiency', 'seed', 'binomial_sampling'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'simple_conversion'"
    ,description=(
        'Generate charge from incident photon via photoelectric effect, simple '
        'model.'
    )
)
@dataclass
class ModelChargeGenerationSimpleConversion:
    name: str
    arguments: ModelChargeGenerationSimpleConversionArguments = field(default_factory=ModelChargeGenerationSimpleConversionArguments)
    func: Literal['pyxel.models.charge_generation.simple_conversion'] = 'pyxel.models.charge_generation.simple_conversion'
    enabled: bool = True


#
# Model: Charge Generation / Simple Dark Current
#
@schema(title='Parameters')
@dataclass
class ModelChargeGenerationSimpleDarkCurrentArguments(Mapping[str, Any]):
    dark_rate: float = field(
        metadata=schema(
            title='dark_rate'
            ,description=(
                    'Dark current, in electrons/pixel/second, which is the way '
                    'manufacturers typically report it.'
                )
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('dark_rate', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'simple_dark_current'"
    ,description='Simulate dark current in a detector.'
)
@dataclass
class ModelChargeGenerationSimpleDarkCurrent:
    name: str
    arguments: ModelChargeGenerationSimpleDarkCurrentArguments
    func: Literal['pyxel.models.charge_generation.simple_dark_current'] = 'pyxel.models.charge_generation.simple_dark_current'
    enabled: bool = True


#
# Model: Charge Collection / Fixed Pattern Noise
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionFixedPatternNoiseArguments(Mapping[str, Any]):
    filename: Union[pathlib.Path, str, None] = field(
        default=None,
        metadata=schema(
            title='filename'
            ,description='Path to a file with an array or an image.'
        )
    )
    position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='position'
            ,description=(
                    'Indices of starting row and column, used when fitting noise to '
                    'detector.'
                )
        )
    )
    align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='align'
            ,description=(
                    'Keyword to align the noise to detector. Can be any from: ("center", '
                    '"top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    fixed_pattern_noise_factor: Optional[float] = field(
        default=None,
        metadata=schema(
            title='fixed_pattern_noise_factor'
            ,description='Fixed pattern noise factor.'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('filename', 'position', 'align', 'fixed_pattern_noise_factor', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'fixed_pattern_noise'"
    ,description=(
        'Add fixed pattern noise caused by pixel non-uniformity during charge '
        'collection.'
    )
)
@dataclass
class ModelChargeCollectionFixedPatternNoise:
    name: str
    arguments: ModelChargeCollectionFixedPatternNoiseArguments = field(default_factory=ModelChargeCollectionFixedPatternNoiseArguments)
    func: Literal['pyxel.models.charge_collection.fixed_pattern_noise'] = 'pyxel.models.charge_collection.fixed_pattern_noise'
    enabled: bool = True


#
# Model: Charge Collection / Persistence
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionPersistenceArguments(Mapping[str, Any]):
    trap_time_constants: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_time_constants'
            ,description='A list of trap time constants.'
        )
    )
    trap_proportions: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_proportions'
            ,description='A list of trap proportions.'
        )
    )
    trap_densities_filename: Union[pathlib.Path, str] = field(
        metadata=schema(
            title='trap_densities_filename'
            ,description='Path to densities file.'
        )
    )
    trap_capacities_filename: Union[pathlib.Path, str, None] = field(
        default=None,
        metadata=schema(
            title='trap_capacities_filename'
            ,description='Path to capacities file.'
        )
    )
    trap_densities_position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='trap_densities_position'
            ,description=(
                    'Indices of starting row and column, used when fitting densities to '
                    'detector.'
                )
        )
    )
    trap_densities_align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='trap_densities_align'
            ,description=(
                    'Keyword to align the densities to detector. Can be any from: '
                    '("center", "top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    trap_capacities_position: tuple[int, int] = field(
        default=(0, 0),
        metadata=schema(
            title='trap_capacities_position'
            ,description=(
                    'Indices of starting row and column, used when fitting capacities to '
                    'detector.'
                )
        )
    )
    trap_capacities_align: Optional[Literal['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']] = field(
        default=None,
        metadata=schema(
            title='trap_capacities_align'
            ,description=(
                    'Keyword to align the capacities to detector. Can be any from: '
                    '("center", "top_left", "top_right", "bottom_left", "bottom_right")'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('trap_time_constants', 'trap_proportions', 'trap_densities_filename', 'trap_capacities_filename', 'trap_densities_position', 'trap_densities_align', 'trap_capacities_position', 'trap_capacities_align'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 8


@schema(
    title="Model 'persistence'"
    ,description='Apply persistence model.'
)
@dataclass
class ModelChargeCollectionPersistence:
    name: str
    arguments: ModelChargeCollectionPersistenceArguments
    func: Literal['pyxel.models.charge_collection.persistence'] = 'pyxel.models.charge_collection.persistence'
    enabled: bool = True


#
# Model: Charge Collection / Simple Collection
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionSimpleCollectionArguments(Mapping[str, Any]):
    def __iter__(self) -> Iterator[str]:
        return iter(())
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 0


@schema(
    title="Model 'simple_collection'"
    ,description='Associate charge with the closest pixel.'
)
@dataclass
class ModelChargeCollectionSimpleCollection:
    name: str
    arguments: ModelChargeCollectionSimpleCollectionArguments = field(default_factory=ModelChargeCollectionSimpleCollectionArguments)
    func: Literal['pyxel.models.charge_collection.simple_collection'] = 'pyxel.models.charge_collection.simple_collection'
    enabled: bool = True


#
# Model: Charge Collection / Simple Full Well
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionSimpleFullWellArguments(Mapping[str, Any]):
    fwc: Optional[int] = field(
        default=None,
        metadata=schema(
            title='fwc'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('fwc',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'simple_full_well'"
    ,description='Limit the amount of charge in pixel due to full well capacity.'
)
@dataclass
class ModelChargeCollectionSimpleFullWell:
    name: str
    arguments: ModelChargeCollectionSimpleFullWellArguments = field(default_factory=ModelChargeCollectionSimpleFullWellArguments)
    func: Literal['pyxel.models.charge_collection.simple_full_well'] = 'pyxel.models.charge_collection.simple_full_well'
    enabled: bool = True


#
# Model: Charge Collection / Simple Ipc
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionSimpleIpcArguments(Mapping[str, Any]):
    coupling: float = field(
        metadata=schema(
            title='coupling'
        )
    )
    diagonal_coupling: float = field(
        default=0.0,
        metadata=schema(
            title='diagonal_coupling'
        )
    )
    anisotropic_coupling: float = field(
        default=0.0,
        metadata=schema(
            title='anisotropic_coupling'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('coupling', 'diagonal_coupling', 'anisotropic_coupling'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'simple_ipc'"
    ,description='Convolve pixel array with the IPC kernel.'
)
@dataclass
class ModelChargeCollectionSimpleIpc:
    name: str
    arguments: ModelChargeCollectionSimpleIpcArguments
    func: Literal['pyxel.models.charge_collection.simple_ipc'] = 'pyxel.models.charge_collection.simple_ipc'
    enabled: bool = True


#
# Model: Charge Collection / Simple Persistence
#
@schema(title='Parameters')
@dataclass
class ModelChargeCollectionSimplePersistenceArguments(Mapping[str, Any]):
    trap_time_constants: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_time_constants'
            ,description='List of trap time constants.'
        )
    )
    trap_densities: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_densities'
            ,description='List of trap densities.'
        )
    )
    trap_capacities: Optional[collections.abc.Sequence[float]] = field(
        default=None,
        metadata=schema(
            title='trap_capacities'
            ,description='List of trap capacities.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('trap_time_constants', 'trap_densities', 'trap_capacities'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'simple_persistence'"
    ,description='Apply simple persistence model.'
)
@dataclass
class ModelChargeCollectionSimplePersistence:
    name: str
    arguments: ModelChargeCollectionSimplePersistenceArguments
    func: Literal['pyxel.models.charge_collection.simple_persistence'] = 'pyxel.models.charge_collection.simple_persistence'
    enabled: bool = True


#
# Model: Charge Transfer / Arctic Add
#
@schema(title='Parameters')
@dataclass
class ModelChargeTransferArcticAddArguments(Mapping[str, Any]):
    well_fill_power: float = field(
        metadata=schema(
            title='well_fill_power'
        )
    )
    trap_densities: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_densities'
            ,description='A 1D arrays of all trap species densities for serial clocking.'
        )
    )
    trap_release_timescales: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_release_timescales'
            ,description='A 1D arrays of all trap release timescales for serial clocking.'
        )
    )
    express: int = field(
        default=0,
        metadata=schema(
            title='express'
            ,description=(
                    'As described in more detail in :cite:p:`2014:massey` section 2.1.5, '
                    'the effects of each individual pixel-to-pixel transfer can be very '
                    'similar, so multiple transfers can be computed at once for efficiency.'
                    ' The ``express`` input sets the number of times the transfers are '
                    'calculated.  * ``express = 1`` is the fastest and least accurate. * '
                    '``express = 2`` means the transfers are re-computed half-way through '
                    'readout. * ``express = N`` where ``N`` is the total number of pixels.'
                    '  Default ``express = 0`` is a convenient input for automatic '
                    '``express = N``.'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('well_fill_power', 'trap_densities', 'trap_release_timescales', 'express'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 4


@schema(
    title="Model 'arctic_add'"
    ,description=(
        'Add :term:`CTI` trails to an image by trapping, releasing and moving '
        'electrons.'
    )
)
@dataclass
class ModelChargeTransferArcticAdd:
    name: str
    arguments: ModelChargeTransferArcticAddArguments
    func: Literal['pyxel.models.charge_transfer.arctic_add'] = 'pyxel.models.charge_transfer.arctic_add'
    enabled: bool = True


#
# Model: Charge Transfer / Arctic Remove
#
@schema(title='Parameters')
@dataclass
class ModelChargeTransferArcticRemoveArguments(Mapping[str, Any]):
    well_fill_power: float = field(
        metadata=schema(
            title='well_fill_power'
        )
    )
    trap_densities: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_densities'
        )
    )
    trap_release_timescales: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_release_timescales'
        )
    )
    num_iterations: int = field(
        metadata=schema(
            title='num_iterations'
            ,description=(
                    'Number of iterations for the forward modelling. More iterations '
                    'provide higher accuracy at the cost of longer runtime. In practice, '
                    'just 1 to 3 iterations are usually sufficient.'
                )
        )
    )
    express: int = field(
        default=0,
        metadata=schema(
            title='express'
            ,description=(
                    'As described in more detail in :cite:p:`2014:massey` section 2.1.5, '
                    'the effects of each individual pixel-to-pixel transfer can be very '
                    'similar, so multiple transfers can be computed at once for efficiency.'
                    ' The ``express`` input sets the number of times the transfers are '
                    'calculated.  * ``express = 1`` is the fastest and least accurate. * '
                    '``express = 2`` means the transfers are re-computed half-way through '
                    'readout. * ``express = N`` where ``N`` is the total number of pixels.'
                    '  Default ``express = 0`` is a convenient input for automatic '
                    '``express = N``.'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('well_fill_power', 'trap_densities', 'trap_release_timescales', 'num_iterations', 'express'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'arctic_remove'"
    ,description=(
        'Remove :term:`CTI` trails from an image by first modelling the '
        'addition of :term:`CTI`.'
    )
)
@dataclass
class ModelChargeTransferArcticRemove:
    name: str
    arguments: ModelChargeTransferArcticRemoveArguments
    func: Literal['pyxel.models.charge_transfer.arctic_remove'] = 'pyxel.models.charge_transfer.arctic_remove'
    enabled: bool = True


#
# Model: Charge Transfer / Cdm
#
@schema(title='Parameters')
@dataclass
class ModelChargeTransferCdmArguments(Mapping[str, Any]):
    direction: Literal['parallel', 'serial'] = field(
        metadata=schema(
            title='direction'
            ,description=(
                    'Set ``"parallel"`` for :term:`CTI` in parallel direction or '
                    '``"serial"`` for :term:`CTI` in serial register.'
                )
        )
    )
    beta: float = field(
        metadata=schema(
            title='beta'
            ,description='Electron cloud expansion coefficient :math:`\\beta`.'
        )
    )
    trap_release_times: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_release_times'
            ,description='Trap release time constants :math:`\\tau_r`. Unit: :math:`s`.'
        )
    )
    trap_densities: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='trap_densities'
            ,description='Absolute trap densities :math:`n_t`. Unit: :math:`cm^{-3}`.'
        )
    )
    sigma: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='sigma'
            ,description='Trap capture cross section :math:`\\sigma`. Unit: :math:`cm^2`.'
        )
    )
    full_well_capacity: Optional[float] = field(
        default=None,
        metadata=schema(
            title='full_well_capacity'
            ,description='Full well capacity :math:`FWC`. Unit: :math:`e^-`.'
        )
    )
    max_electron_volume: float = field(
        default=0.0,
        metadata=schema(
            title='max_electron_volume'
            ,description=(
                    'Maximum geometrical volume :math:`V_g` that electrons can occupy '
                    'within a pixel. Unit: :math:`cm^3`.'
                )
        )
    )
    transfer_period: float = field(
        default=0.0,
        metadata=schema(
            title='transfer_period'
            ,description='Transfer period :math:`t` (TDI period). Unit: :math:`s`.'
        )
    )
    charge_injection: bool = field(
        default=False,
        metadata=schema(
            title='charge_injection'
            ,description='Enable charge injection (only used in ``"parallel"`` mode).'
        )
    )
    electron_effective_mass: float = field(
        default=0.5,
        metadata=schema(
            title='electron_effective_mass'
            ,description=(
                    'Electron effective mass in the semiconductor lattice. Unit: 1 electron'
                    ' mass'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('direction', 'beta', 'trap_release_times', 'trap_densities', 'sigma', 'full_well_capacity', 'max_electron_volume', 'transfer_period', 'charge_injection', 'electron_effective_mass'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 10


@schema(
    title="Model 'cdm'"
    ,description='Charge Distortion Model (CDM) model wrapper.'
)
@dataclass
class ModelChargeTransferCdm:
    name: str
    arguments: ModelChargeTransferCdmArguments
    func: Literal['pyxel.models.charge_transfer.cdm'] = 'pyxel.models.charge_transfer.cdm'
    enabled: bool = True


#
# Model: Charge Transfer / Multiplication Register
#
@schema(title='Parameters')
@dataclass
class ModelChargeTransferMultiplicationRegisterArguments(Mapping[str, Any]):
    total_gain: int = field(
        metadata=schema(
            title='total_gain'
        )
    )
    gain_elements: int = field(
        metadata=schema(
            title='gain_elements'
            ,description='Amount of single stage gain elements in the EMCCD register.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('total_gain', 'gain_elements'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'multiplication_register'"
    ,description='Calculate total gain of image with EMCCD multiplication register.'
)
@dataclass
class ModelChargeTransferMultiplicationRegister:
    name: str
    arguments: ModelChargeTransferMultiplicationRegisterArguments
    func: Literal['pyxel.models.charge_transfer.multiplication_register'] = 'pyxel.models.charge_transfer.multiplication_register'
    enabled: bool = True


#
# Model: Charge Transfer / Multiplication Register Cic
#
@schema(title='Parameters')
@dataclass
class ModelChargeTransferMultiplicationRegisterCicArguments(Mapping[str, Any]):
    total_gain: int = field(
        metadata=schema(
            title='total_gain'
        )
    )
    gain_elements: int = field(
        metadata=schema(
            title='gain_elements'
            ,description='Amount of single stage gain elements in the EMCCD register.'
        )
    )
    pcic_rate: float = field(
        metadata=schema(
            title='pcic_rate'
            ,description='Parallel CIC rate'
        )
    )
    scic_rate: float = field(
        metadata=schema(
            title='scic_rate'
            ,description='Serial CIC rate'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('total_gain', 'gain_elements', 'pcic_rate', 'scic_rate'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 4


@schema(
    title="Model 'multiplication_register_cic'"
    ,description='Calculate total gain of image with EMCCD multiplication register.'
)
@dataclass
class ModelChargeTransferMultiplicationRegisterCic:
    name: str
    arguments: ModelChargeTransferMultiplicationRegisterCicArguments
    func: Literal['pyxel.models.charge_transfer.multiplication_register_cic'] = 'pyxel.models.charge_transfer.multiplication_register_cic'
    enabled: bool = True


#
# Model: Charge Measurement / Ac Crosstalk
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementAcCrosstalkArguments(Mapping[str, Any]):
    coupling_matrix: Union[str, pathlib.Path, collections.abc.Sequence] = field(
        metadata=schema(
            title='coupling_matrix'
        )
    )
    channel_matrix: Sequence = field(
        metadata=schema(
            title='channel_matrix'
        )
    )
    readout_directions: Sequence = field(
        metadata=schema(
            title='readout_directions'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('coupling_matrix', 'channel_matrix', 'readout_directions'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'ac_crosstalk'"
    ,description='Apply AC crosstalk signal to detector signal.'
)
@dataclass
class ModelChargeMeasurementAcCrosstalk:
    name: str
    arguments: ModelChargeMeasurementAcCrosstalkArguments
    func: Literal['pyxel.models.charge_measurement.ac_crosstalk'] = 'pyxel.models.charge_measurement.ac_crosstalk'
    enabled: bool = True


#
# Model: Charge Measurement / Dc Crosstalk
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementDcCrosstalkArguments(Mapping[str, Any]):
    coupling_matrix: Union[str, pathlib.Path, collections.abc.Sequence] = field(
        metadata=schema(
            title='coupling_matrix'
        )
    )
    channel_matrix: Sequence = field(
        metadata=schema(
            title='channel_matrix'
        )
    )
    readout_directions: Sequence = field(
        metadata=schema(
            title='readout_directions'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('coupling_matrix', 'channel_matrix', 'readout_directions'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'dc_crosstalk'"
    ,description='Apply DC crosstalk signal to detector signal.'
)
@dataclass
class ModelChargeMeasurementDcCrosstalk:
    name: str
    arguments: ModelChargeMeasurementDcCrosstalkArguments
    func: Literal['pyxel.models.charge_measurement.dc_crosstalk'] = 'pyxel.models.charge_measurement.dc_crosstalk'
    enabled: bool = True


#
# Model: Charge Measurement / Dc Offset
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementDcOffsetArguments(Mapping[str, Any]):
    offset: float = field(
        metadata=schema(
            title='offset'
            ,description='DC offset voltage. Unit: V'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('offset',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'dc_offset'"
    ,description='Apply DC voltage to the detector.'
)
@dataclass
class ModelChargeMeasurementDcOffset:
    name: str
    arguments: ModelChargeMeasurementDcOffsetArguments
    func: Literal['pyxel.models.charge_measurement.dc_offset'] = 'pyxel.models.charge_measurement.dc_offset'
    enabled: bool = True


#
# Model: Charge Measurement / Ktc Noise
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementKtcNoiseArguments(Mapping[str, Any]):
    node_capacitance: Optional[float] = field(
        default=None,
        metadata=schema(
            title='node_capacitance'
            ,description='Node capacitance. Unit: F'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('node_capacitance', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'ktc_noise'"
    ,description='Apply KTC reset noise to detector signal array.'
)
@dataclass
class ModelChargeMeasurementKtcNoise:
    name: str
    arguments: ModelChargeMeasurementKtcNoiseArguments = field(default_factory=ModelChargeMeasurementKtcNoiseArguments)
    func: Literal['pyxel.models.charge_measurement.ktc_noise'] = 'pyxel.models.charge_measurement.ktc_noise'
    enabled: bool = True


#
# Model: Charge Measurement / Nghxrg
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementNghxrgArguments(Mapping[str, Any]):
    noise: collections.abc.Sequence[collections.abc.Mapping[Literal['ktc_bias_noise', 'white_read_noise', 'corr_pink_noise', 'uncorr_pink_noise', 'acn_noise', 'pca_zero_noise'], collections.abc.Mapping[str, float]]] = field(
        metadata=schema(
            title='noise'
        )
    )
    window_position: Optional[tuple[int, int]] = field(
        default=None,
        metadata=schema(
            title='window_position'
            ,description='[x0 (columns), y0 (rows)].'
        )
    )
    window_size: Optional[tuple[int, int]] = field(
        default=None,
        metadata=schema(
            title='window_size'
            ,description='[x (columns), y (rows)].'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    n_output: int = field(
        default=1,
        metadata=schema(
            title='n_output'
            ,description='Number of detector outputs.'
        )
    )
    n_row_overhead: int = field(
        default=0,
        metadata=schema(
            title='n_row_overhead'
            ,description=(
                    'New row overhead in pixel. This allows for a short wait at the end of '
                    'a row before starting the next row.'
                )
        )
    )
    n_frame_overhead: int = field(
        default=0,
        metadata=schema(
            title='n_frame_overhead'
            ,description=(
                    'New frame overhead in rows. This allows for a short wait at the end of'
                    ' a frame before starting the next frame.'
                )
        )
    )
    reverse_scan_direction: bool = field(
        default=False,
        metadata=schema(
            title='reverse_scan_direction'
            ,description=(
                    'Set this True to reverse the fast scanner readout directions. This '
                    'capability was added to support Teledyne’s programmable fast scan '
                    'readout directions. The default setting (False) corresponds to what '
                    'HxRG detectors default to upon power up.'
                )
        )
    )
    reference_pixel_border_width: int = field(
        default=4,
        metadata=schema(
            title='reference_pixel_border_width'
            ,description='Width of reference pixel border around image area.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('noise', 'window_position', 'window_size', 'seed', 'n_output', 'n_row_overhead', 'n_frame_overhead', 'reverse_scan_direction', 'reference_pixel_border_width'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 9


@schema(
    title="Model 'nghxrg'"
    ,description='Generate fourier noise power spectrum on HXRG detector.'
)
@dataclass
class ModelChargeMeasurementNghxrg:
    name: str
    arguments: ModelChargeMeasurementNghxrgArguments
    func: Literal['pyxel.models.charge_measurement.nghxrg'] = 'pyxel.models.charge_measurement.nghxrg'
    enabled: bool = True


#
# Model: Charge Measurement / Output Node Linearity Poly
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementOutputNodeLinearityPolyArguments(Mapping[str, Any]):
    coefficients: collections.abc.Sequence[float] = field(
        metadata=schema(
            title='coefficients'
            ,description='Coefficient of the polynomial function.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('coefficients',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'output_node_linearity_poly'"
    ,description=(
        'Add non-linearity to signal array to simulate the non-linearity of the'
        ' output node circuit.'
    )
)
@dataclass
class ModelChargeMeasurementOutputNodeLinearityPoly:
    name: str
    arguments: ModelChargeMeasurementOutputNodeLinearityPolyArguments
    func: Literal['pyxel.models.charge_measurement.output_node_linearity_poly'] = 'pyxel.models.charge_measurement.output_node_linearity_poly'
    enabled: bool = True


#
# Model: Charge Measurement / Output Node Noise
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementOutputNodeNoiseArguments(Mapping[str, Any]):
    std_deviation: float = field(
        metadata=schema(
            title='std_deviation'
            ,description='Standard deviation. Unit: V'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('std_deviation', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'output_node_noise'"
    ,description=(
        'Add noise to signal array of detector output node using normal random '
        'distribution.'
    )
)
@dataclass
class ModelChargeMeasurementOutputNodeNoise:
    name: str
    arguments: ModelChargeMeasurementOutputNodeNoiseArguments
    func: Literal['pyxel.models.charge_measurement.output_node_noise'] = 'pyxel.models.charge_measurement.output_node_noise'
    enabled: bool = True


#
# Model: Charge Measurement / Output Node Noise Cmos
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementOutputNodeNoiseCmosArguments(Mapping[str, Any]):
    readout_noise: float = field(
        metadata=schema(
            title='readout_noise'
            ,description='Mean readout noise for the array in units of electrons. Unit: electron'
        )
    )
    readout_noise_std: float = field(
        metadata=schema(
            title='readout_noise_std'
            ,description='Readout noise standard deviation in units of electrons. Unit: electron'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
            ,description='Random seed.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('readout_noise', 'readout_noise_std', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'output_node_noise_cmos'"
    ,description=(
        'Output node noise model for :term:`CMOS` detectors where readout is '
        'statistically independent for each pixel.'
    )
)
@dataclass
class ModelChargeMeasurementOutputNodeNoiseCmos:
    name: str
    arguments: ModelChargeMeasurementOutputNodeNoiseCmosArguments
    func: Literal['pyxel.models.charge_measurement.output_node_noise_cmos'] = 'pyxel.models.charge_measurement.output_node_noise_cmos'
    enabled: bool = True


#
# Model: Charge Measurement / Output Pixel Reset Voltage Apd
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementOutputPixelResetVoltageApdArguments(Mapping[str, Any]):
    roic_drop: float = field(
        metadata=schema(
            title='roic_drop'
            ,description='Readout circuit drop voltage. Unit: V'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('roic_drop',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'output_pixel_reset_voltage_apd'"
    ,description='Apply output pixel reset voltage to APD detector.'
)
@dataclass
class ModelChargeMeasurementOutputPixelResetVoltageApd:
    name: str
    arguments: ModelChargeMeasurementOutputPixelResetVoltageApdArguments
    func: Literal['pyxel.models.charge_measurement.output_pixel_reset_voltage_apd'] = 'pyxel.models.charge_measurement.output_pixel_reset_voltage_apd'
    enabled: bool = True


#
# Model: Charge Measurement / Physical Non Linearity
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementPhysicalNonLinearityArguments(Mapping[str, Any]):
    cutoff: float = field(
        metadata=schema(
            title='cutoff'
            ,description='Cutoff wavelength. unit: um'
        )
    )
    n_donor: float = field(
        metadata=schema(
            title='n_donor'
            ,description='Donor density. Unit: atoms/cm^3'
        )
    )
    n_acceptor: float = field(
        metadata=schema(
            title='n_acceptor'
            ,description='Acceptor density. Unit: atoms/cm^3'
        )
    )
    diode_diameter: float = field(
        metadata=schema(
            title='diode_diameter'
            ,description='Diode diameter. Unit: um'
        )
    )
    v_bias: float = field(
        metadata=schema(
            title='v_bias'
            ,description='Initial bias voltage. Unit: V.'
        )
    )
    fixed_capacitance: float = field(
        metadata=schema(
            title='fixed_capacitance'
            ,description='Additional fixed capacitance. Unit: F'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('cutoff', 'n_donor', 'n_acceptor', 'diode_diameter', 'v_bias', 'fixed_capacitance'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 6


@schema(
    title="Model 'physical_non_linearity'"
    ,description='Apply physical non-linearity.'
)
@dataclass
class ModelChargeMeasurementPhysicalNonLinearity:
    name: str
    arguments: ModelChargeMeasurementPhysicalNonLinearityArguments
    func: Literal['pyxel.models.charge_measurement.physical_non_linearity'] = 'pyxel.models.charge_measurement.physical_non_linearity'
    enabled: bool = True


#
# Model: Charge Measurement / Physical Non Linearity With Saturation
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementPhysicalNonLinearityWithSaturationArguments(Mapping[str, Any]):
    cutoff: float = field(
        metadata=schema(
            title='cutoff'
            ,description='Cutoff wavelength. unit: um'
        )
    )
    n_donor: float = field(
        metadata=schema(
            title='n_donor'
            ,description='Donor density. Unit: atoms/cm^3'
        )
    )
    n_acceptor: float = field(
        metadata=schema(
            title='n_acceptor'
            ,description='Acceptor density. Unit: atoms/cm^3'
        )
    )
    phi_implant: float = field(
        metadata=schema(
            title='phi_implant'
            ,description='Diameter of the implantation. Unit: um'
        )
    )
    d_implant: float = field(
        metadata=schema(
            title='d_implant'
            ,description='Depth of the implamantation. Unit: um'
        )
    )
    saturation_current: float = field(
        metadata=schema(
            title='saturation_current'
            ,description='Saturation current: e-/s/pix.'
        )
    )
    ideality_factor: float = field(
        metadata=schema(
            title='ideality_factor'
            ,description='Ideality factor.'
        )
    )
    v_reset: float = field(
        metadata=schema(
            title='v_reset'
            ,description='VRESET. Unit: V.'
        )
    )
    d_sub: float = field(
        metadata=schema(
            title='d_sub'
            ,description='DSUB. Unit: V.'
        )
    )
    fixed_capacitance: float = field(
        metadata=schema(
            title='fixed_capacitance'
            ,description='Additional fixed capacitance. Unit: F.'
        )
    )
    euler_points: int = field(
        metadata=schema(
            title='euler_points'
            ,description='Number of points in the euler method.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('cutoff', 'n_donor', 'n_acceptor', 'phi_implant', 'd_implant', 'saturation_current', 'ideality_factor', 'v_reset', 'd_sub', 'fixed_capacitance', 'euler_points'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 11


@schema(
    title="Model 'physical_non_linearity_with_saturation'"
    ,description='Apply physical non-linearity with saturation.'
)
@dataclass
class ModelChargeMeasurementPhysicalNonLinearityWithSaturation:
    name: str
    arguments: ModelChargeMeasurementPhysicalNonLinearityWithSaturationArguments
    func: Literal['pyxel.models.charge_measurement.physical_non_linearity_with_saturation'] = 'pyxel.models.charge_measurement.physical_non_linearity_with_saturation'
    enabled: bool = True


#
# Model: Charge Measurement / Readout Noise Saphira
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementReadoutNoiseSaphiraArguments(Mapping[str, Any]):
    roic_readout_noise: float = field(
        metadata=schema(
            title='roic_readout_noise'
            ,description='Readout integrated circuit noise in volts RMS. Unit: V'
        )
    )
    controller_noise: float = field(
        default=0.0,
        metadata=schema(
            title='controller_noise'
            ,description='Controller noise in volts RMS. Unit: V'
        )
    )
    seed: Optional[int] = field(
        default=None,
        metadata=schema(
            title='seed'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('roic_readout_noise', 'controller_noise', 'seed'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'readout_noise_saphira'"
    ,description='Apply Saphira specific readout noise to the APD detector.'
)
@dataclass
class ModelChargeMeasurementReadoutNoiseSaphira:
    name: str
    arguments: ModelChargeMeasurementReadoutNoiseSaphiraArguments
    func: Literal['pyxel.models.charge_measurement.readout_noise_saphira'] = 'pyxel.models.charge_measurement.readout_noise_saphira'
    enabled: bool = True


#
# Model: Charge Measurement / Simple Measurement
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementSimpleMeasurementArguments(Mapping[str, Any]):
    gain: Optional[float] = field(
        default=None,
        metadata=schema(
            title='gain'
            ,description=(
                    'Gain to apply. By default, this is the sensitivity of charge readout. '
                    'Unit: V/e-'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('gain',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'simple_measurement'"
    ,description='Convert the pixel array into signal array.'
)
@dataclass
class ModelChargeMeasurementSimpleMeasurement:
    name: str
    arguments: ModelChargeMeasurementSimpleMeasurementArguments = field(default_factory=ModelChargeMeasurementSimpleMeasurementArguments)
    func: Literal['pyxel.models.charge_measurement.simple_measurement'] = 'pyxel.models.charge_measurement.simple_measurement'
    enabled: bool = True


#
# Model: Charge Measurement / Simple Physical Non Linearity
#
@schema(title='Parameters')
@dataclass
class ModelChargeMeasurementSimplePhysicalNonLinearityArguments(Mapping[str, Any]):
    cutoff: float = field(
        metadata=schema(
            title='cutoff'
            ,description='Cutoff wavelength. unit: um'
        )
    )
    n_donor: float = field(
        metadata=schema(
            title='n_donor'
            ,description='Donor density. Unit: atoms/cm^3'
        )
    )
    n_acceptor: float = field(
        metadata=schema(
            title='n_acceptor'
            ,description='Acceptor density. Unit: atoms/cm^3'
        )
    )
    diode_diameter: float = field(
        metadata=schema(
            title='diode_diameter'
            ,description='Diode diameter. Unit: um'
        )
    )
    v_bias: float = field(
        metadata=schema(
            title='v_bias'
            ,description='Initial bias voltage. Unit: V.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('cutoff', 'n_donor', 'n_acceptor', 'diode_diameter', 'v_bias'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'simple_physical_non_linearity'"
    ,description='Apply simple physical non-linearity.'
)
@dataclass
class ModelChargeMeasurementSimplePhysicalNonLinearity:
    name: str
    arguments: ModelChargeMeasurementSimplePhysicalNonLinearityArguments
    func: Literal['pyxel.models.charge_measurement.simple_physical_non_linearity'] = 'pyxel.models.charge_measurement.simple_physical_non_linearity'
    enabled: bool = True


#
# Model: Readout Electronics / Dead Time Filter
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsDeadTimeFilterArguments(Mapping[str, Any]):
    tau_0: float = field(
        default=4.4e-07,
        metadata=schema(
            title='tau_0'
            ,description=(
                    'Material dependent characteristic time for the electron-phonon '
                    'coupling. Unit: s'
                )
        )
    )
    n_0: float = field(
        default=17200000000.0,
        metadata=schema(
            title='n_0'
            ,description=(
                    'Material dependent single spin density of states at the Fermi-level. '
                    'Unit: um^-3 eV^-1'
                )
        )
    )
    t_c: float = field(
        default=1.26,
        metadata=schema(
            title='t_c'
            ,description='Material dependent critical temperature. Unit: K'
        )
    )
    v: float = field(
        default=30.0,
        metadata=schema(
            title='v'
            ,description='Superconducting volume. Unit: um^3'
        )
    )
    t_op: float = field(
        default=0.3,
        metadata=schema(
            title='t_op'
            ,description='Temperature. Unit: K'
        )
    )
    tau_pb: float = field(
        default=2.8e-10,
        metadata=schema(
            title='tau_pb'
            ,description='Phonon pair-breaking time. Unit: s'
        )
    )
    tau_esc: float = field(
        default=1.4e-10,
        metadata=schema(
            title='tau_esc'
            ,description='Phonon escape time. Unit: s'
        )
    )
    tau_sat: float = field(
        default=0.001,
        metadata=schema(
            title='tau_sat'
            ,description='Saturation time. Unit: s'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('tau_0', 'n_0', 't_c', 'v', 't_op', 'tau_pb', 'tau_esc', 'tau_sat'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 8


@schema(
    title="Model 'dead_time_filter'"
    ,description='Dead time filter.'
)
@dataclass
class ModelReadoutElectronicsDeadTimeFilter:
    name: str
    arguments: ModelReadoutElectronicsDeadTimeFilterArguments = field(default_factory=ModelReadoutElectronicsDeadTimeFilterArguments)
    func: Literal['pyxel.models.readout_electronics.dead_time_filter'] = 'pyxel.models.readout_electronics.dead_time_filter'
    enabled: bool = True


#
# Model: Readout Electronics / Sar Adc
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsSarAdcArguments(Mapping[str, Any]):
    def __iter__(self) -> Iterator[str]:
        return iter(())
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 0


@schema(
    title="Model 'sar_adc'"
    ,description=(
        'Digitize signal array using :term:`SAR` (Successive Approximation '
        'Register) :term:`ADC` logic.'
    )
)
@dataclass
class ModelReadoutElectronicsSarAdc:
    name: str
    arguments: ModelReadoutElectronicsSarAdcArguments = field(default_factory=ModelReadoutElectronicsSarAdcArguments)
    func: Literal['pyxel.models.readout_electronics.sar_adc'] = 'pyxel.models.readout_electronics.sar_adc'
    enabled: bool = True


#
# Model: Readout Electronics / Sar Adc With Noise
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsSarAdcWithNoiseArguments(Mapping[str, Any]):
    strengths: tuple[float, ...] = field(
        metadata=schema(
            title='strengths'
            ,description=(
                    'Sequence of ``detector.characteristics.adc_bit_resolution`` number(s).'
                    ' Unit: V'
                )
        )
    )
    noises: tuple[float, ...] = field(
        metadata=schema(
            title='noises'
            ,description=(
                    'Sequence of ``detector.characteristics.adc_bit_resolution`` number(s).'
                    ' Unit: V'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('strengths', 'noises'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'sar_adc_with_noise'"
    ,description=(
        'Digitize signal array using :term:`SAR` (Successive Approximation '
        'Register) :term:`ADC` logic with noise.'
    )
)
@dataclass
class ModelReadoutElectronicsSarAdcWithNoise:
    name: str
    arguments: ModelReadoutElectronicsSarAdcWithNoiseArguments
    func: Literal['pyxel.models.readout_electronics.sar_adc_with_noise'] = 'pyxel.models.readout_electronics.sar_adc_with_noise'
    enabled: bool = True


#
# Model: Readout Electronics / Simple Adc
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsSimpleAdcArguments(Mapping[str, Any]):
    data_type: Optional[Literal['uint8', 'uint16', 'uint32', 'uint64']] = field(
        default=None,
        metadata=schema(
            title='data_type'
            ,description=(
                    'The desired data-type for the Image array. The data-type must be an '
                    'unsigned integer. If not provided, the data type is determined based '
                    'on `detector.characteristics.adc_bit_resolution`. Valid values: '
                    "'uint8', 'uint16', 'uint32', 'uint64' Invalid values: 'int16', "
                    "'int32', 'int64', 'int', 'float'..."
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('data_type',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'simple_adc'"
    ,description=(
        'Apply simple Analog-to-Digital Converter (ADC) to the `signal` bucket '
        'from `Detector`.'
    )
)
@dataclass
class ModelReadoutElectronicsSimpleAdc:
    name: str
    arguments: ModelReadoutElectronicsSimpleAdcArguments = field(default_factory=ModelReadoutElectronicsSimpleAdcArguments)
    func: Literal['pyxel.models.readout_electronics.simple_adc'] = 'pyxel.models.readout_electronics.simple_adc'
    enabled: bool = True


#
# Model: Readout Electronics / Simple Amplifier
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsSimpleAmplifierArguments(Mapping[str, Any]):
    def __iter__(self) -> Iterator[str]:
        return iter(())
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 0


@schema(
    title="Model 'simple_amplifier'"
    ,description=(
        'Amplify signal using gain from the output amplifier and the signal '
        'processor.'
    )
)
@dataclass
class ModelReadoutElectronicsSimpleAmplifier:
    name: str
    arguments: ModelReadoutElectronicsSimpleAmplifierArguments = field(default_factory=ModelReadoutElectronicsSimpleAmplifierArguments)
    func: Literal['pyxel.models.readout_electronics.simple_amplifier'] = 'pyxel.models.readout_electronics.simple_amplifier'
    enabled: bool = True


#
# Model: Readout Electronics / Simple Phase Conversion
#
@schema(title='Parameters')
@dataclass
class ModelReadoutElectronicsSimplePhaseConversionArguments(Mapping[str, Any]):
    phase_conversion: float = field(
        default=1.0,
        metadata=schema(
            title='phase_conversion'
            ,description='Phase conversion factor'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('phase_conversion',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'simple_phase_conversion'"
    ,description='Create an image array from phase array.'
)
@dataclass
class ModelReadoutElectronicsSimplePhaseConversion:
    name: str
    arguments: ModelReadoutElectronicsSimplePhaseConversionArguments = field(default_factory=ModelReadoutElectronicsSimplePhaseConversionArguments)
    func: Literal['pyxel.models.readout_electronics.simple_phase_conversion'] = 'pyxel.models.readout_electronics.simple_phase_conversion'
    enabled: bool = True


#
# Model: Data Processing / Extract Roi To Xarray
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingExtractRoiToXarrayArguments(Mapping[str, Any]):
    array_type: str = field(
        default='pixel',
        metadata=schema(
            title='array_type'
        )
    )
    thresh: int = field(
        default=50,
        metadata=schema(
            title='thresh'
            ,description=(
                    'Threshold pixel value above which information from the image array is '
                    'extracted'
                )
        )
    )
    minarea: int = field(
        default=5,
        metadata=schema(
            title='minarea'
            ,description=(
                    'Minimum area of pixels required that are above the threshold for the '
                    'extractor to extract information'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('array_type', 'thresh', 'minarea'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 3


@schema(
    title="Model 'extract_roi_to_xarray'"
    ,description=(
        'Extract the roi data converts it to xarray dataset and saves the '
        'information to the final result.'
    )
)
@dataclass
class ModelDataProcessingExtractRoiToXarray:
    name: str
    arguments: ModelDataProcessingExtractRoiToXarrayArguments = field(default_factory=ModelDataProcessingExtractRoiToXarrayArguments)
    func: Literal['pyxel.models.data_processing.extract_roi_to_xarray'] = 'pyxel.models.data_processing.extract_roi_to_xarray'
    enabled: bool = True


#
# Model: Data Processing / Linear Regression
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingLinearRegressionArguments(Mapping[str, Any]):
    data_structure: Literal['pixel', 'photon', 'image', 'signal'] = field(
        default='image',
        metadata=schema(
            title='data_structure'
            ,description='Data bucket to use for the linear regression.'
        )
    )
    name: Optional[str] = field(
        default=None,
        metadata=schema(
            title='name'
            ,description='Name to use for the result.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('data_structure', 'name'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'linear_regression'"
    ,description=(
        "Compute a linear regression along 'readout_time' and store it in "
        "'.data' bucket."
    )
)
@dataclass
class ModelDataProcessingLinearRegression:
    name: str
    arguments: ModelDataProcessingLinearRegressionArguments = field(default_factory=ModelDataProcessingLinearRegressionArguments)
    func: Literal['pyxel.models.data_processing.linear_regression'] = 'pyxel.models.data_processing.linear_regression'
    enabled: bool = True


#
# Model: Data Processing / Mean Variance
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingMeanVarianceArguments(Mapping[str, Any]):
    data_structure: Literal['pixel', 'photon', 'image', 'signal'] = field(
        default='image',
        metadata=schema(
            title='data_structure'
            ,description='Data bucket to use for the linear regression.'
        )
    )
    name: Optional[str] = field(
        default=None,
        metadata=schema(
            title='name'
            ,description='Name to use for the result.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('data_structure', 'name'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 2


@schema(
    title="Model 'mean_variance'"
    ,description="Compute mean-variance and store it in '.data' bucket."
)
@dataclass
class ModelDataProcessingMeanVariance:
    name: str
    arguments: ModelDataProcessingMeanVarianceArguments = field(default_factory=ModelDataProcessingMeanVarianceArguments)
    func: Literal['pyxel.models.data_processing.mean_variance'] = 'pyxel.models.data_processing.mean_variance'
    enabled: bool = True


#
# Model: Data Processing / Remove Cosmic Rays
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingRemoveCosmicRaysArguments(Mapping[str, Any]):
    contrast: float = field(
        default=1.0,
        metadata=schema(
            title='contrast'
            ,description=(
                    'Contrast threshold between the Laplacian image and the fine-structure '
                    'image.'
                )
        )
    )
    cr_threshold: float = field(
        default=50.0,
        metadata=schema(
            title='cr_threshold'
            ,description=(
                    'The Laplacian signal-to-noise ratio threshold for cosmic-ray '
                    'detection.'
                )
        )
    )
    neighbor_threshold: float = field(
        default=50.0,
        metadata=schema(
            title='neighbor_threshold'
            ,description=(
                    'The Laplacian signal-to-noise ratio threshold for detection of cosmic '
                    'rays in pixels neighboring the initially-identified cosmic rays.'
                )
        )
    )
    effective_gain: float = field(
        default=1.0,
        metadata=schema(
            title='effective_gain'
            ,description='Ratio of counts (e.g., electrons or photons) to the units of data.'
        )
    )
    readnoise: float = field(
        default=0.0,
        metadata=schema(
            title='readnoise'
            ,description='The read noise (in electrons) in the input data.'
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('contrast', 'cr_threshold', 'neighbor_threshold', 'effective_gain', 'readnoise'))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 5


@schema(
    title="Model 'remove_cosmic_rays'"
    ,description=(
        'Extract the roi data converts it to xarray dataset and saves the '
        'information to the final result.'
    )
)
@dataclass
class ModelDataProcessingRemoveCosmicRays:
    name: str
    arguments: ModelDataProcessingRemoveCosmicRaysArguments = field(default_factory=ModelDataProcessingRemoveCosmicRaysArguments)
    func: Literal['pyxel.models.data_processing.remove_cosmic_rays'] = 'pyxel.models.data_processing.remove_cosmic_rays'
    enabled: bool = True


#
# Model: Data Processing / Signal To Noise Ratio
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingSignalToNoiseRatioArguments(Mapping[str, Any]):
    data_structure: Literal['pixel', 'photon', 'signal', 'image', 'all'] = field(
        default='signal',
        metadata=schema(
            title='data_structure'
            ,description=(
                    'Keyword to choose data structure. Can be any from: ("pixel", "photon",'
                    ' "signal", "image", "all"). Default is "signal" and computes the SNR '
                    'on "signal".'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('data_structure',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'signal_to_noise_ratio'"
    ,description='Get signal-to-noise-ratio (SNR) for given data structure.'
)
@dataclass
class ModelDataProcessingSignalToNoiseRatio:
    name: str
    arguments: ModelDataProcessingSignalToNoiseRatioArguments = field(default_factory=ModelDataProcessingSignalToNoiseRatioArguments)
    func: Literal['pyxel.models.data_processing.signal_to_noise_ratio'] = 'pyxel.models.data_processing.signal_to_noise_ratio'
    enabled: bool = True


#
# Model: Data Processing / Statistics
#
@schema(title='Parameters')
@dataclass
class ModelDataProcessingStatisticsArguments(Mapping[str, Any]):
    data_structure: Literal['pixel', 'photon', 'signal', 'image', 'all'] = field(
        default='all',
        metadata=schema(
            title='data_structure'
            ,description=(
                    'Keyword to choose data structure. Can be any from: ("pixel", "photon",'
                    ' "signal", "image", "all"). Default is "all" and computes the '
                    'statistics on "pixel", "photon", "signal" and "image".'
                )
        )
    )
    def __iter__(self) -> Iterator[str]:
        return iter(('data_structure',))
    def __getitem__(self, item: Any) -> Any:
        if item in tuple(self):
            return getattr(self, item)
        else:
            raise KeyError
    def __len__(self) -> int:
        return 1


@schema(
    title="Model 'statistics'"
    ,description='Compute basic statistics.'
)
@dataclass
class ModelDataProcessingStatistics:
    name: str
    arguments: ModelDataProcessingStatisticsArguments = field(default_factory=ModelDataProcessingStatisticsArguments)
    func: Literal['pyxel.models.data_processing.statistics'] = 'pyxel.models.data_processing.statistics'
    enabled: bool = True


#
# Detection pipeline
#
@dataclass
class DetailedDetectionPipeline(DetectionPipeline):
    scene_generation: Optional[
        Sequence[Union[ModelSceneGenerationLoadStarMap, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Scene Generation'))
    photon_collection: Optional[
        Sequence[Union[ModelPhotonCollectionIllumination, ModelPhotonCollectionLoadImage, ModelPhotonCollectionLoadPsf, ModelPhotonCollectionLoadWavelengthPsf, ModelPhotonCollectionOpticalPsf, ModelPhotonCollectionShotNoise, ModelPhotonCollectionSimpleCollection, ModelPhotonCollectionStripePattern, ModelPhotonCollectionWavelengthDependenceAirs, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Photon Collection'))
    phasing: Optional[
        Sequence[Union[ModelPhasingPulseProcessing, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Phasing'))
    charge_generation: Optional[
        Sequence[Union[ModelChargeGenerationApdGain, ModelChargeGenerationApplyQeCurve, ModelChargeGenerationChargeBlocks, ModelChargeGenerationChargeDeposition, ModelChargeGenerationChargeDepositionInMct, ModelChargeGenerationConversionWith3dQeMap, ModelChargeGenerationConversionWithQeMap, ModelChargeGenerationCosmix, ModelChargeGenerationDarkCurrent, ModelChargeGenerationDarkCurrentRule07, ModelChargeGenerationDarkCurrentSaphira, ModelChargeGenerationLoadCharge, ModelChargeGenerationRadiationInducedDarkCurrent, ModelChargeGenerationSimpleConversion, ModelChargeGenerationSimpleDarkCurrent, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Charge Generation'))
    charge_collection: Optional[
        Sequence[Union[ModelChargeCollectionFixedPatternNoise, ModelChargeCollectionPersistence, ModelChargeCollectionSimpleCollection, ModelChargeCollectionSimpleFullWell, ModelChargeCollectionSimpleIpc, ModelChargeCollectionSimplePersistence, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Charge Collection'))
    charge_transfer: Optional[
        Sequence[Union[ModelChargeTransferArcticAdd, ModelChargeTransferArcticRemove, ModelChargeTransferCdm, ModelChargeTransferMultiplicationRegister, ModelChargeTransferMultiplicationRegisterCic, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Charge Transfer'))
    charge_measurement: Optional[
        Sequence[Union[ModelChargeMeasurementAcCrosstalk, ModelChargeMeasurementDcCrosstalk, ModelChargeMeasurementDcOffset, ModelChargeMeasurementKtcNoise, ModelChargeMeasurementNghxrg, ModelChargeMeasurementOutputNodeLinearityPoly, ModelChargeMeasurementOutputNodeNoise, ModelChargeMeasurementOutputNodeNoiseCmos, ModelChargeMeasurementOutputPixelResetVoltageApd, ModelChargeMeasurementPhysicalNonLinearity, ModelChargeMeasurementPhysicalNonLinearityWithSaturation, ModelChargeMeasurementReadoutNoiseSaphira, ModelChargeMeasurementSimpleMeasurement, ModelChargeMeasurementSimplePhysicalNonLinearity, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Charge Measurement'))
    signal_transfer: Optional[
        Sequence[Union[ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Signal Transfer'))
    readout_electronics: Optional[
        Sequence[Union[ModelReadoutElectronicsDeadTimeFilter, ModelReadoutElectronicsSarAdc, ModelReadoutElectronicsSarAdcWithNoise, ModelReadoutElectronicsSimpleAdc, ModelReadoutElectronicsSimpleAmplifier, ModelReadoutElectronicsSimplePhaseConversion, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Readout Electronics'))
    data_processing: Optional[
        Sequence[Union[ModelDataProcessingExtractRoiToXarray, ModelDataProcessingLinearRegression, ModelDataProcessingMeanVariance, ModelDataProcessingRemoveCosmicRays, ModelDataProcessingSignalToNoiseRatio, ModelDataProcessingStatistics, ModelLoadDetector, ModelSaveDetector, ModelFunction]]
    ] = field(default=None, metadata=schema(title='Data Processing'))

@dataclass
class WavelengthHandling:
    cut_on: float
    cut_off: float
    resolution: int

@schema(
    title='Environment',
    description='Environmental attributes of the detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class Environment:
    temperature: Optional[float] = field(
        default=None,
        metadata=schema(
            title='temperature',
            description='Temperature of the detector. Unit: K'
        )
    )
    wavelength: Union[float, WavelengthHandling, None] = field(
        default=None,
        metadata=schema(
            title='wavelength',
            description='Information about multi-wavelength. Unit: nm'
        )
    )


@schema(
    title='Characteristics',
    description='Characteristic attributes of the detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class Characteristics:
    quantum_efficiency: Optional[float] = field(
        default=None,
        metadata=schema(
            title='quantum_efficiency',
            description='Quantum efficiency.'
        )
    )
    charge_to_volt_conversion: Optional[float] = field(
        default=None,
        metadata=schema(
            title='charge_to_volt_conversion',
            description='Sensitivity of charge readout. Unit: V/e-'
        )
    )
    pre_amplification: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pre_amplification',
            description='Gain of pre-amplifier. Unit: V/V'
        )
    )
    full_well_capacity: Optional[float] = field(
        default=None,
        metadata=schema(
            title='full_well_capacity',
            description='Full well capacity. Unit: e-'
        )
    )
    adc_voltage_range: Optional[tuple[float, float]] = field(
        default=None,
        metadata=schema(
            title='adc_voltage_range',
            description='ADC voltage range. Unit: V'
        )
    )
    adc_bit_resolution: Optional[int] = field(
        default=None,
        metadata=schema(
            title='adc_bit_resolution',
            description='ADC bit resolution.'
        )
    )


@schema(
    title='Geometry',
    description='Geometrical attributes of the detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class Geometry:
    row: int = field(
        metadata=schema(
            title='row',
            description='Number of pixel rows.'
        )
    )
    col: int = field(
        metadata=schema(
            title='col',
            description='Number of pixel columns.'
        )
    )
    total_thickness: Optional[float] = field(
        default=None,
        metadata=schema(
            title='total_thickness',
            description='Thickness of detector. Unit: um'
        )
    )
    pixel_vert_size: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_vert_size',
            description='Vertical dimension of pixel. Unit: um'
        )
    )
    pixel_horz_size: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_horz_size',
            description='Horizontal dimension of pixel. Unit: um'
        )
    )
    pixel_scale: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_scale',
            description=(
                    'Dimension of how much of the sky is covered by one pixel. Unit: '
                    'arcsec/pixel'
                )
        )
    )


@schema(
    title='APDCharacteristics',
    description='Characteristic attributes of the APD detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class APDCharacteristics:
    roic_gain: float = field(
        metadata=schema(
            title='roic_gain',
            description='Gain of the read-out integrated circuit. Unit: V/V'
        )
    )
    quantum_efficiency: Optional[float] = field(
        default=None,
        metadata=schema(
            title='quantum_efficiency',
            description='Quantum efficiency.'
        )
    )
    full_well_capacity: Optional[float] = field(
        default=None,
        metadata=schema(
            title='full_well_capacity',
            description='Full well capacity. Unit: e-'
        )
    )
    adc_bit_resolution: Optional[int] = field(
        default=None,
        metadata=schema(
            title='adc_bit_resolution',
            description='ADC bit resolution.'
        )
    )
    adc_voltage_range: Optional[tuple[float, float]] = field(
        default=None,
        metadata=schema(
            title='adc_voltage_range',
            description='ADC voltage range. Unit: V'
        )
    )
    avalanche_gain: Optional[float] = field(
        default=None,
        metadata=schema(
            title='avalanche_gain',
            description='APD gain. Unit: electron/electron'
        )
    )
    pixel_reset_voltage: Optional[float] = field(
        default=None,
        metadata=schema(
            title='pixel_reset_voltage',
            description=(
                    'DC voltage going into the detector, not the voltage of a reset pixel. '
                    'Unit: V'
                )
        )
    )
    common_voltage: Optional[float] = field(
        default=None,
        metadata=schema(
            title='common_voltage',
            description='Common voltage. Unit: V'
        )
    )


@schema(
    title='Detector',
    description='The detector base class.'
)
@dataclass(kw_only=True)  # Python 3.10+
class Detector:
    environment: Optional[Environment] = field(
        default=None,
        metadata=schema(
            title='environment'
        )
    )


@schema(
    title='CCDGeometry',
    description='Geometrical attributes of a :term:`CCD` detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class CCDGeometry(Geometry):
    pass


@schema(
    title='CMOSGeometry',
    description='Geometrical attributes of a :term:`CMOS`-based detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class CMOSGeometry(Geometry):
    pass


@schema(
    title='MKIDGeometry',
    description='Geometrical attributes of a :term:`MKID`-based detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class MKIDGeometry(Geometry):
    pass


@schema(
    title='APDGeometry',
    description='Geometrical attributes of a :term:`APD`-based detector.'
)
@dataclass(kw_only=True)  # Python 3.10+
class APDGeometry(Geometry):
    pass


@schema(
    title='CCD',
    description=(
        ':term:`Charge-Coupled Device<CCD>` class containing all detector '
        'attributes and data.'
        )
)
@dataclass(kw_only=True)  # Python 3.10+
class CCD(Detector):
    geometry: CCDGeometry = field(
        metadata=schema(
            title='geometry'
        )
    )
    characteristics: Characteristics = field(
        metadata=schema(
            title='characteristics'
        )
    )


@schema(
    title='CMOS',
    description=(
        ':term:`CMOS`-based detector class containing all detector attributes '
        'and data.'
        )
)
@dataclass(kw_only=True)  # Python 3.10+
class CMOS(Detector):
    geometry: CMOSGeometry = field(
        metadata=schema(
            title='geometry'
        )
    )
    characteristics: Characteristics = field(
        metadata=schema(
            title='characteristics'
        )
    )


@schema(
    title='MKID',
    description=(
        ':term:`MKID`-based detector class containing all detector attributes '
        'and data.'
        )
)
@dataclass(kw_only=True)  # Python 3.10+
class MKID(Detector):
    geometry: MKIDGeometry = field(
        metadata=schema(
            title='geometry'
        )
    )
    characteristics: Characteristics = field(
        metadata=schema(
            title='characteristics'
        )
    )


@schema(
    title='APD',
    description=(
        ':term:`CMOS`-based detector class containing all detector attributes '
        'and data.'
        )
)
@dataclass(kw_only=True)  # Python 3.10+
class APD(Detector):
    geometry: APDGeometry = field(
        metadata=schema(
            title='geometry'
        )
    )
    characteristics: APDCharacteristics = field(
        metadata=schema(
            title='characteristics'
        )
    )



#
# Outputs
#
ValidName = Literal[
    'detector.image.array', 'detector.signal.array', 'detector.pixel.array'
]
ValidFormat = Literal['fits', 'hdf', 'npy', 'txt', 'csv', 'png', 'jpg', 'jpeg']


@dataclass
class Outputs:
    output_folder: pathlib.Path
    save_data_to_file: Optional[
        Sequence[Mapping[ValidName, Sequence[ValidFormat]]]
    ] = None


#
# Exposure
#
@dataclass
class ExposureOutputs(Outputs):
    save_exposure_data: Optional[
        Sequence[Mapping[str, Sequence[str]]]
    ] = None
@dataclass
class Readout:
    times: Union[Sequence, str, None] = None
    times_from_file: Optional[str] = None
    start_time: float = 0.0
    non_destructive: bool = False


@schema(title='Exposure')
@dataclass
class Exposure:
    outputs: ExposureOutputs
    readout: Readout = field(default_factory=Readout)
    result_type: Literal['image', 'signal', 'pixel', 'all'] = 'all'
    pipeline_seed: Optional[int] = None


#
# Observation
#


@dataclass
class ObservationOutputs(Outputs):
    save_observation_data: Optional[
        Sequence[Mapping[str, Sequence[str]]]
    ] = None


@dataclass
class ParameterValues:
    key: str
    values: Union[
        Literal['_'],
        Sequence[Literal['_']],
        Sequence[Union[int, float]],
        Sequence[Sequence[Union[int, float]]],
        Sequence[Sequence[Sequence[Union[int, float]]]],
        Sequence[str],
        str, # e.g. 'numpy.unique(...)'
    ]
    boundaries: Union[Tuple[float, float], Sequence[Tuple[float, float]], None] = None
    enabled: bool = True
    logarithmic: bool = False


@schema(title='Observation')
@dataclass
class Observation:
    outputs: ObservationOutputs
    parameters: Sequence[ParameterValues]
    readout: Optional[Readout] = None
    mode: Literal['product', 'sequential', 'custom'] = 'product'
    from_file: Optional[str] = None
    column_range: Optional[Tuple[int, int]] = None
    with_dask: bool = False
    result_type: Literal['image', 'signal', 'pixel', 'all'] = 'all'
    pipeline_seed: Optional[int] = None


#
# Calibration
#
@dataclass
class CalibrationOutputs(Outputs):
    save_calibration_data: Optional[
        Sequence[Mapping[str, Sequence[str]]]
    ] = None


@dataclass
class Algorithm:
    type: Literal['sade', 'sga', 'nlopt'] = 'sade'
    generations: int = 1
    population_size: int = 1
    # SADE #####
    variant: int = 2
    variant_adptv: int = 1
    ftol: float = 1e-6
    xtol: float = 1e-6
    memory: bool = False
    # SGA #####
    cr: float = 0.9
    eta_c: float = 1.0
    m: float = 0.02
    param_m: float = 1.0
    param_s: int = 2
    crossover: Literal['single', 'exponential', 'binominal', 'sbx'] = 'exponential'
    mutation: Literal['uniform', 'gaussian', 'polynomial'] = 'polynomial'
    selection: Literal['tournament', 'truncated'] = 'tournament'
    # NLOPT #####
    nlopt_solver: Literal[
        'cobyla', 'bobyqa', 'newuoa', 'newuoa_bound', 'praxis', 'neldermead',
        'sbplx', 'mma', 'ccsaq', 'slsqp', 'lbfgs', 'tnewton_precond_restart',
        'tnewton_precond', 'tnewton_restart', 'tnewton', 'var2', 'var1', 'auglag',
        'auglag_eq'
    ] = 'neldermead'
    maxtime: int = 0
    maxeval: int = 0
    xtol_rel: float = 1.0e-8
    xtol_abs: float = 0.0
    ftol_rel: float = 0.0
    ftol_abs: float = 0.0
    stopval: Optional[float] = None
    # local_optimizer: Optional['pg.nlopt'] = None
    replacement: Literal['best', 'worst', 'random'] = 'best'
    nlopt_selection: Literal['best', 'worst', 'random'] = 'best'


@schema(title='Fitness function')
@dataclass
class FitnessFunction:
    func: str
    arguments: Optional[Mapping[str, Any]] = None


@schema(title='Calibration')
@dataclass
class Calibration:
    outputs: CalibrationOutputs
    target_data_path: Sequence[pathlib.Path]
    fitness_function: FitnessFunction
    algorithm: Algorithm
    parameters: Sequence[ParameterValues]
    readout: Optional[Readout] = None
    mode: Literal['pipeline', 'single_model'] = 'pipeline'
    result_type: Literal['image', 'signal', 'pixel'] = 'image'
    result_fit_range: Optional[Sequence[int]] = None
    result_input_arguments: Optional[Sequence[ParameterValues]] = None
    target_fit_range: Optional[Sequence[int]] = None
    pygmo_seed: Optional[int] = None
    pipeline_seed: Optional[int] = None
    num_islands: int = 1
    num_evolutions: int = 1
    num_best_decisions: Optional[int] = None
    topology: Literal['unconnected', 'ring', 'fully_connected'] = 'unconnected'
    type_islands: Literal[
        'multiprocessing', 'multithreading', 'ipyparallel'
    ] = 'multiprocessing'
    weights_from_file: Optional[Sequence[pathlib.Path]] = None
    weights: Optional[Sequence[float]] = None



@dataclass
class Configuration_Exposure_CCD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    exposure: Exposure = field(metadata=schema(title='Exposure'))
    ccd_detector: CCD = field(metadata=schema(title='CCD'))
@dataclass
class Configuration_Exposure_CMOS:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    exposure: Exposure = field(metadata=schema(title='Exposure'))
    cmos_detector: CMOS = field(metadata=schema(title='CMOS'))
@dataclass
class Configuration_Exposure_MKID:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    exposure: Exposure = field(metadata=schema(title='Exposure'))
    mkid_detector: MKID = field(metadata=schema(title='MKID'))
@dataclass
class Configuration_Exposure_APD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    exposure: Exposure = field(metadata=schema(title='Exposure'))
    apd_detector: APD = field(metadata=schema(title='APD'))
@dataclass
class Configuration_Observation_CCD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    observation: Observation = field(metadata=schema(title='Observation'))
    ccd_detector: CCD = field(metadata=schema(title='CCD'))
@dataclass
class Configuration_Observation_CMOS:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    observation: Observation = field(metadata=schema(title='Observation'))
    cmos_detector: CMOS = field(metadata=schema(title='CMOS'))
@dataclass
class Configuration_Observation_MKID:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    observation: Observation = field(metadata=schema(title='Observation'))
    mkid_detector: MKID = field(metadata=schema(title='MKID'))
@dataclass
class Configuration_Observation_APD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    observation: Observation = field(metadata=schema(title='Observation'))
    apd_detector: APD = field(metadata=schema(title='APD'))
@dataclass
class Configuration_Calibration_CCD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    calibration: Calibration = field(metadata=schema(title='Calibration'))
    ccd_detector: CCD = field(metadata=schema(title='CCD'))
@dataclass
class Configuration_Calibration_CMOS:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    calibration: Calibration = field(metadata=schema(title='Calibration'))
    cmos_detector: CMOS = field(metadata=schema(title='CMOS'))
@dataclass
class Configuration_Calibration_MKID:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    calibration: Calibration = field(metadata=schema(title='Calibration'))
    mkid_detector: MKID = field(metadata=schema(title='MKID'))
@dataclass
class Configuration_Calibration_APD:
    pipeline: DetailedDetectionPipeline = field(metadata=schema(title='Pipeline'))
    calibration: Calibration = field(metadata=schema(title='Calibration'))
    apd_detector: APD = field(metadata=schema(title='APD'))
class NotEqualError(Exception):
    ...

def compare(first, second) -> None:
    if type(first) != type(second):
        raise NotEqualError

    if isinstance(first, dict) and isinstance(second, dict):
        if set(first) != set(second):
            raise NotEqualError

        for key in first:
            compare(first[key], second[key])

    elif isinstance(first, list) and isinstance(second, list):
        if len(first) != len(second):
            raise NotEqualError

        if first != second:
            sorted_first = sorted(first)
            sorted_second = sorted(second)

            if sorted_first != sorted_second:
                raise NotEqualError
    else:
        if first != second:
            raise NotEqualError


@click.command()
@click.option(
    '-f',
    '--filename',
    default='../../static/pyxel_schema.json',
    type=click.Path(),
    help='JSON schema filename',
    show_default=True,
)
@click.option('--check', is_flag=True,
     help="Don't write the JSON Schema back, just return the status.")
def create_json_schema(filename: pathlib.Path, check: bool):
    if sys.version_info < (3, 10):
        raise NotImplementedError('This script must run on Python 3.10+')

    # Manually define a 'format' for JSON Schema for 'Path'
    schema(format='uri')(Path)

    dct_schema = deserialization_schema(
        Union[Configuration_Exposure_CCD,Configuration_Exposure_CMOS,Configuration_Exposure_MKID,Configuration_Exposure_APD,Configuration_Observation_CCD,Configuration_Observation_CMOS,Configuration_Observation_MKID,Configuration_Observation_APD,Configuration_Calibration_CCD,Configuration_Calibration_CMOS,Configuration_Calibration_MKID,Configuration_Calibration_APD], version=JsonSchemaVersion.DRAFT_7, all_refs=True
    )


    full_filename = pathlib.Path(filename).resolve()

    if check:
        with full_filename.open() as fh:
            dct_reference = json.load(fh)

        new_dct_schema: Mapping[str, Any] = json.loads(json.dumps(dct_schema))

        try:
           compare(dct_reference, new_dct_schema)
        except NotEqualError:
            print(
                f"Error, JSON Schema file: {full_filename} is not the newest version. "
                f"Please run 'tox -e json_schema'"
             )
            pprint(result)
            sys.exit(1)
        else:
            sys.exit(0)
    else:
        print(json.dumps(dct_schema))
        with full_filename.open('w') as fh:
            json.dump(obj=dct_schema, fp=fh, indent=2, sort_keys=True)


if __name__ == '__main__':
    create_json_schema()
