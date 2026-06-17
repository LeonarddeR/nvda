# Handy Tech extended packets — gaps in NVDA vs. Handy Tech's own driver

Reverse-engineered from `C:\Sources\HT\jaws\handy.jlb` (Help Tech JAWS braille driver,
x86-64, 2023, full RTTI). Companion to
[`handyTechAtcReverseEngineered.md`](./handyTechAtcReverseEngineered.md). Tooling and
disassembly dumps as described there (`C:\Sources\HT\re\`).

Scope: which extended packet **send** and **receive** paths NVDA's
`source/brailleDisplayDrivers/handyTech.py` is missing, and the correct layout for the
`GET_PROTOCOL_PROPERTIES` (`0xc1`) response.

## `GET_PROTOCOL_PROPERTIES` (`0xc1`) — full response layout

This is the most consequential gap. NVDA currently parses only three bytes:

```python
elif extPacketType == HT_EXTPKT_GET_PROTOCOL_PROPERTIES:
    self._protocolVersion = (packet[1], packet[2])
    self.numCells = packet[3]
```

Handy Tech's parser (`fcn.180017e50`, reached from the device init handshake) reads **seven**
data bytes. With `packet[0]` = the `0xc1` type byte, the data bytes map as:

| `packet[]` | field | HT log string | stored at (device obj) |
| --- | --- | --- | --- |
| `[1]` | protocol **major** version | `Protocol version: %d.%d` | — |
| `[2]` | protocol **minor** version | (same) | — |
| `[3]` | display **cell count** | `display cell count: %d` | numCells |
| `[4]` | **supports ATC** (bool, `== 1`) | `support ATC: %d` | `+0x60` |
| `[5]` | **max ATC sensitivity step** | `max ATC sensitivity step: %d` | `+0x121` |
| `[6]` | **supports ATC** — second variant (bool, `== 1`) | `support ATC: %d` | `+0x122` |
| `[7]` | **max ATC sensitivity step** — second variant | `max ATC sensitivity step: %d` | `+0x123` |

The driver therefore **discovers ATC support and the sensitivity range from the device**,
rather than hard-coding them per model class.

### Interpretation of the two capability pairs

Bytes `[4]/[5]` and `[6]/[7]` are two independent `(supportsAtc, maxSensitivityStep)`
pairs. The most likely meaning, given Handy Tech runs two ATC protocols:

* `[4]/[5]` → **legacy ATC** (Modular Evolution: `SET_ATC_MODE 0x50`,
  `SET_ATC_SENSITIVITY 0x51` encoded as `0xFF − step*0x28`, `ATC_INFO 0x52` pressure map).
* `[6]/[7]` → **reading-position ATC** (Active family: `SET_ATC_SENSITIVITY_2 0x53` direct
  value, `READING_POSITION 0x55`).

> Confidence: the byte offsets, the `== 1` bool test, and the storage fields are **confirmed**
> from the disassembly. The *legacy-vs-reading-position* split of the two pairs is an
> **inference** from the duplicated log strings plus the two known ATC protocols — worth
> confirming against Help Tech's protocol spec before relying on it.

### Recommendation for NVDA

* Parse all seven bytes. Use `packet[4]`/`packet[6]` to decide ATC capability and which ATC
  protocol the device speaks, instead of selecting `AtcMixin` vs `AtcReadingPositionMixin`
  purely by model subclass.
* Drive the `atcSensitivity` setting's valid range from the reported max-step
  (`packet[5]`/`packet[7]`) instead of the hard-coded `0..6`.
* Keep the model-class defaults as a fallback for devices/firmware that don't return the
  full structure (older firmware returns a shorter payload — see firmware note below).
* Guard the reads: only `packet[1..3]` are guaranteed; treat `packet[4..7]` as optional and
  fall back to model defaults when the payload is short.

## Full receive dispatcher trace

Handy Tech's receive path is two functions on the device class (shared by `Actilino`,
`ActiveBraille`, `BasicBraille`, `HsiBraille`, `Activator`, …):

* **`fcn.1800179f0`** — a **byte-at-a-time framing state machine** (NVDA's
  `_processHidSerialBuffer` / `_handleInputStream` equivalent). Fed one byte at a time;
  advances a parser state and, on a complete packet, returns a "ready" code.
* **`Actilino::virtual_336`** (`0x1800174c0`) — the **dispatcher**: calls the state machine,
  and when a complete packet is ready, switches on the stored command byte.

### Framing state machine (`fcn.1800179f0`)

State is held in `this+0x88`; the in-progress packet is accumulated into device fields:

| field | meaning |
| --- | --- |
| `+0x88` | parse state (0–5) |
| `+0x8c` | flag: current packet is an `OK`/reset (not an extended packet) |
| `+0x90` | data-byte index while collecting |
| `+0x94` | received command/type byte |
| `+0x98` | received data-byte count |
| `+0x9c …` | received data bytes |
| `+0x10` | expected device model id (for the model-id byte check) |

State transitions per incoming byte `b`:

| state | expects | action |
| --- | --- | --- |
| 0 | start byte | `b==0x79` (EXTENDED) → state 1. `b==0xfe` (OK) → state 1, set `+0x8c`. else → error (ret 6). |
| 1 | model id | `b==model`: extended → state 2 (ret 1); OK packet → state 0, packet complete (ret 5). mismatch → error (ret 6, *"Braille protocol mismatch"*). |
| 2 | length | `+0x98 = b − 1` (wire length includes the command byte), reset index, → state 3 (ret 2). |
| 3 | command byte | `+0x94 = b`; if `+0x98 > 0` → state 4, else state 5 (ret 3). |
| 4 | data bytes | store `+0x9c[idx++] = b`; when `idx == +0x98` → state 5 (ret 4). |
| 5 | terminator | `b==0x16` → state 0, packet complete (ret 5). else → error (ret 6). |

Return code semantics used by the dispatcher: **5 = a complete packet is ready**, 6 = framing
/ protocol / model mismatch, 0–4 = still mid-packet.

So the on-wire formats (identical to NVDA's understanding):

```
extended:  0x79  <modelId>  <len>  <cmd>  <data[len-1]>  0x16      ; len = #data + 1
OK/reset:  0xfe  <modelId>                                          ; sets ack/reset
```

### Command dispatch (`virtual_336`, only when a complete packet is ready)

If the completed packet was an `OK`/reset (`+0x8c` set): notify the ack observer and
`SetEvent` the reset event (`+0x38`). Otherwise switch on the command byte `+0x94`
(data at `+0x9c`, count `+0x98`). Each handler that the init handshake waits on calls
`SetEvent` on a dedicated event so the synchronous request/response helpers wake up:

| cmd | NVDA const | len | HT action | event |
| --- | --- | --- | --- | --- |
| `0x04` | `KEY` | N | for each of N bytes → key handler (vtable `+0x158`) | — |
| `0x05` | *(none)* | N | for each of N bytes → a **second input handler** (vtable `+0x160`) | — |
| `0x07` | `CONFIRMATION` | 1–2 | `data[0]==0x7e` ACK → `SetEvent(+0x40)`; NAK → decode `data[1]` reason (`fcn.180017d50`) | ack `+0x40` |
| `0x54` | `GET_ATC_SENSITIVITY_2` | 1 | store sensitivity → `+0x118` | `+0x100` |
| `0x55` | `READING_POSITION` | 1 | `data[0]==0xff` → "no touch" (observer vtable `+0x40`); else focal cell → reading-position handler (observer vtable `+0x38`) → ATC decider | — |
| `0x61` | `GET_FIRMNESS` | 1 | store dot firmness → `+0x11c` | `+0x108` |
| `0xc1` | `GET_PROTOCOL_PROPERTIES` | **11** | parse (see above) | `+0x110` |
| else | — | N | log `unknown command: 0x%02x` + dump `additional user data` | — |

The NAK reason byte decoded by `fcn.180017d50`: **1** = unknown command byte, **2** = wrong
count of data bytes, **3** = invalid value, **4** = protocol mismatch.

### Notes from the trace

* **Protocol properties is an 11-byte payload** (`+0x98 == 0xb`), but this firmware's parser
  consumes only bytes 0–6 (version, cell count, two ATC capability pairs). Bytes 7–10 are
  reserved / unused here — NVDA should length-check `0xb` but tolerate shorter.
* **Command `0x05` is a second per-byte input stream** that NVDA has no constant or handler
  for (routed to a different vtable slot than `KEY 0x04`). Worth identifying on the wire — it
  may carry secondary controls (e.g. a separate key bank / status). Currently NVDA would log
  it as an unhandled extended packet.
* **`CONFIRMATION 0x07` carries a NAK reason byte** that NVDA ignores (it just logs
  `"NAK received!"`). Decoding it (unknown-command / wrong-count / invalid-value /
  protocol-mismatch) would make protocol bugs far easier to diagnose.
* This shared dispatcher does **not** handle `ATC_INFO 0x52` (pressure map — separate input
  path, `JawsInputProcessor::virtual_48`, see the ATC doc), `SCANCODE 0x09` (HID-keyboard
  passthrough, separate), or `GET_RTC 0x45` / `SERIAL_NUMBER 0x41` /
  `GET_FIRMWARE_VERSION 0xc2` / `PING 0x19`. The RTC/firmware/serial responses are not
  received in this code path at all — NVDA's `GET_RTC` handling has no counterpart here, so
  validate RTC behaviour against a real device rather than assuming parity.
* The whole exchange is **synchronous request/response during init**: send a `GET_*`, then
  block on the matching event (`+0x100`/`+0x108`/`+0x110`/`+0x40`) with a timeout
  (`WaitForMultipleObjects` against a shutdown event). NVDA's model is event-driven receive
  instead, which is fine, but explains why the device only answers `GET_*` requests.

## Missing **send** paths in NVDA

NVDA's `sendExtendedPacket` call sites cover: braille data, `SET_ATC_MODE`,
`SET_ATC_SENSITIVITY`, `SET_ATC_SENSITIVITY_2`, `GET_ATC_SENSITIVITY_2`, `GET_RTC`,
`SET_RTC`, `GET_FIRMNESS`, `SET_FIRMNESS`, `GET_PROTOCOL_PROPERTIES`, `NO_RECONNECT`.

Defined-but-never-sent (and not parsed on receive):

| Packet | const in NVDA | What HT uses it for | Impact |
| --- | --- | --- | --- |
| `GET_FIRMWARE_VERSION` `0xc2` | `HT_EXTPKT_GET_FIRMWARE_VERSION` | HT keys protocol behaviour off firmware version (e.g. *"Modular with firmware version 1.10 detected. Uses not extended protocol."*) | NVDA can't read firmware; can't make firmware-conditional decisions or surface it for support |
| `SERIAL_NUMBER` `0x41` | `HT_EXTPKT_SERIAL_NUMBER` | HT reads and displays it (*"Serial number: %s"* in its config/maintenance UI) | NVDA can't expose serial number |
| `PING` `0x19` | `HT_EXTPKT_PING` | keep-alive / liveness probe | NVDA has no keep-alive (relies on the reconnection logic instead) |

## Missing **receive** paths in NVDA

NVDA's receive switch handles `CONFIRMATION 0x07`, `KEY 0x04`,
`GET_PROTOCOL_PROPERTIES 0xc1`, `ATC_INFO 0x52`, `READING_POSITION 0x55`,
`GET_ATC_SENSITIVITY_2 0x54`, `GET_RTC 0x45`, `GET_FIRMNESS 0x61`. Everything else hits the
`Unhandled extended packet` warning. Packets Handy Tech's driver acts on that NVDA drops:

| Packet | HT behaviour | Should NVDA handle? |
| --- | --- | --- |
| `SCANCODE 0x09` | Translates a device scancode to a virtual key and **injects it into the OS** via `MapVirtualKeyExW` + `SendInput` (HID-keyboard passthrough mode). | No — NVDA has its own braille-input path. But it should recognise the type and not emit a warning. |
| `GET_FIRMWARE_VERSION 0xc2` | Parsed into a firmware version used for protocol gating. | Yes, if NVDA starts sending `0xc2` (see above). |
| `SERIAL_NUMBER 0x41` | Parsed into the device serial string. | Optional — useful for diagnostics/logging. |
| `PING 0x19` | Liveness echo. | Optional — only if a keep-alive is added. |
| `BLUETOOTH_PIN 0x47` | Bluetooth pairing PIN exchange. | Unlikely needed in NVDA's transport model. |

HT also emits an `onHtLayoutChangeEvent(%d,%d,%d,%d)` host callback (display layout / cell
count changed at runtime). NVDA re-reads `numCells` only from the initial handshake /
protocol-properties; it has no runtime layout-change path. Low priority, but relevant for
devices whose active cell count can change (e.g. docking/splitting).

## Handshake / firmware-gating notes

* The protocol-properties exchange is **event-driven with a timeout**: after requesting,
  HT blocks on a `WaitForMultipleObjects` of a *shutdown* event and a
  *properties-received* event, with a device-specific timeout (`fcn.1800183c0`). NVDA's
  request/response is fine as-is, but be aware the device may not answer on older firmware.
* HT explicitly downgrades behaviour by firmware: *Modular firmware 1.10* is treated as
  **non-extended protocol**. NVDA has `OldProtocolMixin` for the non-extended serial key
  path; tying that (and ATC availability) to the firmware version / protocol-properties
  response — rather than only to the model class — would match Handy Tech's logic more
  closely.

## Summary of concrete changes for `handyTech.py`

1. Extend the `0xc1` handler to parse bytes `[4..7]` (ATC capability + sensitivity ranges),
   with length guards and model-class fallback.
2. Select ATC protocol/availability and the `atcSensitivity` range from the
   protocol-properties response, not solely from the model subclass.
3. (Optional) Send `GET_FIRMWARE_VERSION 0xc2` and `SERIAL_NUMBER 0x41` during init and add
   receive handlers, to expose firmware/serial and enable firmware-conditional logic.
4. Add a no-op (non-warning) receive branch for `SCANCODE 0x09` and `PING 0x19`.
5. (Optional, low priority) Handle a runtime layout/cell-count change.
