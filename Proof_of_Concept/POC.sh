#!/bin/bash

# Configuration
EXEC_NAME="jetson_32bit_cpa"       # Generated executable filename
SOURCE_FILE="jetson_32bit_cpa.cu"  # CUDA source file (supports .cu or .c)
TRACEFILE=("SBK_FILE")       # Execution modes (run in sequential order)
LOG_FILE="Result.txt"

NVCC_COMPILE_FLAGS=(
  -arch=sm_89     # GPU ARCH
  -O3             # LvL 3
)

# Function to check command existence
check_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: Required command '$1' not found"
        return 1
    fi
}

# Recompile CUDA program unconditionally
function compile_program() {
    echo "Compiling POC program with nvcc..."
    nvcc "${NVCC_COMPILE_FLAGS[@]}" -o "$EXEC_NAME" "$SOURCE_FILE"
    if [ $? -ne 0 ]; then
        echo "Compilation failed! Check CUDA code/environment."
        exit 1
    fi
    echo "POC executable created: $EXEC_NAME"
}

# Validate tracefile strings ("SBK_FILE" allowed)
function validate_tracefile() {
    local tracefile="$1"
    case "$tracefile" in
        SBK_FILE)
            return 0 ;;  # Valid tracefile
        *)
            return 1 ;;  # Invalid tracefile
    esac
}

# Main execution flow
function main() {
    # Verify Python installation
    if ! check_cmd python3 && ! check_cmd python; then
        echo "Python is not installed. Please install Python 3 first."
        exit 1
    fi

    # Get proper Python command
    local PYTHON_CMD
    PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
    # Verify pycryptodome installation
    if ! "$PYTHON_CMD" -c 'from Crypto.Cipher import AES' 2>/dev/null; then
        echo "Installing pycryptodome library..."
        if ! "$PYTHON_CMD" -m pip install --user pycryptodome; then
            echo "Failed to install pycryptodome. Try one of these solutions:"
            echo "1. Run with sudo"
            echo "2. Use virtual environment"
            echo "3. Install manually: python -m pip install pycryptodome" 
            exit 1
        fi
    fi

    # Redirect stdout and stderr to tee, appending to log file
    exec > >(tee "$LOG_FILE") 2>&1
    echo "......................................................"
    # Check nvcc availability
    if ! command -v nvcc >/dev/null 2>&1; then
        echo "Error: nvcc compiler not found. Install CUDA Toolkit!"
        exit 1
    fi

    # Enforce recompilation
    compile_program

    # Iterate through tracefile sequentially
    for tracefile in "${TRACEFILE[@]}"; do
        # Validate tracefile integrity (defensive check)
        if ! validate_tracefile "$tracefile"; then
            echo "Critical Error: Unknown Trace File '$tracefile' in script configuration!"
            exit 1
        fi
        echo "......................................................"
        # Execute program with current tracefile
        if [[ "$tracefile" == "SBK_FILE" ]]; then
            echo "Cracking SBK ... "
        else
            echo "Cracking NV-MEK ... "
        fi

        ./"$EXEC_NAME" "$tracefile"  2>&1 | tee -a "$LOG_FILE"

        # Check exit status
        if [ $? -ne 0 ]; then
            echo "Execution failed for trace file: $tracefile"
            exit 1
        else
            echo "Completed."
        fi
    done

    echo "SBK crack successfully!"
    echo "......................................................"
    echo "Starting decryption RCM Message process..."
    local SCRIPT_DIR
    SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
    "$PYTHON_CMD" "$SCRIPT_DIR/decrypt.py"
    echo "Decryption completed successfully!"
    echo "......................................................"
}

# --- Entry Point ---
main