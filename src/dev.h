#pragma once

#include "defines.h"

class dev {
    protected:
        std::vector<uint8_t> mem;
    public:
        dev() = delete;
        dev(size_t size) : mem(size) {}
        uint8_t rd(uint32_t address) { return mem[address]; }
        virtual void wr(uint32_t address, uint8_t data) { mem[address] = data; }
};
