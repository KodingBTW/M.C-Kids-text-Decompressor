# M.C. Kids Text Decompressor
# Source code by Alchemic; Re-writeen by koda
# Version 1.1 - 03-04-2024
#
# This code uses python-bitstring version 4.1.4:
# http://code.google.com/p/python-bitstring/

import sys
import bitstring


def decompress(romFile, startOffset):
    # Define some useful constants.
    BIT_PASTCOPY = 0
    BIT_LITERAL = 1

    # Open the ROM.
    romStream = bitstring.ConstBitStream(filename=romFile)
    romStream.bytepos += startOffset

    # Allocate storage for the decompressed output.
    decomp = bytearray()

    # Read the first byte.
    # (It specifies the size of pastcopy's two arguments.)
    copySourceSize = romStream.read('uint:4')
    copyLengthSize = romStream.read('uint:4')

    # Main decompression loop.
    while True:
        nextCommand = romStream.read('bool')

        if nextCommand == BIT_PASTCOPY:
            # 0: Pastcopy case.
            copySource = romStream.read(copySourceSize).uint
            copyLength = romStream.read(copyLengthSize).uint
            copyLength += 3

            # A copy source of 0 indicates the end.
            if copySource == 0:
                break
           
            for i in range(copyLength):
                decomp.append(decomp[-copySource])

        elif nextCommand == BIT_LITERAL:
            # 1: Literal case.
            literalByte = romStream.read('uint:8')
            decomp.append(literalByte)

    # Calculate the end offset.
    romStream.bytealign()
    endOffset = romStream.bytepos

    # Return the decompressed data and end offset.
    return (decomp, endOffset)

if __name__ == "__main__":

    # Check for incorrect usage.
    argc = len(sys.argv)
    if argc < 3 or argc > 4:
        sys.stdout.write("Usage: ")
        sys.stdout.write("{0:s} ".format(sys.argv[0]))
        sys.stdout.write("<romFile> <startOffset> [outFile]\n")
        sys.exit(1)

    # Copy the arguments.
    romFile = sys.argv[1]
    startOffset = int(sys.argv[2], 16)
    outFile = None
    if argc == 4:
        outFile = sys.argv[3]

    # Decompress the data.
    outBytes, endOffset = decompress(romFile, startOffset)

    # Write the decompressed output, if appropriate.
    if outFile is not None:
        outStream = open(outFile, "wb")
        outStream.write(outBytes)
        outStream.close()

    # Report the size of the compressed data and last offset.
    sys.stdout.write("Original compressed size: 0x{0:X} ({0:d}) bytes\n".format(endOffset - startOffset))
    sys.stdout.write("Last offset read, inclusive: {0:X}\n".format(endOffset - 1))

    # Exit.
    sys.exit(0)
