# Project Diagrams

## 1. GitHub Actions CI/CD Pipeline - Activity Diagram

```mermaid
graph TB
    Start([Push to main branch]) --> CheckPath{Changes in<br/>backend/ or<br/>workflow?}
    CheckPath -->|No| End([End])
    CheckPath -->|Yes| BuildJob[Build Job]
    
    subgraph Build["🔨 Build Job"]
        B1[Checkout Code]
        B2[Setup Python 3.12.6]
        B3[Create Virtual Environment]
        B4[Install Dependencies]
        B5[Collect Static Files]
        B6[Upload Artifact]
        
        B1 --> B2 --> B3 --> B4 --> B5 --> B6
    end
    
    BuildJob --> B1
    B6 --> TestJob[Test Job]
    
    subgraph Test["🧪 Test Job"]
        T1[Download Artifact]
        T2[Checkout Code]
        T3[Setup Python 3.12.6]
        T4[Create Virtual Environment]
        T5[Install Dependencies]
        T6[Run Database Migrations]
        T7[Run Pytest with Coverage]
        T8[Upload Coverage Reports]
        T9[Display Test Summary]
        
        T1 --> T2 --> T3 --> T4 --> T5 --> T6 --> T7 --> T8 --> T9
    end
    
    TestJob --> T1
    T9 --> TestPassed{Tests<br/>Passed?}
    TestPassed -->|No| End
    TestPassed -->|Yes| DeployJob[Deploy Job]
    
    subgraph Deploy["🚀 Deploy Job"]
        D1[Download Artifact]
        D2[Login to Azure<br/>OIDC Authentication]
        D3[Deploy to Azure Web App<br/>Production Slot]
        D4[Execute startup.sh]
        
        D1 --> D2 --> D3 --> D4
    end
    
    DeployJob --> D1
    D4 --> Success([✅ Deployment Complete])
    
    style Build fill:#e1f5ff
    style Test fill:#fff4e1
    style Deploy fill:#e7ffe1
    style Success fill:#c8ffc8
```

## 2. GitHub Actions - Sequence Diagram

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant Build as Build Job
    participant Test as Test Job
    participant Azure as Azure Cloud
    
    Dev->>GH: Push to main branch
    GH->>Build: Trigger workflow
    
    Build->>Build: Setup Python 3.12.6
    Build->>Build: Install dependencies
    Build->>Build: Collect static files
    Build->>GH: Upload artifact
    
    GH->>Test: Start test job
    Test->>GH: Download artifact
    Test->>Test: Run migrations
    Test->>Test: Run pytest
    Test->>Test: Generate coverage
    Test->>GH: Upload coverage reports
    
    alt Tests Pass
        GH->>Azure: Login with OIDC
        Azure-->>GH: Authentication success
        GH->>Azure: Deploy to Web App
        Azure->>Azure: Execute startup.sh
        Azure-->>Dev: Deployment successful ✅
    else Tests Fail
        Test-->>Dev: Tests failed ❌
    end
```

## 3. Terraform Infrastructure - Use Case Diagram

```mermaid
graph TB
    subgraph Actors
        DevOps[DevOps Engineer]
        App[Django Application]
        Users[End Users]
    end
    
    subgraph "Azure Infrastructure Use Cases"
        UC1[Create Resource Group]
        UC2[Provision App Service Plan]
        UC3[Deploy Web Application]
        UC4[Setup PostgreSQL Database]
        UC5[Configure Networking]
        UC6[Manage Firewall Rules]
        UC7[Configure App Settings]
        UC8[Enable Database Backups]
        UC9[Scale Resources]
    end
    
    DevOps -->|terraform apply| UC1
    DevOps -->|terraform apply| UC2
    DevOps -->|terraform apply| UC3
    DevOps -->|terraform apply| UC4
    DevOps -->|configure| UC5
    DevOps -->|manage| UC6
    DevOps -->|set environment vars| UC7
    DevOps -->|configure| UC8
    DevOps -->|adjust SKU| UC9
    
    UC1 -.->|contains| UC2
    UC2 -.->|hosts| UC3
    UC1 -.->|contains| UC4
    UC4 -.->|creates| UC5
    UC5 -.->|applies| UC6
    UC3 -.->|requires| UC7
    UC4 -.->|enables| UC8
    
    UC3 -->|serves| Users
    UC3 -->|connects to| UC4
    App -->|runs on| UC3
    App -->|stores data in| UC4
    
    style DevOps fill:#ffcccc
    style App fill:#ccffcc
    style Users fill:#ccccff
```

## 4. Terraform Infrastructure - Component Diagram

```mermaid
graph TB
    subgraph RG["Resource Group: AnomyFormResourceGroup"]
        subgraph AppService["App Service Infrastructure"]
            ASP[App Service Plan<br/>Linux, Python 3.12<br/>SKU: Configurable]
            WebApp[Linux Web App<br/>anonymous-form-backend<br/>Django Application]
            
            ASP -->|hosts| WebApp
        end
        
        subgraph Database["Database Infrastructure"]
            PG[PostgreSQL Flexible Server<br/>Version 14<br/>7-day backups]
            DB[(Database: anonymousform<br/>Charset: UTF8)]
            
            PG -->|contains| DB
        end
        
        subgraph Security["Security & Networking"]
            FW1[Firewall Rule:<br/>Allow Azure Services]
            FW2[Firewall Rule:<br/>Allow All - DEV only]
        end
    end
    
    WebApp -->|connects via| PG
    PG -->|protected by| FW1
    PG -->|protected by| FW2
    
    subgraph Config["Configuration"]
        ENV[Environment Variables<br/>SECRET_KEY, JWT_KEY<br/>DB credentials<br/>Email config]
    end
    
    WebApp -.->|configured with| ENV
    
    subgraph External["External Services"]
        Email[Email Server<br/>SMTP]
        Client[Frontend Application]
    end
    
    WebApp -->|sends emails via| Email
    WebApp -->|serves API to| Client
    
    style RG fill:#e3f2fd
    style AppService fill:#f3e5f5
    style Database fill:#e8f5e9
    style Security fill:#fff3e0
    style Config fill:#fce4ec
```

## 5. Terraform Resource Dependencies

```mermaid
graph LR
    TF[Terraform Apply]
    
    TF --> RG[Resource Group]
    RG --> ASP[App Service Plan]
    RG --> PG[PostgreSQL Server]
    
    ASP --> WebApp[Web App]
    PG --> DB[(Database)]
    PG --> FW1[Firewall Rule 1]
    PG --> FW2[Firewall Rule 2]
    
    WebApp -.->|reads config from| DB
    
    style TF fill:#4caf50
    style RG fill:#2196f3
    style ASP fill:#ff9800
    style PG fill:#9c27b0
    style WebApp fill:#f44336
    style DB fill:#00bcd4
```

## 6. CI/CD Pipeline - Deployment Flow

```mermaid
stateDiagram-v2
    [*] --> CodePushed: Developer pushes code
    
    CodePushed --> Building: Trigger workflow
    
    Building --> InstallingDeps: Setup Python
    InstallingDeps --> CollectingStatic: Install packages
    CollectingStatic --> ArtifactReady: Collect static files
    
    ArtifactReady --> Testing: Upload artifact
    
    Testing --> RunningMigrations: Setup test environment
    RunningMigrations --> RunningTests: Apply migrations
    RunningTests --> GeneratingCoverage: Execute pytest
    GeneratingCoverage --> TestResults: Create reports
    
    TestResults --> Deploying: Tests pass ✅
    TestResults --> Failed: Tests fail ❌
    
    Deploying --> AuthenticatingAzure: Download artifact
    AuthenticatingAzure --> DeployingApp: OIDC login
    DeployingApp --> StartingApp: Push to Azure
    StartingApp --> [*]: Deployment complete
    
    Failed --> [*]: Fix errors
```

## 7. Infrastructure Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Azure Cloud                              │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │         Resource Group: AnomyFormResourceGroup            │  │
│  │                                                           │  │
│  │  ┌─────────────────────┐      ┌───────────────────────┐ │  │
│  │  │  App Service Plan    │      │  PostgreSQL Server    │ │  │
│  │  │  ┌───────────────┐  │      │  ┌─────────────────┐  │ │  │
│  │  │  │ Linux Web App │  │      │  │   Database      │  │ │  │
│  │  │  │               │  │◄────►│  │  anonymousform  │  │ │  │
│  │  │  │ Django API    │  │ TCP  │  │                 │  │ │  │
│  │  │  │ Python 3.12   │  │ 5432 │  │   PostgreSQL    │  │ │  │
│  │  │  └───────────────┘  │      │  └─────────────────┘  │ │  │
│  │  │                     │      │                       │ │  │
│  │  │  Environment Vars   │      │  Firewall Rules:     │ │  │
│  │  │  • SECRET_KEY       │      │  • Azure Services    │ │  │
│  │  │  • JWT_KEY          │      │  • Development IPs   │ │  │
│  │  │  • DB Credentials   │      │  • 7-day backups     │ │  │
│  │  └─────────────────────┘      └───────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              │ HTTPS
                              │
                    ┌─────────┴──────────┐
                    │                    │
              ┌─────▼─────┐      ┌──────▼──────┐
              │  End Users │      │   CI/CD     │
              │  (Browser) │      │  Pipeline   │
              └────────────┘      └─────────────┘
```

## Key Components Summary

### GitHub Actions Workflow
- **Trigger**: Push to `main` branch with backend changes
- **Jobs**: 
  1. **Build** - Prepare application artifacts
  2. **Test** - Run automated tests with coverage
  3. **Deploy** - Deploy to Azure using OIDC authentication
- **Artifacts**: Python application with collected static files
- **Test Framework**: Pytest with coverage reporting

### Terraform Infrastructure
- **Cloud Provider**: Azure
- **Main Resources**:
  - App Service Plan (Linux, Python 3.12)
  - PostgreSQL Flexible Server (v14)
  - Firewall rules for security
  - Automated backups
- **Environment**: Production-ready with configurable SKUs
- **Security**: OIDC authentication, firewall rules, encrypted connections

