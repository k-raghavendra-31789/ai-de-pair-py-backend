# API Endpoint Documentation

## 1. Health Check

**GET /**

- **Description:** Returns a welcome message to verify the backend is running.
- **Response Example:**
  ```json
  { "message": "Welcome to the AI Backend!" }
  ```

---

## 2. Run SQL on Databricks

**POST /run-sql**

- **Description:** Executes a SQL query on a Databricks SQL warehouse using provided connection details.
- **Request Body:**
  ```json
  {
    "sql": "SELECT * FROM your_table",
    "server_hostname": "<databricks-server-hostname>",
    "http_path": "<databricks-http-path>",
    "access_token": "<databricks-access-token>"
  }
  ```
- **Response Example:**
  ```json
  {
    "results": [
      { "column1": "value1", "column2": "value2" },
      { "column1": "value3", "column2": "value4" }
    ]
  }
  ```

---

## 3. Run SQL with SSE Streaming

**POST /run-sql-sse**

- **Description:** Executes a SQL query with Server-Sent Events streaming for real-time progress.
- **Request Body:** Same as `/run-sql`
- **Response:** SSE stream with events like "status", "data", "columns", "close"

---

## 4. AI-Powered SQL Generation (NEW!)

**POST /generate-sql-sse**

- **Description:** Generates SQL from flexible mapping input using AI, with full process streaming via SSE.
- **Request Body:**

  ```json
  {
    "mapping_input": {
      "description": "Join customers with orders and calculate total sales",
      "tables": ["customers", "orders", "order_items"],
      "output": ["customer_name", "total_sales"]
    },
    "connection_details": {
      "server_hostname": "<databricks-server-hostname>",
      "http_path": "<databricks-http-path>",
      "access_token": "<databricks-access-token>"
    },
    "ai_api_key": "<openai-or-claude-api-key>",
    "ai_provider": "openai"
  }
  ```

- **SSE Events Streamed:**
  - `🤖 Starting AI analysis...`
  - `🔍 Analyzing input structure...`
  - `✅ AI analysis complete - found X tables`
  - `🔗 Building dependency graph...`
  - `🔄 Checking for cyclic references...`
  - `📋 Creating execution order...`
  - `📝 Building CTEs...`
  - `🔗 Building JOIN sections...`
  - `📊 Adding output attributes...`
  - `🔧 Constructing final SQL...`
  - `🧪 Testing final SQL...`
  - `✅ SQL generation completed!`
  - Final `sql_generated` event with complete SQL

---

## 5. Test SSE Endpoint

**GET /test-sse**

- **Description:** Simple SSE test endpoint for debugging SSE functionality.
- **Response:** 5 test events followed by close event.

---

## Security Notes

- Never expose or log sensitive connection details or AI API keys
- Restrict CORS and add authentication in production
- Only allow trusted users to access AI-powered endpoints
- Monitor AI API usage and costs
