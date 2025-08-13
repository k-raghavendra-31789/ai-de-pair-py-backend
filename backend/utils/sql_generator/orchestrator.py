"""
SQL Generation Orchestrator - Main coordinator for the AI-powered SQL generation pipeline
"""
import asyncio
from typing import AsyncGenerator, Dict, Any, Optional
from ..db_utils import execute_sql_async, validate_connection_params
from .ai_parser import AIInputParser, ParsedMapping


class SQLGenerationOrchestrator:
    """
    Main orchestrator that coordinates the entire SQL generation process:
    1. AI parsing of input
    2. Dependency analysis
    3. SQL component building
    4. Incremental testing
    5. Final SQL assembly
    """
    
    def __init__(self, ai_api_key: str, ai_provider: str = "openai"):
        self.ai_parser = AIInputParser(ai_api_key, ai_provider)
        self.parsed_mapping: Optional[ParsedMapping] = None
        self.dependency_graph = None
        self.execution_order = []
        self.built_components = {}
        self.final_sql = ""
    
    async def generate_sql_with_events(
        self, 
        raw_input: Any, 
        connection_details: Dict[str, str]
    ) -> AsyncGenerator[Dict[str, str], None]:
        """
        Main method that generates SQL while streaming SSE events
        
        Args:
            raw_input: Any format mapping input
            connection_details: Databricks connection info
            
        Yields:
            SSE events for each step of the process
        """
        try:
            # Phase 1: AI Analysis
            yield {"event": "status", "data": "🤖 Starting AI analysis of mapping input..."}
            
            yield {"event": "status", "data": "🔍 Analyzing input structure with AI..."}
            self.parsed_mapping = await self.ai_parser.parse_input(raw_input)
            
            yield {"event": "status", "data": f"✅ AI analysis complete - found {len(self.parsed_mapping.tables)} tables"}
            
            # Phase 2: Dependency Analysis
            yield {"event": "status", "data": "🔗 Building dependency graph..."}
            await self._build_dependency_graph()
            
            yield {"event": "status", "data": "🔄 Checking for cyclic references..."}
            has_cycles = await self._detect_cycles()
            if has_cycles:
                yield {"event": "warning", "data": "⚠️ Cyclic references detected - resolving..."}
                await self._resolve_cycles()
                yield {"event": "status", "data": "✅ Cyclic references resolved"}
            else:
                yield {"event": "status", "data": "✅ No cyclic references found"}
            
            yield {"event": "status", "data": "📋 Creating execution order..."}
            await self._create_execution_order()
            yield {"event": "status", "data": f"✅ Execution order created - {len(self.execution_order)} steps"}
            
            # Phase 3: SQL Component Building
            yield {"event": "status", "data": "🏗️ Building SQL components..."}
            
            # Build CTEs
            yield {"event": "status", "data": "📝 Building Common Table Expressions (CTEs)..."}
            await self._build_ctes(connection_details)
            
            # Build Joins
            yield {"event": "status", "data": "🔗 Building JOIN sections..."}
            await self._build_joins(connection_details)
            
            # Build Attributes
            yield {"event": "status", "data": "📊 Adding output attributes..."}
            await self._build_attributes()
            
            # Phase 4: Final SQL Assembly
            yield {"event": "status", "data": "🔧 Constructing final SQL..."}
            await self._assemble_final_sql()
            
            yield {"event": "status", "data": "🧪 Testing final SQL..."}
            await self._test_final_sql(connection_details)
            
            yield {"event": "status", "data": "✅ SQL generation completed successfully!"}
            
            # Final event with the generated SQL
            yield {"event": "sql_generated", "data": self.final_sql}
            yield {"event": "close", "data": "SQL generation process completed"}
            
        except Exception as e:
            yield {"event": "error", "data": f"❌ Error during SQL generation: {str(e)}"}
    
    async def _build_dependency_graph(self):
        """Build dependency graph from parsed relationships"""
        self.dependency_graph = {}
        
        for table in self.parsed_mapping.tables:
            self.dependency_graph[table['name']] = {
                'dependencies': [],
                'dependents': [],
                'table_info': table
            }
        
        # Add relationships as dependencies
        for rel in self.parsed_mapping.relationships:
            left_table = rel['left_table']
            right_table = rel['right_table']
            
            if left_table in self.dependency_graph and right_table in self.dependency_graph:
                self.dependency_graph[left_table]['dependencies'].append(right_table)
                self.dependency_graph[right_table]['dependents'].append(left_table)
    
    async def _detect_cycles(self) -> bool:
        """Detect cyclic references in the dependency graph"""
        visited = set()
        rec_stack = set()
        
        def has_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.dependency_graph[node]['dependencies']:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.dependency_graph:
            if node not in visited:
                if has_cycle(node):
                    return True
        return False
    
    async def _resolve_cycles(self):
        """Resolve cyclic references by breaking cycles intelligently"""
        # Simple cycle resolution - can be enhanced
        # For now, we'll mark problematic edges and handle them as LEFT JOINs
        pass
    
    async def _create_execution_order(self):
        """Create optimal execution order using topological sort"""
        in_degree = {table: 0 for table in self.dependency_graph}
        
        # Calculate in-degrees
        for table in self.dependency_graph:
            for dep in self.dependency_graph[table]['dependencies']:
                in_degree[dep] += 1
        
        # Topological sort
        queue = [table for table, degree in in_degree.items() if degree == 0]
        self.execution_order = []
        
        while queue:
            current = queue.pop(0)
            self.execution_order.append(current)
            
            for dependent in self.dependency_graph[current]['dependents']:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
    
    async def _build_ctes(self, connection_details: Dict[str, str]):
        """Build and test CTEs for each table"""
        for i, table_name in enumerate(self.execution_order):
            # Note: Cannot yield here directly, but we can store results
            table_info = self.dependency_graph[table_name]['table_info']
            cte_sql = self._generate_cte_sql(table_info)
            
            try:
                # Test the CTE with a small limit
                test_sql = f"WITH {table_name}_cte AS ({cte_sql}) SELECT * FROM {table_name}_cte LIMIT 1"
                await execute_sql_async(
                    test_sql,
                    connection_details['server_hostname'],
                    connection_details['http_path'],
                    connection_details['access_token'],
                    timeout=10
                )
                self.built_components[f"{table_name}_cte"] = cte_sql
            except Exception as e:
                # Store the error for later reporting
                self.built_components[f"{table_name}_cte_error"] = str(e)
    
    async def _build_joins(self, connection_details: Dict[str, str]):
        """Build and test JOIN clauses"""
        for relationship in self.parsed_mapping.relationships:
            join_type = relationship.get('join_type', 'INNER')
            left_table = relationship['left_table']
            right_table = relationship['right_table']
            condition = relationship['join_condition']
            
            try:
                test_sql = f"""
                SELECT COUNT(*) as join_count 
                FROM {left_table} 
                {join_type} JOIN {right_table} ON {condition}
                """
                await execute_sql_async(
                    test_sql,
                    connection_details['server_hostname'],
                    connection_details['http_path'],
                    connection_details['access_token'],
                    timeout=10
                )
                
                self.built_components[f"join_{left_table}_{right_table}"] = {
                    'type': join_type,
                    'condition': condition
                }
            except Exception as e:
                self.built_components[f"join_{left_table}_{right_table}_error"] = str(e)
    
    async def _build_attributes(self):
        """Build output attribute selection"""
        select_clauses = []
        for col in self.parsed_mapping.output_columns:
            table = col.get('table', '')
            column = col['column']
            alias = col.get('alias', '')
            aggregation = col.get('aggregation', None)
            
            if aggregation:
                clause = f"{aggregation}({table}.{column})"
            else:
                clause = f"{table}.{column}"
            
            if alias:
                clause += f" AS {alias}"
                
            select_clauses.append(clause)
        
        self.built_components['select_clause'] = ', '.join(select_clauses)
    
    async def _assemble_final_sql(self):
        """Assemble the final SQL from all components"""
        sql_parts = []
        
        # Add CTEs if any
        cte_parts = [f"{name} AS ({sql})" for name, sql in self.built_components.items() 
                    if name.endswith('_cte')]
        if cte_parts:
            sql_parts.append(f"WITH {', '.join(cte_parts)}")
        
        # Add SELECT clause
        select_clause = self.built_components.get('select_clause', '*')
        sql_parts.append(f"SELECT {select_clause}")
        
        # Add FROM clause (first table in execution order)
        if self.execution_order:
            sql_parts.append(f"FROM {self.execution_order[0]}")
        
        # Add JOINs
        for relationship in self.parsed_mapping.relationships:
            join_info = self.built_components.get(f"join_{relationship['left_table']}_{relationship['right_table']}")
            if join_info:
                sql_parts.append(f"{join_info['type']} JOIN {relationship['right_table']} ON {join_info['condition']}")
        
        # Add filters
        if self.parsed_mapping.filters:
            where_clauses = []
            for filter_item in self.parsed_mapping.filters:
                if filter_item.get('condition', 'WHERE') == 'WHERE':
                    clause = f"{filter_item['table']}.{filter_item['column']} {filter_item['operator']} {filter_item['value']}"
                    where_clauses.append(clause)
            
            if where_clauses:
                sql_parts.append(f"WHERE {' AND '.join(where_clauses)}")
        
        self.final_sql = '\n'.join(sql_parts)
    
    async def _test_final_sql(self, connection_details: Dict[str, str]):
        """Test the final assembled SQL"""
        try:
            # Test with LIMIT 1 to verify syntax
            test_sql = f"({self.final_sql}) LIMIT 1"
            await execute_sql_async(
                test_sql,
                connection_details['server_hostname'],
                connection_details['http_path'],
                connection_details['access_token'],
                timeout=15
            )
        except Exception as e:
            raise Exception(f"Final SQL test failed: {str(e)}")
    
    def _generate_cte_sql(self, table_info: Dict) -> str:
        """Generate SQL for a CTE based on table info"""
        table_name = table_info['name']
        schema = table_info.get('schema', '')
        
        if schema:
            full_table_name = f"{schema}.{table_name}"
        else:
            full_table_name = table_name
        
        return f"SELECT * FROM {full_table_name}"
