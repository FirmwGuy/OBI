# OBI Hardware GPIO Profile
## OBI Profile: `obi.profile:hw.gpio-0`

**Document Type:** Profile specification (normative)  
**Profile ID:** `obi.profile:hw.gpio-0`  
**Status:** Draft  
**Last Updated:** 2026-03-05

---

## 1. Nontechnical Summary

This profile defines a small ABI for basic GPIO (General-Purpose Input/Output) line access:

- open a GPIO line by chip path and line offset,
- configure direction and optional bias/edge detection,
- read/write digital values,
- optionally receive edge events.

The initial target is user-space GPIO access on Linux SBCs (notably Raspberry Pi). Hosts should
expect this profile to be unsupported on platforms without user-accessible GPIO.

---

## 2. Technical Details

### 2.1 Scope

In scope:

- user-space GPIO line I/O (read/write digital 0/1)
- optional edge event observation (rising/falling)

Out of scope:

- kernel/driver authoring
- privileged MMIO-only interfaces unless explicitly documented by a provider
- analog I/O, PWM, and high-level bus protocols (I2C/SPI/UART)

### 2.2 Chip and line identification

- A GPIO chip is identified by `chip_path` (UTF-8, NUL-terminated).
  - Example on Linux: `/dev/gpiochip0`
- A line is identified by `line_offset` (a provider-specific integer offset within the chip).

### 2.3 Ownership and lifetime

- `line_open()` returns a provider-owned `obi_gpio_line_id_v0`.
- The host destroys the line with `line_close()`.

### 2.4 Edge events

If edge events are supported (`OBI_GPIO_CAP_EDGE_EVENTS`), providers implement `event_next()` which:

- waits up to `timeout_ns` for the next event
- returns OK and sets `out_has_event` to indicate whether an event was observed
- may honor cancellation (`OBI_GPIO_CAP_CANCEL`) via `obi_cancel_token_v0`

---

## 3. Conformance

Required:

- `line_open`, `line_close`
- `line_get_value`, `line_set_value`

Optional (advertised via caps):

- edge events: `OBI_GPIO_CAP_EDGE_EVENTS` + `event_next`
- bias configuration: `OBI_GPIO_CAP_BIAS`
- cancellation during waits: `OBI_GPIO_CAP_CANCEL`
- provider-specific options: `OBI_GPIO_CAP_OPTIONS_JSON`

Testing note:

- GPIO conformance testing is hardware-specific and should be treated as **pending** unless running
  on a real SBC/test jig.

---

## 4. ABI Reference

The normative C ABI for this profile is defined in:

- `abi/profiles/obi_hw_gpio_v0.h`

---

## Global Q&A

**Q: Why not use the legacy Linux GPIO sysfs interface?**  
sysfs GPIO is deprecated. Modern Linux exposes GPIO via the character device ABI; user-space
libraries (for example libgpiod) build on that.

**Q: Why is this Linux/SBC-focused?**  
GPIO availability and permission models vary widely. The profile is designed so unsupported
platforms can return `OBI_STATUS_UNSUPPORTED`.

