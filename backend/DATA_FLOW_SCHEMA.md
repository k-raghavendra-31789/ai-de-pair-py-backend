# 🔄 AI SQL Generation System - Data Flow Schema

## 📊 **Complete System Data Flow Diagram**

```mermaid
graph TB
    %% Input Layer
    A[📄 Excel Mapping Document] --> B[🔍 Excel Data Processor]
    A1[📁 Multiple Sheets] --> B
    A2[📋 Unstructured Content] --> B
    A3[💼 Business Logic] --> B

    %% Processing Layer
    B --> C{🧠 Information Discovery Engine}
    C --> D[📍 Sheet Pattern Scanner]
    C --> E[🔍 Content Analyzer]
    C --> F[🎯 Information Locator]

    %% Discovery Questions Layer
    D --> G[❓ Discovery Questions Generator]
    E --> G
    F --> G
    G --> H[💬 Strategic Chat Interface]
    H --> I[👤 User Responses]
    I --> J[📝 Information Mapping]

    %% AI Analysis Layer
    J --> K[🤖 AI Strategy Engine]
    K --> L[📊 Mapping Analysis]
    K --> M[🔗 Relationship Detection]
    K --> N[🎯 Target Schema Analysis]

    %% Strategic Clarification Layer
    L --> O{❓ Strategic Clarification Engine}
    M --> O
    N --> O
    O --> P[🎭 Multiple Target Tables?]
    O --> Q[🔄 Transformation Strategy?]
    O --> R[🔗 Join Strategy?]
    O --> S[📊 Output Format?]

    %% Decision Layer
    P --> T[💬 Multi-table Questions]
    Q --> U[💬 Transformation Questions]
    R --> V[💬 Join Questions]
    S --> W[💬 Format Questions]

    %% User Interaction Layer
    T --> X[👤 User Strategic Decisions]
    U --> X
    V --> X
    W --> X
    X --> Y[📋 Final Strategy Document]

    %% SQL Generation Layer
    Y --> Z[⚡ SQL Generator Engine]
    Z --> AA{🎯 Generation Strategy}
    AA --> BB[📄 Single Unified Query]
    AA --> CC[📑 Multiple Separate Queries]
    AA --> DD[🔄 Sequential Pipeline]

    %% Output Layer
    BB --> EE[📤 SQL Output]
    CC --> EE
    DD --> EE
    EE --> FF[📊 Performance Analysis]
    EE --> GG[✅ Validation & Testing]

    %% Feedback Layer
    FF --> HH[📈 SSE Progress Events]
    GG --> HH
    HH --> II[🖥️ Frontend Real-time Updates]

    %% Styling
    classDef inputClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef processClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef aiClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef userClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef outputClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class A,A1,A2,A3 inputClass
    class B,C,D,E,F,G,J,K,L,M,N processClass
    class O,P,Q,R,S,Z,AA aiClass
    class H,I,T,U,V,W,X,Y userClass
    class BB,CC,DD,EE,FF,GG,HH,II outputClass
```

## 🏗️ **Detailed Component Architecture**

### **1. 📥 Input Processing Layer**

```mermaid
graph LR
    A[📄 Excel File] --> B[🔍 Excel Data Processor]
    B --> C[📊 Sheet Parser]
    B --> D[📋 Content Extractor]
    B --> E[🔍 Pattern Detector]

    C --> F[📑 Sheet Metadata]
    D --> G[📝 Text Content]
    E --> H[🎯 Content Patterns]

    F --> I[📋 Consolidated Analysis]
    G --> I
    H --> I

    I --> J[🤖 AI Ready Format]
```

**Components:**

- **Excel Data Processor**: Handles any Excel structure
- **Sheet Parser**: Extracts sheet names, headers, row data
- **Content Extractor**: Pulls meaningful text from cells
- **Pattern Detector**: Identifies tables, lists, mappings
- **Consolidated Analysis**: Creates AI-analyzable text representation

### **2. 🧠 Information Discovery Layer**

```mermaid
graph TB
    A[📊 Excel Analysis] --> B{🔍 Information Discovery Engine}

    B --> C[📍 Transformation Discovery]
    B --> D[🔗 Join Information Discovery]
    B --> E[🎯 Target Schema Discovery]
    B --> F[📊 Filter Criteria Discovery]
    B --> G[🏢 Business Context Discovery]
    B --> H[💾 Data Source Discovery]

    C --> I[❓ Which columns for transformations?]
    D --> J[❓ Which sheet has join details?]
    E --> K[❓ Where is target structure?]
    F --> L[❓ Where are filter rules?]
    G --> M[❓ Where are business rules?]
    H --> N[❓ How to understand source data?]

    I --> O[💬 Discovery Questions]
    J --> O
    K --> O
    L --> O
    M --> O
    N --> O

    O --> P[👤 User Guidance]
    P --> Q[📍 Information Location Map]
```

### **3. 🤖 AI Strategic Analysis Layer**

```mermaid
graph TB
    A[📍 Information Location Map] --> B[🤖 AI Strategy Engine]

    B --> C[📊 Mapping Analysis]
    B --> D[🔗 Relationship Detection]
    B --> E[🎯 Target Schema Analysis]
    B --> F[⚡ Complexity Assessment]

    C --> G{🎭 Multiple Target Tables?}
    D --> H{🔗 Complex Joins Needed?}
    E --> I{🔄 Complex Transformations?}
    F --> J{📊 High Data Volume?}

    G --> K[💬 Multi-table Strategy Questions]
    H --> L[💬 Join Strategy Questions]
    I --> M[💬 Transformation Strategy Questions]
    J --> N[💬 Performance Strategy Questions]

    K --> O[👤 Strategic User Decisions]
    L --> O
    M --> O
    N --> O

    O --> P[📋 Final SQL Strategy]
```

### **4. ⚡ SQL Generation Layer**

```mermaid
graph TB
    A[📋 Final SQL Strategy] --> B{⚡ SQL Generator Engine}

    B --> C{🎯 Generation Strategy Decision}

    C --> D[📄 Single Unified Query Path]
    C --> E[📑 Multiple Queries Path]
    C --> F[🔄 Sequential Pipeline Path]

    D --> G[🔧 Unified Query Builder]
    E --> H[🔧 Individual Query Builder]
    F --> I[🔧 Pipeline Query Builder]

    G --> J[📝 Single Complex SQL]
    H --> K[📝 Multiple SQL Files]
    I --> L[📝 Ordered SQL Sequence]

    J --> M[✅ SQL Validation]
    K --> M
    L --> M

    M --> N[📊 Performance Analysis]
    N --> O[📤 Final SQL Output]
```

### **5. 📡 Real-time Feedback Layer (SSE Events)**

```mermaid
graph LR
    A[⚡ SQL Generation Process] --> B[📡 SSE Event Stream]

    B --> C[🚀 discovery_started]
    B --> D[🔍 analysis_progress]
    B --> E[❓ questions_generated]
    B --> F[✅ strategy_confirmed]
    B --> G[⚡ sql_generation_started]
    B --> H[📊 generation_progress]
    B --> I[✅ sql_completed]
    B --> J[📈 validation_results]

    C --> K[🖥️ Frontend Progress Bar]
    D --> K
    E --> L[💬 Frontend Question UI]
    F --> K
    G --> K
    H --> K
    I --> M[📤 Frontend SQL Display]
    J --> N[📊 Frontend Results Panel]
```

## 🔄 **Complete System Flow Phases**

### **Phase 1: 📥 Input & Discovery**

```
Excel Upload → Content Analysis → Information Discovery Questions → User Guidance
```

### **Phase 2: 🧠 Strategic Analysis**

```
Information Mapping → AI Analysis → Strategic Questions → User Decisions
```

### **Phase 3: ⚡ SQL Generation**

```
Strategy Execution → SQL Building → Validation → Output Delivery
```

### **Phase 4: 📡 Real-time Feedback**

```
SSE Events → Frontend Updates → User Experience → Progress Tracking
```

## 📊 **Data Flow Example**

```json
{
  "input": {
    "excel_file": "sales_mapping.xlsx",
    "sheets": ["Instructions", "Field_Map", "Join_Logic", "Output_Format"],
    "user_context": "Need SQL for monthly sales report"
  },
  "discovery_phase": {
    "questions": [
      "Field_Map sheet has transformations - should I use column C for logic?",
      "Join_Logic has table relationships - are these complete?",
      "Output_Format shows target structure - is this the final format?"
    ],
    "user_responses": {
      "transformation_source": "Field_Map:Column C",
      "join_source": "Join_Logic:ERD section",
      "target_source": "Output_Format:Headers"
    }
  },
  "strategy_phase": {
    "analysis": {
      "target_tables": ["monthly_sales_summary"],
      "source_tables": ["orders", "customers", "products"],
      "complexity": "medium",
      "transformations": ["date_grouping", "sales_calculation"]
    },
    "strategic_questions": [
      "Single query or multiple steps?",
      "How to handle date grouping?",
      "Include all customers or filter?"
    ],
    "decisions": {
      "approach": "single_unified_query",
      "date_strategy": "monthly_grouping",
      "filter_strategy": "active_customers_only"
    }
  },
  "generation_phase": {
    "sql_output": "SELECT ... FROM orders o JOIN customers c ...",
    "validation": "passed",
    "performance_score": 85
  }
}
```

## 🎯 **Key System Benefits**

1. **🔍 Intelligent Discovery**: Automatically finds information in unstructured Excel
2. **💬 Strategic Guidance**: Asks smart questions to understand user intent
3. **🤖 Adaptive AI**: Handles any Excel structure with flexible processing
4. **⚡ Optimized Output**: Generates efficient SQL based on user strategy
5. **📡 Real-time Updates**: Provides live progress feedback via SSE
6. **🎯 User-Centric**: Focuses on business outcomes rather than technical details

This data flow ensures comprehensive, intelligent, and user-friendly SQL generation from any Excel mapping document! 🚀
