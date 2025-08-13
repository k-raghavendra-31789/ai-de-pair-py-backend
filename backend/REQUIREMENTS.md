# AI-DE Pair Backend Requirements Documentation

## 📋 **Detailed Requirements Analysis**

---

## 1. **Input Format & Structure**

### 📊 **Excel Mapping Document Characteristics**

#### **Core Challenge: Unpredictable Structure**

- **No standardized format** - Each Excel file can have completely different layouts
- **Vague instructions** - Business users provide informal, incomplete guidance
- **Random sheet organization** - Information scattered across multiple sheets without logical order
- **Mixed content types** - Text descriptions, partial tables, bullet points, free-form notes

#### **Typical Content (Expected but not guaranteed)**

- **Transformation logic** - How to derive target table attributes from source data
- **Join instructions** - Vague descriptions of how tables should be connected
- **Business rules** - Informal descriptions of data processing requirements
- **Target schema hints** - Partial information about desired output structure

#### **Example Content Patterns (Highly Variable)**

```
Sheet 1: "Instructions"
- "Get customer data from main table"
- "Join with orders somehow"
- "Calculate total sales per customer"

Sheet 2: "Field Mapping"
- Source: customer_id → Target: cust_id
- Source: order_date → Target: order_dt (format YYYY-MM-DD)

Sheet 3: "Business Logic"
- "Only include active customers"
- "Exclude test accounts"
- "Sales amounts should be in USD"

Sheet 4: Random notes, comments, incomplete thoughts...
```

#### **AI Processing Implications**

- **Maximum flexibility required** - Can't assume any specific structure
- **Context inference critical** - AI must understand implicit relationships
- **Gap-filling essential** - AI needs to infer missing technical details
- **Natural language processing** - Must interpret business language

#### **Technical Requirements for Input Handler**

1. **Universal parsing** - Handle any Excel structure
2. **Content extraction** - Pull meaningful text from various cell types
3. **Pattern recognition** - Identify potential tables, lists, mappings
4. **Context preservation** - Maintain relationships between scattered information
5. **Text normalization** - Convert various formats to AI-analyzable text

#### **Expected Input Variability**

- **Structure:** Tables, lists, paragraphs, mixed layouts
- **Language:** Business terms, technical jargon, informal notes
- **Completeness:** Partial specs, missing details, contradictory info
- **Organization:** Random order, no logical flow, cross-sheet references

#### **AI Prompt Strategy for This Input Type**

```
"You are analyzing an unpredictable Excel mapping document. The content is:
- Vague and incomplete
- Scattered across multiple sheets
- Contains informal business language
- May have contradictory or missing information
- Requires significant inference and gap-filling

Your job is to extract whatever meaningful mapping information exists and
infer reasonable defaults for missing pieces."
```

#### **Success Criteria for Input Processing**

- ✅ **Robustness** - Never fail due to unexpected format
- ✅ **Information extraction** - Find useful content regardless of location
- ✅ **Context building** - Connect related information across sheets
- ✅ **Graceful degradation** - Provide best effort even with minimal input

---

**Status:** ✅ **DOCUMENTED** - Ready for implementation validation

**Next:** Continue with point 2 - SQL Generation Requirements

---

## 2. **SQL Generation Requirements**

### 🎯 **Complexity Level: EXTREME**

#### **Expected SQL Complexity Characteristics**

- **Maximum complexity anticipated** - No upper limit on query sophistication
- **Multi-layered transformations** - Complex business logic with nested calculations
- **Advanced SQL features** - CTEs, window functions, recursive queries, advanced joins
- **Performance-critical** - Queries may process large datasets requiring optimization

#### **Multi-Step Pipeline Definition & Clarification**

**Question:** "What do you mean by multi-step pipeline?"

**Possible Interpretations:**

**Option A: Single Complex Query**

```sql
-- One massive query with multiple CTEs
WITH step1_data AS (
  -- Complex transformation 1
),
step2_calculations AS (
  -- Complex transformation 2 using step1
),
final_result AS (
  -- Final aggregation using step2
)
SELECT * FROM final_result
```

**Option B: Multiple Sequential Queries**

```sql
-- Query 1: Create temporary/staging table
CREATE OR REPLACE TABLE temp_step1 AS ...

-- Query 2: Transform and create next stage
CREATE OR REPLACE TABLE temp_step2 AS ...

-- Query 3: Final result query
SELECT * FROM temp_step2 WHERE ...
```

**Option C: Stored Procedure/Script**

```sql
-- Multi-statement execution block
BEGIN
  -- Statement 1
  -- Statement 2
  -- Statement 3
END
```

#### **Clarification Needed:**

- **Single complex query with CTEs** vs **Multiple separate queries**?
- **Temporary tables** allowed/preferred?
- **Transaction boundaries** - Should everything be atomic?
- **Intermediate result storage** - Memory vs persistent tables?

#### **Extreme Complexity Implications**

**Technical Requirements:**

- **Advanced SQL generation** - Beyond basic SELECT/JOIN
- **Query optimization** - Performance considerations for complex queries
- **Dependency management** - Complex relationships between query components
- **Memory management** - Large intermediate result sets
- **Error isolation** - Identify which part of complex query fails

**AI Processing Requirements:**

- **Sophisticated SQL knowledge** - AI must understand advanced SQL patterns
- **Performance awareness** - AI should consider query efficiency
- **Optimization strategies** - AI may need to suggest performance improvements
- **Alternative approaches** - AI should offer different SQL strategies

#### **Architecture Impact**

- **Enhanced SQL builder** - Must handle extreme complexity
- **Advanced testing** - Each component needs thorough validation
- **Performance monitoring** - Track execution time and resource usage
- **Rollback capabilities** - Ability to revert partial failures

#### **DECISION: Mix of Both Approaches + Environment Adaptability**

**Core Requirement:**

- **User preference driven** - Allow users to specify their preferred approach
- **Environment adaptability** - Support different database/warehouse capabilities
- **Syntax flexibility** - Handle varying temporary table/view syntax across platforms

**Supported Patterns:**

**Pattern 1: Single Complex Query (Default)**

```sql
WITH step1 AS (...), step2 AS (...), step3 AS (...)
SELECT * FROM step3
```

**Pattern 2: Multiple Queries with Temporary Views**

```sql
-- Databricks syntax
CREATE OR REPLACE TEMPORARY VIEW temp_step1 AS ...;
CREATE OR REPLACE TEMPORARY VIEW temp_step2 AS ...;
```

**Pattern 3: Multiple Queries with Temporary Tables**

```sql
-- Alternative syntax for environments that don't support temp views
CREATE TEMPORARY TABLE temp_step1 AS ...;
CREATE TEMPORARY TABLE temp_step2 AS ...;
```

**Pattern 4: Environment-Specific Adaptations**

- **Snowflake:** Different temp table syntax
- **BigQuery:** Different temporary dataset approach
- **Databricks:** Native temp view support
- **PostgreSQL:** Different temp table creation

#### **Technical Implementation Requirements**

**AI Decision Engine:**

- **User preference detection** - Parse Excel for user's preferred approach
- **Environment detection** - Identify target database capabilities
- **Complexity assessment** - Determine optimal approach based on query complexity
- **Fallback strategies** - Provide alternatives when preferred approach isn't feasible

**SQL Generation Flexibility:**

- **Template-based generation** - Support multiple SQL patterns
- **Syntax adaptation** - Adjust syntax based on target environment
- **Performance optimization** - Choose approach based on expected performance
- **Testing compatibility** - Ensure each approach can be validated

**Configuration Options:**

```json
{
  "sql_generation_preference": "single_query|multi_query|auto",
  "target_environment": "databricks|snowflake|bigquery|postgresql",
  "temp_object_syntax": "temp_view|temp_table|cte_only",
  "performance_priority": "readability|performance|memory_efficient"
}
```

**SSE Event Implications:**

- **Pattern detection** - "analyzing complexity, choosing generation approach..."
- **Environment adaptation** - "adapting SQL for Databricks environment..."
- **Multi-query coordination** - "building query 1 of 3...", "testing query dependencies..."
- **Approach switching** - "single query too complex, switching to multi-query approach..."

---

**Status:** ✅ **DOCUMENTED** - Flexible approach with environment adaptability

**Implementation Impact:**

- **SQL Builder** must support multiple generation patterns
- **AI Parser** needs to detect user preferences and environment constraints
- **Testing Framework** must validate different SQL approaches
- **Orchestrator** coordinates between single/multi-query strategies

---

## 3. **AI Processing Expectations**

### 🎯 **Three-Tier AI Intelligence System**

**Core Principle:** User-selectable AI behavior based on use case and risk tolerance

#### **Option 1: Conservative Generation (High Confidence Only)**

**Behavior:**

- **No gap-filling** - AI only generates what it's highly confident about
- **Explicit commenting** - Leave detailed comments for missing/uncertain elements
- **Documentation focus** - Prioritize clear explanations over complete implementation
- **Risk-averse** - Prefer incomplete but accurate over complete but potentially wrong

**Example Output:**

```sql
-- Customer base query - VERIFIED from mapping
SELECT
  customer_id,
  customer_name
  -- TODO: Missing join condition to orders table
  -- Excel mentions "connect with orders" but no specific field mapping provided
  -- SUGGESTION: Likely customer_id = orders.customer_id but needs confirmation
FROM customers c
-- WHERE clause incomplete - Excel mentions "active customers only"
-- TODO: Define "active" criteria (status field? date range? transaction history?)
```

**Use Case:**

- **High-stakes environments** where errors are costly
- **Audit/compliance requirements** where AI decisions must be explainable
- **Learning scenarios** where users want to understand the gaps

#### **Option 2: Batch Processing with Incremental Validation**

**Behavior:**

- **Chunked generation** - Build SQL components in logical batches
- **Progressive validation** - Test each batch before proceeding
- **Iterative refinement** - Adjust approach based on batch results
- **Balanced risk** - Fill reasonable gaps but validate frequently

**Processing Flow:**

```
Batch 1: Base table selection + basic filters
  → Validate on database
  → SSE: "batch 1 validated, 50 rows returned"

Batch 2: Add first level joins
  → Validate joins don't explode data
  → SSE: "batch 2 validated, join ratio 1:1.2 acceptable"

Batch 3: Add transformations and calculations
  → Validate logic produces expected ranges
  → SSE: "batch 3 validated, calculations within expected bounds"

Batch 4: Final aggregations and output formatting
  → Full validation
  → SSE: "final query validated, ready for use"
```

**Use Case:**

- **Production environments** with some risk tolerance
- **Complex queries** where full validation is expensive
- **Iterative development** workflows

#### **Option 3: Aggressive AI with Self-Correction (Maximum Intelligence)**

**Behavior:**

- **Full gap-filling** - AI makes intelligent assumptions for missing information
- **Metadata-driven validation** - Use database schema to verify assumptions
- **Self-correction loops** - Retry with different approaches when validation fails
- **Adaptive learning** - Adjust strategy based on validation results
- **Comprehensive optimization** - Performance tuning based on actual table metadata

**Advanced Features:**

```
Intelligent Gap-Filling:
- Infer join conditions from foreign key relationships
- Auto-correct column name misspellings using fuzzy matching
- Suggest data type conversions based on schema analysis
- Optimize join order using table statistics

Self-Correction Process:
1. Generate initial SQL
2. Validate against schema → Fix column/table name issues
3. Execute sample query → Analyze performance/results
4. Detect issues (performance, data explosion, etc.)
5. Retry with alternative approach
6. Repeat up to N iterations
7. If still failing, add detailed comment explaining attempts
```

**Validation Layers:**

- **Schema validation** - Verify tables/columns exist
- **Data type compatibility** - Check join field types match
- **Performance analysis** - Estimate query cost, suggest optimizations
- **Result reasonableness** - Check output ranges, row counts, null percentages
- **Spelling correction** - Fix common field name typos using Levenshtein distance

**Use Case:**

- **Rapid prototyping** environments
- **Expert users** who can handle AI mistakes
- **Learning systems** where AI improves over time

#### **Clarification and Iteration Protocol**

**Principle:** AI asks questions ONLY after attempting SQL generation and validation

**Process:**

1. **Initial generation** - AI creates best-effort SQL with chosen intelligence level
2. **Validation execution** - Run SQL and analyze results
3. **Issue identification** - Detect problems through validation
4. **Iterative questioning** - Ask specific, informed questions based on actual issues

**Example Iteration:**

```
Iteration 1: AI generates SQL
→ Validation fails: "Join produces 10M rows from 1K input"
→ AI question: "The join between customers and orders is producing excessive rows.
   Should this be: a) One order per customer (LEFT JOIN with row_number),
   b) All orders per customer (current INNER JOIN is correct),
   c) Latest order per customer (JOIN with MAX date filter)?"

Iteration 2: User provides feedback
→ AI regenerates with specific guidance
→ Validation succeeds
```

**No Upfront Questions:** AI never asks "What should I do?" without first attempting and learning from failures.

#### **Configuration Selection**

**User Interface Options:**

```json
{
  "ai_intelligence_level": "conservative|balanced|aggressive",
  "retry_attempts": 3,
  "validation_strictness": "basic|standard|comprehensive",
  "question_threshold": "never|after_failure|after_multiple_failures",
  "optimization_level": "none|basic|aggressive"
}
```

---

**Status:** ✅ **DOCUMENTED** - Three-tier AI system with iterative feedback

**Implementation Requirements:**

- **Mode selector** in AI parser for different intelligence levels
- **Validation engine** with increasing sophistication levels
- **Retry mechanism** with learning from failures
- **Question generation** system for post-validation clarification
- **Metadata integration** for schema-aware validation

---

## 4. **SSE Event Requirements**

### 🎯 **Grouped Event System with Section Markers**

**Core Principle:** Events are grouped by processing phase with clear section markers for frontend UI organization

#### **Event Structure Format**

```json
{
  "event": "progress",
  "data": {
    "section": "dependency_analysis|joins|attributes|validation|completion",
    "phase": "start|progress|retry|complete|error",
    "message": "Human readable description",
    "details": {
      "current_item": "specific item being processed",
      "progress": "2/5",
      "retry_count": 1,
      "validation_status": "passed|failed|pending"
    },
    "timestamp": "ISO-8601"
  }
}
```

#### **Processing Sections with Events**

### **Section 1: Initial Analysis**

```json
{"event": "progress", "data": {"section": "analysis", "phase": "start", "message": "analyzing mapping document"}}
{"event": "progress", "data": {"section": "analysis", "phase": "progress", "message": "extracting table information"}}
{"event": "progress", "data": {"section": "analysis", "phase": "progress", "message": "identifying relationships"}}
{"event": "progress", "data": {"section": "analysis", "phase": "complete", "message": "analysis complete: 5 tables, 8 relationships found"}}
```

### **Section 2: Dependency Analysis**

```json
{"event": "progress", "data": {"section": "dependency", "phase": "start", "message": "building dependency graph"}}
{"event": "progress", "data": {"section": "dependency", "phase": "progress", "message": "analyzing table dependencies", "details": {"current_item": "customers -> orders"}}}
{"event": "progress", "data": {"section": "dependency", "phase": "progress", "message": "checking for cyclic references"}}
{"event": "progress", "data": {"section": "dependency", "phase": "complete", "message": "dependency graph built: 5 levels, no cycles detected"}}
```

### **Section 3: Join Construction**

```json
{"event": "progress", "data": {"section": "joins", "phase": "start", "message": "building join section"}}
{"event": "progress", "data": {"section": "joins", "phase": "progress", "message": "adding LEFT JOIN", "details": {"current_item": "customers LEFT JOIN orders ON c.id = o.customer_id", "progress": "1/4"}}}
{"event": "progress", "data": {"section": "joins", "phase": "progress", "message": "testing join performance", "details": {"current_item": "customers-orders join", "validation_status": "pending"}}}
{"event": "progress", "data": {"section": "joins", "phase": "retry", "message": "join validation failed, retrying with different approach", "details": {"retry_count": 1, "current_item": "customers-orders"}}}
{"event": "progress", "data": {"section": "joins", "phase": "progress", "message": "adding INNER JOIN", "details": {"current_item": "orders INNER JOIN products ON o.product_id = p.id", "progress": "2/4"}}}
{"event": "progress", "data": {"section": "joins", "phase": "complete", "message": "all joins completed and validated", "details": {"progress": "4/4"}}}
```

### **Section 4: CTE Construction**

```json
{"event": "progress", "data": {"section": "cte", "phase": "start", "message": "building common table expressions"}}
{"event": "progress", "data": {"section": "cte", "phase": "progress", "message": "creating CTE: customer_base", "details": {"current_item": "customer filtering logic"}}}
{"event": "progress", "data": {"section": "cte", "phase": "progress", "message": "testing CTE: customer_base", "details": {"validation_status": "passed", "rows_returned": 1250}}}
{"event": "progress", "data": {"section": "cte", "phase": "progress", "message": "creating CTE: order_aggregations", "details": {"current_item": "rolling calculations"}}}
{"event": "progress", "data": {"section": "cte", "phase": "complete", "message": "all CTEs created and validated"}}
```

### **Section 5: Attribute Generation**

```json
{"event": "progress", "data": {"section": "attributes", "phase": "start", "message": "generating output attributes"}}
{"event": "progress", "data": {"section": "attributes", "phase": "progress", "message": "adding attribute: customer_name", "details": {"current_item": "customer_name", "progress": "1/8"}}}
{"event": "progress", "data": {"section": "attributes", "phase": "progress", "message": "adding calculated attribute: lifetime_value", "details": {"current_item": "SUM(order_amount) calculation", "progress": "2/8"}}}
{"event": "progress", "data": {"section": "attributes", "phase": "retry", "message": "attribute validation failed, adjusting data type", "details": {"current_item": "lifetime_value", "retry_count": 1}}}
{"event": "progress", "data": {"section": "attributes", "phase": "complete", "message": "all attributes generated", "details": {"progress": "8/8"}}}
```

### **Section 6: Final Validation**

```json
{"event": "progress", "data": {"section": "validation", "phase": "start", "message": "validating complete SQL"}}
{"event": "progress", "data": {"section": "validation", "phase": "progress", "message": "syntax validation passed"}}
{"event": "progress", "data": {"section": "validation", "phase": "progress", "message": "performance analysis", "details": {"estimated_cost": "medium", "row_estimate": 5000}}}
{"event": "progress", "data": {"section": "validation", "phase": "progress", "message": "executing test query", "details": {"sample_size": 100}}}
{"event": "progress", "data": {"section": "validation", "phase": "complete", "message": "full validation passed"}}
```

### **Section 7: Completion**

```json
{"event": "progress", "data": {"section": "completion", "phase": "complete", "message": "SQL generation completed successfully"}}
{"event": "sql_result", "data": {"final_sql": "WITH customer_base AS (...) SELECT ...", "metadata": {"total_time": "45s", "complexity": "high"}}}
```

#### **Frontend UI Grouping**

**Chat Interface Organization:**

```
📊 Analysis Phase
  ✓ Analyzing mapping document
  ✓ Extracting table information
  ✓ Analysis complete: 5 tables, 8 relationships found

🔗 Dependency Analysis
  ✓ Building dependency graph
  ✓ No cycles detected

🔀 Join Construction
  ⏳ Adding LEFT JOIN: customers-orders (1/4)
  ⚠️ Join validation failed, retrying...
  ✓ All joins completed (4/4)

📝 Attribute Generation
  ⏳ Adding calculated attribute: lifetime_value (2/8)

✅ Validation & Completion
  ⏳ Executing test query...
```

#### **Event Intelligence Level Variations**

**Conservative Mode - More Comments:**

```json
{
  "event": "progress",
  "data": {
    "section": "joins",
    "phase": "progress",
    "message": "insufficient information for join condition",
    "details": {
      "current_item": "customers-orders",
      "comment_added": "TODO: Specify join condition"
    }
  }
}
```

**Aggressive Mode - More Retries:**

```json
{
  "event": "progress",
  "data": {
    "section": "joins",
    "phase": "retry",
    "message": "optimizing join order based on table statistics",
    "details": {
      "retry_count": 2,
      "optimization": "moved smaller table to left side"
    }
  }
}
```

#### **Error Handling Events**

```json
{
  "event": "error",
  "data": {
    "section": "joins",
    "message": "fatal join error after 3 retries",
    "details": {
      "last_error": "column 'customer_id' not found",
      "suggestions": ["check column spelling", "verify table schema"]
    }
  }
}
```

---

**Status:** ✅ **DOCUMENTED** - Structured event system with section grouping

**Frontend Implementation Requirements:**

- **Section-based UI grouping** for organized progress display
- **Phase indicators** (start/progress/retry/complete/error)
- **Progress tracking** within each section
- **Retry visualization** for aggressive mode
- **Expandable details** for technical information

---

## 5. **Environment Adaptability Requirements**

### 🎯 **Multi-Database SQL Generation**

**Core Principle:** Generate SQL that works optimally in the target database environment while maintaining logical equivalence

#### **Supported Database Environments**

### **Primary Target: Databricks SQL**

```sql
-- Databricks-specific optimizations
WITH customer_summary AS (
  SELECT
    customer_id,
    SUM(order_amount) as lifetime_value,
    COUNT(*) as order_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_amount) as median_order
  FROM orders
  WHERE order_date >= CURRENT_DATE() - INTERVAL 365 DAYS
  GROUP BY customer_id
  CLUSTER BY customer_id  -- Databricks optimization
)
SELECT * FROM customer_summary
```

### **Secondary Targets: PostgreSQL, MySQL, BigQuery**

```sql
-- PostgreSQL equivalent
WITH customer_summary AS (
  SELECT
    customer_id,
    SUM(order_amount) as lifetime_value,
    COUNT(*) as order_count,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_amount) as median_order
  FROM orders
  WHERE order_date >= CURRENT_DATE - INTERVAL '365 days'
  GROUP BY customer_id
)
SELECT * FROM customer_summary;
```

#### **Environment-Specific Adaptations**

### **🔧 Syntax Adaptations**

**Date Functions:**

```json
{
  "databricks": "CURRENT_DATE() - INTERVAL 365 DAYS",
  "postgresql": "CURRENT_DATE - INTERVAL '365 days'",
  "mysql": "DATE_SUB(CURDATE(), INTERVAL 365 DAY)",
  "bigquery": "DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)"
}
```

**String Functions:**

```json
{
  "databricks": "CONCAT(first_name, ' ', last_name)",
  "postgresql": "first_name || ' ' || last_name",
  "mysql": "CONCAT(first_name, ' ', last_name)",
  "bigquery": "CONCAT(first_name, ' ', last_name)"
}
```

**Window Functions:**

```json
{
  "databricks": "ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)",
  "postgresql": "ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)",
  "mysql": "ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)",
  "bigquery": "ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date)"
}
```

### **⚡ Performance Optimizations**

**Databricks Optimizations:**

```sql
-- Use Delta Lake optimizations
SELECT /*+ BROADCAST(small_table) */
  large_table.customer_id,
  small_table.category_name
FROM large_table
JOIN small_table ON large_table.category_id = small_table.id
CLUSTER BY customer_id;
```

**PostgreSQL Optimizations:**

```sql
-- Use appropriate indexes and partitioning
SELECT
  customer_id,
  category_name
FROM large_table
JOIN small_table ON large_table.category_id = small_table.id
WHERE large_table.created_date >= '2024-01-01'::date;
```

**BigQuery Optimizations:**

```sql
-- Use partitioning and clustering
SELECT
  customer_id,
  category_name
FROM `project.dataset.large_table`
JOIN `project.dataset.small_table`
ON large_table.category_id = small_table.id
WHERE _PARTITIONTIME >= TIMESTAMP('2024-01-01');
```

#### **🎛️ Environment Detection & Selection**

### **Automatic Detection Strategy**

```python
# Environment detection logic
environment_patterns = {
    "databricks": {
        "indicators": ["CLUSTER BY", "DELTA", "BROADCAST hint"],
        "connection_string": "databricks+connector://",
        "default_schema": "default"
    },
    "postgresql": {
        "indicators": ["::date", "||", "INTERVAL '"],
        "connection_string": "postgresql://",
        "default_schema": "public"
    },
    "bigquery": {
        "indicators": ["`project.dataset`", "_PARTITIONTIME"],
        "connection_string": "bigquery://",
        "default_schema": None
    }
}
```

### **Manual Override Capability**

```json
{
  "request": {
    "excel_data": "...",
    "target_environment": "databricks", // Override detection
    "optimization_level": "high", // performance vs compatibility
    "custom_functions": {
      // Environment-specific functions
      "date_diff": "DATEDIFF(day, start_date, end_date)"
    }
  }
}
```

#### **🔄 Environment-Adaptive AI Prompts**

### **Databricks-Specific AI Instructions**

```
ENVIRONMENT: Databricks SQL Warehouse
OPTIMIZATIONS: Use CLUSTER BY for large result sets, BROADCAST hints for small tables
SYNTAX: Use CURRENT_DATE(), INTERVAL syntax, Delta Lake features when beneficial
LIMITS: Avoid MySQL-specific functions, prefer Spark SQL standards
```

### **PostgreSQL-Specific AI Instructions**

```
ENVIRONMENT: PostgreSQL Database
OPTIMIZATIONS: Use appropriate indexes, consider partitioning for large tables
SYNTAX: Use PostgreSQL date operators (::date), string concatenation (||)
LIMITS: Avoid proprietary functions, stick to ANSI SQL when possible
```

#### **📊 Compatibility Matrix**

### **Feature Support by Environment**

```json
{
  "window_functions": {
    "databricks": "full_support",
    "postgresql": "full_support",
    "mysql": "limited_support",
    "bigquery": "full_support"
  },
  "cte_recursive": {
    "databricks": "supported",
    "postgresql": "supported",
    "mysql": "mysql_8+",
    "bigquery": "supported"
  },
  "json_functions": {
    "databricks": "spark_json",
    "postgresql": "native_json",
    "mysql": "mysql_5.7+",
    "bigquery": "native_json"
  }
}
```

#### **🔄 Cross-Environment Translation**

### **Translation Pipeline**

```python
class EnvironmentTranslator:
    def translate_sql(self, sql: str, source_env: str, target_env: str):
        """
        Convert SQL from one environment to another
        - Parse SQL into abstract syntax tree
        - Apply environment-specific transformations
        - Regenerate SQL for target environment
        """

    def validate_compatibility(self, sql: str, target_env: str):
        """
        Check if SQL features are supported in target environment
        - Identify unsupported functions
        - Suggest alternatives
        - Flag potential performance issues
        """
```

### **Real-Time Environment Switching**

```json
{
  "event": "progress",
  "data": {
    "section": "environment_adaptation",
    "phase": "progress",
    "message": "adapting SQL for Databricks environment",
    "details": {
      "source_environment": "generic",
      "target_environment": "databricks",
      "adaptations": [
        "converted DATE_SUB to INTERVAL syntax",
        "added CLUSTER BY optimization",
        "applied BROADCAST hint for small table"
      ]
    }
  }
}
```

#### **⚙️ Configuration Management**

### **Environment Profiles**

```json
{
  "environments": {
    "databricks_production": {
      "type": "databricks",
      "optimization_level": "high",
      "max_query_complexity": "unlimited",
      "preferred_join_types": ["broadcast", "sort_merge"],
      "custom_settings": {
        "spark.sql.adaptive.enabled": true,
        "spark.sql.adaptive.coalescePartitions.enabled": true
      }
    },
    "postgresql_dev": {
      "type": "postgresql",
      "optimization_level": "medium",
      "max_query_complexity": "medium",
      "preferred_join_types": ["hash", "nested_loop"],
      "version": "14.0"
    }
  }
}
```

### **Dynamic Environment Selection**

```python
# Based on connection parameters
def detect_environment(connection_string: str, query_hints: dict) -> str:
    if "databricks" in connection_string:
        return "databricks"
    elif "postgresql" in connection_string:
        return "postgresql"
    elif query_hints.get("use_bigquery_syntax"):
        return "bigquery"
    else:
        return "generic_sql"
```

---

**Status:** ✅ **DOCUMENTED** - Multi-environment SQL generation with automatic adaptation

**Key Capabilities:**

- **Automatic environment detection** from connection strings and context
- **Syntax translation** between database dialects
- **Performance optimization** per environment
- **Compatibility validation** and alternative suggestions
- **Real-time environment switching** during generation

---

## 6. **Performance Requirements**

### 🎯 **Response Time Targets**

**Core Principle:** Balance speed with accuracy while handling external API limitations gracefully

#### **Target Response Times**

### **🚀 Processing Speed Targets**

```json
{
  "simple_queries": {
    "target": "15-30 seconds",
    "description": "Single table with basic filters",
    "ai_calls": "1-2 API calls"
  },
  "medium_queries": {
    "target": "45-90 seconds",
    "description": "2-4 tables with joins and calculations",
    "ai_calls": "3-5 API calls"
  },
  "complex_queries": {
    "target": "2-4 minutes",
    "description": "5+ tables with CTEs, window functions",
    "ai_calls": "6-12 API calls"
  },
  "maximum_timeout": {
    "target": "10 minutes",
    "description": "Absolute limit before giving up",
    "fallback": "Return partial results with comments"
  }
}
```

#### **🔄 AI Rate Limit Management**

### **Rate Limit Specifications**

```json
{
  "openai_gpt4": {
    "requests_per_minute": 60,
    "tokens_per_minute": 150000,
    "daily_limit": 500000,
    "retry_strategy": "exponential_backoff"
  },
  "claude_anthropic": {
    "requests_per_minute": 50,
    "tokens_per_minute": 100000,
    "daily_limit": 300000,
    "retry_strategy": "exponential_backoff"
  }
}
```

### **⚡ Intelligent Retry Mechanism**

**Exponential Backoff Strategy:**

```python
class AIRateLimitHandler:
    def __init__(self):
        self.base_delay = 1.0  # Start with 1 second
        self.max_delay = 300.0  # Max 5 minutes
        self.backoff_factor = 2.0
        self.jitter = True  # Add randomness

    async def retry_with_backoff(self, api_call, max_retries=5):
        """
        Retry API calls with exponential backoff
        """
        for attempt in range(max_retries):
            try:
                return await api_call()
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    raise

                delay = min(
                    self.base_delay * (self.backoff_factor ** attempt),
                    self.max_delay
                )

                if self.jitter:
                    delay *= (0.5 + random.random() * 0.5)

                # Send SSE update about retry
                await self.send_retry_event(attempt + 1, delay, str(e))
                await asyncio.sleep(delay)
```

### **🔀 Multi-Provider Failover**

**Provider Switching Logic:**

```python
class AIProviderManager:
    def __init__(self):
        self.providers = ["openai", "claude"]
        self.current_provider = 0
        self.provider_cooldowns = {}

    async def get_ai_response(self, prompt: str):
        """
        Try providers in order, switch on rate limits
        """
        for _ in range(len(self.providers)):
            provider = self.providers[self.current_provider]

            # Check if provider is in cooldown
            if self.is_in_cooldown(provider):
                self.switch_provider()
                continue

            try:
                response = await self.call_provider(provider, prompt)
                return response

            except RateLimitError:
                # Put provider in cooldown
                self.set_cooldown(provider, 300)  # 5 minutes
                await self.send_failover_event(provider)
                self.switch_provider()

        raise AllProvidersUnavailableError()
```

#### **📊 Rate Limit Monitoring & SSE Events**

### **Real-Time Rate Limit Status**

```json
{
  "event": "rate_limit_status",
  "data": {
    "section": "ai_processing",
    "phase": "monitoring",
    "message": "checking API rate limits",
    "details": {
      "openai_remaining": "45/60 requests",
      "claude_remaining": "30/50 requests",
      "recommended_provider": "openai"
    }
  }
}
```

### **Retry Events**

```json
{
  "event": "progress",
  "data": {
    "section": "ai_processing",
    "phase": "retry",
    "message": "OpenAI rate limit hit, retrying in 5 seconds",
    "details": {
      "provider": "openai",
      "retry_count": 2,
      "retry_delay": "5.2s",
      "reason": "rate_limit_exceeded",
      "next_attempt": "2025-08-13T10:15:32Z"
    }
  }
}
```

### **Provider Failover Events**

```json
{
  "event": "progress",
  "data": {
    "section": "ai_processing",
    "phase": "failover",
    "message": "switching from OpenAI to Claude due to rate limits",
    "details": {
      "from_provider": "openai",
      "to_provider": "claude",
      "reason": "rate_limit_cooldown",
      "estimated_delay_saved": "4m 30s"
    }
  }
}
```

#### **⚙️ Performance Optimization Strategies**

### **Request Batching**

```python
class AIRequestBatcher:
    def __init__(self, batch_size=3, batch_timeout=10):
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self.pending_requests = []

    async def batch_ai_requests(self, requests: List[str]):
        """
        Combine multiple AI requests into single call
        Example: Analyze joins, CTEs, and validation in one prompt
        """
        batched_prompt = self.combine_prompts(requests)
        response = await self.call_ai_provider(batched_prompt)
        return self.split_response(response, len(requests))
```

### **Intelligent Caching**

```python
class AIResponseCache:
    def __init__(self, ttl=3600):  # 1 hour cache
        self.cache = {}
        self.ttl = ttl

    def cache_key(self, prompt: str, context: dict) -> str:
        """
        Generate cache key from normalized prompt + context
        """
        normalized = self.normalize_prompt(prompt)
        context_hash = hashlib.md5(str(context).encode()).hexdigest()
        return f"{normalized}:{context_hash}"

    async def get_cached_response(self, prompt: str, context: dict):
        """
        Check cache before making AI API call
        """
        key = self.cache_key(prompt, context)
        if key in self.cache:
            cached_item = self.cache[key]
            if time.time() - cached_item['timestamp'] < self.ttl:
                await self.send_cache_hit_event(key)
                return cached_item['response']
```

#### **📈 Resource Management**

### **Memory Management**

```json
{
  "memory_limits": {
    "max_excel_file_size": "50MB",
    "max_concurrent_requests": 10,
    "max_ai_response_size": "100KB",
    "cache_size_limit": "500MB"
  },
  "cleanup_strategies": {
    "request_timeout": "10 minutes",
    "cache_cleanup_interval": "1 hour",
    "memory_pressure_threshold": "80%"
  }
}
```

### **Connection Pooling**

```python
class DatabaseConnectionPool:
    def __init__(self, max_connections=20):
        self.max_connections = max_connections
        self.active_connections = {}
        self.connection_timeout = 300  # 5 minutes

    async def get_connection(self, connection_params: dict):
        """
        Reuse database connections when possible
        """
        conn_key = self.generate_connection_key(connection_params)

        if conn_key in self.active_connections:
            return self.active_connections[conn_key]

        if len(self.active_connections) >= self.max_connections:
            await self.cleanup_idle_connections()

        connection = await self.create_connection(connection_params)
        self.active_connections[conn_key] = connection
        return connection
```

#### **🎯 Performance Monitoring**

### **Real-Time Performance Metrics**

```json
{
  "event": "performance_metrics",
  "data": {
    "section": "system_performance",
    "phase": "monitoring",
    "message": "performance metrics update",
    "details": {
      "current_processing_time": "45s",
      "estimated_completion": "2m 15s",
      "ai_api_latency": "1.2s avg",
      "database_query_time": "0.8s",
      "memory_usage": "125MB",
      "cache_hit_rate": "67%"
    }
  }
}
```

### **Performance Degradation Alerts**

```json
{
  "event": "warning",
  "data": {
    "section": "performance",
    "message": "processing slower than expected",
    "details": {
      "expected_time": "90s",
      "current_time": "145s",
      "bottleneck": "ai_rate_limits",
      "mitigation": "switched to cached responses where possible"
    }
  }
}
```

#### **⚠️ Timeout & Fallback Strategies**

### **Progressive Timeout Handling**

```python
class TimeoutManager:
    def __init__(self):
        self.timeouts = {
            "ai_request": 30,      # Individual AI call
            "section_processing": 120,  # Each section (joins, etc)
            "total_generation": 600     # Entire SQL generation
        }

    async def with_timeout_and_fallback(self, coro, timeout_key: str):
        """
        Execute with timeout and fallback options
        """
        timeout = self.timeouts[timeout_key]

        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            await self.send_timeout_event(timeout_key, timeout)
            return await self.execute_fallback(timeout_key)
```

### **Graceful Degradation**

```python
async def execute_fallback(self, failed_section: str):
    """
    When AI processing fails/times out, provide fallback
    """
    fallback_strategies = {
        "joins": self.generate_basic_joins,
        "attributes": self.generate_simple_selects,
        "validation": self.skip_validation_return_sql
    }

    strategy = fallback_strategies.get(failed_section)
    if strategy:
        result = await strategy()
        await self.send_fallback_event(failed_section, result)
        return result

    raise TimeoutError(f"No fallback available for {failed_section}")
```

---

**Status:** ✅ **DOCUMENTED** - Comprehensive performance and rate limit management

**Key Features:**

- **Exponential backoff retry** with jitter for rate limits
- **Multi-provider failover** (OpenAI ↔ Claude)
- **Intelligent caching** to reduce API calls
- **Request batching** for efficiency
- **Real-time performance monitoring** via SSE
- **Progressive timeout handling** with graceful degradation

---

## 7. **Error Handling & Recovery Requirements**

### 🎯 **Comprehensive Error Management**

**Core Principle:** Never leave the user hanging - always provide actionable feedback and recovery options

#### **🚨 Error Classification System**

### **Error Categories with Recovery Strategies**

**Level 1: Recoverable Errors (Auto-Retry)**

```python
class RecoverableError(Exception):
    """Errors that can be automatically retried"""
    error_types = {
        "api_rate_limit": {
            "strategy": "exponential_backoff",
            "max_retries": 5,
            "base_delay": 1.0,
            "fallback": "switch_ai_provider"
        },
        "network_timeout": {
            "strategy": "immediate_retry",
            "max_retries": 3,
            "base_delay": 0.5,
            "fallback": "use_cached_response"
        },
        "database_connection": {
            "strategy": "reconnect_retry",
            "max_retries": 3,
            "base_delay": 2.0,
            "fallback": "return_sql_without_validation"
        },
        "ai_service_busy": {
            "strategy": "provider_failover",
            "max_retries": 2,
            "base_delay": 5.0,
            "fallback": "use_template_based_generation"
        }
    }
```

**Level 2: Degraded Processing (Partial Success)**

```python
class DegradedProcessingError(Exception):
    """Errors requiring fallback to simpler processing"""
    error_types = {
        "complex_join_analysis_failed": {
            "fallback": "generate_simple_joins",
            "user_message": "Using basic join logic due to complexity",
            "impact": "reduced_accuracy",
            "recovery": "manual_review_recommended"
        },
        "ai_response_incomplete": {
            "fallback": "use_partial_response_with_comments",
            "user_message": "Generated partial SQL with TODO comments",
            "impact": "requires_completion",
            "recovery": "reprocess_missing_sections"
        },
        "validation_timeout": {
            "fallback": "skip_validation_return_sql",
            "user_message": "SQL generated without validation due to timeout",
            "impact": "unvalidated_output",
            "recovery": "manual_validation_required"
        }
    }
```

**Level 3: Critical Errors (User Intervention Required)**

```python
class CriticalError(Exception):
    """Errors requiring user action or configuration change"""
    error_types = {
        "invalid_excel_structure": {
            "user_action": "fix_excel_format",
            "guidance": "Excel must contain table mappings in recognizable format",
            "examples": "provide_sample_excel_templates"
        },
        "database_authentication_failed": {
            "user_action": "check_credentials",
            "guidance": "Verify database connection parameters",
            "recovery": "update_connection_settings"
        },
        "ai_quota_exhausted": {
            "user_action": "wait_or_upgrade",
            "guidance": "Daily AI API quota exceeded",
            "recovery": "retry_tomorrow_or_upgrade_plan"
        },
        "unsupported_database_type": {
            "user_action": "use_supported_database",
            "guidance": "Currently supports: Databricks, PostgreSQL, MySQL, BigQuery",
            "recovery": "request_new_database_support"
        }
    }
```

#### **🔄 Multi-Level Recovery Pipeline**

### **Recovery Strategy Flow**

```python
class ErrorRecoveryOrchestrator:
    async def handle_error(self, error: Exception, context: dict):
        """
        Execute recovery pipeline based on error type and context
        """
        error_classification = self.classify_error(error)

        if error_classification.level == "recoverable":
            return await self.execute_auto_recovery(error, context)
        elif error_classification.level == "degraded":
            return await self.execute_fallback_processing(error, context)
        else:  # critical
            return await self.request_user_intervention(error, context)

    async def execute_auto_recovery(self, error: Exception, context: dict):
        """
        Automatic recovery without user intervention
        """
        recovery_config = self.get_recovery_config(error)

        for attempt in range(recovery_config.max_retries):
            try:
                # Send SSE update about retry attempt
                await self.send_recovery_event("auto_retry", attempt + 1, error)

                # Apply recovery strategy
                if recovery_config.strategy == "exponential_backoff":
                    delay = recovery_config.base_delay * (2 ** attempt)
                    await asyncio.sleep(delay)

                # Retry the failed operation
                result = await self.retry_failed_operation(context)

                # Send success event
                await self.send_recovery_event("auto_recovery_success", attempt + 1, error)
                return result

            except Exception as retry_error:
                if attempt == recovery_config.max_retries - 1:
                    # All retries failed, execute fallback
                    return await self.execute_fallback(recovery_config.fallback, context)
                continue
```

#### **📡 Error SSE Event System**

### **Real-Time Error Communication**

**Auto-Recovery Events:**

```json
{
  "event": "error_recovery",
  "data": {
    "section": "error_handling",
    "phase": "auto_retry",
    "message": "OpenAI rate limit hit, automatically retrying",
    "details": {
      "error_type": "api_rate_limit",
      "attempt": "2/5",
      "retry_delay": "4.0s",
      "strategy": "exponential_backoff",
      "next_attempt": "2025-08-13T10:15:45Z"
    }
  }
}
```

**Fallback Processing Events:**

```json
{
  "event": "error_recovery",
  "data": {
    "section": "error_handling",
    "phase": "fallback",
    "message": "Complex join analysis failed, using simpler approach",
    "details": {
      "original_error": "ai_response_timeout",
      "fallback_strategy": "template_based_joins",
      "impact": "reduced_accuracy",
      "user_action": "review_generated_joins"
    }
  }
}
```

**Critical Error Events:**

```json
{
  "event": "critical_error",
  "data": {
    "section": "error_handling",
    "phase": "user_intervention_required",
    "message": "Database authentication failed",
    "details": {
      "error_type": "database_authentication_failed",
      "user_action": "verify_connection_credentials",
      "guidance": "Check hostname, username, password, and port",
      "recovery_options": [
        "update_connection_settings",
        "test_connection_separately",
        "contact_admin_for_credentials"
      ]
    }
  }
}
```

#### **🛡️ Input Validation & Sanitization**

### **Excel Data Validation**

```python
class ExcelDataValidator:
    def validate_excel_structure(self, excel_data: dict) -> ValidationResult:
        """
        Comprehensive validation of Excel input data
        """
        validation_errors = []

        # Structure validation
        if not self.has_table_definitions(excel_data):
            validation_errors.append({
                "type": "missing_table_definitions",
                "message": "No recognizable table structures found",
                "guidance": "Excel should contain table names and column mappings",
                "severity": "critical"
            })

        # Content validation
        if not self.has_sufficient_mapping_info(excel_data):
            validation_errors.append({
                "type": "insufficient_mapping_data",
                "message": "Not enough information to generate meaningful SQL",
                "guidance": "Include table relationships and column mappings",
                "severity": "warning"
            })

        # Security validation
        dangerous_patterns = self.check_for_dangerous_content(excel_data)
        if dangerous_patterns:
            validation_errors.append({
                "type": "potential_security_risk",
                "message": f"Detected potentially dangerous content: {dangerous_patterns}",
                "guidance": "Remove SQL injection patterns or script content",
                "severity": "critical"
            })

        return ValidationResult(errors=validation_errors)
```

### **Database Connection Validation**

```python
class DatabaseConnectionValidator:
    async def validate_connection(self, conn_params: dict) -> ValidationResult:
        """
        Validate database connection before processing
        """
        try:
            # Test basic connectivity
            connection = await self.create_test_connection(conn_params)

            # Test permissions
            await self.test_query_permissions(connection)

            # Test schema access
            available_schemas = await self.get_available_schemas(connection)

            return ValidationResult(
                success=True,
                metadata={
                    "available_schemas": available_schemas,
                    "connection_type": self.detect_database_type(conn_params),
                    "version": await self.get_database_version(connection)
                }
            )

        except Exception as e:
            return ValidationResult(
                success=False,
                error={
                    "type": "connection_failed",
                    "message": str(e),
                    "guidance": self.get_connection_guidance(e),
                    "recovery_steps": [
                        "verify_hostname_and_port",
                        "check_credentials",
                        "test_network_connectivity",
                        "verify_database_exists"
                    ]
                }
            )
```

#### **⚡ Smart Fallback Strategies**

### **AI Processing Fallbacks**

```python
class AIProcessingFallbacks:
    async def execute_fallback_strategy(self, failed_section: str, context: dict):
        """
        Execute appropriate fallback based on failed section
        """
        fallback_strategies = {
            "dependency_analysis": self.fallback_to_simple_dependencies,
            "join_generation": self.fallback_to_template_joins,
            "attribute_mapping": self.fallback_to_direct_column_mapping,
            "validation": self.fallback_to_syntax_check_only,
            "optimization": self.fallback_to_basic_sql
        }

        strategy = fallback_strategies.get(failed_section)
        if strategy:
            await self.send_fallback_notification(failed_section)
            result = await strategy(context)
            await self.send_fallback_completion(failed_section, result)
            return result
        else:
            raise NoFallbackAvailableError(f"No fallback for {failed_section}")

    async def fallback_to_template_joins(self, context: dict):
        """
        When AI join analysis fails, use template-based approach
        """
        # Use predefined join patterns based on common relationships
        common_joins = [
            "customers.id = orders.customer_id",
            "orders.product_id = products.id",
            "orders.id = order_items.order_id"
        ]

        detected_tables = context.get("detected_tables", [])
        return self.generate_template_joins(detected_tables, common_joins)
```

### **Progressive Degradation Chain**

```python
class ProgressiveDegradationChain:
    def __init__(self):
        self.degradation_levels = [
            "full_ai_processing",      # Complete AI analysis
            "simplified_ai_processing", # Reduced complexity
            "template_based_processing", # Use predefined templates
            "manual_sql_skeleton",     # Basic SQL structure only
            "error_report_only"        # Return error with guidance
        ]

    async def execute_with_degradation(self, operation: str, context: dict):
        """
        Try operation at each degradation level until success
        """
        for level in self.degradation_levels:
            try:
                await self.send_degradation_attempt_event(operation, level)
                result = await self.execute_at_level(operation, level, context)
                await self.send_degradation_success_event(operation, level)
                return result

            except Exception as e:
                await self.send_degradation_failed_event(operation, level, str(e))
                if level == "error_report_only":
                    # Last resort - return detailed error report
                    return self.generate_error_report(operation, context, e)
                continue
```

#### **🔍 Error Monitoring & Analytics**

### **Error Tracking System**

```python
class ErrorAnalytics:
    def __init__(self):
        self.error_history = []
        self.error_patterns = {}
        self.recovery_success_rates = {}

    async def log_error_occurrence(self, error: Exception, context: dict):
        """
        Track error patterns for improvement
        """
        error_record = {
            "timestamp": datetime.utcnow(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context,
            "recovery_attempted": False,
            "recovery_success": False
        }

        self.error_history.append(error_record)
        await self.analyze_error_patterns()

    async def analyze_error_patterns(self):
        """
        Identify recurring error patterns and suggest improvements
        """
        recent_errors = self.get_recent_errors(hours=24)

        # Detect error clustering
        error_clusters = self.cluster_similar_errors(recent_errors)

        for cluster in error_clusters:
            if cluster.frequency > 5:  # More than 5 similar errors
                await self.send_error_pattern_alert(cluster)
```

### **Health Check System**

```python
class SystemHealthMonitor:
    async def perform_health_check(self):
        """
        Regular system health monitoring
        """
        health_status = {
            "ai_providers": await self.check_ai_provider_health(),
            "database_connections": await self.check_database_health(),
            "cache_system": await self.check_cache_health(),
            "memory_usage": await self.check_memory_usage(),
            "error_rate": await self.calculate_error_rate()
        }

        if self.detect_degraded_performance(health_status):
            await self.send_health_warning_event(health_status)

        return health_status
```

#### **📋 User-Friendly Error Messages**

### **Error Message Templates**

```python
class UserFriendlyErrorMessages:
    templates = {
        "api_rate_limit": {
            "title": "Processing Temporarily Slower",
            "message": "We're experiencing high demand. Your request is being processed with automatic retries.",
            "action": "Please wait - we'll keep trying automatically",
            "technical": "OpenAI API rate limit exceeded, using exponential backoff"
        },
        "complex_excel_structure": {
            "title": "Excel Structure Too Complex",
            "message": "Your Excel file has a very complex structure. We've generated a simplified version.",
            "action": "Review the generated SQL and add manual refinements if needed",
            "technical": "AI failed to parse complex nested relationships"
        },
        "database_connection_failed": {
            "title": "Database Connection Issue",
            "message": "Unable to connect to your database. Please check your connection settings.",
            "action": "Verify hostname, credentials, and network access",
            "technical": "Connection timeout or authentication failure"
        }
    }

    def format_user_message(self, error_type: str, technical_details: dict) -> dict:
        """
        Convert technical errors to user-friendly messages
        """
        template = self.templates.get(error_type, self.templates["generic"])

        return {
            "user_message": template["message"],
            "suggested_action": template["action"],
            "severity": self.determine_severity(error_type),
            "recovery_options": self.get_recovery_options(error_type),
            "technical_details": technical_details if self.user_wants_technical_details() else None
        }
```

---

**Status:** ✅ **DOCUMENTED** - Comprehensive error handling with auto-recovery

**Key Features:**

- **3-level error classification** (recoverable, degraded, critical)
- **Multi-level recovery pipeline** with automatic fallbacks
- **Real-time error communication** via SSE events
- **Progressive degradation chain** ensuring some output is always provided
- **Smart fallback strategies** for each processing section
- **User-friendly error messages** with actionable guidance
- **Error pattern analysis** for continuous improvement

---

## 8. **Monitoring & Logging Requirements**

### 🎯 **Comprehensive Logging Strategy**

**Core Principle:** Log everything for debugging, analytics, and system optimization while maintaining performance

#### **📊 Multi-Level Logging Architecture**

### **Log Level Hierarchy**

```python
class LogLevel:
    """Structured logging levels with specific use cases"""

    TRACE = {
        "level": 10,
        "purpose": "Fine-grained execution flow",
        "examples": ["AI prompt construction", "SQL parsing steps", "Cache lookups"],
        "retention": "7 days",
        "performance_impact": "high"
    }

    DEBUG = {
        "level": 20,
        "purpose": "Development and troubleshooting",
        "examples": ["AI API request/response", "Database query execution", "Excel parsing results"],
        "retention": "30 days",
        "performance_impact": "medium"
    }

    INFO = {
        "level": 30,
        "purpose": "Normal operation tracking",
        "examples": ["Request started/completed", "Section processing", "Performance metrics"],
        "retention": "90 days",
        "performance_impact": "low"
    }

    WARNING = {
        "level": 40,
        "purpose": "Potential issues or degraded performance",
        "examples": ["Rate limit approaching", "Fallback strategies used", "Validation concerns"],
        "retention": "180 days",
        "performance_impact": "minimal"
    }

    ERROR = {
        "level": 50,
        "purpose": "Recoverable errors with retry attempts",
        "examples": ["AI API failures", "Database timeouts", "Recovery executions"],
        "retention": "365 days",
        "performance_impact": "minimal"
    }

    CRITICAL = {
        "level": 60,
        "purpose": "System failures requiring immediate attention",
        "examples": ["Authentication failures", "Quota exhaustion", "Data corruption"],
        "retention": "permanent",
        "performance_impact": "minimal"
    }
```

#### **🔍 Request Lifecycle Logging**

### **End-to-End Request Tracking**

```python
class RequestLifecycleLogger:
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.time()
        self.checkpoints = []

    async def log_request_start(self, excel_data_size: int, target_env: str):
        """Log request initiation with full context"""
        await self.log_structured({
            "event": "request_started",
            "request_id": self.request_id,
            "timestamp": datetime.utcnow().isoformat(),
            "input_data": {
                "excel_data_size_bytes": excel_data_size,
                "estimated_tables": self.estimate_table_count(excel_data_size),
                "target_environment": target_env,
                "ai_intelligence_level": self.get_intelligence_level()
            },
            "system_state": {
                "memory_usage_mb": psutil.Process().memory_info().rss / 1024 / 1024,
                "active_connections": self.get_active_connection_count(),
                "cache_hit_rate": self.get_current_cache_hit_rate()
            }
        })

    async def log_section_checkpoint(self, section: str, status: str, details: dict):
        """Log completion of each processing section"""
        checkpoint_time = time.time()
        section_duration = checkpoint_time - (self.checkpoints[-1]["time"] if self.checkpoints else self.start_time)

        checkpoint_data = {
            "event": "section_checkpoint",
            "request_id": self.request_id,
            "section": section,
            "status": status,  # started, completed, failed, retried
            "duration_seconds": section_duration,
            "cumulative_duration": checkpoint_time - self.start_time,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.checkpoints.append({"section": section, "time": checkpoint_time, "data": checkpoint_data})
        await self.log_structured(checkpoint_data)
```

#### **🤖 AI API Interaction Logging**

### **Detailed AI Call Tracking**

```python
class AIInteractionLogger:
    async def log_ai_request(self, provider: str, prompt: str, context: dict):
        """Log all AI API interactions with full details"""
        await self.log_structured({
            "event": "ai_request_sent",
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat(),
            "request_details": {
                "prompt_length": len(prompt),
                "prompt_hash": hashlib.md5(prompt.encode()).hexdigest(),
                "estimated_tokens": self.estimate_token_count(prompt),
                "context_size": len(str(context)),
                "temperature": context.get("temperature", 0.7),
                "max_tokens": context.get("max_tokens", 4000)
            },
            "rate_limit_status": {
                "requests_remaining": await self.get_requests_remaining(provider),
                "tokens_remaining": await self.get_tokens_remaining(provider),
                "reset_time": await self.get_reset_time(provider)
            },
            "cache_status": {
                "cache_checked": True,
                "cache_hit": await self.check_cache_hit(prompt, context),
                "cache_key": self.generate_cache_key(prompt, context)
            }
        })

    async def log_ai_response(self, provider: str, response: dict, performance_metrics: dict):
        """Log AI API responses with quality metrics"""
        await self.log_structured({
            "event": "ai_response_received",
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat(),
            "response_details": {
                "response_length": len(str(response)),
                "tokens_used": response.get("usage", {}).get("total_tokens", 0),
                "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
                "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
                "finish_reason": response.get("choices", [{}])[0].get("finish_reason"),
                "response_quality_score": self.assess_response_quality(response)
            },
            "performance_metrics": {
                "total_duration_ms": performance_metrics.get("total_duration"),
                "api_latency_ms": performance_metrics.get("api_latency"),
                "processing_time_ms": performance_metrics.get("processing_time"),
                "retry_count": performance_metrics.get("retry_count", 0)
            },
            "cost_tracking": {
                "estimated_cost_usd": self.calculate_api_cost(provider, response),
                "tokens_consumed": response.get("usage", {}).get("total_tokens", 0),
                "cost_per_request": self.get_cost_per_request(provider)
            }
        })
```

#### **💾 Database Interaction Logging**

### **SQL Execution Tracking**

```python
class DatabaseLogger:
    async def log_sql_execution(self, sql: str, connection_params: dict, execution_result: dict):
        """Log all database operations with performance data"""
        await self.log_structured({
            "event": "sql_execution",
            "timestamp": datetime.utcnow().isoformat(),
            "database_info": {
                "environment": connection_params.get("environment"),
                "host": connection_params.get("host", "").split('.')[0] + "...",  # Anonymized
                "database": connection_params.get("database"),
                "connection_pool_size": self.get_pool_size()
            },
            "sql_details": {
                "sql_hash": hashlib.sha256(sql.encode()).hexdigest(),
                "sql_length": len(sql),
                "query_type": self.detect_query_type(sql),
                "estimated_complexity": self.assess_query_complexity(sql),
                "table_count": self.count_tables_in_query(sql),
                "join_count": self.count_joins_in_query(sql)
            },
            "execution_metrics": {
                "duration_ms": execution_result.get("duration_ms"),
                "rows_returned": execution_result.get("row_count"),
                "bytes_transferred": execution_result.get("bytes_transferred"),
                "execution_status": execution_result.get("status"),
                "error_message": execution_result.get("error"),
                "memory_usage_mb": execution_result.get("memory_usage")
            },
            "performance_analysis": {
                "is_slow_query": execution_result.get("duration_ms", 0) > 5000,
                "cache_eligible": self.is_cache_eligible(sql),
                "optimization_suggestions": self.generate_optimization_suggestions(sql, execution_result)
            }
        })

    async def log_connection_event(self, event_type: str, connection_details: dict):
        """Log database connection lifecycle events"""
        await self.log_structured({
            "event": f"database_connection_{event_type}",
            "timestamp": datetime.utcnow().isoformat(),
            "connection_details": {
                "connection_id": connection_details.get("connection_id"),
                "database_type": connection_details.get("database_type"),
                "pool_status": {
                    "active_connections": self.get_active_connections(),
                    "idle_connections": self.get_idle_connections(),
                    "max_connections": self.get_max_connections()
                }
            },
            "connection_metrics": {
                "connection_time_ms": connection_details.get("connection_time_ms"),
                "last_activity": connection_details.get("last_activity"),
                "total_queries_executed": connection_details.get("query_count", 0)
            }
        })
```

#### **📈 Performance & Resource Monitoring**

### **System Resource Tracking**

```python
class ResourceMonitor:
    async def log_system_metrics(self, context: str):
        """Comprehensive system resource monitoring"""
        process = psutil.Process()

        await self.log_structured({
            "event": "system_metrics",
            "context": context,
            "timestamp": datetime.utcnow().isoformat(),
            "cpu_metrics": {
                "cpu_percent": process.cpu_percent(),
                "cpu_count": psutil.cpu_count(),
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else None,
                "cpu_freq": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            "memory_metrics": {
                "process_memory_mb": process.memory_info().rss / 1024 / 1024,
                "process_memory_percent": process.memory_percent(),
                "system_memory": psutil.virtual_memory()._asdict(),
                "swap_memory": psutil.swap_memory()._asdict()
            },
            "disk_metrics": {
                "disk_usage": psutil.disk_usage('/')._asdict(),
                "disk_io": psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else None
            },
            "network_metrics": {
                "network_io": psutil.net_io_counters()._asdict(),
                "active_connections": len(psutil.net_connections())
            },
            "application_metrics": {
                "active_requests": self.get_active_request_count(),
                "cache_size_mb": self.get_cache_size_mb(),
                "cache_hit_rate": self.get_cache_hit_rate(),
                "average_response_time": self.get_average_response_time(),
                "error_rate": self.get_error_rate()
            }
        })
```

#### **🔐 Security & Audit Logging**

### **Security Event Tracking**

```python
class SecurityLogger:
    async def log_security_event(self, event_type: str, details: dict, risk_level: str):
        """Log security-related events for audit trail"""
        await self.log_structured({
            "event": "security_event",
            "event_type": event_type,
            "risk_level": risk_level,  # low, medium, high, critical
            "timestamp": datetime.utcnow().isoformat(),
            "client_info": {
                "ip_address": self.anonymize_ip(details.get("client_ip")),
                "user_agent": details.get("user_agent"),
                "request_origin": details.get("origin")
            },
            "security_details": {
                "authentication_method": details.get("auth_method"),
                "input_validation_result": details.get("validation_result"),
                "detected_patterns": details.get("suspicious_patterns", []),
                "sanitization_applied": details.get("sanitization_applied", False)
            },
            "action_taken": {
                "blocked": details.get("blocked", False),
                "rate_limited": details.get("rate_limited", False),
                "logged_for_review": True,
                "notification_sent": risk_level in ["high", "critical"]
            }
        })

    async def log_data_access(self, operation: str, data_classification: str, user_context: dict):
        """Log data access for compliance and audit"""
        await self.log_structured({
            "event": "data_access",
            "operation": operation,  # read, process, transform, export
            "data_classification": data_classification,  # public, internal, confidential
            "timestamp": datetime.utcnow().isoformat(),
            "user_context": {
                "session_id": user_context.get("session_id"),
                "request_id": user_context.get("request_id"),
                "client_info": self.sanitize_client_info(user_context)
            },
            "data_details": {
                "data_size_bytes": user_context.get("data_size"),
                "data_source": user_context.get("data_source"),
                "processing_purpose": user_context.get("purpose"),
                "retention_period": self.get_retention_period(data_classification)
            },
            "compliance": {
                "gdpr_applicable": self.check_gdpr_applicability(user_context),
                "data_minimization_applied": True,
                "purpose_limitation_satisfied": True,
                "consent_status": user_context.get("consent_status")
            }
        })
```

#### **📊 Business Intelligence & Analytics**

### **Usage Analytics Logging**

```python
class AnalyticsLogger:
    async def log_usage_analytics(self, session_data: dict, outcome: dict):
        """Log usage patterns for business intelligence"""
        await self.log_structured({
            "event": "usage_analytics",
            "timestamp": datetime.utcnow().isoformat(),
            "session_metrics": {
                "session_duration": session_data.get("duration_seconds"),
                "sections_completed": session_data.get("sections_completed"),
                "user_intelligence_preference": session_data.get("intelligence_level"),
                "target_database": session_data.get("target_database"),
                "excel_complexity_score": self.calculate_complexity_score(session_data)
            },
            "outcome_metrics": {
                "success_status": outcome.get("success"),
                "sql_generated": outcome.get("sql_generated", False),
                "validation_passed": outcome.get("validation_passed", False),
                "user_satisfaction_implicit": self.infer_satisfaction(outcome),
                "retry_count": outcome.get("retry_count", 0),
                "fallback_used": outcome.get("fallback_used", False)
            },
            "performance_metrics": {
                "total_processing_time": outcome.get("total_time"),
                "ai_api_calls": outcome.get("ai_calls_made"),
                "ai_api_cost": outcome.get("estimated_cost"),
                "database_queries": outcome.get("db_queries_executed"),
                "cache_utilization": outcome.get("cache_hit_rate")
            },
            "quality_metrics": {
                "sql_complexity_generated": self.assess_generated_sql_complexity(outcome),
                "error_count": outcome.get("error_count", 0),
                "warning_count": outcome.get("warning_count", 0),
                "manual_intervention_required": outcome.get("manual_review_needed", False)
            }
        })
```

#### **🎛️ Centralized Logging Configuration**

### **Structured Logging Framework**

```python
class CentralizedLogger:
    def __init__(self):
        self.logger = structlog.get_logger()
        self.log_destinations = [
            {"type": "file", "path": "/logs/app.log", "level": "INFO"},
            {"type": "elasticsearch", "index": "ai-sql-generator", "level": "DEBUG"},
            {"type": "cloudwatch", "group": "/aws/lambda/sql-generator", "level": "WARNING"},
            {"type": "metrics", "service": "datadog", "level": "ERROR"}
        ]

    async def log_structured(self, log_data: dict, level: str = "INFO"):
        """Central logging with automatic routing and enrichment"""

        # Enrich log data with common fields
        enriched_data = {
            **log_data,
            "service": "ai-sql-generator",
            "version": self.get_service_version(),
            "environment": os.getenv("ENVIRONMENT", "development"),
            "hostname": socket.gethostname(),
            "process_id": os.getpid(),
            "thread_id": threading.get_ident()
        }

        # Route to appropriate destinations based on level
        for destination in self.log_destinations:
            if self.should_log_to_destination(level, destination["level"]):
                await self.send_to_destination(enriched_data, destination)

        # Send to SSE if this is a user-facing event
        if log_data.get("event") in ["progress", "error", "completion"]:
            await self.send_sse_event(log_data)
```

#### **📋 Log Retention & Management**

### **Intelligent Log Lifecycle Management**

```python
class LogRetentionManager:
    retention_policies = {
        "trace_logs": {"retention_days": 7, "compression": True},
        "debug_logs": {"retention_days": 30, "compression": True},
        "info_logs": {"retention_days": 90, "compression": False},
        "warning_logs": {"retention_days": 180, "compression": False},
        "error_logs": {"retention_days": 365, "compression": False},
        "critical_logs": {"retention_days": "permanent", "compression": False},
        "security_logs": {"retention_days": "permanent", "compression": False},
        "audit_logs": {"retention_days": 2555, "compression": False}  # 7 years
    }

    async def apply_retention_policies(self):
        """Automatic log cleanup based on retention policies"""
        for log_type, policy in self.retention_policies.items():
            if policy["retention_days"] != "permanent":
                cutoff_date = datetime.now() - timedelta(days=policy["retention_days"])
                await self.cleanup_logs_before_date(log_type, cutoff_date)

            if policy["compression"]:
                await self.compress_old_logs(log_type, days_old=7)
```

---

**Status:** ✅ **DOCUMENTED** - Comprehensive monitoring and logging system

**Key Features:**

- **Multi-level logging** (TRACE to CRITICAL) with appropriate retention
- **End-to-end request tracking** with performance checkpoints
- **Detailed AI API interaction logging** including cost tracking
- **Database operation monitoring** with performance analysis
- **System resource monitoring** for optimization insights
- **Security and audit logging** for compliance
- **Business intelligence analytics** for usage patterns
- **Centralized logging framework** with automatic routing
- **Intelligent log retention** with compression and cleanup

---

## 9. **AI Memory & Context Management Requirements**

### 🎯 **Intelligent Context Understanding System**

**Core Principle:** Build contextual awareness and learning capabilities without expensive external services - optimize for local/cost-effective solutions

#### **🧠 Multi-Layered Memory Architecture**

### **Layer 1: Immediate Context (In-Memory - Free)**

```python
class ImmediateContext:
    """Current request context - zero cost, fast access"""
    def __init__(self, request_id: str):
        self.request_id = request_id
        self.excel_structure_analysis = {}
        self.discovered_relationships = []
        self.generated_sections = {}
        self.validation_results = {}
        self.user_corrections = []
        self.ai_reasoning_chain = []

    def track_ai_reasoning(self, section: str, reasoning: str, confidence: float):
        """Track AI decision-making process for learning"""
        self.ai_reasoning_chain.append({
            "section": section,
            "reasoning": reasoning,
            "confidence": confidence,
            "timestamp": time.time(),
            "tokens_used": len(reasoning.split()) * 1.3  # Rough token estimate
        })
```

### **Layer 2: Session Memory (Local File Cache - Free)**

```python
class LocalSessionMemory:
    """File-based session storage - no external costs"""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.cache_dir = f"./cache/sessions/{session_id}"
        self.session_file = f"{self.cache_dir}/session_memory.json"
        self.ttl_hours = 24  # Auto-cleanup after 24 hours

    async def store_session_learning(self, learning_data: dict):
        """Store session insights locally"""
        os.makedirs(self.cache_dir, exist_ok=True)

        session_data = {
            "session_id": self.session_id,
            "created_at": datetime.utcnow().isoformat(),
            "learning_data": learning_data,
            "success_patterns": self.extract_success_patterns(learning_data),
            "failure_patterns": self.extract_failure_patterns(learning_data),
            "user_preferences": self.infer_user_preferences(learning_data)
        }

        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

    async def get_relevant_session_context(self, current_task: str) -> dict:
        """Retrieve relevant context from session history"""
        if not os.path.exists(self.session_file):
            return {}

        with open(self.session_file, 'r') as f:
            session_data = json.load(f)

        # Filter for relevant context based on task similarity
        relevant_context = self.filter_relevant_context(session_data, current_task)
        return relevant_context
```

### **Layer 3: Local Vector Storage (SQLite + Embeddings - Free)**

```python
class LocalVectorMemory:
    """Local vector storage using free sentence-transformers"""
    def __init__(self):
        self.db_path = "./cache/vector_memory.db"
        self.embedding_model = None  # Load on demand
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for vector storage"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS interaction_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                interaction_hash TEXT UNIQUE,
                prompt_text TEXT,
                response_text TEXT,
                embedding BLOB,
                success_score REAL,
                created_at TIMESTAMP,
                context_metadata TEXT
            )
        """)
        conn.commit()
        conn.close()

    async def get_embedding_model(self):
        """Lazy load free sentence transformer model"""
        if self.embedding_model is None:
            from sentence_transformers import SentenceTransformer
            # Use free, local model - no API costs
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.embedding_model

    async def store_interaction_vector(self, prompt: str, response: str, context: dict, success_score: float):
        """Store interaction as vector for similarity search"""
        model = await self.get_embedding_model()
        combined_text = f"{prompt} {response}"
        embedding = model.encode(combined_text)

        interaction_hash = hashlib.md5(combined_text.encode()).hexdigest()

        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT OR REPLACE INTO interaction_embeddings
            (interaction_hash, prompt_text, response_text, embedding, success_score, created_at, context_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            interaction_hash,
            prompt,
            response,
            embedding.tobytes(),
            success_score,
            datetime.utcnow(),
            json.dumps(context)
        ])
        conn.commit()
        conn.close()

    async def find_similar_interactions(self, current_prompt: str, top_k: int = 3) -> List[dict]:
        """Find similar past interactions using cosine similarity"""
        model = await self.get_embedding_model()
        query_embedding = model.encode(current_prompt)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT prompt_text, response_text, embedding, success_score, context_metadata
            FROM interaction_embeddings
            WHERE success_score > 0.7
            ORDER BY created_at DESC
            LIMIT 50
        """)

        candidates = []
        for row in cursor.fetchall():
            stored_embedding = np.frombuffer(row[2], dtype=np.float32)
            similarity = self.cosine_similarity(query_embedding, stored_embedding)

            if similarity > 0.6:  # Similarity threshold
                candidates.append({
                    "prompt": row[0],
                    "response": row[1],
                    "similarity": similarity,
                    "success_score": row[3],
                    "context": json.loads(row[4])
                })

        conn.close()
        return sorted(candidates, key=lambda x: x["similarity"], reverse=True)[:top_k]
```

#### **🔍 Project Context Understanding (Free)**

### **Local Code Analysis Engine**

```python
class LocalProjectAnalyzer:
    """Analyze project structure without external API costs"""
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.file_cache = {}
        self.dependency_graph = {}

    async def analyze_project_structure(self) -> dict:
        """Build comprehensive project understanding locally"""
        project_analysis = {
            "file_structure": await self.build_file_tree(),
            "code_components": await self.extract_code_components(),
            "dependency_relationships": await self.analyze_dependencies(),
            "architectural_patterns": await self.detect_patterns(),
            "key_entities": await self.extract_key_entities()
        }

        # Cache for fast retrieval
        await self.cache_project_analysis(project_analysis)
        return project_analysis

    async def extract_code_components(self) -> dict:
        """Extract classes, functions, imports without AI"""
        components = {
            "classes": {},
            "functions": {},
            "imports": {},
            "constants": {},
            "api_endpoints": {}
        }

        for file_path in self.get_python_files():
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Use AST parsing - free and accurate
                tree = ast.parse(content)

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        components["classes"][node.name] = {
                            "file": file_path,
                            "line": node.lineno,
                            "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                            "docstring": ast.get_docstring(node)
                        }
                    elif isinstance(node, ast.FunctionDef):
                        components["functions"][node.name] = {
                            "file": file_path,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args],
                            "docstring": ast.get_docstring(node)
                        }

            except Exception as e:
                print(f"Error parsing {file_path}: {e}")

        return components
```

### **Intelligent Query Understanding (Local NLP)**

```python
class LocalQueryProcessor:
    """Process user queries using free NLP libraries"""
    def __init__(self):
        self.nlp_model = None
        self.intent_patterns = self.load_intent_patterns()

    async def get_nlp_model(self):
        """Load free spaCy model locally"""
        if self.nlp_model is None:
            import spacy
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
            except OSError:
                # Fallback to basic pattern matching if spaCy not installed
                self.nlp_model = "basic"
        return self.nlp_model

    async def understand_user_query(self, query: str, project_context: dict) -> dict:
        """Extract intent and entities from user query"""
        nlp = await self.get_nlp_model()

        if nlp != "basic":
            # Use spaCy for entity extraction
            doc = nlp(query)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            keywords = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
        else:
            # Fallback to basic keyword extraction
            entities = self.extract_entities_basic(query)
            keywords = self.extract_keywords_basic(query)

        intent = await self.classify_intent(query, keywords)
        relevant_files = await self.find_relevant_files(intent, keywords, project_context)

        return {
            "intent": intent,
            "entities": entities,
            "keywords": keywords,
            "relevant_files": relevant_files,
            "confidence": self.calculate_confidence(intent, entities, keywords)
        }

    def load_intent_patterns(self) -> dict:
        """Define intent patterns for SQL generator domain"""
        return {
            "excel_processing": {
                "keywords": ["excel", "spreadsheet", "mapping", "column", "row", "sheet"],
                "patterns": [r".*excel.*process.*", r".*mapping.*document.*", r".*spreadsheet.*"]
            },
            "sql_generation": {
                "keywords": ["sql", "query", "join", "select", "database", "table"],
                "patterns": [r".*generate.*sql.*", r".*create.*query.*", r".*join.*tables.*"]
            },
            "error_debugging": {
                "keywords": ["error", "bug", "issue", "problem", "fail", "exception"],
                "patterns": [r".*error.*", r".*not.*work.*", r".*problem.*with.*"]
            },
            "performance_optimization": {
                "keywords": ["slow", "fast", "optimize", "performance", "cache", "speed"],
                "patterns": [r".*too.*slow.*", r".*optimize.*", r".*improve.*performance.*"]
            }
        }
```

#### **💰 Cost-Optimized Context Building**

### **Smart Context Injection (Minimize AI Tokens)**

```python
class CostOptimizedContextBuilder:
    """Build AI context efficiently to minimize token costs"""
    def __init__(self, max_context_tokens: int = 8000):
        self.max_context_tokens = max_context_tokens
        self.token_estimator = TokenEstimator()

    async def build_optimized_context(self, query: str, project_context: dict, session_memory: dict) -> str:
        """Build minimal but effective context for AI prompt"""

        # Prioritize context sources by relevance vs token cost
        context_sources = [
            ("immediate_context", self.get_immediate_context(), 1.0),  # High priority
            ("similar_patterns", await self.get_similar_patterns(query), 0.8),
            ("project_structure", self.summarize_project_structure(project_context), 0.6),
            ("session_learnings", self.get_relevant_session_learnings(session_memory), 0.7),
            ("error_patterns", self.get_relevant_error_patterns(query), 0.5)
        ]

        # Build context within token budget
        context_parts = []
        remaining_tokens = self.max_context_tokens

        for source_name, content, priority in sorted(context_sources, key=lambda x: x[2], reverse=True):
            if not content:
                continue

            content_tokens = self.token_estimator.count_tokens(content)

            if content_tokens <= remaining_tokens:
                context_parts.append(f"## {source_name.upper()}\n{content}\n")
                remaining_tokens -= content_tokens
            else:
                # Truncate content to fit budget
                truncated = self.token_estimator.truncate_to_tokens(content, remaining_tokens)
                if truncated:
                    context_parts.append(f"## {source_name.upper()} (truncated)\n{truncated}\n")
                break

        return "\n".join(context_parts)
```

#### **📊 Local Analytics & Learning**

### **Pattern Recognition Engine (Free)**

```python
class LocalPatternLearner:
    """Learn from interactions without external services"""
    def __init__(self):
        self.patterns_db = "./cache/learned_patterns.json"
        self.success_threshold = 0.8

    async def learn_from_interaction(self, interaction_data: dict):
        """Extract learnable patterns from successful interactions"""
        if interaction_data.get("success_score", 0) > self.success_threshold:
            patterns = await self.extract_patterns(interaction_data)
            await self.store_patterns(patterns)

    async def extract_patterns(self, interaction_data: dict) -> dict:
        """Extract reusable patterns from successful interactions"""
        return {
            "excel_structure_patterns": self.analyze_excel_structure_success(interaction_data),
            "sql_generation_patterns": self.analyze_sql_generation_success(interaction_data),
            "join_logic_patterns": self.analyze_join_logic_success(interaction_data),
            "error_recovery_patterns": self.analyze_error_recovery_success(interaction_data)
        }

    async def get_applicable_patterns(self, current_context: dict) -> List[dict]:
        """Retrieve patterns applicable to current situation"""
        if not os.path.exists(self.patterns_db):
            return []

        with open(self.patterns_db, 'r') as f:
            all_patterns = json.load(f)

        applicable = []
        for pattern in all_patterns:
            similarity = self.calculate_pattern_similarity(pattern["context"], current_context)
            if similarity > 0.6:
                applicable.append({
                    "pattern": pattern,
                    "similarity": similarity,
                    "confidence": pattern.get("confidence", 0.5)
                })

        return sorted(applicable, key=lambda x: x["similarity"] * x["confidence"], reverse=True)
```

#### **🚀 Implementation Strategy (Zero External Costs)**

### **Phase 1: Basic Local Memory (Immediate)**

```python
# Start with file-based caching and in-memory context
components_to_implement = [
    "ImmediateContext",           # In-memory request context
    "LocalSessionMemory",         # File-based session storage
    "LocalProjectAnalyzer",       # AST-based code analysis
    "LocalQueryProcessor"         # Basic NLP with spaCy/regex
]
```

### **Phase 2: Local Vector Storage (Next)**

```python
# Add similarity search without external APIs
additional_components = [
    "LocalVectorMemory",          # SQLite + sentence-transformers
    "CostOptimizedContextBuilder", # Smart token management
    "LocalPatternLearner"         # Pattern extraction and storage
]
```

### **Phase 3: Advanced Features (Future)**

```python
# Enhanced capabilities as system matures
future_enhancements = [
    "MultiModalContextProcessor", # Handle images, diagrams
    "SemanticCodeSearch",        # Advanced code understanding
    "AutomaticPatternMining",    # Discover patterns automatically
    "ContextCompressionEngine"   # Compress context for efficiency
]
```

---

**Status:** ✅ **DOCUMENTED** - Cost-optimized AI memory and context system

**Key Benefits:**

- **Zero external API costs** for memory and context
- **Local vector storage** using free sentence-transformers
- **Project understanding** via AST parsing and pattern matching
- **Smart context building** to minimize AI token usage
- **Pattern learning** from successful interactions
- **Session memory** with automatic cleanup
- **Scalable architecture** that can grow with system needs

**Local Tools Used:**

- **SQLite** for vector storage (free)
- **sentence-transformers** for embeddings (free)
- **spaCy** for NLP processing (free)
- **AST parsing** for code analysis (built-in)
- **File system** for caching (free)
- **JSON** for pattern storage (built-in)

---

## 10. **Token Usage Tracking & Cost Management**

### 🎯 **Comprehensive Token Monitoring System**

**Core Principle:** Track every token consumed and produced to optimize costs and prevent quota exhaustion

#### **💰 Real-Time Token Accounting**

### **Token Counter & Estimator**

```python
class TokenCounter:
    """Accurate token counting for multiple AI providers"""

    def __init__(self):
        self.provider_configs = {
            "openai": {
                "encoding": "cl100k_base",  # GPT-4, GPT-3.5
                "cost_per_input_token": 0.00003,   # $30/1M tokens
                "cost_per_output_token": 0.00006,  # $60/1M tokens
                "rate_limits": {
                    "requests_per_minute": 60,
                    "tokens_per_minute": 150000,
                    "tokens_per_day": 10000000
                }
            },
            "claude": {
                "encoding": "cl100k_base",  # Approximation
                "cost_per_input_token": 0.000008,  # $8/1M tokens
                "cost_per_output_token": 0.000024, # $24/1M tokens
                "rate_limits": {
                    "requests_per_minute": 50,
                    "tokens_per_minute": 100000,
                    "tokens_per_day": 5000000
                }
            }
        }
        self.encoders = {}

    def get_encoder(self, provider: str):
        """Get or create tokenizer for provider"""
        if provider not in self.encoders:
            import tiktoken
            encoding_name = self.provider_configs[provider]["encoding"]
            self.encoders[provider] = tiktoken.get_encoding(encoding_name)
        return self.encoders[provider]

    def count_tokens(self, text: str, provider: str = "openai") -> int:
        """Accurate token count for specific provider"""
        if not text:
            return 0

        encoder = self.get_encoder(provider)
        return len(encoder.encode(text))

    def estimate_cost(self, input_tokens: int, output_tokens: int, provider: str) -> float:
        """Calculate exact cost for token usage"""
        config = self.provider_configs[provider]
        input_cost = input_tokens * config["cost_per_input_token"]
        output_cost = output_tokens * config["cost_per_output_token"]
        return input_cost + output_cost

    def truncate_to_token_limit(self, text: str, max_tokens: int, provider: str = "openai") -> str:
        """Truncate text to fit within token limit"""
        encoder = self.get_encoder(provider)
        tokens = encoder.encode(text)

        if len(tokens) <= max_tokens:
            return text

        truncated_tokens = tokens[:max_tokens]
        return encoder.decode(truncated_tokens)
```

### **Request-Level Token Tracking**

```python
class RequestTokenTracker:
    """Track tokens for entire SQL generation request"""

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.start_time = time.time()
        self.token_usage = {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_cost": 0.0,
            "provider_breakdown": {},
            "section_breakdown": {},
            "ai_calls": []
        }
        self.token_counter = TokenCounter()

    async def track_ai_call(self, section: str, provider: str, prompt: str, response: str, api_response: dict):
        """Track tokens for individual AI API call"""

        # Count tokens accurately
        input_tokens = self.token_counter.count_tokens(prompt, provider)
        output_tokens = self.token_counter.count_tokens(response, provider)

        # Get actual usage from API response if available
        api_usage = api_response.get("usage", {})
        if api_usage:
            input_tokens = api_usage.get("prompt_tokens", input_tokens)
            output_tokens = api_usage.get("completion_tokens", output_tokens)

        # Calculate cost
        call_cost = self.token_counter.estimate_cost(input_tokens, output_tokens, provider)

        # Record the call
        call_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "section": section,
            "provider": provider,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost": call_cost,
            "prompt_hash": hashlib.md5(prompt.encode()).hexdigest()[:8],
            "response_quality_score": self.assess_response_quality(response),
            "api_latency_ms": api_response.get("latency_ms", 0)
        }

        # Update totals
        self.token_usage["input_tokens"] += input_tokens
        self.token_usage["output_tokens"] += output_tokens
        self.token_usage["total_cost"] += call_cost
        self.token_usage["ai_calls"].append(call_record)

        # Update breakdowns
        if provider not in self.token_usage["provider_breakdown"]:
            self.token_usage["provider_breakdown"][provider] = {
                "input_tokens": 0, "output_tokens": 0, "cost": 0.0, "calls": 0
            }

        provider_stats = self.token_usage["provider_breakdown"][provider]
        provider_stats["input_tokens"] += input_tokens
        provider_stats["output_tokens"] += output_tokens
        provider_stats["cost"] += call_cost
        provider_stats["calls"] += 1

        if section not in self.token_usage["section_breakdown"]:
            self.token_usage["section_breakdown"][section] = {
                "input_tokens": 0, "output_tokens": 0, "cost": 0.0, "calls": 0
            }

        section_stats = self.token_usage["section_breakdown"][section]
        section_stats["input_tokens"] += input_tokens
        section_stats["output_tokens"] += output_tokens
        section_stats["cost"] += call_cost
        section_stats["calls"] += 1

        # Send SSE event with token usage
        await self.send_token_usage_event(call_record)

    async def get_usage_summary(self) -> dict:
        """Get comprehensive usage summary"""
        duration = time.time() - self.start_time

        return {
            "request_id": self.request_id,
            "duration_seconds": duration,
            "total_tokens": self.token_usage["input_tokens"] + self.token_usage["output_tokens"],
            "input_tokens": self.token_usage["input_tokens"],
            "output_tokens": self.token_usage["output_tokens"],
            "total_cost_usd": round(self.token_usage["total_cost"], 4),
            "cost_per_token": self.token_usage["total_cost"] / max(1, self.token_usage["input_tokens"] + self.token_usage["output_tokens"]),
            "ai_calls_made": len(self.token_usage["ai_calls"]),
            "average_tokens_per_call": (self.token_usage["input_tokens"] + self.token_usage["output_tokens"]) / max(1, len(self.token_usage["ai_calls"])),
            "provider_breakdown": self.token_usage["provider_breakdown"],
            "section_breakdown": self.token_usage["section_breakdown"],
            "efficiency_metrics": {
                "tokens_per_second": (self.token_usage["input_tokens"] + self.token_usage["output_tokens"]) / max(1, duration),
                "cost_per_second": self.token_usage["total_cost"] / max(1, duration),
                "average_response_quality": self.calculate_average_quality()
            }
        }
```

#### **📊 Rate Limit & Quota Management**

### **Provider Rate Limit Tracker**

```python
class RateLimitTracker:
    """Track and enforce rate limits across providers"""

    def __init__(self):
        self.provider_usage = {}
        self.quota_windows = {
            "minute": 60,
            "hour": 3600,
            "day": 86400
        }

    async def check_rate_limits(self, provider: str, estimated_tokens: int) -> dict:
        """Check if request would exceed rate limits"""
        if provider not in self.provider_usage:
            self.provider_usage[provider] = {
                "requests": [],
                "tokens": [],
                "daily_tokens": 0,
                "daily_requests": 0,
                "last_reset": datetime.utcnow().date()
            }

        usage = self.provider_usage[provider]
        now = datetime.utcnow()

        # Reset daily counters if new day
        if usage["last_reset"] < now.date():
            usage["daily_tokens"] = 0
            usage["daily_requests"] = 0
            usage["last_reset"] = now.date()

        # Clean old entries
        minute_ago = now - timedelta(minutes=1)
        usage["requests"] = [req for req in usage["requests"] if req > minute_ago]
        usage["tokens"] = [token for token in usage["tokens"] if token["timestamp"] > minute_ago]

        # Check limits
        config = TokenCounter().provider_configs[provider]["rate_limits"]

        current_rpm = len(usage["requests"])
        current_tpm = sum(token["count"] for token in usage["tokens"])

        return {
            "can_proceed": (
                current_rpm < config["requests_per_minute"] and
                current_tpm + estimated_tokens <= config["tokens_per_minute"] and
                usage["daily_tokens"] + estimated_tokens <= config["tokens_per_day"]
            ),
            "current_usage": {
                "requests_per_minute": current_rpm,
                "tokens_per_minute": current_tpm,
                "daily_tokens": usage["daily_tokens"],
                "estimated_tokens": estimated_tokens
            },
            "limits": config,
            "time_until_reset": {
                "minute_reset": 60 - (now.second),
                "day_reset": (86400 - (now.hour * 3600 + now.minute * 60 + now.second))
            },
            "recommendations": self.get_recommendations(current_rpm, current_tpm, config)
        }

    async def record_api_call(self, provider: str, tokens_used: int):
        """Record API call for rate limiting"""
        now = datetime.utcnow()
        usage = self.provider_usage[provider]

        usage["requests"].append(now)
        usage["tokens"].append({"timestamp": now, "count": tokens_used})
        usage["daily_tokens"] += tokens_used
        usage["daily_requests"] += 1
```

#### **💡 Cost Optimization Engine**

### **Smart Cost Management**

```python
class CostOptimizer:
    """Optimize token usage and costs automatically"""

    def __init__(self):
        self.cost_targets = {
            "max_cost_per_request": 0.50,  # $0.50 max per request
            "max_tokens_per_section": 8000,
            "efficiency_threshold": 0.7  # Quality vs cost ratio
        }

    async def optimize_prompt(self, original_prompt: str, context: dict, provider: str) -> dict:
        """Optimize prompt to reduce token usage while maintaining quality"""
        token_counter = TokenCounter()
        original_tokens = token_counter.count_tokens(original_prompt, provider)

        # Apply optimization strategies
        optimization_strategies = [
            self.remove_redundant_context,
            self.compress_examples,
            self.use_abbreviations,
            self.optimize_formatting,
            self.prioritize_essential_context
        ]

        optimized_prompt = original_prompt
        optimization_log = []

        for strategy in optimization_strategies:
            result = await strategy(optimized_prompt, context)
            if result["tokens_saved"] > 0 and result["quality_impact"] < 0.2:
                optimized_prompt = result["optimized_prompt"]
                optimization_log.append({
                    "strategy": strategy.__name__,
                    "tokens_saved": result["tokens_saved"],
                    "quality_impact": result["quality_impact"]
                })

        final_tokens = token_counter.count_tokens(optimized_prompt, provider)

        return {
            "original_prompt": original_prompt,
            "optimized_prompt": optimized_prompt,
            "original_tokens": original_tokens,
            "optimized_tokens": final_tokens,
            "tokens_saved": original_tokens - final_tokens,
            "cost_savings": token_counter.estimate_cost(original_tokens - final_tokens, 0, provider),
            "optimization_strategies": optimization_log,
            "quality_preservation_score": self.estimate_quality_preservation(optimization_log)
        }

    async def suggest_provider_switch(self, current_provider: str, estimated_tokens: int) -> dict:
        """Suggest cheaper provider if appropriate"""
        token_counter = TokenCounter()

        provider_costs = {}
        for provider in ["openai", "claude"]:
            cost = token_counter.estimate_cost(estimated_tokens, estimated_tokens // 2, provider)
            provider_costs[provider] = cost

        cheapest_provider = min(provider_costs, key=provider_costs.get)
        current_cost = provider_costs[current_provider]
        cheapest_cost = provider_costs[cheapest_provider]

        return {
            "should_switch": cheapest_provider != current_provider and (current_cost - cheapest_cost) > 0.01,
            "current_provider": current_provider,
            "recommended_provider": cheapest_provider,
            "current_cost": current_cost,
            "recommended_cost": cheapest_cost,
            "savings": current_cost - cheapest_cost,
            "provider_comparison": provider_costs
        }
```

#### **📈 Token Usage Analytics & SSE Events**

### **Real-Time Token Monitoring**

```json
{
  "event": "token_usage",
  "data": {
    "section": "token_tracking",
    "phase": "ai_call_completed",
    "message": "AI call completed - dependency analysis",
    "details": {
      "section": "dependency_analysis",
      "provider": "openai",
      "input_tokens": 1250,
      "output_tokens": 420,
      "total_tokens": 1670,
      "cost_usd": 0.0876,
      "cumulative_cost": 0.2341,
      "remaining_budget": 0.2659,
      "efficiency_score": 0.85
    }
  }
}
```

### **Cost Alert Events**

```json
{
  "event": "cost_alert",
  "data": {
    "section": "token_tracking",
    "phase": "budget_warning",
    "message": "Approaching cost limit - optimizing remaining sections",
    "details": {
      "current_cost": 0.42,
      "budget_limit": 0.5,
      "remaining_budget": 0.08,
      "sections_remaining": 2,
      "optimization_applied": true,
      "alternative_approach": "template_based_fallback"
    }
  }
}
```

### **Daily Usage Summary**

```python
class DailyUsageReporter:
    """Generate daily token usage reports"""

    async def generate_daily_report(self, date: datetime.date) -> dict:
        """Generate comprehensive daily usage report"""
        usage_data = await self.get_daily_usage_data(date)

        return {
            "date": date.isoformat(),
            "total_requests": usage_data["request_count"],
            "total_tokens": usage_data["total_tokens"],
            "total_cost": usage_data["total_cost"],
            "average_cost_per_request": usage_data["total_cost"] / max(1, usage_data["request_count"]),
            "provider_breakdown": usage_data["provider_stats"],
            "section_performance": usage_data["section_stats"],
            "cost_trends": {
                "vs_yesterday": await self.calculate_trend(date, days=1),
                "vs_last_week": await self.calculate_trend(date, days=7),
                "monthly_projection": await self.project_monthly_cost(usage_data)
            },
            "optimization_opportunities": await self.identify_optimization_opportunities(usage_data),
            "efficiency_metrics": {
                "tokens_per_successful_request": usage_data["tokens_per_success"],
                "cost_per_successful_sql": usage_data["cost_per_success"],
                "average_quality_score": usage_data["avg_quality"]
            }
        }
```

#### **🎛️ Budget Management & Controls**

### **Request Budget Enforcement**

```python
class BudgetManager:
    """Enforce spending limits and optimize within budget"""

    def __init__(self):
        self.budgets = {
            "per_request": 0.50,     # Max $0.50 per request
            "daily": 25.00,          # Max $25 per day
            "monthly": 500.00        # Max $500 per month
        }

    async def check_budget_before_request(self, estimated_cost: float) -> dict:
        """Check if request can proceed within budget"""
        current_usage = await self.get_current_usage()

        budget_status = {
            "can_proceed": True,
            "budget_alerts": [],
            "optimization_required": False,
            "fallback_recommended": False
        }

        # Check per-request budget
        if estimated_cost > self.budgets["per_request"]:
            budget_status["can_proceed"] = False
            budget_status["budget_alerts"].append({
                "type": "per_request_exceeded",
                "limit": self.budgets["per_request"],
                "estimated": estimated_cost,
                "recommendation": "optimize_prompt_or_use_fallback"
            })

        # Check daily budget
        if current_usage["daily"] + estimated_cost > self.budgets["daily"]:
            budget_status["optimization_required"] = True
            budget_status["budget_alerts"].append({
                "type": "daily_limit_approaching",
                "remaining": self.budgets["daily"] - current_usage["daily"],
                "estimated": estimated_cost,
                "recommendation": "enable_aggressive_optimization"
            })

        return budget_status
```

---

**Status:** ✅ **DOCUMENTED** - Comprehensive token tracking and cost management

**Key Features:**

- **Accurate token counting** for multiple AI providers
- **Real-time cost tracking** with detailed breakdowns
- **Rate limit monitoring** to prevent quota exhaustion
- **Cost optimization engine** with automatic prompt optimization
- **Budget enforcement** with spending limits
- **Provider switching** recommendations for cost savings
- **Detailed analytics** and daily usage reports
- **SSE events** for real-time token/cost updates

---

## 11. **Input Format Requirements**

### 🎯 **Excel Data Input Specification**

**Core Principle:** Accept flexible, unstructured Excel data and intelligently parse it into actionable SQL generation context

#### **📋 Primary Input Structure**

### **API Request Format**

```json
{
  "excel_data": {
    "sheets": [
      {
        "name": "Customer Mapping",
        "data": [
          [
            "Customer ID",
            "First Name",
            "Last Name",
            "Email",
            "Registration Date"
          ],
          ["CUST001", "John", "Doe", "john.doe@email.com", "2024-01-15"],
          ["CUST002", "Jane", "Smith", "jane.smith@email.com", "2024-01-16"]
        ]
      },
      {
        "name": "Order Details",
        "data": [
          [
            "Order ID",
            "Customer ID",
            "Product",
            "Quantity",
            "Amount",
            "Order Date"
          ],
          ["ORD001", "CUST001", "Widget A", "2", "29.99", "2024-02-01"],
          ["ORD002", "CUST001", "Widget B", "1", "19.99", "2024-02-02"],
          ["ORD003", "CUST002", "Widget A", "3", "44.99", "2024-02-03"]
        ]
      },
      {
        "name": "Relationships",
        "data": [
          ["Table 1", "Column 1", "Relationship", "Table 2", "Column 2"],
          ["customers", "customer_id", "1:M", "orders", "customer_id"],
          ["orders", "product_id", "M:1", "products", "id"]
        ]
      }
    ],
    "metadata": {
      "filename": "customer_order_mapping.xlsx",
      "created_by": "data_analyst_user",
      "purpose": "Generate customer lifetime value report",
      "target_database": "databricks"
    }
  },
  "generation_options": {
    "intelligence_level": "balanced",
    "target_environment": "databricks",
    "optimization_level": "high",
    "include_comments": true,
    "max_cost_budget": 0.5
  },
  "database_connection": {
    "host": "adb-workspace.cloud.databricks.com",
    "http_path": "/sql/1.0/warehouses/abc123",
    "catalog": "main",
    "schema": "analytics"
  }
}
```

#### **📊 Supported Excel Patterns**

### **Pattern 1: Table Definition Sheets**

```python
# Example: Each sheet represents a database table
table_definition_pattern = {
    "sheet_name": "customers",  # Becomes table name
    "structure": [
        ["Column Name", "Data Type", "Description", "Example"],
        ["customer_id", "INT", "Unique customer identifier", "12345"],
        ["first_name", "VARCHAR(50)", "Customer first name", "John"],
        ["last_name", "VARCHAR(50)", "Customer last name", "Doe"],
        ["email", "VARCHAR(100)", "Email address", "john@example.com"],
        ["created_at", "TIMESTAMP", "Registration timestamp", "2024-01-15 10:30:00"]
    ]
}
```

### **Pattern 2: Relationship Mapping Sheets**

```python
# Example: Dedicated sheet for table relationships
relationship_pattern = {
    "sheet_name": "Table_Relationships",
    "structure": [
        ["Source Table", "Source Column", "Relationship Type", "Target Table", "Target Column", "Description"],
        ["customers", "id", "ONE_TO_MANY", "orders", "customer_id", "Customer can have multiple orders"],
        ["orders", "product_id", "MANY_TO_ONE", "products", "id", "Order references single product"],
        ["orders", "id", "ONE_TO_MANY", "order_items", "order_id", "Order contains multiple line items"]
    ]
}
```

### **Pattern 3: Data Sample Sheets**

```python
# Example: Sample data for understanding structure
data_sample_pattern = {
    "sheet_name": "Sample_Data_Customers",
    "structure": [
        ["id", "name", "email", "signup_date", "status"],
        [1, "Alice Johnson", "alice@company.com", "2024-01-10", "active"],
        [2, "Bob Smith", "bob@company.com", "2024-01-12", "active"],
        [3, "Carol Davis", "carol@company.com", "2024-01-15", "inactive"]
    ]
}
```

### **Pattern 4: Business Logic Sheets**

```python
# Example: Business rules and calculations
business_logic_pattern = {
    "sheet_name": "Calculations",
    "structure": [
        ["Metric", "Formula", "Description", "Example"],
        ["Customer Lifetime Value", "SUM(order_amount) WHERE customer_id = X", "Total value per customer", "1250.75"],
        ["Monthly Recurring Revenue", "AVG(monthly_subscription) * active_customers", "MRR calculation", "15000.00"],
        ["Churn Rate", "churned_customers / total_customers * 100", "Monthly churn percentage", "2.5"]
    ]
}
```

### **Pattern 5: Data Mapping Sheets (Advanced)**

```python
# Example: Comprehensive data mapping with quality rules
data_mapping_pattern = {
    "sheet_name": "data_map",
    "structure": [
        ["TargetTable", "TargetField", "Uniqueness", "Definition", "DataQuality Rules", "Context", "Valid Values", "Source Table", "Source Column Name", "Logic"],
        ["customers", "customer_id", "Primary Key", "Unique customer identifier", "NOT NULL, UNIQUE", "Customer entity", "Numeric > 0", "raw_customers", "cust_id", "Direct mapping"],
        ["orders", "order_total", "Required", "Total order amount", "NOT NULL, > 0", "Financial calculation", "Decimal(10,2)", "order_lines", "line_total", "SUM(line_total) GROUP BY order_id"],
        ["customers", "full_name", "Optional", "Customer display name", "Length <= 100", "Display purposes", "String", "raw_customers", "fname, lname", "CONCAT(fname, ' ', lname)"],
        ["orders", "order_status", "Required", "Current order state", "IN valid_values", "Business process", "pending,confirmed,shipped,delivered,cancelled", "order_tracking", "status_code", "CASE WHEN status_code = 1 THEN 'pending' WHEN status_code = 2 THEN 'confirmed' END"]
    ]
}
```

### **Pattern 6: Source System Mapping (Advanced)**

```python
# Example: Source system configuration and filters
source_mapping_pattern = {
    "sheet_name": "source_mapping",
    "structure": [
        ["Source Table Name", "Source Table", "Note", "Filters to Apply", "NLP Filters", "Joins", "NLP Join"],
        ["Customer Master", "crm.customers", "Main customer table", "active = 1 AND created_date >= '2024-01-01'", "only active customers from this year", "LEFT JOIN crm.addresses ON customers.id = addresses.customer_id", "include customer addresses when available"],
        ["Order History", "sales.orders", "All order data", "order_date BETWEEN '2024-01-01' AND CURRENT_DATE", "orders from current year only", "INNER JOIN sales.order_items ON orders.id = order_items.order_id", "must have order line items"],
        ["Product Catalog", "inventory.products", "Current products only", "discontinued = 0", "exclude discontinued products", "LEFT JOIN inventory.categories ON products.category_id = categories.id", "include product category information"],
        ["Customer Segments", "analytics.customer_segments", "Derived segmentation", "segment_date = (SELECT MAX(segment_date) FROM analytics.customer_segments)", "use most recent segmentation data", "INNER JOIN crm.customers ON customer_segments.customer_id = customers.id", "only for existing customers"]
    ]
}
```

#### **🔍 Input Validation & Processing**

### **Data Quality Validation**

```python
class ExcelInputValidator:
    def validate_input_format(self, excel_data: dict) -> ValidationResult:
        """Comprehensive input validation"""
        validation_errors = []
        validation_warnings = []

        # Structure validation
        if not excel_data.get("sheets"):
            validation_errors.append({
                "type": "missing_sheets",
                "message": "No sheets found in Excel data",
                "severity": "critical"
            })

        # Content validation for each sheet
        for sheet in excel_data.get("sheets", []):
            sheet_validation = self.validate_sheet_structure(sheet)
            validation_errors.extend(sheet_validation["errors"])
            validation_warnings.extend(sheet_validation["warnings"])

        # Metadata validation
        metadata = excel_data.get("metadata", {})
        if not metadata.get("purpose"):
            validation_warnings.append({
                "type": "missing_purpose",
                "message": "No purpose specified - may affect SQL generation quality",
                "suggestion": "Include purpose in metadata for better results"
            })

        return ValidationResult(
            is_valid=len(validation_errors) == 0,
            errors=validation_errors,
            warnings=validation_warnings,
            processed_data=self.normalize_excel_data(excel_data) if len(validation_errors) == 0 else None
        )

    def validate_sheet_structure(self, sheet: dict) -> dict:
        """Validate individual sheet structure"""
        errors = []
        warnings = []

        # Check for minimum data
        if not sheet.get("data") or len(sheet["data"]) < 2:
            errors.append({
                "sheet": sheet.get("name", "unknown"),
                "type": "insufficient_data",
                "message": "Sheet must have at least header row and one data row"
            })

        # Check for recognizable patterns
        if not self.detect_sheet_pattern(sheet):
            warnings.append({
                "sheet": sheet.get("name", "unknown"),
                "type": "unrecognized_pattern",
                "message": "Could not identify sheet pattern - will attempt generic parsing"
            })

        return {"errors": errors, "warnings": warnings}
```

### **Intelligent Pattern Recognition**

````python
class ExcelPatternRecognizer:
    def __init__(self):
        self.pattern_indicators = {
            "table_definition": {
                "header_patterns": [
                    ["column", "name", "type"],
                    ["field", "data", "type"],
                    ["attribute", "datatype", "description"]
                ],
                "confidence_threshold": 0.7
            },
            "relationship_mapping": {
                "header_patterns": [
                    ["source", "target", "relationship"],
                    ["table1", "table2", "join"],
                    ["parent", "child", "type"]
                ],
                "confidence_threshold": 0.8
            },
            "sample_data": {
                "indicators": [
                    "more_data_rows_than_definition_rows",
                    "consistent_data_types_in_columns",
                    "no_metadata_columns"
                ],
                "confidence_threshold": 0.6
            },
            "business_logic": {
                "header_patterns": [
                    ["metric", "formula", "description"],
                    ["calculation", "expression", "example"],
                    ["kpi", "definition", "target"]
                ],
                "confidence_threshold": 0.7
            }
        }

    def detect_sheet_patterns(self, excel_data: dict) -> dict:
        """Detect patterns in each sheet"""
        pattern_analysis = {}

        for sheet in excel_data.get("sheets", []):
            sheet_name = sheet.get("name", "unknown")
            pattern_scores = {}

            for pattern_type, config in self.pattern_indicators.items():
                score = self.calculate_pattern_score(sheet, pattern_type, config)
                pattern_scores[pattern_type] = score

            # Determine primary pattern
            best_pattern = max(pattern_scores, key=pattern_scores.get)
            confidence = pattern_scores[best_pattern]

            pattern_analysis[sheet_name] = {
                "primary_pattern": best_pattern if confidence > 0.5 else "unknown",
                "confidence": confidence,
                "all_scores": pattern_scores,
                "suggested_processing": self.get_processing_strategy(best_pattern, confidence)
            }

        return pattern_analysis

#### **💬 Intelligent SQL Strategy Clarification System**

### **Strategic Mapping Interpretation Engine**
```python
class SQLStrategyClairificationEngine:
    """Ask strategic questions about how to interpret mapping document for SQL generation"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.mapping_analysis = {}
        self.sql_strategy_questions = []

    async def analyze_mapping_for_sql_strategy(self, excel_data: dict) -> dict:
        """Analyze mapping document and generate strategic questions for SQL generation"""

        # Extract available information from mapping sheets
        mapping_info = await self.extract_mapping_information(excel_data)

        # Generate strategic questions about SQL structure
        strategy_questions = await self.generate_sql_strategy_questions(mapping_info)

        return {
            "mapping_analysis": mapping_info,
            "strategy_questions": strategy_questions,
            "confidence_level": self.calculate_interpretation_confidence(mapping_info),
            "can_proceed_without_clarification": self.can_proceed_automatically(mapping_info, strategy_questions)
        }

    async def generate_sql_strategy_questions(self, mapping_info: dict) -> List[dict]:
        """Generate strategic questions about SQL structure and column usage"""
        questions = []

        # Questions about information discovery and location
        questions.extend(await self.generate_information_discovery_questions(mapping_info))

        # Questions about SELECT clause strategy
        questions.extend(await self.generate_select_strategy_questions(mapping_info))

        # Questions about JOIN strategy
        questions.extend(await self.generate_join_strategy_questions(mapping_info))

        # Questions about WHERE clause strategy
        questions.extend(await self.generate_filter_strategy_questions(mapping_info))

        # Questions about business logic interpretation
        questions.extend(await self.generate_business_logic_questions(mapping_info))

        # Questions about output structure
        questions.extend(await self.generate_output_structure_questions(mapping_info))

        return self.prioritize_strategy_questions(questions)

    async def generate_information_discovery_questions(self, mapping_info: dict) -> List[dict]:
        """Ask questions to help locate and identify information needed for SQL building"""
        questions = []
        available_sheets = mapping_info.get("sheet_names", [])

        # Question about transformation logic discovery
        questions.append({
            "type": "transformation_data_discovery",
            "priority": "critical",
            "category": "information_location",
            "question": "I need to understand which column data to use for transformations. Where should I look for this information?",
            "context": f"Excel has {len(available_sheets)} sheets: {', '.join(available_sheets)}. Need to identify transformation rules.",
            "options": [
                {
                    "value": "specific_sheet_transformations",
                    "label": "Transformations are in a specific sheet",
                    "follow_up": "Which sheet contains the transformation rules?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "column_descriptions_sheet",
                    "label": "Look for column description/mapping sheet",
                    "description": "Find sheet with source→target column mappings"
                },
                {
                    "value": "business_rules_sheet",
                    "label": "Business rules/calculations sheet",
                    "description": "Find sheet explaining calculation logic"
                },
                {
                    "value": "mixed_across_sheets",
                    "label": "Transformation info is scattered across sheets",
                    "description": "I need to piece together info from multiple places"
                },
                {
                    "value": "infer_from_examples",
                    "label": "Infer from data examples",
                    "description": "Use sample data to understand transformations"
                }
            ],
            "impact": "Critical for understanding how to build SELECT clause transformations",
            "sql_section": "Data transformation logic"
        })

        # Question about join relationship discovery
        questions.append({
            "type": "join_information_discovery",
            "priority": "critical",
            "category": "information_location",
            "question": "Where can I find details about how tables should be joined together?",
            "context": "Need to locate join conditions and relationship information for FROM/JOIN clauses",
            "options": [
                {
                    "value": "relationships_sheet",
                    "label": "There's a dedicated relationships/joins sheet",
                    "follow_up": "Which sheet contains the join information?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "erd_diagram_sheet",
                    "label": "Entity relationship diagram sheet",
                    "description": "Look for ERD or table relationship diagrams"
                },
                {
                    "value": "table_definitions_sheet",
                    "label": "Table definitions with foreign keys",
                    "description": "Find sheet describing table structures and keys"
                },
                {
                    "value": "business_process_sheet",
                    "label": "Business process description sheet",
                    "description": "Join logic described in business context"
                },
                {
                    "value": "infer_from_fields",
                    "label": "Infer joins from common field names",
                    "description": "Use field naming patterns to guess relationships"
                },
                {
                    "value": "no_explicit_joins",
                    "label": "No explicit join information provided",
                    "description": "Need to ask user for join strategy"
                }
            ],
            "impact": "Essential for building correct FROM and JOIN clauses",
            "sql_section": "Table relationships and joins"
        })

        # Question about data filtering/selection criteria discovery
        questions.append({
            "type": "filter_criteria_discovery",
            "priority": "high",
            "category": "information_location",
            "question": "Where should I look for information about data filtering and selection criteria?",
            "context": "Need to identify WHERE clause conditions and data filtering rules",
            "options": [
                {
                    "value": "filter_rules_sheet",
                    "label": "Dedicated filter/criteria sheet",
                    "follow_up": "Which sheet has the filtering rules?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "business_requirements_sheet",
                    "label": "Business requirements sheet",
                    "description": "Look for selection criteria in requirements"
                },
                {
                    "value": "data_quality_sheet",
                    "label": "Data quality/validation sheet",
                    "description": "Find data quality rules and exclusions"
                },
                {
                    "value": "embedded_in_mappings",
                    "label": "Filters embedded in field mappings",
                    "description": "Filtering logic mixed with column mappings"
                },
                {
                    "value": "no_explicit_filters",
                    "label": "No specific filtering mentioned",
                    "description": "Include all data unless told otherwise"
                }
            ],
            "impact": "Determines WHERE clause and data selection logic",
            "sql_section": "Data filtering and selection"
        })

        # Question about target schema/structure discovery
        questions.append({
            "type": "target_schema_discovery",
            "priority": "high",
            "category": "information_location",
            "question": "Where can I find information about the target table structure and expected output format?",
            "context": "Need to understand target schema, column names, data types, and output requirements",
            "options": [
                {
                    "value": "target_schema_sheet",
                    "label": "Dedicated target schema sheet",
                    "follow_up": "Which sheet defines the target structure?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "output_template_sheet",
                    "label": "Output template/example sheet",
                    "description": "Look for example of desired output format"
                },
                {
                    "value": "field_mapping_sheet",
                    "label": "Field mapping sheet with target columns",
                    "description": "Target structure defined in mapping sheet"
                },
                {
                    "value": "requirements_doc_sheet",
                    "label": "Requirements document sheet",
                    "description": "Target specs in requirements documentation"
                },
                {
                    "value": "infer_from_mappings",
                    "label": "Infer target structure from field mappings",
                    "description": "Build target schema from source→target mappings"
                }
            ],
            "impact": "Defines the final SELECT clause structure and column naming",
            "sql_section": "Output structure and column definitions"
        })

        # Question about business context and validation rules discovery
        questions.append({
            "type": "business_context_discovery",
            "priority": "medium",
            "category": "information_location",
            "question": "Where should I look for business context and validation rules that might affect the SQL logic?",
            "context": "Need to understand business rules, constraints, and context that impact SQL generation",
            "options": [
                {
                    "value": "business_rules_sheet",
                    "label": "Business rules and logic sheet",
                    "follow_up": "Which sheet contains business rules?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "validation_rules_sheet",
                    "label": "Data validation and constraints sheet",
                    "description": "Look for data quality and validation rules"
                },
                {
                    "value": "process_documentation_sheet",
                    "label": "Process documentation sheet",
                    "description": "Business process context and workflow"
                },
                {
                    "value": "notes_comments_sheet",
                    "label": "Notes and comments sheet",
                    "description": "Additional context in notes/comments"
                },
                {
                    "value": "embedded_in_other_sheets",
                    "label": "Business context scattered across sheets",
                    "description": "Context embedded within other information"
                },
                {
                    "value": "minimal_business_context",
                    "label": "Minimal business context provided",
                    "description": "Focus on technical implementation only"
                }
            ],
            "impact": "Influences business logic implementation and data validation",
            "sql_section": "Business rules and constraints"
        })

        # Question about data source discovery
        questions.append({
            "type": "data_source_discovery",
            "priority": "high",
            "category": "information_location",
            "question": "How should I identify and understand the source data structures referenced in this mapping?",
            "context": "Need to understand source table schemas, column names, and data characteristics",
            "options": [
                {
                    "value": "source_schema_sheet",
                    "label": "Dedicated source schema/structure sheet",
                    "follow_up": "Which sheet describes source data structures?",
                    "sheet_options": available_sheets
                },
                {
                    "value": "table_catalog_sheet",
                    "label": "Data catalog or table inventory sheet",
                    "description": "Look for comprehensive source table documentation"
                },
                {
                    "value": "sample_data_sheet",
                    "label": "Sample data or examples sheet",
                    "description": "Understand source structure from data examples"
                },
                {
                    "value": "field_list_sheet",
                    "label": "Source field list or data dictionary",
                    "description": "Find detailed source column descriptions"
                },
                {
                    "value": "assume_standard_naming",
                    "label": "Assume standard database naming conventions",
                    "description": "Use typical database field naming patterns"
                },
                {
                    "value": "infer_from_mappings",
                    "label": "Infer source structure from mapping references",
                    "description": "Deduce source schema from mapping document references"
                }
            ],
            "impact": "Critical for understanding FROM clause and source data references",
            "sql_section": "Source data understanding and FROM clause"
        })

        # Question about handling missing or incomplete information
        questions.append({
            "type": "missing_information_strategy",
            "priority": "critical",
            "category": "information_completeness",
            "question": "What should I do when I can't find specific information needed for SQL generation?",
            "context": "Some details for building complete SQL might be missing or unclear from the Excel mapping",
            "options": [
                {
                    "value": "ask_specific_questions",
                    "label": "Ask specific follow-up questions",
                    "description": "Generate targeted questions about missing pieces"
                },
                {
                    "value": "make_reasonable_assumptions",
                    "label": "Make reasonable assumptions and document them",
                    "description": "Fill gaps with best practices and note assumptions"
                },
                {
                    "value": "generate_partial_sql",
                    "label": "Generate partial SQL with TODO comments",
                    "description": "Create SQL template with placeholders for missing info"
                },
                {
                    "value": "request_additional_context",
                    "label": "Request additional documentation",
                    "description": "Ask user to provide missing specification details"
                },
                {
                    "value": "use_database_analysis",
                    "label": "Analyze actual database structure if available",
                    "description": "Query source database to understand schema"
                }
            ],
            "impact": "Determines how to handle incomplete specifications",
            "sql_section": "Overall SQL completeness and accuracy"
        })

        # Question about information validation and cross-referencing
        questions.append({
            "type": "information_validation_strategy",
            "priority": "medium",
            "category": "information_verification",
            "question": "How should I validate and cross-reference information found across different sheets?",
            "context": "Information might be scattered or contradictory across multiple sheets",
            "options": [
                {
                    "value": "primary_source_priority",
                    "label": "Prioritize specific sheets as primary sources",
                    "description": "Establish hierarchy of information sources",
                    "follow_up": "Which sheets should take priority for conflicts?"
                },
                {
                    "value": "cross_reference_validation",
                    "label": "Cross-reference and validate across sheets",
                    "description": "Check for consistency and flag conflicts"
                },
                {
                    "value": "most_detailed_wins",
                    "label": "Use most detailed/specific information",
                    "description": "Prefer more detailed specs over general ones"
                },
                {
                    "value": "ask_for_clarification",
                    "label": "Ask user to resolve conflicts",
                    "description": "Present conflicts for user resolution"
                },
                {
                    "value": "combine_complementary_info",
                    "label": "Combine complementary information intelligently",
                    "description": "Merge non-conflicting info from multiple sources"
                }
            ],
            "impact": "Ensures accuracy and consistency of SQL generation",
            "sql_section": "Information reliability and SQL accuracy"
        })

        return questions

### **📋 Example Information Discovery Session**

```json
{
  "information_discovery_analysis": {
    "session_id": "discovery_session_001",
    "excel_analysis": {
      "filename": "customer_sales_mapping.xlsx",
      "sheet_count": 6,
      "sheet_names": ["Instructions", "Source Tables", "Field Mappings", "Business Rules", "Join Logic", "Output Examples"],
      "initial_scan_results": {
        "potential_transformations_found": true,
        "join_information_detected": true,
        "filtering_criteria_found": true,
        "target_schema_partially_defined": true,
        "business_context_available": true
      }
    },
    "discovery_questions": [
      {
        "type": "transformation_data_discovery",
        "priority": "critical",
        "question": "I found potential transformation logic scattered across sheets. Where should I focus to understand column transformations?",
        "context": "Detected calculation references in 'Field Mappings' and 'Business Rules' sheets",
        "user_response": {
          "selected_option": "specific_sheet_transformations",
          "specified_sheet": "Field Mappings",
          "additional_context": "Column C has transformation formulas, Business Rules has validation logic"
        },
        "ai_action": "Focus analysis on 'Field Mappings' Column C and cross-reference with 'Business Rules'"
      },
      {
        "type": "join_information_discovery",
        "priority": "critical",
        "question": "I see a 'Join Logic' sheet. Does this contain the complete relationship information I need?",
        "context": "Found dedicated sheet that might have join conditions",
        "user_response": {
          "selected_option": "relationships_sheet",
          "specified_sheet": "Join Logic",
          "additional_context": "Contains ERD-style connections, some conditions in text format"
        },
        "ai_action": "Parse 'Join Logic' sheet for relationship definitions and convert text conditions to SQL"
      },
      {
        "type": "target_schema_discovery",
        "priority": "high",
        "question": "I found an 'Output Examples' sheet. Should I use this to understand the target structure?",
        "context": "Sheet appears to show desired output format",
        "user_response": {
          "selected_option": "output_template_sheet",
          "specified_sheet": "Output Examples",
          "additional_context": "Shows final table structure with sample data and column types"
        },
        "ai_action": "Use 'Output Examples' to define target schema and validate against field mappings"
      }
    ],
    "information_mapping_results": {
      "transformation_sources": ["Field Mappings:Column C", "Business Rules:Validation section"],
      "join_sources": ["Join Logic:ERD section", "Join Logic:Text conditions"],
      "filter_sources": ["Business Rules:Selection criteria", "Instructions:Data scope"],
      "target_schema_sources": ["Output Examples:Headers and types", "Field Mappings:Target columns"],
      "business_context_sources": ["Instructions:Overview", "Business Rules:Context section"]
    },
    "sql_generation_strategy": {
      "can_proceed": true,
      "confidence_level": "high",
      "information_completeness": 85,
      "remaining_questions": [
        "Clarify ambiguous join condition in customers->orders relationship",
        "Confirm date format preference for order_date transformation"
      ]
    }
  }
}
````

### **🔍 AI Discovery Process Flow**

```python
class InformationDiscoveryEngine:
    """Systematically discover and locate SQL building information from Excel mapping"""

    async def conduct_discovery_session(self, excel_data: dict) -> dict:
        """Run complete information discovery process"""

        # Phase 1: Initial scan and detection
        scan_results = await self.scan_for_information_patterns(excel_data)

        # Phase 2: Generate targeted discovery questions
        discovery_questions = await self.generate_discovery_questions(scan_results)

        # Phase 3: Process user responses and map information sources
        if discovery_questions:
            user_responses = await self.present_discovery_questions(discovery_questions)
            information_mapping = await self.map_information_sources(user_responses)
        else:
            information_mapping = await self.auto_detect_sources(scan_results)

        # Phase 4: Validate information completeness
        completeness_analysis = await self.analyze_completeness(information_mapping)

        # Phase 5: Generate follow-up questions for gaps
        follow_up_questions = await self.generate_gap_questions(completeness_analysis)

        return {
            "discovery_results": information_mapping,
            "completeness": completeness_analysis,
            "follow_up_questions": follow_up_questions,
            "ready_for_sql_generation": completeness_analysis["can_proceed"]
        }
```

### **💬 Example AI Discovery Conversation**

```
AI: "I've analyzed your Excel file 'sales_report_mapping.xlsx' and found 5 sheets:
'Overview', 'Table Definitions', 'Field Mappings', 'Business Logic', 'Output Format'.

Before I can generate the SQL, I need to understand where to find key information:

🔍 **TRANSFORMATION DISCOVERY**
I found references to calculations and transformations in multiple places. Which sheet should I focus on for understanding how to transform source columns into target columns?

• Field Mappings (has columns like 'Source Field' → 'Target Field' → 'Logic')
• Business Logic (contains calculation descriptions)
• Both sheets have transformation info
• I should infer transformations from the data examples

🔍 **JOIN INFORMATION DISCOVERY**
I see potential table relationship information. Where should I look for details about how tables should be joined?

• Table Definitions (appears to have foreign key references)
• Business Logic (mentions table connections in text)
• I should infer joins from common field names
• No explicit join information is provided

🔍 **TARGET STRUCTURE DISCOVERY**
Where can I find the clearest definition of what the final output should look like?

• Output Format (shows example results)
• Field Mappings (lists target column names)
• Infer from the source→target mappings
• Build structure from business requirements

Your answers will help me locate the right information and generate accurate SQL."

USER RESPONSE EXAMPLE:
"Use Field Mappings for transformations - column D has the formulas. For joins, check Table Definitions sheet - it has a simple ERD. Use Output Format sheet for the final structure."

AI FOLLOW-UP:
"Perfect! I'll focus on:
✅ Field Mappings Column D for transformation logic
✅ Table Definitions ERD for join relationships
✅ Output Format for target structure

Let me analyze these specific locations and I'll ask follow-up questions if I find any ambiguities..."
```

### **🎯 Strategic Discovery Questions Summary**

The AI asks discovery questions to:

1. **📍 Locate Information Sources**

   - "Which sheet has transformation rules?"
   - "Where are join conditions defined?"
   - "What sheet shows target structure?"

2. **🔍 Identify Data Requirements**

   - "Which columns should be used for calculations?"
   - "What fields are needed for table joins?"
   - "Which source tables are primary vs supporting?"

3. **📋 Understand Context Priorities**

   - "Should I prioritize business rules over technical mappings?"
   - "How should I handle conflicting information across sheets?"
   - "What's missing that I need to ask about?"

4. **⚡ Optimize SQL Generation**
   - "Should I create separate queries for each target table?"
   - "How should I structure complex transformations?"
   - "What performance considerations should I include?"

This ensures the AI can systematically discover and utilize all available information before generating SQL, rather than making assumptions or missing critical details.

```

    async def generate_select_strategy_questions(self, mapping_info: dict) -> List[dict]:
        """Ask about which columns to include in SELECT and how to transform them"""
        questions = []
        available_fields = mapping_info.get("target_fields", [])

        if len(available_fields) > 10:
            questions.append({
                "type": "column_selection_strategy",
                "priority": "high",
                "category": "SELECT_clause",
                "question": f"I found {len(available_fields)} target fields in your mapping. Which ones should be included in the main output?",
                "context": "The mapping document has many fields. Should I include all of them or focus on specific ones?",
                "options": [
                    {"value": "all_fields", "label": "Include all mapped fields", "fields": available_fields},
                    {"value": "core_fields", "label": "Only core/required fields", "description": "Let me select essential fields"},
                    {"value": "user_select", "label": "Let me choose specific fields", "type": "multi_select", "options": available_fields},
                    {"value": "purpose_driven", "label": "Based on analysis purpose", "description": "Select fields relevant to the stated purpose"}
                ],
                "impact": "Determines what columns appear in final SQL output",
                "sql_section": "SELECT clause"
            })

        # Questions about column transformations
        transformation_fields = [f for f in available_fields if f.get("logic") and f["logic"] != "Direct mapping"]
        if transformation_fields:
            questions.append({
                "type": "transformation_strategy",
                "priority": "high",
                "category": "SELECT_clause",
                "question": f"I found {len(transformation_fields)} fields with transformation logic. How should I handle these calculations?",
                "context": "Some fields require complex transformations from source to target",
                "details": [
                    {
                        "field": field["target_field"],
                        "source": field["source_column"],
                        "logic": field["logic"],
                        "options": [
                            "Apply transformation in SELECT clause",
                            "Create calculated field in CTE",
                            "Handle in separate subquery",
                            "Skip this transformation"
                        ]
                    } for field in transformation_fields[:3]  # Show top 3
                ],
                "impact": "Affects SQL complexity and performance",
                "sql_section": "SELECT clause / CTEs"
            })

        return questions

    async def generate_join_strategy_questions(self, mapping_info: dict) -> List[dict]:
        """Ask about JOIN strategy and table relationships"""
        questions = []
        available_tables = mapping_info.get("source_tables", [])
        relationships = mapping_info.get("relationships", [])

        if len(available_tables) > 1:
            questions.append({
                "type": "join_strategy",
                "priority": "critical",
                "category": "FROM_JOIN_clause",
                "question": f"I found {len(available_tables)} source tables. What should be the main table and how should others be joined?",
                "context": "Multiple tables need to be connected. I need to understand the relationship strategy.",
                "table_analysis": [
                    {
                        "table": table["source_table"],
                        "name": table["source_name"],
                        "note": table.get("note", ""),
                        "suggested_role": self.suggest_table_role(table, available_tables),
                        "join_options": ["Main table (FROM)", "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "Don't include"]
                    } for table in available_tables
                ],
                "relationship_hints": relationships,
                "impact": "Determines which data is included and how tables are connected",
                "sql_section": "FROM and JOIN clauses"
            })

        # Ask about specific join conditions when missing
        unclear_joins = [rel for rel in relationships if not rel.get("join_condition")]
        if unclear_joins:
            questions.append({
                "type": "join_condition_strategy",
                "priority": "critical",
                "category": "FROM_JOIN_clause",
                "question": "I found table relationships but need to confirm the join conditions. How should these tables be connected?",
                "context": "The mapping shows table relationships but join conditions need clarification",
                "unclear_relationships": [
                    {
                        "source_table": rel["source_table"],
                        "target_table": rel["target_table"],
                        "relationship_type": rel.get("relationship_type", "Unknown"),
                        "nlp_description": rel.get("nlp_join", ""),
                        "suggested_conditions": self.suggest_join_conditions(rel, available_tables)
                    } for rel in unclear_joins
                ],
                "impact": "Critical for data accuracy and query performance",
                "sql_section": "JOIN ON conditions"
            })

        return questions

    async def generate_filter_strategy_questions(self, mapping_info: dict) -> List[dict]:
        """Ask about filtering and WHERE clause strategy"""
        questions = []
        filter_info = mapping_info.get("filters", [])

        # Ask about combining multiple filters
        if len(filter_info) > 1:
            questions.append({
                "type": "filter_combination_strategy",
                "priority": "medium",
                "category": "WHERE_clause",
                "question": f"I found {len(filter_info)} different filters. How should they be combined?",
                "context": "Multiple tables have different filter conditions. Need to understand the overall filtering strategy.",
                "filter_details": [
                    {
                        "table": filter_item["source_table"],
                        "sql_filter": filter_item.get("filters_to_apply", ""),
                        "nlp_filter": filter_item.get("nlp_filters", ""),
                        "combination_options": ["AND with other filters", "OR with other filters", "Table-specific only", "Skip this filter"]
                    } for filter_item in filter_info
                ],
                "combination_strategies": [
                    "All filters must be true (AND logic)",
                    "Any filter can be true (OR logic)",
                    "Apply filters separately to each table",
                    "Let me specify custom combination logic"
                ],
                "impact": "Determines which data rows are included in results",
                "sql_section": "WHERE clause"
            })

        return questions

    async def generate_business_logic_questions(self, mapping_info: dict) -> List[dict]:
        """Ask about business logic interpretation and implementation"""
        questions = []
        business_rules = mapping_info.get("business_rules", [])
        calculated_fields = mapping_info.get("calculated_fields", [])

        if calculated_fields:
            questions.append({
                "type": "calculation_strategy",
                "priority": "high",
                "category": "business_logic",
                "question": f"I found {len(calculated_fields)} calculated fields. How should these be implemented in the SQL?",
                "context": "Business calculations can be implemented in different ways, affecting performance and readability",
                "calculation_details": [
                    {
                        "field_name": calc["target_field"],
                        "description": calc.get("definition", ""),
                        "formula": calc.get("logic", ""),
                        "context": calc.get("context", ""),
                        "implementation_options": [
                            "Direct calculation in SELECT",
                            "CTE with intermediate steps",
                            "Window function approach",
                            "Subquery calculation",
                            "Case-by-case handling"
                        ]
                    } for calc in calculated_fields[:3]
                ],
                "impact": "Affects SQL complexity, performance, and maintainability",
                "sql_section": "SELECT calculations / CTEs"
            })

        return questions

    async def generate_output_structure_questions(self, mapping_info: dict) -> List[dict]:
        """Ask about final output structure and organization"""
        questions = []

        # Ask about grouping and aggregation strategy
        potential_grouping_fields = self.identify_potential_grouping_fields(mapping_info)
        if potential_grouping_fields:
            questions.append({
                "type": "aggregation_strategy",
                "priority": "medium",
                "category": "output_structure",
                "question": "Should the output be aggregated/grouped, or show individual records?",
                "context": "Based on the field types and business purpose, I can create different output structures",
                "output_options": [
                    {
                        "type": "individual_records",
                        "description": "One row per source record",
                        "example": "Show each customer order separately"
                    },
                    {
                        "type": "grouped_summary",
                        "description": "Aggregate data by key fields",
                        "example": "One row per customer with totals/counts",
                        "suggested_grouping": potential_grouping_fields
                    },
                    {
                        "type": "hierarchical",
                        "description": "Multiple levels of aggregation",
                        "example": "Customer summary with order details"
                    },
                    {
                        "type": "user_defined",
                        "description": "Let me specify the grouping strategy"
                    }
                ],
                "impact": "Determines the granularity and structure of final results",
                "sql_section": "GROUP BY clause and aggregations"
            })

        return questions
```

### **Example Strategic Clarification Session**

```json
{
  "strategic_clarification": {
    "session_id": "strategy_abc123",
    "mapping_confidence": 0.65,
    "needs_clarification": true,
    "questions": [
      {
        "question_id": "s_1",
        "type": "join_strategy",
        "priority": "critical",
        "category": "FROM_JOIN_clause",
        "title": "🔗 Table Relationship Strategy",
        "question": "I found 3 source tables (customers, orders, products). What should be the main table and how should others be joined?",
        "context": "Your mapping document references multiple tables but I need to understand the relationship strategy for the SQL structure.",
        "table_analysis": [
          {
            "table": "crm.customers",
            "name": "Customer Master",
            "note": "Main customer table",
            "suggested_role": "Main table (good candidate for FROM clause)",
            "confidence": 0.85,
            "join_options": [
              "Main table (FROM)",
              "INNER JOIN",
              "LEFT JOIN",
              "Don't include"
            ]
          },
          {
            "table": "sales.orders",
            "name": "Order History",
            "note": "All order data",
            "suggested_role": "Related data (good for LEFT JOIN)",
            "confidence": 0.75,
            "join_options": [
              "Main table (FROM)",
              "INNER JOIN",
              "LEFT JOIN",
              "Don't include"
            ]
          },
          {
            "table": "inventory.products",
            "name": "Product Catalog",
            "note": "Current products only",
            "suggested_role": "Lookup data (good for INNER JOIN)",
            "confidence": 0.7,
            "join_options": ["INNER JOIN", "LEFT JOIN", "Don't include"]
          }
        ],
        "my_recommendation": {
          "strategy": "customers as main table, LEFT JOIN orders (include customers without orders), INNER JOIN products (only for valid products)",
          "reasoning": "Based on the purpose of customer analysis, this preserves all customers while ensuring data quality"
        }
      },
      {
        "question_id": "s_2",
        "type": "column_selection_strategy",
        "priority": "high",
        "category": "SELECT_clause",
        "title": "📊 Column Selection Strategy",
        "question": "I found 15 target fields in your mapping. Which ones should be included in the main output?",
        "context": "Including all fields makes complex SQL. I can help optimize based on your analysis purpose.",
        "field_categories": {
          "core_identity": ["customer_id", "customer_name", "email"],
          "metrics": ["total_orders", "lifetime_value", "avg_order_value"],
          "dates": ["registration_date", "last_order_date", "first_order_date"],
          "status_flags": ["customer_status", "is_active", "risk_level"],
          "detailed_attributes": [
            "phone",
            "address",
            "segment",
            "source_channel"
          ]
        },
        "my_recommendation": {
          "include": "core_identity + metrics + key_dates",
          "reasoning": "Focus on actionable insights while keeping query maintainable",
          "optional": "detailed_attributes can be added later if needed"
        }
      },
      {
        "question_id": "s_3",
        "type": "calculation_strategy",
        "priority": "high",
        "category": "business_logic",
        "title": "🧮 Calculation Implementation Strategy",
        "question": "I found customer lifetime value and status calculations. How should these be implemented?",
        "context": "Complex calculations can be done in different ways. I need to understand your preference for SQL structure.",
        "calculations": [
          {
            "field": "lifetime_value",
            "formula": "SUM(order_amount) GROUP BY customer_id",
            "complexity": "medium",
            "options": [
              "Direct aggregation in main SELECT",
              "Calculate in CTE, then join back",
              "Use window function approach"
            ]
          },
          {
            "field": "customer_status",
            "formula": "CASE WHEN conditions based on order recency and activity",
            "complexity": "high",
            "options": [
              "Complex CASE statement in SELECT",
              "Create status logic in separate CTE",
              "Use multiple CTEs for step-by-step logic"
            ]
          }
        ],
        "my_recommendation": {
          "approach": "Use CTEs for complex calculations, keep main SELECT clean",
          "reasoning": "Better readability and easier to debug/modify"
        }
      }
    ],
    "estimated_time": "5-8 minutes",
    "can_proceed_partially": true,
    "fallback_strategy": "Use conservative defaults if no response"
  }
}
```

### **Chat Response Integration**

```python
async def process_strategic_responses(self, responses: dict) -> dict:
    """Convert strategic responses into SQL generation instructions"""
    sql_strategy = {
        "main_table": None,
        "join_strategy": [],
        "column_selection": [],
        "calculation_approach": {},
        "filter_combination": "AND",
        "output_structure": "individual_records"
    }

    for question_id, response in responses.items():
        if response["type"] == "join_strategy":
            # Convert table role selections to SQL structure
            for table_choice in response["table_selections"]:
                if table_choice["role"] == "Main table (FROM)":
                    sql_strategy["main_table"] = table_choice["table"]
                elif table_choice["role"] in ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN"]:
                    sql_strategy["join_strategy"].append({
                        "table": table_choice["table"],
                        "join_type": table_choice["role"],
                        "condition": table_choice.get("join_condition")
                    })

        elif response["type"] == "column_selection_strategy":
            # Convert column selections to SELECT clause strategy
            if response["selection"] == "core_fields":
                sql_strategy["column_selection"] = response["selected_categories"]
            elif response["selection"] == "user_select":
                sql_strategy["column_selection"] = response["selected_fields"]

        elif response["type"] == "calculation_strategy":
            # Convert calculation preferences to implementation approach
            for calc in response["calculations"]:
                sql_strategy["calculation_approach"][calc["field"]] = calc["selected_approach"]

    return sql_strategy
```

    async def analyze_mapping_ambiguities(self, excel_data: dict) -> List[dict]:
        """Identify areas needing clarification from mapping documents"""
        ambiguities = []

        # Analyze data_map sheet for unclear mappings
        data_map_issues = await self.analyze_data_map_ambiguities(excel_data)
        ambiguities.extend(data_map_issues)

        # Analyze source_mapping for complex logic
        source_map_issues = await self.analyze_source_mapping_ambiguities(excel_data)
        ambiguities.extend(source_map_issues)

        # Prioritize by impact and complexity
        prioritized_ambiguities = self.prioritize_clarifications(ambiguities)

        return prioritized_ambiguities

    async def analyze_data_map_ambiguities(self, excel_data: dict) -> List[dict]:
        """Identify unclear aspects in data_map sheet"""
        ambiguities = []
        data_map_sheet = self.find_sheet_by_name(excel_data, "data_map")

        if not data_map_sheet:
            return ambiguities

        for row_idx, row in enumerate(data_map_sheet.get("data", [])[1:], 1):  # Skip header
            target_table, target_field, uniqueness, definition, quality_rules, context, valid_values, source_table, source_column, logic = row

            # Check for complex logic that needs clarification
            if logic and any(keyword in logic.lower() for keyword in ["case when", "complex", "multiple", "conditional"]):
                ambiguities.append({
                    "type": "complex_logic_clarification",
                    "priority": "high",
                    "context": f"Target: {target_table}.{target_field}",
                    "question": f"The logic for {target_table}.{target_field} appears complex: '{logic}'. Could you provide more specific rules or examples?",
                    "suggestions": [
                        f"Provide specific CASE WHEN conditions for {target_field}",
                        f"Share example input/output values for {source_column} -> {target_field}",
                        f"Clarify business rules for {context}"
                    ],
                    "row_reference": row_idx,
                    "current_logic": logic
                })

            # Check for ambiguous valid values
            if valid_values and ("etc" in valid_values.lower() or "..." in valid_values):
                ambiguities.append({
                    "type": "incomplete_valid_values",
                    "priority": "medium",
                    "context": f"Target: {target_table}.{target_field}",
                    "question": f"The valid values for {target_field} seem incomplete: '{valid_values}'. What are all possible values?",
                    "suggestions": [
                        "Provide complete list of valid values",
                        "Specify if there are dynamic/calculated values",
                        "Clarify validation rules"
                    ],
                    "row_reference": row_idx,
                    "current_values": valid_values
                })

            # Check for unclear data quality rules
            if quality_rules and any(unclear in quality_rules.lower() for unclear in ["complex", "business rule", "depends on"]):
                ambiguities.append({
                    "type": "unclear_quality_rules",
                    "priority": "medium",
                    "context": f"Target: {target_table}.{target_field}",
                    "question": f"The data quality rules for {target_field} need clarification: '{quality_rules}'. Could you specify exact validation logic?",
                    "suggestions": [
                        "Provide specific validation SQL conditions",
                        "Share examples of valid/invalid data",
                        "Clarify business rule dependencies"
                    ],
                    "row_reference": row_idx,
                    "current_rules": quality_rules
                })

        return ambiguities

    async def analyze_source_mapping_ambiguities(self, excel_data: dict) -> List[dict]:
        """Identify unclear aspects in source_mapping sheet"""
        ambiguities = []
        source_map_sheet = self.find_sheet_by_name(excel_data, "source_mapping")

        if not source_map_sheet:
            return ambiguities

        for row_idx, row in enumerate(source_map_sheet.get("data", [])[1:], 1):  # Skip header
            source_name, source_table, note, filters, nlp_filters, joins, nlp_join = row

            # Check for ambiguous NLP filters
            if nlp_filters and any(ambiguous in nlp_filters.lower() for ambiguous in ["recent", "active", "relevant", "important"]):
                ambiguities.append({
                    "type": "ambiguous_nlp_filter",
                    "priority": "high",
                    "context": f"Source: {source_name}",
                    "question": f"The filter '{nlp_filters}' for {source_name} is ambiguous. Could you specify exact criteria?",
                    "suggestions": [
                        f"Define 'recent' - last 30/90/365 days?",
                        f"Define 'active' - specific status values?",
                        f"Provide specific date ranges or status codes"
                    ],
                    "row_reference": row_idx,
                    "current_filter": nlp_filters,
                    "suggested_sql": self.suggest_filter_sql(nlp_filters)
                })

            # Check for complex joins needing clarification
            if nlp_join and any(complex_word in nlp_join.lower() for complex_word in ["sometimes", "depending", "if available", "when possible"]):
                ambiguities.append({
                    "type": "conditional_join_clarification",
                    "priority": "high",
                    "context": f"Source: {source_name}",
                    "question": f"The join logic '{nlp_join}' has conditional behavior. Should this be LEFT JOIN, INNER JOIN, or something else?",
                    "suggestions": [
                        "Specify exact join type (INNER/LEFT/RIGHT)",
                        "Clarify join conditions and when to apply them",
                        "Provide examples of edge cases"
                    ],
                    "row_reference": row_idx,
                    "current_join": nlp_join,
                    "join_options": ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN"]
                })

            # Check for missing join conditions
            if joins and not any(join_keyword in joins.upper() for join_keyword in ["ON", "USING", "WHERE"]):
                ambiguities.append({
                    "type": "missing_join_condition",
                    "priority": "critical",
                    "context": f"Source: {source_name}",
                    "question": f"The join '{joins}' is missing specific join conditions. What columns should be used to join?",
                    "suggestions": [
                        "Specify exact ON conditions (table1.col = table2.col)",
                        "Provide foreign key relationships",
                        "Clarify composite key joins if needed"
                    ],
                    "row_reference": row_idx,
                    "current_join": joins
                })

        return ambiguities

    async def generate_clarification_chat(self, ambiguities: List[dict]) -> dict:
        """Generate chat-based clarification questions for frontend"""
        if not ambiguities:
            return {"status": "no_clarifications_needed", "questions": []}

        # Group by priority and type
        critical_questions = [q for q in ambiguities if q["priority"] == "critical"]
        high_questions = [q for q in ambiguities if q["priority"] == "high"]
        medium_questions = [q for q in ambiguities if q["priority"] == "medium"]

        chat_session = {
            "session_id": self.session_id,
            "status": "awaiting_clarifications",
            "total_questions": len(ambiguities),
            "critical_count": len(critical_questions),
            "estimated_time": f"{len(ambiguities) * 2-3} minutes",
            "questions": []
        }

        # Start with critical questions
        for idx, question in enumerate(critical_questions + high_questions + medium_questions):
            chat_question = {
                "question_id": f"q_{idx + 1}",
                "type": question["type"],
                "priority": question["priority"],
                "title": self.generate_question_title(question),
                "message": question["question"],
                "context_info": question["context"],
                "suggestions": question["suggestions"],
                "input_type": self.determine_input_type(question),
                "validation_rules": self.get_validation_rules(question),
                "examples": self.generate_examples(question),
                "skip_allowed": question["priority"] in ["medium", "low"]
            }

            chat_session["questions"].append(chat_question)

        return chat_session

    def determine_input_type(self, question: dict) -> dict:
        """Determine appropriate UI input type for question"""
        question_type = question["type"]

        input_types = {
            "complex_logic_clarification": {
                "type": "textarea",
                "placeholder": "Provide detailed logic or SQL CASE statement",
                "validation": "min_length:10"
            },
            "incomplete_valid_values": {
                "type": "multi_select_with_custom",
                "options": self.extract_existing_values(question.get("current_values", "")),
                "allow_custom": True,
                "placeholder": "Add additional valid values"
            },
            "ambiguous_nlp_filter": {
                "type": "select_with_custom",
                "options": ["Last 30 days", "Last 90 days", "Last year", "Active status only", "Custom SQL condition"],
                "custom_input": "textarea"
            },
            "conditional_join_clarification": {
                "type": "radio_with_details",
                "options": question.get("join_options", ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN"]),
                "details_required": True
            },
            "missing_join_condition": {
                "type": "join_builder",
                "tables": self.extract_tables_from_context(question),
                "suggested_columns": self.suggest_join_columns(question)
            }
        }

        return input_types.get(question_type, {"type": "textarea", "placeholder": "Please provide clarification"})

### **Example Chat Flow for Complex Mapping**

```json
{
  "chat_session": {
    "session_id": "clarify_789xyz",
    "status": "awaiting_clarifications",
    "total_questions": 5,
    "critical_count": 2,
    "current_question": 1,
    "questions": [
      {
        "question_id": "q_1",
        "type": "missing_join_condition",
        "priority": "critical",
        "title": "🔗 Join Condition Missing",
        "message": "The join between 'crm.customers' and 'sales.orders' is missing specific conditions. What columns should be used to join these tables?",
        "context_info": "Source: Customer Master -> Order History",
        "suggestions": [
          "customers.id = orders.customer_id",
          "customers.customer_code = orders.cust_code",
          "Custom join condition"
        ],
        "input_type": {
          "type": "join_builder",
          "left_table": "crm.customers",
          "right_table": "sales.orders",
          "suggested_columns": {
            "customers": ["id", "customer_id", "customer_code"],
            "orders": ["customer_id", "cust_id", "cust_code"]
          }
        },
        "skip_allowed": false
      },
      {
        "question_id": "q_2",
        "type": "ambiguous_nlp_filter",
        "priority": "high",
        "title": "📅 Define 'Recent' Data",
        "message": "The filter 'only active customers from this year' for Customer Master needs clarification. What exactly defines 'this year' and 'active'?",
        "context_info": "Source: crm.customers filter",
        "suggestions": [
          "Last 365 days",
          "Calendar year 2024",
          "Fiscal year",
          "Custom date range"
        ],
        "input_type": {
          "type": "select_with_custom",
          "options": [
            {
              "value": "calendar_year",
              "label": "Calendar year (2024-01-01 to 2024-12-31)"
            },
            { "value": "last_365", "label": "Last 365 days from today" },
            { "value": "fiscal_year", "label": "Fiscal year (specify dates)" },
            { "value": "custom", "label": "Custom date range" }
          ]
        },
        "skip_allowed": true
      },
      {
        "question_id": "q_3",
        "type": "complex_logic_clarification",
        "priority": "high",
        "title": "🧮 Complex Status Logic",
        "message": "The logic for orders.order_status appears complex: 'CASE WHEN status_code = 1 THEN pending WHEN status_code = 2 THEN confirmed END'. Are there other status codes to handle?",
        "context_info": "Target: orders.order_status",
        "current_logic": "CASE WHEN status_code = 1 THEN 'pending' WHEN status_code = 2 THEN 'confirmed' END",
        "input_type": {
          "type": "case_statement_builder",
          "current_cases": [
            { "condition": "status_code = 1", "result": "pending" },
            { "condition": "status_code = 2", "result": "confirmed" }
          ],
          "allow_add_cases": true,
          "require_else_clause": true
        },
        "examples": [
          "What should happen when status_code = 3?",
          "What's the default for unknown status codes?",
          "Are there any other status transformations needed?"
        ],
        "skip_allowed": true
      }
    ]
  }
}
```

### **Chat Response Processing**

```python
class ChatResponseProcessor:
    """Process user responses from chat clarifications"""

    async def process_chat_responses(self, session_id: str, responses: dict) -> dict:
        """Convert chat responses back to structured mapping data"""
        processed_responses = {
            "session_id": session_id,
            "clarifications_resolved": 0,
            "updated_mappings": {},
            "remaining_ambiguities": [],
            "ready_for_generation": False
        }

        for question_id, response in responses.items():
            question_type = response.get("question_type")

            if question_type == "missing_join_condition":
                # Convert join builder response to SQL
                join_sql = self.build_join_from_response(response)
                processed_responses["updated_mappings"][question_id] = {
                    "type": "join_condition",
                    "sql": join_sql,
                    "confidence": 0.95
                }

            elif question_type == "ambiguous_nlp_filter":
                # Convert filter selection to SQL WHERE clause
                filter_sql = self.build_filter_from_response(response)
                processed_responses["updated_mappings"][question_id] = {
                    "type": "filter_condition",
                    "sql": filter_sql,
                    "confidence": 0.90
                }

            elif question_type == "complex_logic_clarification":
                # Convert case statement to proper SQL
                case_sql = self.build_case_from_response(response)
                processed_responses["updated_mappings"][question_id] = {
                    "type": "transformation_logic",
                    "sql": case_sql,
                    "confidence": 0.85
                }

            processed_responses["clarifications_resolved"] += 1

        # Check if we have enough information to proceed
        critical_responses = [r for r in responses.values() if r.get("priority") == "critical"]
        processed_responses["ready_for_generation"] = len(critical_responses) > 0

        return processed_responses

    def build_join_from_response(self, response: dict) -> str:
        """Convert join builder response to SQL"""
        left_table = response["data"]["left_table"]
        right_table = response["data"]["right_table"]
        left_column = response["data"]["left_column"]
        right_column = response["data"]["right_column"]
        join_type = response["data"].get("join_type", "INNER")

        return f"{join_type} JOIN {right_table} ON {left_table}.{left_column} = {right_table}.{right_column}"

    def build_filter_from_response(self, response: dict) -> str:
        """Convert filter selection to SQL WHERE clause"""
        filter_type = response["data"]["selected_option"]

        if filter_type == "calendar_year":
            return "created_date >= '2024-01-01' AND created_date < '2025-01-01'"
        elif filter_type == "last_365":
            return "created_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 365 DAY)"
        elif filter_type == "custom":
            start_date = response["data"]["custom_start_date"]
            end_date = response["data"]["custom_end_date"]
            return f"created_date >= '{start_date}' AND created_date <= '{end_date}'"

        return "1=1"  # Default no filter
```

### **SSE Events for Chat Interaction**

```json
{
  "event": "clarification_needed",
  "data": {
    "section": "input_processing",
    "phase": "analysis_complete",
    "message": "Found 5 items needing clarification before SQL generation",
    "details": {
      "total_questions": 5,
      "critical_questions": 2,
      "estimated_time": "10-15 minutes",
      "can_skip_optional": true,
      "chat_session_id": "clarify_789xyz"
    }
  }
}
```

```json
{
  "event": "clarification_progress",
  "data": {
    "section": "chat_interaction",
    "phase": "question_answered",
    "message": "Clarification received for join conditions",
    "details": {
      "question_answered": "q_1",
      "questions_remaining": 4,
      "progress": "20%",
      "can_proceed_partial": false,
      "estimated_completion": "8-12 minutes"
    }
  }
}
```

```

```

---

## 12. **Output Format Requirements**

### 🎯 **Structured SQL Output Specification**

**Core Principle:** Generate clean, well-documented, executable SQL with comprehensive metadata and validation information

#### **📋 Primary Output Structure**

### **Complete API Response Format**

```json
{
  "request_id": "req_789abc123",
  "status": "completed",
  "processing_time_seconds": 67.5,
  "generated_sql": {
    "final_query": "-- Customer Lifetime Value Analysis\n-- Generated on: 2025-08-13 14:30:22 UTC\n-- Intelligence Level: Balanced\n-- Target Environment: Databricks\n\nWITH customer_base AS (\n  SELECT \n    c.customer_id,\n    c.first_name,\n    c.last_name,\n    c.email,\n    c.registration_date,\n    COUNT(DISTINCT o.order_id) as total_orders,\n    SUM(o.order_amount) as lifetime_value,\n    AVG(o.order_amount) as avg_order_value,\n    MAX(o.order_date) as last_order_date,\n    DATEDIFF(CURRENT_DATE(), MAX(o.order_date)) as days_since_last_order\n  FROM customers c\n  LEFT JOIN orders o ON c.customer_id = o.customer_id\n  WHERE c.registration_date >= '2024-01-01'\n  GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.registration_date\n),\nvalue_segments AS (\n  SELECT \n    *,\n    CASE \n      WHEN lifetime_value >= 1000 THEN 'High Value'\n      WHEN lifetime_value >= 500 THEN 'Medium Value'\n      WHEN lifetime_value >= 100 THEN 'Low Value'\n      ELSE 'New/Inactive'\n    END as value_segment,\n    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY lifetime_value) OVER () as median_clv\n  FROM customer_base\n)\nSELECT \n  customer_id,\n  CONCAT(first_name, ' ', last_name) as customer_name,\n  email,\n  registration_date,\n  total_orders,\n  ROUND(lifetime_value, 2) as lifetime_value,\n  ROUND(avg_order_value, 2) as avg_order_value,\n  last_order_date,\n  days_since_last_order,\n  value_segment,\n  ROUND(median_clv, 2) as median_customer_value,\n  CASE \n    WHEN days_since_last_order <= 30 THEN 'Active'\n    WHEN days_since_last_order <= 90 THEN 'At Risk'\n    ELSE 'Churned'\n  END as customer_status\nFROM value_segments\nORDER BY lifetime_value DESC, last_order_date DESC;",

    "query_sections": {
      "cte_definitions": [
        {
          "name": "customer_base",
          "purpose": "Aggregate customer order data and calculate core metrics",
          "complexity": "medium",
          "estimated_rows": 5000,
          "key_calculations": [
            "total_orders",
            "lifetime_value",
            "avg_order_value"
          ]
        },
        {
          "name": "value_segments",
          "purpose": "Categorize customers by value and calculate percentiles",
          "complexity": "low",
          "estimated_rows": 5000,
          "key_calculations": ["value_segment", "median_clv"]
        }
      ],
      "main_select": {
        "purpose": "Final customer analysis with status classification",
        "output_columns": 12,
        "estimated_rows": 5000,
        "sort_strategy": "lifetime_value DESC, last_order_date DESC"
      },
      "joins_used": [
        {
          "type": "LEFT JOIN",
          "tables": ["customers", "orders"],
          "condition": "c.customer_id = o.customer_id",
          "purpose": "Include all customers even without orders",
          "estimated_impact": "1:N relationship, may multiply rows"
        }
      ],
      "filters_applied": [
        {
          "column": "registration_date",
          "condition": ">= '2024-01-01'",
          "purpose": "Focus on recent customers",
          "selectivity": "high"
        }
      ]
    },

    "metadata": {
      "query_type": "analytical_report",
      "complexity_score": 7.5,
      "estimated_execution_time": "2-5 seconds",
      "estimated_cost": "low",
      "tables_involved": ["customers", "orders"],
      "environment_optimizations": {
        "databricks_specific": [
          "Uses PERCENTILE_CONT for statistical analysis",
          "Optimized for Delta Lake with predicate pushdown",
          "CONCAT function for string concatenation"
        ]
      },
      "performance_notes": [
        "Consider indexing on customer_id for join performance",
        "registration_date filter enables partition pruning",
        "GROUP BY may require shuffle operation"
      ]
    }
  },

  "generation_details": {
    "intelligence_level_used": "balanced",
    "ai_reasoning_chain": [
      {
        "step": "excel_analysis",
        "decision": "Identified customer and order tables with 1:M relationship",
        "confidence": 0.95
      },
      {
        "step": "business_logic_inference",
        "decision": "Purpose indicates lifetime value analysis - added CLV calculations",
        "confidence": 0.87
      },
      {
        "step": "segmentation_strategy",
        "decision": "Added value-based customer segmentation with percentile analysis",
        "confidence": 0.82
      },
      {
        "step": "environment_optimization",
        "decision": "Applied Databricks-specific functions and optimizations",
        "confidence": 0.91
      }
    ],
    "sections_processed": [
      {
        "section": "dependency_analysis",
        "status": "completed",
        "duration_seconds": 12.3,
        "ai_calls": 1,
        "tokens_used": 1250,
        "cost": 0.0375
      },
      {
        "section": "join_construction",
        "status": "completed",
        "duration_seconds": 18.7,
        "ai_calls": 2,
        "tokens_used": 2100,
        "cost": 0.063
      },
      {
        "section": "cte_generation",
        "status": "completed",
        "duration_seconds": 21.4,
        "ai_calls": 2,
        "tokens_used": 1890,
        "cost": 0.0567
      },
      {
        "section": "final_select",
        "status": "completed",
        "duration_seconds": 15.1,
        "ai_calls": 1,
        "tokens_used": 980,
        "cost": 0.0294
      }
    ],
    "fallbacks_used": [],
    "validation_results": {
      "syntax_check": "passed",
      "performance_analysis": "acceptable",
      "security_scan": "passed",
      "test_execution": {
        "status": "success",
        "sample_rows_returned": 100,
        "execution_time_ms": 1847
      }
    }
  },

  "token_usage": {
    "total_input_tokens": 6220,
    "total_output_tokens": 2180,
    "total_tokens": 8400,
    "total_cost_usd": 0.1866,
    "provider_breakdown": {
      "openai": {
        "calls": 5,
        "input_tokens": 4850,
        "output_tokens": 1650,
        "cost": 0.1446
      },
      "claude": {
        "calls": 1,
        "input_tokens": 1370,
        "output_tokens": 530,
        "cost": 0.042
      }
    },
    "efficiency_metrics": {
      "tokens_per_output_line": 120,
      "cost_per_query_line": 0.0024,
      "quality_score": 0.89
    }
  },

  "recommendations": {
    "query_improvements": [
      {
        "type": "performance",
        "suggestion": "Consider partitioning customers table by registration_date for better query performance",
        "impact": "medium",
        "implementation": "ALTER TABLE customers CLUSTER BY registration_date"
      },
      {
        "type": "business_logic",
        "suggestion": "Add recency scoring to complement lifetime value analysis",
        "impact": "low",
        "implementation": "Include days_since_last_order in segmentation logic"
      }
    ],
    "data_quality_checks": [
      {
        "check": "null_customer_ids",
        "query": "SELECT COUNT(*) FROM customers WHERE customer_id IS NULL",
        "expected_result": 0
      },
      {
        "check": "future_order_dates",
        "query": "SELECT COUNT(*) FROM orders WHERE order_date > CURRENT_DATE()",
        "expected_result": 0
      }
    ],
    "monitoring_queries": [
      {
        "purpose": "track_daily_clv",
        "query": "SELECT DATE(created_at), AVG(lifetime_value) FROM customer_analysis GROUP BY DATE(created_at)",
        "frequency": "daily"
      }
    ]
  },

  "execution_instructions": {
    "prerequisites": [
      "Ensure customers and orders tables exist in the specified schema",
      "Verify Databricks warehouse is running and accessible",
      "Confirm user has SELECT permissions on both tables"
    ],
    "execution_steps": [
      {
        "step": 1,
        "action": "Test query with LIMIT 10 to verify structure",
        "command": "-- Add LIMIT 10 to the final SELECT for testing"
      },
      {
        "step": 2,
        "action": "Execute full query and save results",
        "command": "CREATE OR REPLACE TABLE analytics.customer_lifetime_value AS (/* full query */)"
      },
      {
        "step": 3,
        "action": "Verify data quality with recommended checks",
        "command": "-- Run data quality validation queries"
      }
    ],
    "troubleshooting": {
      "common_issues": [
        {
          "error": "Table 'customers' not found",
          "solution": "Verify table exists in specified catalog.schema",
          "check_query": "SHOW TABLES IN main.analytics LIKE 'customers'"
        },
        {
          "error": "Column 'customer_id' not found",
          "solution": "Check actual column names in source tables",
          "check_query": "DESCRIBE customers"
        }
      ]
    }
  }
}
```

#### **📊 Alternative Output Formats**

### **Simplified Output (When Complexity is Low)**

```json
{
  "request_id": "req_simple_456",
  "status": "completed",
  "generated_sql": {
    "final_query": "-- Simple customer list\nSELECT \n  customer_id,\n  first_name,\n  last_name,\n  email\nFROM customers\nWHERE registration_date >= '2024-01-01'\nORDER BY last_name, first_name;",
    "complexity_score": 2.0,
    "estimated_execution_time": "< 1 second"
  },
  "token_usage": {
    "total_tokens": 1250,
    "total_cost_usd": 0.0375
  },
  "processing_time_seconds": 8.2
}
```

### **Error Output (When Generation Fails)**

```json
{
  "request_id": "req_error_789",
  "status": "error",
  "error": {
    "type": "insufficient_data",
    "message": "Unable to generate SQL: Excel data lacks sufficient table relationship information",
    "suggestions": [
      "Add a relationships sheet with table connections",
      "Include sample data to infer column types",
      "Specify join conditions in metadata"
    ],
    "partial_results": {
      "tables_identified": ["customers", "orders"],
      "columns_found": ["customer_id", "first_name", "order_amount"],
      "missing_information": ["join_conditions", "business_logic"]
    }
  },
  "token_usage": {
    "total_tokens": 890,
    "total_cost_usd": 0.0267
  },
  "processing_time_seconds": 15.3
}
```

---

**Status:** ✅ **DOCUMENTED** - Comprehensive input/output format specifications

**Input Format Features:**

- **Flexible Excel data structure** supporting multiple sheet patterns
- **Intelligent pattern recognition** for table definitions, relationships, and business logic
- **Comprehensive validation** with actionable error messages
- **Metadata enrichment** for better SQL generation context

**Output Format Features:**

- **Complete executable SQL** with environment-specific optimizations
- **Detailed metadata** including complexity scores and performance estimates
- **AI reasoning chain** showing decision-making process
- **Token usage breakdown** with cost analysis
- **Actionable recommendations** for query improvements
- **Execution instructions** with troubleshooting guidance
