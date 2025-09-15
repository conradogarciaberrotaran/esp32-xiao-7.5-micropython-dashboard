"""
Clean Dashboard using Adafruit Display Libraries
Uses adafruit_display_text, adafruit_displayio_layout, and shapes
"""

try:
    from epaperdisplay import EPaperDisplay
except ImportError:
    from adafruit_epaperdisplay import EPaperDisplay

import time

import busio
import displayio
import microcontroller
import terminalio
from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.layouts.page_layout import PageLayout
from fourwire import FourWire

displayio.release_displays()

_START_SEQUENCE = (
    b"\x01\x04\x07\x07\x3f\x3f"  # POWERSETTING
    b"\x04\x00"  # POWERON
    b"\x00\x01\x1f"  # PANELSETTING - using working value 0x1F
    b"\x61\x04\x00\x00\x00\x00"  # TRES: resolution
    b"\x15\x01\x00"  # DUALSPI: single SPI
    b"\x50\x02\x10\x07"  # WRITE_VCOM
    b"\x60\x01\x22"  # TCON
)

_STOP_SEQUENCE = b"\x02\x00"  # POWEROFF


class UC8179(EPaperDisplay):
    """UC8179 ePaper display driver"""

    def __init__(self, bus, **kwargs):
        width = kwargs.get("width", 800)
        height = kwargs.get("height", 600)

        width = (width + 7) // 8 * 8

        start_sequence = bytearray(_START_SEQUENCE)
        start_sequence[13] = width >> 8
        start_sequence[14] = width & 0xFF
        start_sequence[15] = height >> 8
        start_sequence[16] = height & 0xFF

        if "highlight_color" in kwargs:
            color_ram_command = 0x13
            black_ram_command = 0x10
        else:
            color_ram_command = None
            black_ram_command = 0x13

        super().__init__(
            bus,
            start_sequence,
            _STOP_SEQUENCE,
            **kwargs,
            ram_width=800,
            ram_height=600,
            busy_state=False,
            write_black_ram_command=black_ram_command,
            write_color_ram_command=color_ram_command,
            refresh_display_command=0x12,
            refresh_time=16,
            always_toggle_chip_select=True,
        )


spi = busio.SPI(microcontroller.pin.GPIO8, microcontroller.pin.GPIO10)
epd_cs = microcontroller.pin.GPIO3
epd_dc = microcontroller.pin.GPIO5
epd_reset = microcontroller.pin.GPIO2
epd_busy = microcontroller.pin.GPIO4

display_bus = FourWire(spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=1000000)
time.sleep(1)

display = UC8179(
    display_bus,
    width=800,
    height=480,
    busy_pin=epd_busy,
    rotation=0,
    black_bits_inverted=True,
    colstart=0,
)


def main():
    main_group = displayio.Group()

    display.root_group = main_group

    test_page_layout = PageLayout(x=0, y=0)

    page_1_lbl = Label(
        font=terminalio.FONT,
        scale=2,
        text="This is the first page!",
        anchor_point=(0, 0),
        anchored_position=(10, 10),
    )

    page_2_lbl = Label(
        font=terminalio.FONT,
        scale=2,
        text="This page is the second page!",
        anchor_point=(0, 0),
        anchored_position=(10, 10),
    )

    page_1_group = displayio.Group()

    page_2_group = displayio.Group()

    page_1_group.append(page_1_lbl)

    page_2_group.append(page_2_lbl)

    test_page_layout.add_content(page_1_group, "page_1")

    test_page_layout.add_content(page_2_group, "page_2")

    main_group.append(test_page_layout)
    display.root_group = main_group
    display.refresh()

    while True:
        time.sleep(display.time_to_refresh + 5)

        test_page_layout.next_page()
        display.refresh()


if __name__ == "__main__":
    main()
