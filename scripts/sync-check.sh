#!/bin/bash
# sync-check.sh - Compare local repo with global installation

LOCAL_DIR=".claude/skills/coihuin-compress"
GLOBAL_DIR="$HOME/.claude/skills/coihuin-compress"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "=== Coihuin Compress Sync Check ==="
echo ""

# Check directories exist
if [ ! -d "$LOCAL_DIR" ]; then
    echo -e "${RED}✗ Local directory not found: $LOCAL_DIR${NC}"
    exit 1
fi

if [ ! -d "$GLOBAL_DIR" ]; then
    echo -e "${RED}✗ Global directory not found: $GLOBAL_DIR${NC}"
    echo "  Run: cp -r $LOCAL_DIR $GLOBAL_DIR"
    exit 1
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
    echo -e "${RED}✗ Out of sync - run: cp -r $LOCAL_DIR/* $GLOBAL_DIR/${NC}"
    exit 1
fi
