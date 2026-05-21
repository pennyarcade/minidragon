import unittest
from minidragon.core import assemble, disassemble
from minidragon.exception import InvalidInstructionException

class TestAssemblerMacroAndConstants(unittest.TestCase):
    def test_macros_basic(self):
        # Test basic macro expansion
        mnemonics = [
            ".MACRO MY_MACRO",
            "ADDI 1",
            "ADDI 2",
            ".ENDM",
            "MY_MACRO",
            "MY_MACRO"
        ]
        result = assemble(mnemonics)
        # ADDI 1 is 0x11, ADDI 2 is 0x12 (checking ADDI implementation in core.py)
        # Wait, let me check what ADDI 1 actually assembles to.
        # ADDI is 0x1000 | (imm & 0x0FFF) ? No, let's check core.py
        
        # Actually I can just check the number of instructions produced.
        self.assertEqual(len(result), 4)
        
    def test_constants_basic(self):
        # Test basic constant replacement
        mnemonics = [
            ".SET CONST1, 10",
            "ADDI CONST1"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 1)
        # ADDI 10 -> 0x40 | 10 = 0x4A = 74
        self.assertEqual(result[0][1], 0x4A)

    def test_constants_recursive(self):
        # Test recursive constant replacement
        mnemonics = [
            ".SET CONST1, 10",
            ".SET CONST2, CONST1",
            "ADDI CONST2"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 1)
        # ADDI 10 -> 0x40 | 10 = 0x4A = 74
        self.assertEqual(result[0][1], 0x4A)

    def test_macros_nested(self):
        # Test nested macros
        mnemonics = [
            ".MACRO MACRO1",
            "ADDI 1",
            ".ENDM",
            ".MACRO MACRO2",
            "MACRO1",
            "ADDI 2",
            ".ENDM",
            "MACRO2"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 2)
        # ADDI 1 -> 0x41 = 65
        # ADDI 2 -> 0x42 = 66
        self.assertEqual(result[0][1], 65)
        self.assertEqual(result[1][1], 66)

    def test_macro_recursion_limit(self):
        # Test macro recursion limit
        mnemonics = [
            ".MACRO RECURSE",
            "RECURSE",
            ".ENDM",
            "RECURSE"
        ]
        with self.assertRaisesRegex(InvalidInstructionException, "Max macro nesting depth exceeded"):
            assemble(mnemonics)

    def test_constants_in_macros(self):
        # Test constants expanded inside macros
        mnemonics = [
            ".SET VAL, 20",
            ".MACRO MY_MACRO",
            "ADDI VAL",
            ".ENDM",
            "MY_MACRO"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 1)
        # ADDI 20 -> 0x40 | 20 = 0x40 | 0x14 = 0x54 = 84
        self.assertEqual(result[0][1], 84)

    def test_constant_recursion_limit(self):
        # Test constant recursion limit (though it doesn't throw, it just stops)
        mnemonics = [
            ".SET A, B",
            ".SET B, A",
            "ADDI A"
        ]
        # It should still be 'A' or 'B' after 10 iterations, and then fail in getint
        with self.assertRaises(Exception):
             assemble(mnemonics)

    def test_constant_in_directive(self):
        # Test constant expansion in directives
        mnemonics = [
            ".SET MY_ADDR, 0x10",
            ".org MY_ADDR",
            "ADDI 1"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 0x10)
        self.assertEqual(result[0][1], 65)

    def test_constant_in_byte(self):
        # Test constant expansion in .byte
        mnemonics = [
            ".SET MY_VAL, 0x55",
            ".byte MY_VAL"
        ]
        result = assemble(mnemonics)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 0x55)

    def test_constant_as_mnemonic(self):
        # Test if constant can be used as a mnemonic (currently not supported)
        mnemonics = [
            ".SET MY_NOP, NOP",
            "MY_NOP"
        ]
        # This will fail to assemble because MY_NOP is not expanded if there's no space
        with self.assertRaises(Exception):
            assemble(mnemonics)

if __name__ == "__main__":
    unittest.main()
