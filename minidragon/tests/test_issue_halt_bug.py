import unittest
from minidragon.core import CPUCore, MemoryFilter

class MockMemoryFilter(MemoryFilter):
    def __init__(self, mappings):
        self.mappings = mappings

    def read(self, address):
        return self.mappings.get(address)

    def write(self, address, data):
        pass

class TestHaltBug(unittest.TestCase):
    def test_mnemonic_uses_memory_filter(self):
        # The bug was that mnemonic property read directly from ram instead of using memory filter.
        # This meant that instructions in cartridge space (0x8000+) were not correctly identified
        # by the emulator loop which checks cpu.mnemonic == "HALT".

        ram = [0] * 65536
        # Put something in RAM at 0x8000
        ram[0x8000] = 0x41  # ADDI 1
        
        # Create a memory filter that returns something else at 0x8000
        # 0x3F is JRI -1 which is disassembled as HALT
        filter = MockMemoryFilter({0x8000: 0x3F})
        
        cpu = CPUCore(ram, filter)
        cpu.ip = 0x8000
        
        # After the fix, it should return "HALT" (from filter)
        self.assertEqual(cpu.mnemonic, "HALT")

    def test_read_memory_handles_zero(self):
        # The bug was that __read_memory would fall back to RAM if the filter returned 0.
        
        ram = [0] * 65536
        ram[0x8000] = 0x41  # ADDI 1
        
        # Filter returns 0 at 0x8000. 0 is also an instruction (NOP).
        filter = MockMemoryFilter({0x8000: 0})
        
        cpu = CPUCore(ram, filter)
        
        # We need to access __read_memory. It's private but we can access it for testing.
        # Or just use mnemonic if it uses __read_memory.
        cpu.ip = 0x8000
        
        # After the fix, it should return "NOP" (disassembly of 0)
        self.assertEqual(cpu.mnemonic, "NOP")

if __name__ == "__main__":
    unittest.main()
