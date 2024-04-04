# M.C.-Kids-NES-text-Decompressor

Use same patch nes rom then use:

decompressor.py [romFile] [startOffset] [outFile]

Otherwise there are three block of text. Located in:

- 0x4010 to 0x4608
- 0x4609 to 0x4AAB
- 0x4AAC to 0x5082

The gamr text compression It's a kind of Lempel-Ziv:

- 4 bits: size of the "source" argument for pastcopies, in bits
- 4 bits: size of the "length" argument for pastcopies, in bits
- Stream of compressed bits; read each byte most significant bit to least

The stream of compressed bits consists of a sequence of these two commands:

Pastcopy

- 0 (source) (length)
- Copies previously-decompressed data.
- The number of bits used by "source" and "length" is specified in the first byte of compressed data.
- The "source" is how many bytes ago to copy from, and a source of 0 indicates the end.
- The "length" is the number of bytes to copy, less three (so a length of 0 copies 3 bytes, 1 copies 4, etc).

Literal

- 1 nnnnnnnn
- Outputs one literal byte.
