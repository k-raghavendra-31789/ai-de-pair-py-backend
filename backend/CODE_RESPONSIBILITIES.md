# Code Responsibility Matrix

## 📋 **File-by-File Code Responsibilities**

### 🎯 **Core API** (`app/main.py`)

| Function/Class                  | Lines   | Responsibility                             |
| ------------------------------- | ------- | ------------------------------------------ |
| `app = FastAPI()`               | 14      | Main application instance                  |
| `CORSMiddleware`                | 16-22   | Handle cross-origin requests               |
| `SQLRequest`                    | 25-29   | Data model for basic SQL requests          |
| `run_sql_sse()`                 | 32-95   | Stream SQL execution with real-time events |
| `generate_sql_from_excel_sse()` | 98-130  | Process Excel data → AI → SQL generation   |
| `generate_sql_sse()`            | 133-150 | Generic AI SQL generation endpoint         |
| `read_root()`                   | 155     | Health check endpoint                      |
| `test_sse()`                    | 158-165 | SSE functionality testing                  |
| `run_sql()`                     | 168-183 | Basic SQL execution (non-streaming)        |

---

### 🏗️ **Data Models** (`utils/models.py`)

| Function/Class        | Responsibility                                         |
| --------------------- | ------------------------------------------------------ |
| `ExcelSheetData`      | Represents single Excel sheet data structure           |
| `ExcelMappingRequest` | Complete request format for Excel-based SQL generation |

---

### 📊 **Excel Processing** (`utils/sql_generator/excel_data_processor.py`)

| Function/Class               | Responsibility                                           |
| ---------------------------- | -------------------------------------------------------- |
| `ExcelDataProcessor`         | Main class for converting Excel data to AI-friendly text |
| `process_excel_request()`    | Convert ExcelMappingRequest to consolidated text         |
| `_process_sheet()`           | Analyze individual sheet content and structure           |
| `_analyze_table_structure()` | Identify table patterns, headers, column usage           |
| `_extract_all_text()`        | Extract and prioritize meaningful text content           |

---

### 🤖 **AI Processing** (`utils/sql_generator/ai_parser.py`)

| Function/Class             | Responsibility                                       |
| -------------------------- | ---------------------------------------------------- |
| `ParsedMapping`            | Data structure for AI-extracted mapping information  |
| `AIInputParser`            | Main AI processing class                             |
| `parse_input()`            | Orchestrate AI analysis of input data                |
| `_prepare_input()`         | Convert any input format to string for AI            |
| `_create_parsing_prompt()` | Generate comprehensive AI prompts for Excel analysis |
| `_call_openai()`           | Raw HTTP requests to OpenAI GPT-4 API                |
| `_call_claude()`           | Raw HTTP requests to Claude API                      |
| `_parse_ai_response()`     | Convert AI JSON response to ParsedMapping object     |
| `AIParser`                 | Context manager for cleaner AI parser usage          |

---

### 🎼 **Orchestration** (`utils/sql_generator/orchestrator.py`)

| Function/Class                                                                          | Responsibility                                        |
| --------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `SQLGenerationOrchestrator`                                                             | Coordinate entire AI → SQL generation pipeline        |
| `generate_sql_with_events()`                                                            | Main method that streams SSE events during generation |
| **Note:** This class will coordinate future components (dependency, builder, validator) |

---

### 🔗 **Database Operations** (`utils/db_utils.py`)

| Function/Class                 | Responsibility                                     |
| ------------------------------ | -------------------------------------------------- |
| `execute_sql_async()`          | Async SQL execution with timeout handling          |
| `validate_connection_params()` | Validate required Databricks connection parameters |
| `format_row_data()`            | Convert database rows to dictionary format         |

---

### 📡 **SSE Utilities** (`utils/sse_utils.py`)

| Function/Class          | Responsibility                       |
| ----------------------- | ------------------------------------ |
| `create_sse_event()`    | Format events for Server-Sent Events |
| `stream_status_event()` | Helper for status events             |
| `stream_error_event()`  | Helper for error events              |
| `stream_data_event()`   | Helper for data events               |
| `stream_close_event()`  | Helper for close events              |

---

## 🔄 **Data Flow by Function**

### **Excel → SQL Generation Flow**

```
1. main.py:generate_sql_from_excel_sse()
   ↓
2. excel_data_processor.py:process_excel_request()
   ↓
3. ai_parser.py:parse_input()
   ↓
4. orchestrator.py:generate_sql_with_events()
   ↓
5. [Future: dependency.py, builder.py, validator.py]
   ↓
6. db_utils.py:execute_sql_async() [for testing]
```

### **Direct SQL Execution Flow**

```
1. main.py:run_sql_sse()
   ↓
2. db_utils.py:execute_sql_async()
   ↓
3. sse_utils.py:stream_*_event() [for formatting]
```

---

## 🛠️ **Component Status**

### ✅ **Fully Implemented**

- **API Layer** (`main.py`) - All endpoints working
- **Excel Processing** (`excel_data_processor.py`) - Complete
- **AI Integration** (`ai_parser.py`) - OpenAI & Claude support
- **Database Utils** (`db_utils.py`) - Async SQL execution
- **SSE Utils** (`sse_utils.py`) - Event formatting
- **Data Models** (`models.py`) - Request structures

### 🚧 **Planned/Stub Implementation**

- **Orchestrator** (`orchestrator.py`) - Basic structure, needs full pipeline
- **Dependency Analysis** (`dependency.py`) - Not yet created
- **SQL Builder** (`builder.py`) - Not yet created
- **SQL Validator** (`validator.py`) - Not yet created

---

## 🎯 **Key Responsibilities by Concern**

### **HTTP/API Handling**

- **File:** `main.py`
- **Functions:** All endpoint functions
- **Purpose:** Request routing, response formatting, error handling

### **Data Transformation**

- **File:** `excel_data_processor.py`
- **Functions:** `process_excel_request()`, `_process_sheet()`
- **Purpose:** Convert Excel data to AI-analyzable text

### **AI Integration**

- **File:** `ai_parser.py`
- **Functions:** `parse_input()`, `_call_openai()`, `_call_claude()`
- **Purpose:** Interface with AI APIs, prompt engineering

### **Database Operations**

- **File:** `db_utils.py`
- **Functions:** `execute_sql_async()`, `validate_connection_params()`
- **Purpose:** Databricks connectivity and SQL execution

### **Real-time Communication**

- **File:** `sse_utils.py` + SSE parts of `main.py`
- **Functions:** Event generators, SSE formatters
- **Purpose:** Stream progress updates to frontend

### **Business Logic Coordination**

- **File:** `orchestrator.py`
- **Functions:** `generate_sql_with_events()`
- **Purpose:** Coordinate AI → dependency → SQL → testing pipeline

---

## 🔍 **Error Handling Responsibilities**

### **API Level** (`main.py`)

- HTTP status codes
- Request validation
- Exception catching and formatting

### **AI Level** (`ai_parser.py`)

- API key validation
- Network error handling
- JSON parsing errors
- AI response validation

### **Database Level** (`db_utils.py`)

- Connection timeouts
- SQL execution errors
- Result formatting errors

### **Processing Level** (`excel_data_processor.py`)

- Invalid Excel data handling
- Missing sheet handling
- Data type conversion errors
