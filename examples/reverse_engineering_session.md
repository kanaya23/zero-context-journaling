# Project State & Execution Journal: Native Target Reversing

## 1. Completed Task List (Micro-Steps)
- [x] **Attach Debugger & Verify PID**: Identified running target process `TargetGame.exe` (PID 14220) using `open_process`; verified 64-bit architecture and loaded module base `0x00007FF610000000`.
- [x] **Locate Player Health Offset**: Executed Cheat Engine AOB scan for signature `F3 0F 11 83 ?? ?? 00 00 48 8B 5C 24`; identified write instruction at `TargetGame.exe+0x24C1A0` (`movss [rbx+000001B4], xmm0`).
- [x] **Verify Player VTable Structure**: Read quadword at `[rbx]` (address `0x000001D4829A0000`); verified RTTI class name descriptor `.?AVPlayerController@@`.
- [x] **Confirm No-Damage Hook Safety**: Assembled non-destructive test patch injecting `nop` across 8 bytes at `TargetGame.exe+0x24C1A0`; observed player takes 0 damage from hazards without memory corruption or crash.

---

## 2. Pending (Ongoing / Unfinished)
### [Progress 50%] Dynamic Ammo Consumption Bypass
- [x] Set hardware write breakpoint on Ammo DWORD address `0x000001D4829A02F8`.
- [ ] Capture instruction pointer and register context when firing weapon in test arena.
- [ ] Identify enclosing function boundaries and calling convention.
- [ ] Author auto-assemble code cave preserving register integrity and stack alignment.

---

## 3. Milestone (User Remarks & Future Backlog)
- **Persistent DLL Plugin Packaging**: User requested compiling the verified memory patches into a native proxy DLL (`version.dll` or `dinput8.dll`) for automatic injection at startup.
- **GUI Overlay Integration**: Future integration with ImGui to render runtime entity coordinates on screen.

---

## 4. Summary (Rolling Ground Truth)
### Proven Findings & Verifications
- Player health offset is verified at `[RBX + 0x1B4]` (single-precision float, default value 100.0f).
- Base address is dynamic ASLR, base module offset `+0x24C1A0` is invariant across restarts.
- Target process is currently running and attached under Cheat Engine API handle `0x2A4`.

### Current Ground-Truth Environment State
- **Process ID**: 14220 (`TargetGame.exe`).
- **Debugger State**: Attached via Cheat Engine API, hardware breakpoints cleared.
- **Modified Memory**: Health write patch reverted to original opcodes (`F3 0F 11 83 B4 01 00 00`).
- **Local Files**: `scripts/health_hook.lua` authored and tested.

### Immediate Next Action Upon Resuming
- Trigger weapon fire in game client while monitoring hardware write breakpoint on address `0x000001D4829A02F8` to log the calling opcode into `scripts/ammo_hook.lua`.
