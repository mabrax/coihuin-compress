#!/bin/bash
# sync-check.sh - Compare local repo with global installation
#
# Usage:
#   ./scripts/sync-check.sh          Check for differences
#   ./scripts/sync-check.sh --sync   Sync local -> global (with confirmation)

LOCAL_DIR=".claude/skills/coihuin-compress"
GLOBAL_DIR="$HOME/.claude/skills/coihuin-compress"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse arguments
SYNC_MODE=false
if [ "$1" = "--sync" ]; then
    SYNC_MODE=true
elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Compare local skill files with global installation."
    echo ""
    echo "Options:"
    echo "  --sync    Sync local -> global (copies local files to global)"
    echo "  --help    Show this help message"
    echo ""
    echo "Directories:"
    echo "  Local:  $LOCAL_DIR"
    echo "  Global: $GLOBAL_DIR"
    exit 0
fi

echo "=== Coihuin Compress Sync Check ==="
echo ""

# Check directories exist
if [ ! -d "$LOCAL_DIR" ]; then
    echo -e "${RED}✗ Local directory not found: $LOCAL_DIR${NC}"
    exit 1
fi

if [ ! -d "$GLOBAL_DIR" ]; then
    echo -e "${YELLOW}⚠ Global directory not found: $GLOBAL_DIR${NC}"
    if $SYNC_MODE; then
        echo -e "${BLUE}Creating global directory and copying files...${NC}"
        mkdir -p "$GLOBAL_DIR"
        cp -r "$LOCAL_DIR"/* "$GLOBAL_DIR/"
        echo -e "${GREEN}✓ Initial sync complete${NC}"
        exit 0
    else
        echo "  Run: $0 --sync"
        exit 1
    fi
fi

# Compare files
all_match=true
files_checked=0

for local_file in $(find "$LOCAL_DIR" -type f | sort); do
    relative_path="${local_file#$LOCAL_DIR/}"
    global_file="$GLOBAL_DIR/$relative_path"

    if [ ! -f "$global_file" ]; then
        echo -e "${RED}✗ Missing in global: $relative_path${NC}"
        all_match=false
        continue
    fi

    local_md5=$(md5 -q "$local_file")
    global_md5=$(md5 -q "$global_file")

    if [ "$local_md5" = "$global_md5" ]; then
        echo -e "${GREEN}✓${NC} $relative_path"
    else
        echo -e "${RED}✗ DIFFERS: $relative_path${NC}"
        echo "    local:  $local_md5"
        echo "    global: $global_md5"
        all_match=false
    fi
    ((files_checked++))
done

# Check for extra files in global
for global_file in $(find "$GLOBAL_DIR" -type f | sort); do
    relative_path="${global_file#$GLOBAL_DIR/}"
    local_file="$LOCAL_DIR/$relative_path"

    if [ ! -f "$local_file" ]; then
        echo -e "${YELLOW}⚠ Extra in global: $relative_path${NC}"
        all_match=false
    fi
done

echo ""
echo "Files checked: $files_checked"

if $all_match; then
    echo -e "${GREEN}✓ All files in sync${NC}"
    exit 0
else
    if $SYNC_MODE; then
        echo ""
        echo -e "${BLUE}Syncing local -> global...${NC}"

        # Remove files in global that don't exist in local
        for global_file in $(find "$GLOBAL_DIR" -type f | sort); do
            relative_path="${global_file#$GLOBAL_DIR/}"
            local_file="$LOCAL_DIR/$relative_path"
            if [ ! -f "$local_file" ]; then
                echo -e "${YELLOW}Removing: $relative_path${NC}"
                rm "$global_file"
            fi
        done

        # Copy all files from local to global
        cp -r "$LOCAL_DIR"/* "$GLOBAL_DIR/"

        echo -e "${GREEN}✓ Sync complete${NC}"
        exit 0
    else
        echo -e "${RED}✗ Out of sync${NC}"
        echo "  Run: $0 --sync"
        exit 1
    fi
fi
