"""
Task Orchestration Protocol Module

This module implements a Collaborative Task Orchestration protocol for decomposing complex tasks,
matching them to appropriate agents, and coordinating their execution across multiple agents.
It enables Coherence Weaver to effectively manage distributed multi-agent workflows.
"""

import uuid
import asyncio
from typing import Dict, List, Any, Optional

from coherence_weaver.src.agents.base_agent import BaseAgent
from coherence_weaver.src.agents.coherence_weaver_llm_agent import CoherenceWeaverLLMAgent
from coherence_weaver.src.models.agent_models import Message, Conversation
from coherence_weaver.src.services.service_manager import ServiceManager
from coherence_weaver.src.a2a_client import A2AClient


class TaskOrchestration:
    """
    Implements collaborative task orchestration across multiple agents.
    
    This protocol uses a sequential workflow to:
    1. Analyze complex tasks to identify component subtasks and required capabilities
    2. Match subtasks to the most appropriate agents based on their capabilities
    3. Create coordination structures and feedback mechanisms for multi-agent tasks
    """
    
    def __init__(self, core_agent: BaseAgent, service_manager: ServiceManager, a2a_client: Optional[A2AClient] = None):
        """
        Initialize the Task Orchestration Protocol.
        
        Args:
            core_agent: The main Coherence Weaver agent
            service_manager: Service manager providing access to memory and session services
            a2a_client: Optional A2A client for communicating with external agents
        """
        self.core_agent = core_agent
        self.service_manager = service_manager
        self.memory_service = service_manager.get_memory_service()
        self.session_service = service_manager.get_session_service()
        self.a2a_client = a2a_client or A2AClient(auth_token=core_agent.get_auth_token())
        
        # Initialize specialized agents for the task orchestration workflow
        self.task_analyzer = CoherenceWeaverLLMAgent(
            agent_id="task_analyzer",
            name="Task Analyzer",
            description="Analyzes complex tasks to identify component subtasks and required capabilities",
            system_prompt="""
            Your role is to decompose complex tasks into clearly defined components by:
            1. Identifying the core objectives and constraints of the task
            2. Breaking the task into logical subtasks with clear inputs and outputs
            3. Determining what capabilities or skills are needed for each subtask
            4. Identifying dependencies between subtasks
            
            Focus on creating a clear, modular structure that enables effective delegation.
            Generate a structured analysis that includes:
            - Core task objectives and constraints
            - Subtask breakdown with clear descriptions, inputs, and outputs
            - Capability requirements for each subtask
            - Dependency map showing task relationships
            """
        )
        
        self.agent_matcher = CoherenceWeaverLLMAgent(
            agent_id="agent_matcher",
            name="Agent Matcher",
            description="Matches subtasks to the most appropriate agents based on their capabilities",
            system_prompt="""
            Your role is to match tasks with the most appropriate agents by:
            1. Analyzing the capability requirements for each subtask
            2. Comparing these requirements with the known capabilities of available agents
            3. Considering past performance and reliability for similar tasks
            4. Optimizing for complementary capabilities when multiple agents are involved
            
            Prioritize finding the right fit rather than just technical capability.
            Generate a structured matching plan that includes:
            - Subtask-to-agent assignments with clear rationales
            - Capability alignment analysis for each match
            - Identification of any capability gaps
            - Suggestions for agent coordination at capability boundary points
            """
        )
        
        self.coordination_manager = CoherenceWeaverLLMAgent(
            agent_id="coordination_manager",
            name="Coordination Manager",
            description="Creates coordination structures and feedback mechanisms for multi-agent tasks",
            system_prompt="""
            Your role is to create effective coordination structures for multi-agent collaboration by:
            1. Defining clear interfaces between different agents' work
            2. Establishing communication protocols appropriate to the task
            3. Creating feedback mechanisms that help all participating agents improve
            4. Monitoring progress and adjusting coordination as needed
            
            Focus on minimizing dependency while maximizing collective intelligence.
            Generate a structured coordination plan that includes:
            - Interface definitions for agent interactions
            - Communication protocols and schedules
            - Feedback mechanisms and quality checks
            - Progress monitoring approach and adjustment triggers
            """
        )
    
    async def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze a complex task to identify component subtasks and required capabilities.
        
        Args:
            task_description: Description of the task to analyze
            
        Returns:
            Task analysis results
        """
        # Generate prompt for task analysis
        prompt = f"""
        Analyze this complex task and decompose it into a modular structure:
        
        TASK: {task_description}
        
        Please provide:
        1. Core task objectives and constraints
        2. Subtask breakdown with clear descriptions, inputs, and outputs
        3. Capability requirements for each subtask
        4. Dependency map showing task relationships
        """
        
        # Process with the task analyzer
        task_analysis = await self.task_analyzer.process_message(
            message=Message(
                role="user",
                content=prompt,
                metadata={"task": "task_analysis", "original_task": task_description}
            ),
            conversation_id=f"task_analysis_{uuid.uuid4().hex[:8]}"
        )
        
        # Store the task analysis in memory
        analysis_id = f"task_analysis_{uuid.uuid4().hex[:8]}"
        await self.memory_service.store(
            analysis_id,
            {"analysis": task_analysis, "original_task": task_description, "timestamp": str(uuid.uuid4())}
        )
        
        return {
            "analysis_id": analysis_id,
            "analysis": task_analysis,
            "original_task": task_description
        }
    
    async def match_agents(self, task_analysis: Dict[str, Any], available_agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Match subtasks to the most appropriate agents based on their capabilities.
        
        Args:
            task_analysis: Analysis of the task including subtasks and capability requirements
            available_agents: List of available agents with their capabilities
            
        Returns:
            Agent matching results
        """
        # Format available agents information for the prompt
        agents_info = "\n\n".join([
            f"AGENT {i+1}: {agent.get('name', 'Unknown')}\n"
            f"ID: {agent.get('id', 'unknown_id')}\n"
            f"Description: {agent.get('description', 'No description')}\n"
            f"Capabilities: {', '.join(agent.get('capabilities', []))}\n"
            f"History: {agent.get('history', 'No history available')}"
            for i, agent in enumerate(available_agents)
        ])
        
        # Format task analysis for the prompt
        if isinstance(task_analysis.get('analysis'), dict) and 'content' in task_analysis.get('analysis', {}):
            analysis_text = task_analysis['analysis']['content']
        else:
            analysis_text = str(task_analysis.get('analysis', ''))
        
        # Generate prompt for agent matching
        prompt = f"""
        Match the following subtasks with the most appropriate agents:
        
        TASK ANALYSIS:
        {analysis_text}
        
        AVAILABLE AGENTS:
        {agents_info}
        
        Please provide:
        1. Subtask-to-agent assignments with clear rationales
        2. Capability alignment analysis for each match
        3. Identification of any capability gaps
        4. Suggestions for agent coordination at capability boundary points
        """
        
        # Process with the agent matcher
        agent_matching = await self.agent_matcher.process_message(
            message=Message(
                role="user",
                content=prompt,
                metadata={"task": "agent_matching", "analysis_id": task_analysis.get("analysis_id")}
            ),
            conversation_id=f"agent_matching_{uuid.uuid4().hex[:8]}"
        )
        
        # Store the agent matching in memory
        matching_id = f"agent_matching_{uuid.uuid4().hex[:8]}"
        await self.memory_service.store(
            matching_id,
            {
                "matching": agent_matching, 
                "analysis_id": task_analysis.get("analysis_id"),
                "available_agents": [agent.get("id") for agent in available_agents],
                "timestamp": str(uuid.uuid4())
            }
        )
        
        return {
            "matching_id": matching_id,
            "matching": agent_matching,
            "analysis_id": task_analysis.get("analysis_id"),
            "available_agents": [agent.get("id") for agent in available_agents]
        }
    
    async def create_coordination_plan(self, task_analysis: Dict[str, Any], agent_matching: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create coordination structures and feedback mechanisms for multi-agent tasks.
        
        Args:
            task_analysis: Analysis of the task including subtasks and capability requirements
            agent_matching: Matching of subtasks to agents
            
        Returns:
            Coordination plan
        """
        # Format task analysis for the prompt
        if isinstance(task_analysis.get('analysis'), dict) and 'content' in task_analysis.get('analysis', {}):
            analysis_text = task_analysis['analysis']['content']
        else:
            analysis_text = str(task_analysis.get('analysis', ''))
        
        # Format agent matching for the prompt
        if isinstance(agent_matching.get('matching'), dict) and 'content' in agent_matching.get('matching', {}):
            matching_text = agent_matching['matching']['content']
        else:
            matching_text = str(agent_matching.get('matching', ''))
        
        # Generate prompt for coordination planning
        prompt = f"""
        Create a coordination plan for this multi-agent task:
        
        TASK ANALYSIS:
        {analysis_text}
        
        AGENT MATCHING:
        {matching_text}
        
        Please provide:
        1. Interface definitions for agent interactions
        2. Communication protocols and schedules
        3. Feedback mechanisms and quality checks
        4. Progress monitoring approach and adjustment triggers
        """
        
        # Process with the coordination manager
        coordination_plan = await self.coordination_manager.process_message(
            message=Message(
                role="user",
                content=prompt,
                metadata={
                    "task": "coordination_planning", 
                    "analysis_id": task_analysis.get("analysis_id"),
                    "matching_id": agent_matching.get("matching_id")
                }
            ),
            conversation_id=f"coordination_planning_{uuid.uuid4().hex[:8]}"
        )
        
        # Store the coordination plan in memory
        plan_id = f"coordination_plan_{uuid.uuid4().hex[:8]}"
        await self.memory_service.store(
            plan_id,
            {
                "plan": coordination_plan, 
                "analysis_id": task_analysis.get("analysis_id"),
                "matching_id": agent_matching.get("matching_id"),
                "timestamp": str(uuid.uuid4())
            }
        )
        
        return {
            "plan_id": plan_id,
            "plan": coordination_plan,
            "analysis_id": task_analysis.get("analysis_id"),
            "matching_id": agent_matching.get("matching_id")
        }
    
    async def orchestrate_task(self, task_description: str, available_agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Orchestrate a collaborative task across multiple agents.
        
        Args:
            task_description: Description of the task to orchestrate
            available_agents: List of available agents with their capabilities
            
        Returns:
            Complete orchestration results
        """
        try:
            # Record the orchestration process
            orchestration_id = f"orchestration_{uuid.uuid4().hex[:8]}"
            
            # Step 1: Analyze the task
            task_analysis = await self.analyze_task(task_description)
            
            # Step 2: Match agents to subtasks
            agent_matching = await self.match_agents(task_analysis, available_agents)
            
            # Step 3: Create coordination plan
            coordination_plan = await self.create_coordination_plan(task_analysis, agent_matching)
            
            # Create the orchestration record
            orchestration_record = {
                "orchestration_id": orchestration_id,
                "task_description": task_description,
                "analysis": task_analysis,
                "matching": agent_matching,
                "coordination": coordination_plan,
                "available_agents": [agent.get("id") for agent in available_agents],
                "status": "ready",
                "timestamp": str(uuid.uuid4())
            }
            
            # Store the orchestration record in memory
            await self.memory_service.store(
                orchestration_id,
                orchestration_record
            )
            
            return orchestration_record
            
        except Exception as e:
            # Handle errors during orchestration
            error_record = {
                "orchestration_id": f"error_{uuid.uuid4().hex[:8]}",
                "task_description": task_description,
                "error": str(e),
                "status": "failed",
                "timestamp": str(uuid.uuid4())
            }
            
            # Store the error record
            await self.memory_service.store(
                f"orchestration_error_{uuid.uuid4().hex[:8]}",
                error_record
            )
            
            return error_record
    
    def execute(self, task_description: str, available_agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Synchronously orchestrate a collaborative task across multiple agents.
        
        Args:
            task_description: Description of the task to orchestrate
            available_agents: List of available agents with their capabilities
            
        Returns:
            Complete orchestration results
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.orchestrate_task(task_description, available_agents))
