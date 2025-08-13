# AI-DE Pair Backend Architecture Documentation

## 📋 **System Overview**

The AI-DE Pair Backend is a FastAPI-based system that converts Excel mapping documents into SQL queries using AI. The system processes unstructured Excel data and generates optimized SQL with real-time progress streaming via Server-Sent Events (SSE).

## 🏗️ **High-Level Architecture**

```
Frontend (Excel Data) → Backend API → AI Processing → SQL Generation → Database Testing → Final SQL
                                   ↓
                           Real-time SSE Events
```

## 📁 **Project Structure**

```
backend/
├── app/
│   └── main.py                 # FastAPI endpoints and routing
├── utils/
│   ├── __init__.py
│   ├── models.py              # Pydantic data models
│   ├── db_utils.py            # Database connection utilities
│   ├── sse_utils.py           # Server-Sent Events helpers
│   └── sql_generator/
│       ├── __init__.py
│       ├── ai_parser.py       # AI-powered input analysis
│       ├── excel_data_processor.py  # Excel data processing
│       ├── orchestrator.py    # Main SQL generation orchestrator
│       ├── dependency.py      # Dependency graph & cycle detection
│       ├── builder.py         # SQL component builders
│       └── validator.py       # SQL testing & validation
├── requirements.txt
└── ENDPOINTS.md
```

---

## 🔧 **Component Responsibilities**

### 1. **API Layer** (`app/main.py`)

**Purpose:** HTTP endpoints and request routing

- **Regular SQL Execution:** `/run-sql` and `/run-sql-sse`
- **AI SQL Generation:** `/generate-sql-sse`
- **Excel Processing:** `/generate-sql-from-excel-sse`
- **Testing:** `/test-sse`, `/`

### 2. **Data Models** (`utils/models.py`)

**Purpose:** Request/response data structures

- `ExcelSheetData` - Single Excel sheet representation
- `ExcelMappingRequest` - Complete Excel processing request
- `SQLGenerationRequest` - General AI SQL generation request

### 3. **Excel Data Processor** (`utils/sql_generator/excel_data_processor.py`)

**Purpose:** Convert Excel sheet data to AI-friendly text

- `ExcelDataProcessor.process_excel_request()` - Main processing method
- `_process_sheet()` - Individual sheet analysis
- `_analyze_table_structure()` - Identify table patterns
- `_extract_all_text()` - Extract meaningful text content

### 4. **AI Parser** (`utils/sql_generator/ai_parser.py`)

**Purpose:** AI-powered analysis of mapping documents

- `AIInputParser.parse_input()` - Main AI parsing method
- `_call_openai()` / `_call_claude()` - Raw HTTP API calls
- `_create_parsing_prompt()` - AI prompt engineering
- `ParsedMapping` - Structured AI output format

### 5. **SQL Generation Orchestrator** (`utils/sql_generator/orchestrator.py`)

**Purpose:** Coordinate the entire SQL generation pipeline

- `generate_sql_with_events()` - Main orchestration with SSE
- Manages workflow: AI Analysis → Dependency Graph → SQL Building → Testing

### 6. **Database Utilities** (`utils/db_utils.py`)

**Purpose:** Databricks connection and SQL execution

- `execute_sql_async()` - Async SQL execution with timeout
- `validate_connection_params()` - Parameter validation
- `format_row_data()` - Result formatting

### 7. **SSE Utilities** (`utils/sse_utils.py`)

**Purpose:** Server-Sent Events formatting

- `create_sse_event()` - Format SSE events
- Helper functions for different event types

---

## 🔄 **Data Flow Architecture**

### **Option A: Excel-Based Processing**

```
1. Frontend parses Excel file
2. Sends structured data to /generate-sql-from-excel-sse
3. ExcelDataProcessor converts to text
4. AIParser analyzes with LLM
5. Orchestrator manages SQL generation
6. Real-time SSE events sent to frontend
7. Final SQL returned
```

### **Option B: Direct SQL Execution**

```
1. Frontend sends SQL + connection details
2. /run-sql-sse endpoint
3. Direct execution on Databricks
4. Results streamed back
```

---

## 📊 **AI Processing Pipeline**

### **Stage 1: Input Analysis**

- **File:** `ai_parser.py`
- **Function:** `parse_input()`
- **Purpose:** AI analyzes Excel text and extracts structured mapping
- **Output:** `ParsedMapping` object

### **Stage 2: Dependency Analysis**

- **File:** `dependency.py` (to be created)
- **Purpose:** Build dependency graph, detect cycles
- **SSE Events:** "analyzing dependencies...", "building execution order..."

### **Stage 3: SQL Construction**

- **File:** `builder.py` (to be created)
- **Purpose:** Build CTEs, JOINs, subqueries incrementally
- **SSE Events:** "adding CTE...", "building joins...", "adding attributes..."

### **Stage 4: Testing & Validation**

- **File:** `validator.py` (to be created)
- **Purpose:** Test each SQL component on Databricks
- **SSE Events:** "testing CTE...", "testing joins...", "validating final SQL..."

---

## 🎯 **Key Features**

### ✅ **Implemented**

- FastAPI REST API with CORS
- SSE streaming for real-time updates
- Databricks SQL execution (sync & async)
- AI-powered Excel data analysis
- Raw HTTP requests to OpenAI/Claude (no external SDKs)

### 🚧 **To Be Implemented**

- Dependency graph building (`dependency.py`)
- Incremental SQL building (`builder.py`)
- SQL component testing (`validator.py`)
- Cycle detection algorithms
- Advanced join optimization

---

## 🔌 **API Endpoints Reference**

| Endpoint                       | Method | Purpose                 | Input                | Output           |
| ------------------------------ | ------ | ----------------------- | -------------------- | ---------------- |
| `/`                            | GET    | Health check            | None                 | Welcome message  |
| `/test-sse`                    | GET    | SSE testing             | None                 | Test events      |
| `/run-sql`                     | POST   | Execute SQL             | SQL + connection     | JSON results     |
| `/run-sql-sse`                 | POST   | Execute SQL (streaming) | SQL + connection     | SSE events       |
| `/generate-sql-sse`            | POST   | AI SQL generation       | Raw mapping + AI key | SSE events + SQL |
| `/generate-sql-from-excel-sse` | POST   | Excel → SQL             | Excel data + AI key  | SSE events + SQL |

---

## 🛠️ **Development Workflow**

### **Adding New Features**

1. **Models:** Update `utils/models.py` for new data structures
2. **Processing:** Add logic to appropriate processor
3. **API:** Add/modify endpoints in `app/main.py`
4. **Testing:** Use `/test-sse` for SSE validation

### **Debugging SSE Issues**

1. Check server logs for connection attempts
2. Verify CORS configuration
3. Test with simple `/test-sse` endpoint first
4. Ensure proper event formatting

### **AI Integration**

1. Modify prompts in `ai_parser.py`
2. Update `ParsedMapping` structure for new fields
3. Test with various input formats
4. Add error handling for API failures

---

## 🔐 **Security Considerations**

- **API Keys:** Never log or expose AI API keys
- **SQL Injection:** AI generates SQL, validate before execution
- **CORS:** Restrict origins in production
- **Rate Limiting:** Add for AI API calls
- **Connection Details:** Validate Databricks credentials

---

## 📝 **Configuration**

### **Environment Variables**

```bash
# Optional - can be passed via request
OPENAI_API_KEY=your-key
CLAUDE_API_KEY=your-key

# Databricks (can be passed via request)
DATABRICKS_SERVER_HOSTNAME=your-host
DATABRICKS_HTTP_PATH=your-path
DATABRICKS_ACCESS_TOKEN=your-token
```

### **Dependencies**

```bash
pip install fastapi uvicorn databricks-sql-connector aiohttp sse-starlette
```

---

This architecture provides a flexible, AI-powered system that can handle unpredictable Excel mapping documents and generate optimized SQL with real-time feedback.
