#!/bin/bash

# Beyan Document Digitization System - Setup Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Setting up Beyan Document Digitization System with n8n..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_success "Prerequisites check passed"

# Create necessary directories
print_status "Creating project directories..."

directories=(
    "data/uploads"
    "data/processed"
    "data/models"
    "data/backups"
    "n8n/workflows"
    "n8n/credentials"
    "n8n/custom-nodes"
    "n8n/backups"
    "config/postgres"
    "config/monitoring"
    "config/ssl"
    "logs"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    print_status "Created directory: $dir"
done

print_success "Project directories created"

# Copy environment file
print_status "Setting up environment configuration..."

if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success "Created .env file from template"
    print_warning "Please edit .env file with your actual configuration values"
else
    print_warning ".env file already exists, skipping copy"
fi

# Generate encryption key if not set
if ! grep -q "your_32_character_encryption_key_here" .env 2>/dev/null; then
    print_status "Generating n8n encryption key..."
    # Generate a random 32-character key
    encryption_key=$(openssl rand -hex 16)
    sed -i.bak "s/your_32_character_encryption_key_here/$encryption_key/" .env
    print_success "Generated n8n encryption key"
fi

# Create PostgreSQL initialization script
print_status "Setting up database initialization..."

cat > config/postgres/init-multiple-databases.sh << 'EOF'
#!/bin/bash
set -e

function create_user_and_database() {
    local database=$1
    echo "Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_user_and_database $db
    done
    echo "Multiple databases created"
fi
EOF

chmod +x config/postgres/init-multiple-databases.sh
print_success "Database initialization script created"

# Create basic nginx configuration
print_status "Setting up nginx configuration..."

cat > config/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream n8n {
        server n8n:5678;
    }
    
    upstream kimi-vl {
        server kimi-vl:8001;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # n8n interface
        location / {
            proxy_pass http://n8n;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # Kimi-VL API
        location /api/kimi-vl/ {
            proxy_pass http://kimi-vl/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # File uploads
        location /uploads/ {
            alias /var/www/uploads/;
            autoindex on;
        }
    }
}
EOF

print_success "Nginx configuration created"

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_status "Creating .gitignore file..."
    
    cat > .gitignore << 'EOF'
# Environment files
.env
.env.local
.env.production

# Data directories
data/uploads/*
data/processed/*
data/models/*
data/backups/*
!data/uploads/.gitkeep
!data/processed/.gitkeep
!data/models/.gitkeep
!data/backups/.gitkeep

# n8n data
n8n/credentials/*
n8n/backups/*
!n8n/credentials/.gitkeep
!n8n/backups/.gitkeep

# Logs
logs/*
!logs/.gitkeep
*.log

# Docker
.docker/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# SSL certificates
config/ssl/*.pem
config/ssl/*.key
config/ssl/*.crt
EOF
    
    print_success ".gitignore file created"
fi

# Create placeholder files
touch data/uploads/.gitkeep
touch data/processed/.gitkeep
touch data/models/.gitkeep
touch data/backups/.gitkeep
touch n8n/credentials/.gitkeep
touch n8n/backups/.gitkeep
touch logs/.gitkeep

print_success "Setup completed successfully!"

echo ""
echo "🎉 Beyan Document Digitization System is ready!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: docker-compose up -d"
echo "3. Access n8n at: http://localhost:5678"
echo "4. Access Kimi-VL API at: http://localhost:8001"
echo ""
echo "For more information, see the documentation in docs/"
