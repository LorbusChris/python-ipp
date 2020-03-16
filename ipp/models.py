"""Models for IPP."""
from dataclasses import dataclass
from typing import List

PRINTER_STATES = {3: "idle", 4: "printing", 5: "stopped"}

@dataclass(frozen=True)
class Info:
    """Object holding information from IPP."""

    name: str
    uptime: int
    uuid: str
    version: str

    @staticmethod
    def from_dict(data: dict):
        """Return Info object from IPP API response."""
        uuid = data.get("printer-uuid", None)

        return Info(
            name=data.get("printer-make-and-model", "IPP Generic Printer"),
            uptime=data.get("printer-up-time", 0),
            uuid=uuid[9:] if uuid else None,
            version=data.get("printer-firmware-string-version", "Unknown"),
        )


@dataclass(frozen=True)
class Marker:
    """Object holding marker (ink) info from IPP."""

    marker_id: int
    marker_type: str
    name: str
    color: str
    level: int
    low_level: int
    high_level: int


@dataclass(frozen=True)
class Printer:
    """Object holding the IPP printer information."""

    info: Info
    markers: List[Marker]
    state: State

    @staticmethod
    def from_dict(data):
        """Return Printer object from IPP API response."""
        marker_colors = data.get("marker-colors", [])
        marker_levels = data.get("marker-levels", [])
        marker_high_levels = data.get("marker-high-levels", [])
        marker_low_levels = data.get("marker-low-levels", [])
        marker_types = data.get("marker-types", [])
        markers = [
            Marker(
                marker_id=marker_id,
                marker_type=marker_types[marker_id],
                name=marker,
                color=marker_colors[marker_id],
                level=marker_levels[marker_id],
                high_level=marker_high_levels[marker_id],
                low_level=marker_low_levels[marker_id],
            )
            for marker_id, marker in enumerate(data.get("marker-names", {}))
        ]
        markers.sort(key=lambda x: x.name)

        return Printer(
            info=Info.from_dict(data),
            markers=markers,
            state=State.from_dict(data)
        )

@dataclass(frozen=True)
class State:
    ""Object holding the IPP printer state."""

    
    state: str
    reasons: List[str]
    message: str

    @staticmethod
    def from_dict(data):
        """Return State object from IPP API response."""
        state=data.get("printer-state", 0)

        return State(
            state=PRINTER_STATES.get(state, state),
            reasons=data.get("printer-state-reasons", []),
            message=data.get("printer-state-message", None),
        )
        



