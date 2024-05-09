import os
import sys
import glob
import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Any, Tuple, List
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MultipleLocator, FuncFormatter, LogFormatter, LogFormatterSciNotation, MaxNLocator

#SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
PROFILER_ENDS = "_profiler.json"
ARITH = "ARITH"
MEM = "MEM"
BRANCH = "BRANCH"
JUMP = "JUMP"
CSR = "CSR"
ENV = "ENV"
NOP = "NOP"
FENCE = "FENCE"
MEM_S = "MEM_S"
MEM_L = "MEM_L"

INST_BYTES = 4
CACHE_LINE_INSTS = 64//INST_BYTES
BASE_ADDR = 0x80000000

inst_t_mem = {
    MEM_S: ["sb", "sh", "sw"],
    MEM_L: ["lb", "lh", "lw", "lbu", "lhu"],
}

inst_t = {
    ARITH: [
        "add", "sub", "sll", "srl", "sra", "slt", "sltu", "xor", "or", "and", 
        "addi", "slli", "srli", "srai", "slti", "sltiu", "xori", "ori", "andi",
        "lui", "auipc"
    ],
    MEM: inst_t_mem[MEM_S] + inst_t_mem[MEM_L],
    BRANCH: ["beq", "bne", "blt", "bge", "bltu", "bgeu"],
    JUMP: ["jalr", "jal"],
    CSR: ["csrrw", "csrrs", "csrrc", "csrrwi", "csrrsi", "csrrci"],
    ENV: ["ecall", "ebreak"],
    NOP: ["nop"],
    FENCE: ["fence.i"],
}

all_inst = []
for k, v in inst_t.items():
    all_inst.extend(v)

all_inst_types = list(inst_t.keys()) + list(inst_t_mem.keys())

# create a reverse map for instruction types
inst_t_map = {}
for k, v in inst_t.items():
    for inst in v:
        inst_t_map[inst] = k

inst_t_mem_map = {}
for k, v in inst_t_mem.items():
    for inst in v:
        inst_t_mem_map[inst] = k

# TODO: add function calls/graphs highlight when supported by the profiler
colors = {
    "blue_base": "#0077b6",
    "blue_light1": "#00b4d8",
    "blue_light2": "#90e0ef",
}

highlight_colors = [
    #"#2a9d8f", # teal
    #"#33C1B1", # keppel
    "#3ECCBB", # turquoise
    #"#e9c46a", # yellow
    #"#ECCE83", # jasmine
    "#EED595", # peach yellow
    "#f4a261", # orange
    "#e76f51", # red
]

# memory instructions breakdown store vs load
inst_mem_bd = {
    MEM_L : ["Load", colors["blue_light1"]],
    MEM_S : ["Store", colors["blue_light2"]],
}

def find_gs(x) -> Dict[str, Any]:
    prec = 4
    m1 = -0.0058
    b1 = 0.3986
    m2 = 0.0024
    b2 = 0.8092
    return {
        'hspace': round(m1 * x + b1, prec),
        'top': round(m2 * x + b2, prec)
    }

def get_base_int_pc(pc) -> int:
    return int(pc,16) - int(BASE_ADDR)

def get_count(parts, df) -> Tuple[int, int]:
    pc = get_base_int_pc(parts[0].strip())
    count_series  = df.loc[df["pc_real"] == pc, "count"]
    count = count_series.squeeze() if not count_series.empty else 0
    return count, pc

def num_to_hex(val, pos) -> str:
    return f"0x{int(val*INST_BYTES):04X}"

def inst_exists(inst) -> str:
    if inst not in all_inst:
        raise ValueError(f"Invalid instruction '{inst}'. " + \
                         f"Available instructions are: {', '.join(all_inst)}")
    return inst

def inst_type_exists(inst_type) -> str:
    if inst_type not in all_inst_types:
        raise ValueError(f"Invalid instruction type '{inst_type}'. " + \
                         f"Available types are: {', '.join(all_inst_types)}")
    return inst_type

def add_legend_for_hl_groups(ax, chart_type:str) -> None:
    title = "Highlighted\nInstructions"
    if chart_type == "log":
        ax.legend(loc='lower right', title=title, framealpha=0.5)
    elif chart_type == "trace":
        # put legend in the top right corner, outside the plot
        ax.legend(loc='upper left', title=title, framealpha=0.5,
                  bbox_to_anchor=(1.01, 1.03), borderaxespad=0.)
    else:
        raise ValueError(f"Invalid chart type '{chart_type}'")

def parse_args() -> argparse.Namespace:
    TIME_SERIES_LIMIT = 50000
    parser = argparse.ArgumentParser(description="Analyze instruction count and PC trace log")
    # either
    parser.add_argument('-i', '--inst_log', type=str, nargs='+', help="JSON instruction count log with profiling data. Multiple logs can be provided at once without repeating the option. Can be combined with --inst_dir")
    parser.add_argument('--inst_dir', type=str, help="Directory with JSON instruction logs with profiling data")
    # or
    parser.add_argument('-p', '--pc_trace', type=str, nargs='+', help="Binary PC trace of the execution. Multiple traces can be provided at once without repeating the option. Can be combined with --pc_dir")
    parser.add_argument('--pc_dir', type=str, help="Directory with Binary PC traces of the execution")
    
    # instruction count log only options
    parser.add_argument('--exclude', type=inst_exists, nargs='+', help="Exclude specific instructions. Instruction count log only option")
    parser.add_argument('--exclude_type', type=inst_type_exists, nargs='+', help=f"Exclude specific instruction types. Available types are: {', '.join(inst_t.keys())}. Instruction count log only option")
    parser.add_argument('--top', type=int, help="Number of N most common instructions to display. Default is all. Instruction count log only option")
    parser.add_argument('--allow_zero', action='store_true', default=False, help="Allow instructions with zero count to be displayed. Instruction count log only option")
    parser.add_argument('--combined_only', action='store_true', help="Only save combined charts/data. Ignored if single JSON log is provided. Instruction count log only option")
    
    # pc trace only options
    parser.add_argument('--dasm', type=str, help="Path to disassembly 'dasm' file to backannotate the PC trace. New file is generated at the same path with *.prof.<original ext> suffix. PC trace only option")
    parser.add_argument('--symbols_only', action='store_true', help="Only backannotate and display the symbols found in the 'dasm' file. Requires --dasm. Doesn't display figures and ignores all save options except --save_csv. PC trace only option")
    parser.add_argument('--pc_time_series_limit', type=int, default=TIME_SERIES_LIMIT, help=F"Limit the number of PC entries to display in the time series chart. Default is {TIME_SERIES_LIMIT}. PC trace only option")
    #parser.add_argument('--pc_begin', type=str, help="Start PC address to filter the PC trace. PC trace only option")
    #parser.add_argument('--pc_end', type=str, help="End PC address to filter the PC trace. PC trace only option")

    # common options
    parser.add_argument('--highlight', '--hl', type=str, nargs='+', help="Highlight specific instructions. Multiple instructions can be provided as a single string separated by whitespace (multiple groups) or separated by commas (multiple instructions in a group). E.g.: 'add,addi sub' colors 'add' and 'addi' the same and 'sub' a different color.")
    # TODO: add highlighting for function calls/PC ?
    parser.add_argument('-s', '--silent', action='store_true', help="Don't display chart(s) in pop-up window")
    parser.add_argument('--save_png', action='store_true', help="Save charts as PNG")
    parser.add_argument('--save_svg', action='store_true', help="Save charts as SVG")
    parser.add_argument('--save_pdf', type=str, nargs='?', const=os.getcwd(), default=None, help="Save charts as PDF. Saved as a single PDF file if multiple charts are generated. Requires path to save the PDF file. Default is current directory.")
    parser.add_argument('--save_csv', action='store_true', help="Save source data as CSV")
    parser.add_argument('-o', '--output', type=str, default=os.getcwd(), help="Output directory for the combined PNG and CSV. Ignored if single json file is provided. Default is current directory. Standalone PNGs and CSVs will be saved in the same directory as the source json file irrespective of this option.")
    
    return parser.parse_args()

def draw_inst_log(df, hl_groups, title, args) -> plt.Figure:
    inst_profiled = df['count'].sum()
    df['i_type'] = df['name'].map(inst_t_map)
    df['i_mem_type'] = df['name'].map(inst_t_mem_map)

    # filter out instructions if needed
    if args.exclude:
        df = df[~df['name'].isin(args.exclude)]
    
    if args.exclude_type:
        df = df[~df['i_type'].isin(args.exclude_type)]
    
    if args.top:
        df = df.tail(args.top)
    if not args.allow_zero:
        df = df[df['count'] != 0]

    # separate the instructions by type
    df_g = df[['i_type', 'count']].groupby('i_type').sum()
    df_g = df_g.sort_values(by='count', ascending=True)

    # separate the memory instructions by type
    df_mem_g = df[['i_mem_type', 'count']].groupby('i_mem_type').sum()
    df_mem_g = df_mem_g.sort_values(by='count', ascending=False)
    
    # add a bar chart
    ROWS = 2
    COLS = 1
    box = []
    fig, ax = plt.subplots(ROWS, COLS,
                           figsize=(COLS*10, ROWS*(len(df)+len(df_g))/6),
                           height_ratios=(len(df)*.95, len(df_g)),
                           gridspec_kw=find_gs(len(df)+len(df_g)))
    suptitle_str = f"Execution profile for {title}"
    suptitle_str += f"\nInstructions profiled: {inst_profiled}"
    if args.exclude or args.exclude_type:
        suptitle_str += f" ({df['count'].sum()} shown, "
        suptitle_str += f"{inst_profiled - df['count'].sum()} excluded)"
    
    fig.suptitle(suptitle_str, size=12)
    box.append(ax[0].barh(df['name'], df['count'], color=colors["blue_base"]))
    box.append(ax[1].barh(df_g.index, df_g['count'], color=colors["blue_base"]))
    y_ax0_offset = min(0.025, len(df)/2_000)
    ax[0].margins(y=0.03-y_ax0_offset)
    ax[1].margins(y=0.03)

    for i in range(ROWS):
        ax[i].bar_label(box[i], padding=3)
        ax[i].set_xlabel('Count')
        ax[i].grid(axis='x')
        ax[i].margins(x=0.06)

    # highlight specific instructions, if any
    hc = 0
    for hl_g in hl_groups:
        for i, r in enumerate(box[0]):
            if df.iloc[i]['name'] in hl_g:
                r.set_color(highlight_colors[hc])
        ax[0].barh(0, 0, color=highlight_colors[hc], label=', '.join(hl_g))
        hc += 1
    
    if len(hl_groups) > 0:
        add_legend_for_hl_groups(ax[0], "log")
    
    # add memory instructions breakdown, if any
    df_mem_g = df_mem_g[df_mem_g['count'] != 0] # never label if count is zero
    if len(df_mem_g) > 0:
        mem_type_index = df_g.index.get_loc("MEM")
        left_start = 0
        for i, row in df_mem_g.iterrows():
            rect_m = ax[1].barh(mem_type_index, row['count'], left=left_start, 
                                label=inst_mem_bd[row.name][0], 
                                color=inst_mem_bd[row.name][1])
            ax[1].bar_label(rect_m, padding=0, label_type='center', size=7)
            left_start += row['count']

        ax[1].legend(loc='lower right')

    # handle display
    if not args.silent:
        plt.show()
    
    plt.close()
    return fig

def json_prof_to_df(log) -> pd.DataFrame:
    ar = []
    with open(log, 'r') as file:
        data = json.load(file)
        for key in data:
            if key.startswith('_'): # skip internal keys
                continue
            ar.append([key, data[key]['count']])
    
    df = pd.DataFrame(ar, columns=['name', 'count'])
    df['count'] = df['count'].astype(int)
    df = df.sort_values(by='count', ascending=True)
    return df

def run_inst_log(log, hl_groups, title, args) -> \
Tuple[pd.DataFrame, plt.Figure]:
    
    df = json_prof_to_df(log)
    fig = None
    if not args.combined_only:
        fig = draw_inst_log(df, hl_groups, title, args)
    
    return df, fig

def backannotate_dasm(log, df) -> \
Tuple[Dict[str, Dict[str, int]], pd.DataFrame]:
    
    symbols = {}
    pc_inst_map_arr = []
    dasm_ext = os.path.splitext(log)[1]
    with open(log, 'r') as infile, \
    open(log.replace(dasm_ext, '.prof' + dasm_ext), 'w') as outfile:
        current_sym = None
        append = False
        NUM_DIGITS = len(str(df['count'].max())) + 1
        
        for line in infile:
            if line.startswith('Disassembly of section .text'):
                append = True
                outfile.write(line)
                continue
            elif line.startswith('Disassembly of section .'):
                append = False
            
            if append and line.strip():
                parts = line.split(':')
                
                if len(parts) == 2 and parts[1].startswith('\n'):
                    # detected symbol
                    parts = parts[0].split(" ")
                    pc_start = get_base_int_pc(parts[0].strip())
                    symbol_name = parts[1][1:-1] # remove <> from symbol name
                    if current_sym:
                        symbols[current_sym]['pc_end_real'] = prev_pc
                    current_sym = symbol_name
                    symbols[current_sym] = {
                        'pc_start_real': pc_start,
                        "acc_count": 0
                    }
                    prev_pc = pc_start
                
                if len(parts) == 2 and parts[1].startswith('\t'):
                    # detected instruction
                    count, prev_pc = get_count(parts, df)
                    outfile.write("{:{}} {}".format(count, NUM_DIGITS, line))
                    symbols[current_sym]['acc_count'] += count

                    im = line.split('\t')
                    im = [x.strip() for x in im]
                    pc_inst_map_arr.append(
                        [get_base_int_pc(im[0].replace(':', ''))//4, # pc
                         im[2], # instruction mnemonic
                         ' '.join(im[2:]) # full instruction
                         ])
                
                else: # not an instruction
                    outfile.write(line)
                
            else: # not .text section
                outfile.write(line)
        
        # write the last symbol
        symbols[current_sym]['pc_end_real'] = prev_pc
    
    sym_log = []
    for k,v in symbols.items():
        v['func_text'] = f"{k} ({v['acc_count']})"
        sym_log.append(f"{num_to_hex(v['pc_start_real']//4, None)} - " + \
                       f"{num_to_hex(v['pc_end_real']//4, None)}: " + \
                       f"{v['func_text']}")
    
    print(f"Symbols found in {log}:")
    for sym in sym_log[::-1]:
        print(sym)
    
    df_out = pd.DataFrame(pc_inst_map_arr, columns=['pc', 'inst_mnm', 'inst'])
    return symbols, df_out

def annotate_pc_chart(df, symbols, ax, symbol_pos=None) -> plt.Axes:
    if symbol_pos is None:
        symbol_pos = ax.get_xlim()[1]
    
    # add cache line coloring
    # FIXME when filtering is implemented, assumes exec starts from 0 for now
    for i in range(df.pc.min(), df.pc.max(), CACHE_LINE_INSTS):
        color = 'k' if (i//CACHE_LINE_INSTS) % 2 == 0 else 'w'
        ax.axhspan(i, i+CACHE_LINE_INSTS, color=color, alpha=0.08)

    # add lines for symbols, if any
    for k,v in symbols.items():
        pc_start = v['pc_start_real']//INST_BYTES
        pc_end = v['pc_end_real']//INST_BYTES
        ax.axhline(y=pc_start-.5, color='k', linestyle='-', alpha=0.5)
        ax.text(symbol_pos, pc_start,
                f" ^ {v['func_text']}", color='k',
                fontsize=9, ha='left', va='center',
                bbox=dict(facecolor='w', alpha=0.6, linewidth=0, pad=1)
                )

    # add line for the last symbol, if any
    if symbols:
        ax.axhline(y=pc_end+.5, color='k', linestyle='-', alpha=0.5)
    
    return ax

def draw_pc_freq(df, hl_groups, title, symbols, args) -> plt.Figure:
    # TODO: should probably limit the number of PC entries to display or 
    # auto enlarge the figure size (but up to a point, then limit anyways)
    gs = {'top': 0.93, 'bottom': 0.07, 'left': 0.1, 'right': 0.95}
    fig, ax = plt.subplots(figsize=(12,15), gridspec_kw=gs)
    box = ax.barh(df['pc'], df['count'], height=1, alpha=0.8)
    #       , edgecolor=(0, 0, 0, 0.1))
    ax.set_xscale('log')

    # highlight specific instructions, if any
    hc = 0
    for hl_g in hl_groups:
        for i, r in enumerate(box):
            if df.iloc[i]['inst_mnm'] in hl_g:
                r.set_color(highlight_colors[hc])
        # add a dummy bar for the legend
        ax.barh(0, 0, color=highlight_colors[hc], label=', '.join(hl_g))
        hc += 1

    if len(hl_groups) > 0:
        add_legend_for_hl_groups(ax, "trace")
    
    # update axis
    #formatter = LogFormatter(base=10, labelOnlyBase=True)
    formatter = LogFormatterSciNotation(base=10)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_locator(MultipleLocator(CACHE_LINE_INSTS))
    ax.yaxis.set_major_formatter(FuncFormatter(num_to_hex))
    ax.set_xlim(left=0.5)
    ax.margins(y=0.01, x=0.1)

    # add a second x-axis
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim())
    ax_top.set_xscale('log')
    ax_top.xaxis.set_ticks_position('top')
    ax_top.xaxis.set_major_formatter(formatter)

    # label
    ax.set_xlabel("Count (log scale)")
    ax.set_ylabel("Program Counter")
    ax.set_title(f"PC frequency profile for {title}")

    ax.grid(axis='x', linestyle='-', alpha=1, which='major')
    ax.grid(axis='x', linestyle='--', alpha=0.6, which='minor')

    # annotate the chart
    ax = annotate_pc_chart(df, symbols, ax)

    # handle display
    if not args.silent:
        plt.show()
    
    plt.close()
    return fig

def draw_pc_exec(df, hl_groups, title, symbols, args) -> plt.Figure:
    gs = {'top': 0.93, 'bottom': 0.07, 'left': 0.05, 'right': 0.92}
    fig, ax = plt.subplots(figsize=(24,12), gridspec_kw=gs)
    
    # plot the PC trace and don't interpolate linearly between points
    # but step from one to the next
    ax.step(df.index, df['pc'], where='post', linewidth=2, color=(0,.3,.6,0.2),
            marker='.', markersize=5, markerfacecolor='b', markeredgecolor='b')
    
    # scatter plot points from df where inst matches inst_mnm
    hc = 0
    for hl_g in hl_groups:
        for inst in hl_g:
            df_hl = df[df['inst_mnm'] == inst]
            ax.scatter(df_hl.index, df_hl['pc'], color=highlight_colors[hc], 
                       s=10, zorder=10)
        # add a dummy scatter plot for the legend
        ax.scatter([], [], color=highlight_colors[hc], label=', '.join(hl_g))
        hc += 1
    
    if len(hl_groups) > 0:
        add_legend_for_hl_groups(ax, "trace")
    
    # update axis
    current_nbins = len(ax.get_xticks())
    locator = MaxNLocator(nbins=current_nbins*2, integer=True)
    ax.xaxis.set_major_locator(locator)
    ax.set_yticks(range(0, df['pc'].max(), CACHE_LINE_INSTS))
    ax.yaxis.set_major_formatter(FuncFormatter(num_to_hex))
    ax.margins(y=0.03, x=0.01)

    # add a second x-axis
    ax_top = ax.twiny()
    ax_top.set_xlim(ax.get_xlim())
    ax_top.xaxis.set_major_locator(locator)
    ax_top.xaxis.set_ticks_position('top')

    # label
    ax.set_xlabel('Instruction Count')
    ax.set_ylabel('Program Counter')
    ax.set_title(f"PC execution profile for {title}")

    ax = annotate_pc_chart(df, symbols, ax)

    # handle display
    if not args.silent:
        plt.show()

    plt.close()
    return fig

def run_pc_log(bin_log, hl_groups, title, args) -> \
Tuple[pd.DataFrame, plt.Figure, plt.Figure]:
    
    data = np.fromfile(bin_log, dtype=np.uint32)
    df_og = pd.DataFrame(data, columns=['pc'])
    df = df_og.groupby('pc').size().reset_index(name='count')
    df = df.sort_values(by='pc', ascending=True)
    df['pc'] = df['pc'].astype(int)
    df['pc_hex'] = df['pc'].apply(lambda x: f'{x:08x}')
    df['pc_real'] = df['pc'] * INST_BYTES
    df['pc_real_hex'] = df['pc_real'].apply(lambda x: f'{x:08x}')

    # TODO: consider option to reverse the PC log so it grows down from the top
    # like .dump does

    # slice df based on the input
    # TODO filtering as a feature, has to be taken into account when 
    # labeling the chart and when backannotating the .dasm file
    #df = df.loc[
    #    (df.pc >= (int("0x220", 16)//4)) & 
    #    (df.pc < (int("0x300", 16)//4))
    #]

    symbols = {}
    m_hl_groups = []
    if args.dasm:
        m_hl_groups = hl_groups
        symbols, df_map = backannotate_dasm(args.dasm, df)
        # merge df_map into df by keeping only records in the df
        df = pd.merge(df, df_map, how='left', left_on='pc', right_on='pc')
        df_og = pd.merge(df_og, df_map, how='left', left_on='pc', right_on='pc')
    
    if args.symbols_only:
        return df, None, None

    fig = draw_pc_freq(df, m_hl_groups, title, symbols, args)
    
    if len(df_og) > args.pc_time_series_limit:
        print(f"Warning: too many PC entries to display in the time series " + \
              f"chart ({len(df_og)}). Limit is {args.pc_time_series_limit} " + \
              f"entries. Either increase the limit or filter the data.")
        fig2 = None
    else:
        fig2 = draw_pc_exec(df_og, m_hl_groups, title, symbols, args)
    
    return df, fig, fig2

def run_main(args) -> None:
    inst_args = [args.inst_log, args.inst_dir]
    pc_args = [args.pc_trace, args.pc_dir]
    run_inst = any(inst_args)
    run_pc = any(pc_args)

    if run_inst and run_pc:
        raise ValueError("Inst and pc options cannot be mixed")

    if not run_inst and not run_pc:
        raise ValueError("No JSON instruction count log or PC trace provided")

    if not os.path.exists(args.output):
        raise FileNotFoundError(f"Output directory {args.output} not found")

    if args.symbols_only and run_inst:
        raise ValueError("--symbols_only cannot be used with instruction logs")
    
    if args.symbols_only and not args.dasm:
        raise ValueError("--symbols_only requires --dasm")
    
    if run_pc:
        args_log = args.pc_trace
        args_dir = args.pc_dir
        profiler_str = "_pc_trace.bin"
    else:
        args_log = args.inst_log
        args_dir = args.inst_dir
        profiler_str = "_inst_profiler.json"
    
    all_logs = []
    if args_log:
        for l in args_log:
            if not os.path.exists(l):
                raise FileNotFoundError(f"File {l} not found")
            all_logs.append(l)
    
    if args_dir:
        if not os.path.isdir(args_dir):
            raise FileNotFoundError(f"Directory {args_dir} not found")
        all_in_dir = glob.glob(os.path.join(args_dir, "*" + profiler_str))
        if not all_in_dir:
            raise FileNotFoundError(f"No JSON files found in directory " + \
                                    f"{args_dir}")
        all_logs.extend(all_in_dir)

    if len(all_logs) > 1 and args.dasm:
        raise ValueError("Cannot backannotate multiple PC logs at once. " + \
                         "Provide a single PC trace file to backannotate " + \
                         "or remove the --dasm option")
    
    hl_groups = []
    if not (args.highlight == None):
        if len(args.highlight) > len(highlight_colors):
            raise ValueError(f"Too many instructions to highlight " + \
                            f"max is {len(highlight_colors)}, " + \
                            f"got {len(args.highlight)}")
        else:
            if len(args.highlight) == 1: # multiple arguments but 1 element
                hl_groups = args.highlight[0].split()
            else: # already split on whitespace (somehow?)
                hl_groups = args.highlight
            hl_groups = [ah.split(",") for ah in hl_groups]


    df_arr = []
    fig_arr = []
    fig_arr2 = []
    ext = os.path.splitext(all_logs[0])[1]
    for log in all_logs:
        title = os.path.basename(log.replace(profiler_str, ""))
        if run_pc:
            df, fig, fig2 = run_pc_log(log, hl_groups, title, args)
        else:
            df, fig = run_inst_log(log, hl_groups, title, args)
        
        df_arr.append(df)
        if not args.combined_only:
            log_path = os.path.realpath(log)
            fig_arr.append([log_path, fig])
            if run_pc:
                fig_arr2.append([log_path.replace(ext, f"_exec{ext}"), fig2])

    # combine all the data
    combined_fig = None
    if len(all_logs) > 1 and run_inst:
        title_combined = "all_workloads"
        df_combined = pd.concat(df_arr)
        if 'i_type' in df_combined.columns:
            df_combined = df_combined.drop(columns=['i_type'])
        if 'i_mem_type' in df_combined.columns:
            df_combined = df_combined.drop(columns=['i_mem_type'])
        df_combined = df_combined.groupby('name', as_index=False).sum()
        df_combined = df_combined.sort_values(by='count', ascending=True)
        combined_fig = [
            f"{title_combined}{profiler_str}",
            draw_inst_log(df_combined, hl_groups, title_combined, args)
        ]

    if args.save_csv: # each log is saved as a separate CSV file
        for log, df in zip(all_logs, df_arr):
            df.to_csv(log.replace(ext, "_df.csv"), index=False)
        
        if len(all_logs) > 1 and run_inst: # and also saved as a combined CSV
            df_combined.to_csv(combined_out_path.replace(".json", ".csv"),
                               index=False)
    
    if args.symbols_only and run_pc:
        return
    
    if combined_fig:
        combined_out_path = os.path.join(
            args.output, f"{title_combined}{profiler_str}".replace(" ", "_")
        )
    
    if args.save_png: # each chart is saved as a separate PNG file
        for name, fig in (fig_arr + fig_arr2):
            fig.savefig(name.replace(" ", "_").replace(ext, ".png"))
            if combined_fig:
                combined_fig[1].savefig(combined_out_path.replace(ext, ".png"))
    
    if args.save_svg: # each chart is saved as a separate SVG file
        for name, fig in (fig_arr + fig_arr2):
            fig.savefig(name.replace(" ", "_").replace(ext, ".svg"))
            if combined_fig:
                combined_fig[1].savefig(combined_out_path.replace(ext, ".svg"))
    
    if combined_fig: # add combined chart as the first one in the list (ie pdf)
        fig_arr.insert(0, combined_fig)
    
    if args.save_pdf: # all charts are saved in a single PDF file
        pdf_name = f"{profiler_str[1:].split('.')[0]}.pdf"
        pdf_path =  os.path.join(args.save_pdf, pdf_name)
        
        with PdfPages(pdf_path) as pdf:
            save_pdf(fig_arr, pdf)
        
        if run_pc: # also save the second set of charts, if any
            pdf_path2 = pdf_path.replace(".pdf", "_exec.pdf")
            with PdfPages(pdf_path2) as pdf:
                save_pdf(fig_arr2, pdf)
    
def save_pdf(fig_arr, pdf) -> None:
    total_pages = len(fig_arr)
    page = 1
    for name, fig in fig_arr:
        fig.supxlabel(f"Page {page} of {total_pages}", x=0.93, fontsize=10)
        page += 1
        pdf.savefig(fig)

if __name__ == "__main__":
    args = parse_args()
    run_main(args)
