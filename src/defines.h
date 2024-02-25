#pragma once

#include <stdio.h>
#include <stdint.h>
#include <iostream>
#include <iomanip>
#include <array>
#include <fstream>
#include <string>
#include <cmath>
#include <unordered_map>

#define MEM_SIZE 8192
const uint32_t MEM_ADDR_BITWIDTH = std::log10(MEM_SIZE) + 1;

// Decoder types
enum class opcode{ 
    al_reg = 0b011'0011, // R format
    al_imm = 0b001'0011, // I format
    load = 0b000'0011, // I format
    store = 0b010'0011, // S format
    branch = 0b110'0011, // B format
    jalr = 0b110'0111, // I format
    jal = 0b110'1111, // J format
    lui = 0b011'0111, // U format
    auipc = 0b001'0111, // U format
    system = 0b111'0011 // I format
};

enum class alu_op_t {
    op_add = (0b0000),
    op_sub = (0b1000),
    op_sll = (0b0001),
    op_srl = (0b0101),
    op_sra = (0b1101),
    op_slt = (0b0010),
    op_sltu = (0b0011),
    op_xor = (0b0100),
    op_or = (0b0110),
    op_and = (0b0111)
};

enum class load_op_t {
    op_byte = 0b000,
    op_half = 0b001,
    op_word = 0b010,
    op_byte_u = 0b100,
    op_half_u = 0b101,
};

enum class store_op_t {
    op_byte = 0b000,
    op_half = 0b001,
    op_word = 0b010
};

enum class branch_op_t {
    op_beq = 0b000,
    op_bne = 0b001,
    op_blt = 0b100,
    op_bge = 0b101,
    op_bltu = 0b110,
    op_bgeu = 0b111
};

enum class csr_op_t {
    op_csrrw = 0b001,
    op_csrrs = 0b010,
    op_csrrc = 0b011,
    op_csrrwi = 0b101,
    op_csrrsi = 0b110,
    op_csrrci = 0b111
};

// Instruction field masks
#define M_OPC7 uint32_t(0x7F)
#define M_FUNCT7 uint32_t((0x7F)<<25)
#define M_FUNCT7_B5 uint32_t((0x1)<<30)
#define M_FUNCT3 uint32_t((0x7)<<12)
#define M_RD uint32_t((0x1F)<<7)
#define M_RS1 uint32_t((0x1F)<<15)
#define M_RS2 uint32_t((0x1F)<<20)
#define M_IMM_SHAMT uint32_t(0x1F)
#define M_IMM_31 int32_t((0x1)<<31)
#define M_IMM_31_20 int32_t((0xFFF)<<20)
#define M_IMM_30_25 int32_t((0x3F)<<25)
#define M_IMM_31_25 int32_t((0x7F)<<25)
#define M_IMM_20 uint32_t((0x1)<<20)
#define M_IMM_19_12 int32_t((0xFF)<<12)
#define M_IMM_24_21 int32_t((0xF)<<21)
#define M_IMM_11_8 uint32_t((0xF)<<8)
#define M_IMM_7 uint32_t((0x1)<<7)

// Instructions
#define INST_ECALL 0x73
#define INST_EBREAK 0x100073

// CSRs
// TODO: convert to enum
#define CSR_TOHOST 0x51E
#define CSR_MSCRATCH 0x340

// Macros
#define CHECK_ADDRESS(address, align)

/* #define CHECK_ADDRESS(address, align) \
    bool address_out_of_range = (address >= MEM_SIZE); \
    bool address_unaligned = ((address % 4u) + align > 4u); \
    if (address_out_of_range || address_unaligned) { \
        if (address_out_of_range) { \
            std::cerr << "ERROR: Address out of range: 0x" \
                      << std::hex << address << std::dec << std::endl; \
        } \
        else { \
            std::cerr << "ERROR: Unaligned access at address: 0x" \
                      << std::hex << address \
                      << std::dec << "; for: " << align << " bytes" << std::endl; \
        } \
    } */

#define MEM_ADDR_FORMAT(addr) \
    std::setw(MEM_ADDR_BITWIDTH) << std::setfill('0') << std::hex << addr

#define PRINT_INST(inst) \
    std::cout << MEM_ADDR_FORMAT(pc) << " : " << std::setw(8) \
              << std::setfill('0') << std::hex << inst << std::dec

#define FRF_DEF(x,y) \
    std::left << std::setw(2) << std::setfill(' ') << x \
              << ": 0x" \
              << std::right << std::setw(8) << std::setfill('0') \
              << std::hex << y << std::dec
#define FRF(x,y) "  x" << FRF_DEF(x,y) << "  "

#define CSR_DEF(x,y) \
    std::hex << "0x" \
             << std::right << std::setw(3) << std::setfill('0') << x \
             << ": 0x" \
             << std::left << std::setw(8) << std::setfill(' ') \
             << y << std::dec
#define CSR(x,y) "  " << CSR_DEF(x,y) << "  "