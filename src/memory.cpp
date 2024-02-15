#include "memory.h"

memory::memory(uint32_t base_address, std::string test_bin) {
    this->base_address = base_address;
    burn(test_bin);
}

/* Read 8-bit data */
uint8_t memory::rd8(uint32_t address) {
    CHECK_ADDRESS(address, 1u)
    return mem[address];
}

/* Read 16-bit data */
uint16_t memory::rd16(uint32_t address) {
    CHECK_ADDRESS(address, 2u)
    return static_cast<uint16_t>(mem[address]) |
           (static_cast<uint16_t>(mem[address + 1]) << 8);
}

/* Read 32-bit data */
uint32_t memory::rd32(uint32_t address) {
    CHECK_ADDRESS(address, 4u)
    return static_cast<uint32_t>(mem[address]) |
           (static_cast<uint32_t>(mem[address + 1]) << 8) |
           (static_cast<uint32_t>(mem[address + 2]) << 16) |
           (static_cast<uint32_t>(mem[address + 3]) << 24);
}

/* Write 8-bit data */
void memory::wr8(uint32_t address, uint32_t data) {
    CHECK_ADDRESS(address, 1u)
    mem[address] = static_cast<uint8_t>(data);
}

/* Write 16-bit data */
void memory::wr16(uint32_t address, uint32_t data) {
    CHECK_ADDRESS(address, 2u)
    mem[address] = static_cast<uint8_t>(data & 0xFF);
    mem[address + 1] = static_cast<uint8_t>((data >> 8) & 0xFF);
}

/* Write 32-bit data */
void memory::wr32(uint32_t address, uint32_t data) {
    CHECK_ADDRESS(address, 4u)
    mem[address] = static_cast<uint8_t>(data & 0xFF);
    mem[address + 1] = static_cast<uint8_t>((data >> 8) & 0xFF);
    mem[address + 2] = static_cast<uint8_t>((data >> 16) & 0xFF);
    mem[address + 3] = static_cast<uint8_t>((data >> 24) & 0xFF);
}

/* Dump (private) */
void memory::mem_dump(uint32_t start, uint32_t end) {
    const uint32_t max_width = std::log10(MEM_SIZE) + 1;
    const uint32_t bytes_per_row = 16;
    const uint32_t word_boundary = 4;
    uint32_t aligned_start = start - (start % bytes_per_row);
    for (uint32_t i = aligned_start; i < end; i++) {
        if (i % bytes_per_row == 0) { // insert address at the start
            std::cout << std::endl << std::setw(max_width) << std::setfill('0') 
                      << std::hex << i+base_address << ": ";
        }
        std::cout << std::setw(2) << std::setfill('0')
                  << static_cast<unsigned>(mem[i]) << " "; 
        if (i % word_boundary == 3)
            std::cout << "  ";
    }
    std::cout << std::dec << std::endl;
}

/* Dump entire memory to console */
void memory::dump() { 
    mem_dump(0, MEM_SIZE);
}

/* Dump memory range to console */
void memory::dump(uint32_t start, uint32_t end) {
    mem_dump(start, end);
}

/* Load memory with app binary */
void memory::burn(std::string test_bin) {
    std::ifstream bin_file(test_bin, std::ios::binary | std::ios::ate);
    if (!bin_file.is_open()) {
        std::cerr << "BIN failed to open" << std::endl;
        return;
    }

    size_t file_size = bin_file.tellg();
    if (file_size > MEM_SIZE) {
        std::cerr << "ERROR: File size is greater than memory size."
                  << " Binary not loaded" << std::endl;
        return;
    }

    bin_file.seekg(0, std::ios::beg);
    bin_file.read(reinterpret_cast<char*>(mem.data()), file_size);
    size_t bytesRead = bin_file.gcount();
    if (bytesRead != file_size) {
        std::cerr << "Error reading the file. Expected " << file_size 
                  << " bytes, read " << bytesRead << " bytes." << std::endl;
    }
    bin_file.close();
}
