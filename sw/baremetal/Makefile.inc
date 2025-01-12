
# set up for "gcc version 13.2.0 (gc891d8dc23e)"
RV_GNU := $(RV_GNU_LATEST)
# e.g. export RV_GNU_LATEST=riscv64-unknown-elf
SHELL  := /bin/bash

COMMON_OBJ_NAMES += common.o crt0.o
COMMON_PATH := ../common
COMMON_OBJS = $(addprefix $(COMMON_PATH)/, $(COMMON_OBJ_NAMES))

C_SRCS := $(wildcard *.c)
S_SRCS := $(wildcard *.S)
LD_SRC := $(COMMON_PATH)/link.ld
SRCS := $(C_SRCS) $(S_SRCS)
INC += $(COMMON_PATH)
LIBS += -lgcc
USER_DEFINES =

GCC_OPTS += -march=rv32i_zicsr -mabi=ilp32 -static -mcmodel=medany -fno-pic
GCC_OPTS += -fvisibility=hidden -ffreestanding -nostdlib -nostartfiles -g
GCC_OPTS += -save-temps
GCC_OPTS += -T $(LD_SRC) -Wl,--build-id=none
GCC_OPTS += -Wl,--no-warn-rwx-segments
GCC_OPTS += -Wl,-Map=$(TARGET).map

OBJDUMP_OPTS := -D -Mnumeric -t --disassembler-options=no-aliases
#OBJDUMP_OPTS := -S # inline C source code in disassembly
MEM_WIDTH := 32

# run with RTL_SIM=1 to generate hex file for RTL simulation
$(TARGET).elf: $(SRCS) $(INC)/*.h $(CRT0) $(LD_SRC) $(COMMON_OBJS)
	@$(RV_GNU)-gcc $(GCC_OPTS) $(CFLAGS) -I$(INC) $(SRCS) $(COMMON_OBJS) -o $@ $(USER_DEFINES) $(LIBS)
	@$(RV_GNU)-objdump $(OBJDUMP_OPTS) $@ > $(TARGET).dump
	@$(RV_GNU)-objcopy $@ -O binary $(TARGET).bin
	@if [ -n "$(RTL_SIM)" -a "$(RTL_SIM)" == "1" ]; then \
		$(RV_GNU)-bin2hex -w $(MEM_WIDTH) $(TARGET).bin $(TARGET).hex; \
	fi
	@echo "Generated $@"

common:
	@make -C $(COMMON_PATH) all -j

$(COMMON_OBJS):
	@make -C $(COMMON_PATH) $@

clean:
	rm -f *.elf *.dump *.hex *.bin *.o *.d *.i *.s *_symbols.json

clean_common:
	@make -C $(COMMON_PATH) clean

cleanall: clean clean_common

.PHONY: all clean
