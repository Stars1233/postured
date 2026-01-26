from PyQt6.QtCore import QSettings


class Settings:
    """Application settings using Qt's QSettings.

    Stores config in ~/.config/postured/postured.conf (on Linux).
    """

    # Default values
    DEFAULTS = {
        'sensitivity': 0.85,
        'dead_zone': 0.03,
        'camera_index': 0,
        'dim_when_away': False,
        'good_posture_y': 0.4,
        'bad_posture_y': 0.6,
        'is_calibrated': False,
    }

    def __init__(self):
        self._settings = QSettings('postured', 'postured')

    @property
    def sensitivity(self) -> float:
        return float(self._settings.value('sensitivity', self.DEFAULTS['sensitivity']))

    @sensitivity.setter
    def sensitivity(self, value: float):
        self._settings.setValue('sensitivity', value)

    @property
    def dead_zone(self) -> float:
        return float(self._settings.value('dead_zone', self.DEFAULTS['dead_zone']))

    @dead_zone.setter
    def dead_zone(self, value: float):
        self._settings.setValue('dead_zone', value)

    @property
    def camera_index(self) -> int:
        return int(self._settings.value('camera_index', self.DEFAULTS['camera_index']))

    @camera_index.setter
    def camera_index(self, value: int):
        self._settings.setValue('camera_index', value)

    @property
    def dim_when_away(self) -> bool:
        return self._settings.value('dim_when_away', self.DEFAULTS['dim_when_away'], type=bool)

    @dim_when_away.setter
    def dim_when_away(self, value: bool):
        self._settings.setValue('dim_when_away', value)

    @property
    def good_posture_y(self) -> float:
        return float(self._settings.value('good_posture_y', self.DEFAULTS['good_posture_y']))

    @good_posture_y.setter
    def good_posture_y(self, value: float):
        self._settings.setValue('good_posture_y', value)

    @property
    def bad_posture_y(self) -> float:
        return float(self._settings.value('bad_posture_y', self.DEFAULTS['bad_posture_y']))

    @bad_posture_y.setter
    def bad_posture_y(self, value: float):
        self._settings.setValue('bad_posture_y', value)

    @property
    def is_calibrated(self) -> bool:
        return self._settings.value('is_calibrated', self.DEFAULTS['is_calibrated'], type=bool)

    @is_calibrated.setter
    def is_calibrated(self, value: bool):
        self._settings.setValue('is_calibrated', value)

    def sync(self):
        """Force write settings to disk."""
        self._settings.sync()
