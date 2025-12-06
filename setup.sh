#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/pon-tanuki/design-docs-for-ai-driven-development"
RAW_BASE_URL="https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main"
TEMPLATE_VERSION="1.0.0"

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo ""
    print_message "$BLUE" "═══════════════════════════════════════════════════════════"
    print_message "$BLUE" "  AI-First Development Template Setup"
    print_message "$BLUE" "  Version: ${TEMPLATE_VERSION}"
    print_message "$BLUE" "═══════════════════════════════════════════════════════════"
    echo ""
}

print_step() {
    print_message "$GREEN" "▶ $1"
}

print_warning() {
    print_message "$YELLOW" "⚠ $1"
}

print_error() {
    print_message "$RED" "✗ $1"
}

print_success() {
    print_message "$GREEN" "✓ $1"
}

# Check if project directory already exists
check_directory() {
    local project_name=$1

    # If using current directory, don't check existence
    if [ "$project_name" = "." ]; then
        return 0
    fi

    if [ -d "$project_name" ]; then
        print_error "Directory '$project_name' already exists!"
        echo ""
        echo "Please choose one of the following options:"
        echo "  1. Remove the existing directory: rm -rf $project_name"
        echo "  2. Choose a different project name"
        echo "  3. Merge into existing directory (advanced)"
        exit 1
    fi
}

# Download file from GitHub
download_file() {
    local file_path=$1
    local destination=$2
    local url="${RAW_BASE_URL}/${file_path}"

    if command -v curl &> /dev/null; then
        curl -sSfL --connect-timeout 10 --max-time 30 "$url" -o "$destination" 2>/dev/null || {
            print_warning "Failed to download: $file_path"
            return 1
        }
    elif command -v wget &> /dev/null; then
        wget -q --timeout=30 "$url" -O "$destination" 2>/dev/null || {
            print_warning "Failed to download: $file_path"
            return 1
        }
    else
        print_error "Neither curl nor wget is available. Please install one of them."
        exit 1
    fi
    return 0
}

# Create directory structure
create_structure() {
    local project_name=$1

    print_step "Creating directory structure..."

    # Create base directories
    mkdir -p "$project_name"/{docs,generator_instructions,meta,project}

    # Create subdirectories
    mkdir -p "$project_name"/docs/{product,architecture,agent,dev_process,ops}
    mkdir -p "$project_name"/docs/architecture/{api_design,data_schemas}
    mkdir -p "$project_name"/docs/agent/tools
    mkdir -p "$project_name"/project/tasks

    print_success "Directory structure created"
}

# Download template files
download_templates() {
    local project_name=$1

    print_step "Downloading template files..."

    # List of files to download
    local files=(
        "README.md"
        "LICENSE"
        "CLAUDE.md"
        "docs/product/vision.md"
        "docs/product/requirements.yaml"
        "docs/product/user_scenarios.md"
        "docs/product/nonfunctional_requirements.yaml"
        "docs/architecture/system_overview.md"
        "docs/architecture/domain_model.md"
        "docs/architecture/sequence_diagrams.md"
        "docs/architecture/api_design/openapi.yaml"
        "docs/architecture/data_schemas/entities.yaml"
        "docs/architecture/data_schemas/validation_rules.yaml"
        "docs/agent/roles.yaml"
        "docs/agent/behaviours.md"
        "docs/agent/constraints.yaml"
        "docs/agent/tools/available_tools.md"
        "docs/agent/tools/tool_schemas.yaml"
        "docs/dev_process/coding_standards.md"
        "docs/dev_process/branch_strategy.md"
        "docs/dev_process/agent_commit_rules.yaml"
        "docs/dev_process/review_guidelines.md"
        "docs/ops/ci_cd_pipeline.md"
        "docs/ops/monitoring_plan.md"
        "docs/ops/logs_schema.yaml"
        "generator_instructions/system_prompt.md"
        "generator_instructions/file_update_policy.md"
        "generator_instructions/forbidden_actions.md"
        "meta/glossary.md"
        "meta/dependencies.md"
        "meta/risks.md"
        "meta/change_history.md"
        "project/roadmap.md"
        "project/tasks/initial_backlog.yaml"
    )

    local downloaded=0
    local failed=0

    for file in "${files[@]}"; do
        local dest_file="$project_name/$file"
        local dest_dir=$(dirname "$dest_file")

        mkdir -p "$dest_dir"

        if download_file "$file" "$dest_file"; then
            ((downloaded++))
        else
            ((failed++))
        fi
    done

    print_success "Downloaded $downloaded files"

    if [ $failed -gt 0 ]; then
        print_warning "$failed files could not be downloaded"
    fi
}

# Create project-specific files
create_project_files() {
    local project_name=$1
    local display_name="$project_name"

    # For current directory, use the directory name
    if [ "$project_name" = "." ]; then
        display_name="$(basename "$(pwd)")"
    fi

    print_step "Creating project-specific files..."

    # Create .gitignore
    cat > "$project_name/.gitignore" <<'EOF'
# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.venv/
vendor/

# Build outputs
dist/
build/
*.o
*.so
*.exe

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
*.env

# Logs
*.log
logs/

# Temporary
tmp/
temp/
*.tmp

# Test coverage
coverage/
.coverage
*.cover
htmlcov/
EOF

    # Create .editorconfig
    cat > "$project_name/.editorconfig" <<'EOF'
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,ts,jsx,tsx}]
indent_style = space
indent_size = 2

[*.{py}]
indent_style = space
indent_size = 4

[*.{go}]
indent_style = tab
indent_size = 4

[*.{yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
EOF

    # Create project README
    cat > "$project_name/PROJECT_README.md" <<EOF
# $display_name

AIファースト開発テンプレートを使用したプロジェクトです。

## セットアップ日時
$(date '+%Y-%m-%d %H:%M:%S')

## 次のステップ

1. **プロジェクト情報の更新**
   - \`docs/product/vision.md\` - プロダクトビジョンを記述
   - \`docs/product/requirements.yaml\` - 機能要件を定義
   - \`docs/architecture/system_overview.md\` - システム構成を設計

2. **開発環境のセットアップ**
   - 使用する言語・フレームワークのインストール
   - \`docs/dev_process/coding_standards.md\` の確認と調整

3. **AIエージェントの設定**
   - \`CLAUDE.md\` を確認
   - \`docs/agent/roles.yaml\` で必要な役割を定義
   - \`generator_instructions/system_prompt.md\` をカスタマイズ

4. **バージョン管理の初期化**
   \`\`\`bash
   git init
   git add .
   git commit -m "feat: initialize project with AI-first development template"
   \`\`\`

## ドキュメント構造

\`\`\`
$display_name/
├── docs/                          # ドキュメント
│   ├── product/                   # プロダクト定義
│   ├── architecture/              # アーキテクチャ
│   ├── agent/                     # AIエージェント設定
│   ├── dev_process/               # 開発プロセス
│   └── ops/                       # 運用
├── generator_instructions/        # AIエージェント指示
├── meta/                          # メタ情報
├── project/                       # プロジェクト管理
└── CLAUDE.md                      # Claude Code指示書
\`\`\`

## AI駆動開発の開始

Claude Codeまたは他のAIアシスタントに以下を参照させてください:

- \`CLAUDE.md\` - AI向けの包括的な指示書
- \`generator_instructions/\` - 行動規則と制約
- \`docs/dev_process/\` - 開発規約

## リソース

- テンプレートリポジトリ: $REPO_URL
- ドキュメント: [AI-First Development Template](${REPO_URL}#readme)

---
Generated by AI-First Development Template Setup Script v${TEMPLATE_VERSION}
EOF

    print_success "Project-specific files created"
}

# Initialize git repository (optional)
init_git() {
    local project_name=$1

    print_step "Initializing git repository..."

    cd "$project_name"

    if git init; then
        git add .
        git commit -m "feat: initialize project with AI-first development template

- Setup project structure based on AI-first development template
- Add comprehensive documentation templates
- Configure AI agent instructions and constraints
- Prepare development process guidelines

Template version: ${TEMPLATE_VERSION}
Repository: ${REPO_URL}

🤖 Generated with AI-First Development Template Setup Script" 2>/dev/null || true

        print_success "Git repository initialized"
    else
        print_warning "Git initialization failed (git may not be installed)"
    fi

    cd - > /dev/null
}

# Create project metadata
create_metadata() {
    local project_name=$1
    local display_name="$project_name"

    # For current directory, use the directory name
    if [ "$project_name" = "." ]; then
        display_name="$(basename "$(pwd)")"
    fi

    cat > "$project_name/.template-metadata.json" <<EOF
{
  "template_version": "${TEMPLATE_VERSION}",
  "template_source": "${REPO_URL}",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "project_name": "$display_name"
}
EOF
}

# Print next steps
print_next_steps() {
    local project_name=$1

    echo ""
    print_message "$GREEN" "═══════════════════════════════════════════════════════════"
    print_message "$GREEN" "  Setup Complete!"
    print_message "$GREEN" "═══════════════════════════════════════════════════════════"
    echo ""

    if [ "$project_name" = "." ]; then
        echo "Your AI-first development templates have been installed in the current directory."
    else
        echo "Your AI-first development project is ready at: $project_name/"
    fi
    echo ""
    echo "Next steps:"
    echo ""

    if [ "$project_name" != "." ]; then
        echo "  1. Navigate to your project:"
        print_message "$BLUE" "     cd $project_name"
        echo ""
    fi

    echo "  $([ "$project_name" = "." ] && echo "1" || echo "2"). Review the project README:"
    print_message "$BLUE" "     cat PROJECT_README.md"
    echo ""
    echo "  $([ "$project_name" = "." ] && echo "2" || echo "3"). Customize project information:"
    print_message "$BLUE" "     \$EDITOR docs/product/vision.md"
    print_message "$BLUE" "     \$EDITOR docs/product/requirements.yaml"
    echo ""
    echo "  $([ "$project_name" = "." ] && echo "3" || echo "4"). Start using AI agents:"
    print_message "$BLUE" "     # Reference CLAUDE.md for AI instructions"
    print_message "$BLUE" "     # AI agents will read this automatically"
    echo ""
    echo "  $([ "$project_name" = "." ] && echo "4" || echo "5"). (Optional) Setup remote repository:"
    print_message "$BLUE" "     git remote add origin <your-repo-url>"
    print_message "$BLUE" "     git push -u origin main"
    echo ""
    print_success "Happy AI-driven development! 🚀"
    echo ""
}

# Show usage
show_usage() {
    cat <<EOF
Usage: $0 [OPTIONS] [project-name]

Setup AI-first development template for a new project.

Arguments:
  project-name    Name of the project directory to create (optional)
                  If not specified, templates will be installed in the current directory

Options:
  -h, --help      Show this help message
  -v, --version   Show template version
  --no-git        Skip git repository initialization

Examples:
  # Install templates in current directory
  $0

  # Create new project directory
  $0 my-awesome-project

  # Create project without git initialization
  $0 --no-git my-project

  # Quick setup with curl (current directory)
  curl -fsSL https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh | bash

  # Quick setup with curl (new directory)
  curl -fsSL https://raw.githubusercontent.com/pon-tanuki/design-docs-for-ai-driven-development/main/setup.sh | bash -s my-project

EOF
}

# Main function
main() {
    local skip_git=false
    local project_name=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -v|--version)
                echo "AI-First Development Template Setup v${TEMPLATE_VERSION}"
                exit 0
                ;;
            --no-git)
                skip_git=true
                shift
                ;;
            -*)
                print_error "Unknown option: $1"
                echo ""
                show_usage
                exit 1
                ;;
            *)
                project_name="$1"
                shift
                ;;
        esac
    done

    # If no project name is provided, use current directory
    if [ -z "$project_name" ]; then
        project_name="."
        print_warning "No project name specified. Installing templates in current directory."
    fi

    # Validate project name (skip validation for current directory)
    if [ "$project_name" != "." ] && [[ ! "$project_name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        print_error "Invalid project name. Use only letters, numbers, hyphens, and underscores."
        exit 1
    fi

    print_header

    # Check if directory already exists
    check_directory "$project_name"

    # Create project
    create_structure "$project_name"
    download_templates "$project_name"
    create_project_files "$project_name"
    create_metadata "$project_name"

    # Initialize git if not skipped (skip for current directory if already a git repo)
    if [ "$skip_git" = false ]; then
        if [ "$project_name" = "." ] && [ -d ".git" ]; then
            print_warning "Git repository already exists. Skipping git initialization."
        else
            init_git "$project_name"
        fi
    fi

    # Print next steps
    print_next_steps "$project_name"
}

# Run main function
main "$@"
